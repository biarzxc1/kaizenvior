#!/usr/bin/env python3
# Facebook Name Changer Terminal Tool (Fixed for Termux)
# by RIYO - Optimized for JSON appstate paste
# Converted to Python

import requests
import json
import re
import uuid
import hashlib
from urllib.parse import urlencode

# ========== UTILITIES ==========
class Util:
    fb_user_agent = "facebookexternalhit/1.1"
    
    @staticmethod
    def get_uid(cookie):
        if not cookie:
            return None
        c_user_match = re.search(r'(?:^|;)\s*c_user=([^;]+)', cookie)
        i_user_match = re.search(r'(?:^|;)\s*i_user=([^;]+)', cookie)
        return (c_user_match.group(1) if c_user_match else None) or \
               (i_user_match.group(1) if i_user_match else None)
    
    @staticmethod
    def is_instagram(cookie):
        return cookie and ('sessionid' in cookie or 'csrftoken' in cookie or 'rur' in cookie)
    
    @staticmethod
    def generate_mutation_id():
        return str(uuid.uuid4())
    
    @staticmethod
    def get_from(string, start_token, end_token):
        if not string:
            return None
        start = string.find(start_token)
        if start == -1:
            return None
        start_index = start + len(start_token)
        last_half = string[start_index:]
        end = last_half.find(end_token)
        if end == -1:
            return None
        return last_half[:end]
    
    @staticmethod
    def get_fb_data(cookie, is_instagram):
        try:
            headers = {
                "user-agent": Util.fb_user_agent,
                "cookie": cookie,
                "cache-control": "max-age=0",
                "upgrade-insecure-requests": "1",
                "referer": f"https://www.{'instagram' if is_instagram else 'facebook'}.com/",
                "origin": f"https://www.{'instagram' if is_instagram else 'facebook'}.com",
            }
            
            platform = 'instagram' if is_instagram else 'facebook'
            fb = requests.get(f"https://www.{platform}.com", headers=headers, timeout=10)
            
            user_id = Util.get_uid(cookie)
            fb_dtsg = Util.get_from(fb.text, '["DTSGInitData",[],{"token":"', '","')
            
            req = 1
            jazoest = "2"
            if fb_dtsg:
                for char in fb_dtsg:
                    jazoest += str(ord(char))
            
            return {
                "data": {
                    "fb_dtsg": fb_dtsg or "",
                    "jazoest": jazoest,
                    "lsd": Util.get_from(fb.text, '["LSD",[],{"token":"', '"}') or "",
                    "av": user_id,
                    "__a": "1",
                    "__user": user_id,
                    "__req": format(req, 'x'),
                },
                "userID": user_id,
                "headers": headers,
            }
        except Exception as error:
            print(f"Error getting FB data: {str(error)}")
            raise
    
    @staticmethod
    def exec_graph(cookie, data, is_accounts_center, is_instagram):
        try:
            fb_data = Util.get_fb_data(cookie, is_instagram)
            form_data = fb_data["data"]
            headers = fb_data["headers"]
            
            subdomain = "accountscenter" if is_accounts_center else "www"
            platform = "instagram" if is_instagram else "facebook"
            url = f"https://{subdomain}.{platform}.com/api/graphql"
            
            combined_data = {**form_data, **data}
            
            headers.update({
                "content-type": "application/x-www-form-urlencoded",
            })
            
            res = requests.post(url, data=combined_data, headers=headers, timeout=15)
            return res.json()
        except Exception as error:
            print(f"Graph API error: {str(error)}")
            raise
    
    @staticmethod
    def get_accounts_center(cookie):
        try:
            getinsta = Util.exec_graph(cookie, {
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "FXAccountsCenterProfilesPageV2Query",
                "variables": json.dumps({
                    "device_id": "device_id_fetch_datr",
                    "flow": "FB_WEB_SETTINGS",
                    "interface": "FB_WEB",
                    "platform": "FACEBOOK",
                    "scale": 2
                }),
                "server_timestamps": "true",
                "doc_id": "7683343698455923",
            }, True, False)
            
            linked = []
            if getinsta and 'data' in getinsta:
                fx_data = getinsta['data'].get('fx_identity_management', {})
                identities = fx_data.get('identities_and_central_identities', {})
                linked.extend(identities.get('linked_identities_to_pci', []))
                linked.extend(identities.get('business_identities', []))
            
            if not linked:
                return []
            
            accounts = []
            for x in linked:
                if x.get('identity_type') != 'FB_ADDITIONAL_PROFILE':
                    accounts.append({
                        'name': x.get('full_name'),
                        'username': x.get('username'),
                        'uid': x.get('canonical_id') or x.get('administering_account_id'),
                        'type': x.get('account_type'),
                        'id_type': x.get('detailed_identity_type'),
                        'id_type2': x.get('identity_type'),
                    })
            return accounts
        except Exception as error:
            print(f"Error getting accounts center: {str(error)}")
            return []
    
    @staticmethod
    def parse_appstate(input_data):
        try:
            # If input is already a cookie string, return it
            if isinstance(input_data, str) and '=' in input_data and ';' in input_data:
                return input_data
            
            # Try to parse as JSON
            json_str = input_data.strip()
            
            # Fix common JSON issues
            if not json_str.startswith('['):
                # If it starts with random text, find the first [
                start_bracket = json_str.find('[')
                if start_bracket != -1:
                    json_str = json_str[start_bracket:]
            
            # Find the complete JSON array by matching brackets
            bracket_count = 0
            end_index = -1
            
            for i, char in enumerate(json_str):
                if char == '[':
                    bracket_count += 1
                if char == ']':
                    bracket_count -= 1
                if bracket_count == 0 and i > 0:
                    end_index = i
                    break
            
            if end_index != -1:
                json_str = json_str[:end_index + 1]
            
            appstate = json.loads(json_str)
            
            if isinstance(appstate, list):
                cookie_string = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in appstate])
                print(f"✅ Converted {len(appstate)} cookies to string")
                return cookie_string
            
            raise ValueError("Invalid appstate format")
        except Exception as error:
            print("❌ Failed to parse appstate as JSON, using as raw string")
            # Return as is, might be cookie string
            return input_data

# ========== MAIN PROGRAM ==========
def main():
    print("\n" + "=" * 50)
    print("   FB NAME CHANGER (TERMINAL TOOL)")
    print("=" * 50 + "\n")
    
    try:
        print("📝 PASTE INSTRUCTIONS:")
        print("1. Copy your FULL Facebook appstate (entire JSON array)")
        print("2. Long press to paste in Termux")
        print("3. Wait for confirmation before pasting Instagram\n")
        
        appstate_fb_input = input("🔵 Paste Facebook appstate: ").strip()
        
        if not appstate_fb_input:
            print("❌ No Facebook appstate provided!")
            return
        
        print("\n✅ Facebook appstate received!")
        
        appstate_ig_input = input("\n🟣 Paste Instagram appstate: ").strip()
        
        if not appstate_ig_input:
            print("❌ No Instagram appstate provided!")
            return
        
        print("\n✅ Instagram appstate received!\n")
        
        new_name = input("📝 Enter new name: ").strip()
        
        if not new_name:
            print("❌ No name provided!")
            return
        
        print("\n🔄 Processing appstates...")
        
        # Parse appstates
        appstate_fb = Util.parse_appstate(appstate_fb_input)
        appstate_ig = Util.parse_appstate(appstate_ig_input)
        
        print("✅ Appstates processed successfully!")
        
        # Validate Instagram appstate
        if not Util.is_instagram(appstate_ig):
            print("❌ Invalid Instagram appstate! Make sure it contains sessionid or csrftoken")
            return
        
        print("\n🔍 Fetching account data...")
        
        accounts = Util.get_accounts_center(appstate_fb)
        if not accounts:
            raise Exception("No accounts found. Check your Facebook appstate.")
        
        fb_acc = next((a for a in accounts if a['type'] == 'FACEBOOK'), None)
        ig_acc = next((a for a in accounts if a['type'] == 'INSTAGRAM'), None)
        
        print(fb_acc)
        print(ig_acc)
        
        if not fb_acc or not ig_acc:
            raise Exception("Couldn't find connected Facebook and Instagram accounts.")
        
        print(f"✅ Facebook: {fb_acc['name']} ({fb_acc['uid']})")
        print(f"✅ Instagram: {ig_acc['name']} ({ig_acc['uid']})")
        print(f"\n🔄 Changing name to: {new_name}")
        
        # Change IG Name
        print("\n📝 Updating Instagram name...")
        ig_result = Util.exec_graph(appstate_ig, {
            "variables": json.dumps({
                "client_mutation_id": Util.generate_mutation_id(),
                "family_device_id": "device_id_fetch_ig_did",
                "identity_ids": [ig_acc['uid']],
                "full_name": new_name,
                "first_name": None,
                "middle_name": None,
                "last_name": None,
                "interface": "IG_WEB",
            }),
            "fb_api_req_friendly_name": "useFXIMUpdateNameMutation",
            "fb_api_caller_class": "RelayModern",
            "server_timestamps": "true",
            "doc_id": "28573275658982428",
        }, True, True)
        
        if ig_result.get('errors') or ig_result.get('data', {}).get('fxim_update_identity_name', {}).get('error'):
            error_msg = (ig_result.get('data', {}).get('fxim_update_identity_name', {}).get('error', {}).get('description') or
                        (ig_result.get('errors', [{}])[0].get('message') if ig_result.get('errors') else None) or
                        "Unknown error")
            raise Exception(f"Instagram update failed: {error_msg}")
        
        print("✅ Instagram name updated!")
        
        # Sync with Facebook
        print("🔄 Syncing with Facebook...")
        fb_result = Util.exec_graph(appstate_fb, {
            "fb_api_req_friendly_name": "useFXIMUpdateNameMutation",
            "fb_api_caller_class": "RelayModern",
            "variables": json.dumps({
                "client_mutation_id": Util.generate_mutation_id(),
                "accounts_to_sync": [ig_acc['uid'], fb_acc['uid']],
                "resources_to_sync": ["NAME", "PROFILE_PHOTO"],
                "source_of_truth_array": [
                    {"resource_source": "IG"},
                    {"resource_source": "FB"},
                ],
                "source_account": fb_acc['uid'],
                "platform": "FACEBOOK",
                "interface": "FB_WEB",
            }),
            "server_timestamps": "true",
            "doc_id": "9388416374608398",
        }, True, False)
        
        if fb_result.get('errors') or fb_result.get('data', {}).get('fxim_sync_resources_v2', {}).get('error'):
            error_msg = (fb_result.get('data', {}).get('fxim_sync_resources_v2', {}).get('error', {}).get('description') or
                        (fb_result.get('errors', [{}])[0].get('message') if fb_result.get('errors') else None) or
                        "Unknown error")
            raise Exception(f"Facebook sync failed: {error_msg}")
        
        print("\n" + "🎉" * 20)
        print(f"🎉 SUCCESS: Name changed to \"{new_name}\"")
        print("🎉 Changes applied to both Facebook and Instagram!")
        print("🎉" * 20)
        
    except Exception as error:
        print(f"\n❌ Error: {str(error)}")
        if hasattr(error, 'response') and error.response:
            print(f"📡 Server response: {error.response.status_code} {error.response.reason}")

if __name__ == "__main__":
    main()
