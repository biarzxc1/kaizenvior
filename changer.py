#!/usr/bin/env python3
"""
Facebook Name Changer Terminal Tool (Python Version)
by RIYO - Optimized for JSON appstate paste
Converted to Python for Termux compatibility
"""

import json
import re
import uuid
import asyncio
import aiohttp
from urllib.parse import urlencode

# ========== UTILITIES ==========
class FBUtil:
    FB_USER_AGENT = "facebookexternalhit/1.1"
    
    @staticmethod
    def get_uid(cookie):
        """Extract user ID from cookie string"""
        if not cookie:
            return None
        
        c_user_match = re.search(r'(?:^|;)\s*c_user=([^;]+)', cookie)
        i_user_match = re.search(r'(?:^|;)\s*i_user=([^;]+)', cookie)
        
        if c_user_match:
            return c_user_match.group(1)
        elif i_user_match:
            return i_user_match.group(1)
        return None
    
    @staticmethod
    def is_instagram(cookie):
        """Check if cookie is from Instagram"""
        return cookie and any(x in cookie for x in ['sessionid', 'csrftoken', 'rur'])
    
    @staticmethod
    def generate_mutation_id():
        """Generate a unique mutation ID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def get_from(text, start_token, end_token):
        """Extract text between two tokens"""
        if not text:
            return None
        
        start = text.find(start_token)
        if start == -1:
            return None
        
        start_index = start + len(start_token)
        last_half = text[start_index:]
        end = last_half.find(end_token)
        
        if end == -1:
            return None
        
        return last_half[:end]
    
    @staticmethod
    async def get_fb_data(cookie, is_instagram=False):
        """Fetch Facebook/Instagram data including DTSG token"""
        try:
            platform = "instagram" if is_instagram else "facebook"
            headers = {
                "user-agent": FBUtil.FB_USER_AGENT,
                "cookie": cookie,
                "cache-control": "max-age=0",
                "upgrade-insecure-requests": "1",
                "referer": f"https://www.{platform}.com/",
                "origin": f"https://www.{platform}.com",
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"https://www.{platform}.com", headers=headers) as response:
                    html = await response.text()
            
            user_id = FBUtil.get_uid(cookie)
            fb_dtsg = FBUtil.get_from(html, '["DTSGInitData",[],{"token":"', '","')
            
            # Calculate jazoest
            jazoest = "2"
            if fb_dtsg:
                for char in fb_dtsg:
                    jazoest += str(ord(char))
            
            return {
                "data": {
                    "fb_dtsg": fb_dtsg or "",
                    "jazoest": jazoest,
                    "lsd": FBUtil.get_from(html, '["LSD",[],{"token":"', '"}') or "",
                    "av": user_id,
                    "__a": "1",
                    "__user": user_id,
                    "__req": "1",
                },
                "userID": user_id,
                "headers": headers,
            }
        except Exception as e:
            print(f"Error getting FB data: {e}")
            raise
    
    @staticmethod
    async def exec_graph(cookie, data, is_accounts_center=False, is_instagram=False):
        """Execute GraphQL API call"""
        try:
            fb_data = await FBUtil.get_fb_data(cookie, is_instagram)
            form_data = fb_data["data"]
            headers = fb_data["headers"]
            
            platform = "instagram" if is_instagram else "facebook"
            subdomain = "accountscenter" if is_accounts_center else "www"
            url = f"https://{subdomain}.{platform}.com/api/graphql"
            
            # Merge form data with input data
            post_data = {**form_data, **data}
            
            headers_post = {
                **headers,
                "content-type": "application/x-www-form-urlencoded",
            }
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, data=urlencode(post_data), headers=headers_post) as response:
                    return await response.json()
        except Exception as e:
            print(f"Graph API error: {e}")
            raise
    
    @staticmethod
    async def get_accounts_center(cookie):
        """Get linked Facebook and Instagram accounts"""
        try:
            result = await FBUtil.exec_graph(cookie, {
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
            }, is_accounts_center=True)
            
            identities = result.get("data", {}).get("fx_identity_management", {}).get(
                "identities_and_central_identities", {}
            )
            
            linked = [
                *identities.get("linked_identities_to_pci", []),
                *identities.get("business_identities", []),
            ]
            
            if not linked:
                return []
            
            accounts = []
            for identity in linked:
                if identity.get("identity_type") != "FB_ADDITIONAL_PROFILE":
                    accounts.append({
                        "name": identity.get("full_name"),
                        "username": identity.get("username"),
                        "uid": identity.get("canonical_id") or identity.get("administering_account_id"),
                        "type": identity.get("account_type"),
                        "id_type": identity.get("detailed_identity_type"),
                        "id_type2": identity.get("identity_type"),
                    })
            
            return accounts
        except Exception as e:
            print(f"Error getting accounts center: {e}")
            return []
    
    @staticmethod
    def parse_appstate(input_str):
        """Parse appstate JSON or cookie string"""
        try:
            # If already a cookie string, return it
            if isinstance(input_str, str) and '=' in input_str and ';' in input_str:
                return input_str
            
            # Clean and parse JSON
            json_str = input_str.strip()
            
            # Find the JSON array
            if not json_str.startswith('['):
                start_bracket = json_str.find('[')
                if start_bracket != -1:
                    json_str = json_str[start_bracket:]
            
            # Find matching closing bracket
            bracket_count = 0
            end_index = -1
            
            for i, char in enumerate(json_str):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0 and i > 0:
                        end_index = i
                        break
            
            if end_index != -1:
                json_str = json_str[:end_index + 1]
            
            # Parse JSON
            appstate = json.loads(json_str)
            
            if isinstance(appstate, list):
                cookie_string = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in appstate])
                print(f"✅ Converted {len(appstate)} cookies to string")
                return cookie_string
            
            raise ValueError("Invalid appstate format")
        except Exception as e:
            print(f"❌ Failed to parse appstate as JSON, using as raw string")
            return input_str


# ========== MAIN PROGRAM ==========
async def main():
    print("\n" + "=" * 50)
    print("   FB NAME CHANGER (TERMINAL TOOL)")
    print("=" * 50 + "\n")
    
    try:
        print("📝 PASTE INSTRUCTIONS:")
        print("1. Copy your FULL Facebook appstate (entire JSON array)")
        print("2. Long press to paste in Termux")
        print("3. Wait for confirmation before pasting Instagram\n")
        
        # Get Facebook appstate
        print("📱 Paste your Facebook appstate and press Enter:")
        appstate_fb_input = input().strip()
        
        if not appstate_fb_input:
            print("❌ No Facebook appstate provided!")
            return
        
        print("✅ Facebook appstate received!\n")
        
        # Get Instagram appstate
        print("📷 Paste your Instagram appstate and press Enter:")
        appstate_ig_input = input().strip()
        
        if not appstate_ig_input:
            print("❌ No Instagram appstate provided!")
            return
        
        print("\n✅ Instagram appstate received!\n")
        
        # Get new name
        print("✏️  Enter the new name:")
        new_name = input().strip()
        
        if not new_name:
            print("❌ No name provided!")
            return
        
        print("\n🔄 Processing appstates...")
        
        # Parse appstates
        appstate_fb = FBUtil.parse_appstate(appstate_fb_input)
        appstate_ig = FBUtil.parse_appstate(appstate_ig_input)
        
        print("✅ Appstates processed successfully!")
        
        # Validate Instagram appstate
        if not FBUtil.is_instagram(appstate_ig):
            print("❌ Invalid Instagram appstate! Make sure it contains sessionid or csrftoken")
            return
        
        print("\n🔍 Fetching account data...")
        
        # Get linked accounts
        accounts = await FBUtil.get_accounts_center(appstate_fb)
        if not accounts:
            raise Exception("No accounts found. Check your Facebook appstate.")
        
        # Find Facebook and Instagram accounts
        fb_acc = next((acc for acc in accounts if acc["type"] == "FACEBOOK"), None)
        ig_acc = next((acc for acc in accounts if acc["type"] == "INSTAGRAM"), None)
        
        print(f"Facebook Account: {fb_acc}")
        print(f"Instagram Account: {ig_acc}")
        
        if not fb_acc or not ig_acc:
            raise Exception("Couldn't find connected Facebook and Instagram accounts.")
        
        print(f"✅ Facebook: {fb_acc['name']} ({fb_acc['uid']})")
        print(f"✅ Instagram: {ig_acc['name']} ({ig_acc['uid']})")
        print(f"\n🔄 Changing name to: {new_name}")
        
        # Change Instagram name
        print("\n📝 Updating Instagram name...")
        ig_result = await FBUtil.exec_graph(appstate_ig, {
            "variables": json.dumps({
                "client_mutation_id": FBUtil.generate_mutation_id(),
                "family_device_id": "device_id_fetch_ig_did",
                "identity_ids": [ig_acc["uid"]],
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
        }, is_accounts_center=True, is_instagram=True)
        
        # Check for errors
        if ig_result.get("errors") or ig_result.get("data", {}).get("fxim_update_identity_name", {}).get("error"):
            error_msg = (
                ig_result.get("data", {}).get("fxim_update_identity_name", {}).get("error", {}).get("description") or
                ig_result.get("errors", [{}])[0].get("message") or
                "Unknown error"
            )
            raise Exception(f"Instagram update failed: {error_msg}")
        
        print("✅ Instagram name updated!")
        
        # Sync with Facebook
        print("🔄 Syncing with Facebook...")
        fb_result = await FBUtil.exec_graph(appstate_fb, {
            "fb_api_req_friendly_name": "useFXIMUpdateNameMutation",
            "fb_api_caller_class": "RelayModern",
            "variables": json.dumps({
                "client_mutation_id": FBUtil.generate_mutation_id(),
                "accounts_to_sync": [ig_acc["uid"], fb_acc["uid"]],
                "resources_to_sync": ["NAME", "PROFILE_PHOTO"],
                "source_of_truth_array": [
                    {"resource_source": "IG"},
                    {"resource_source": "FB"},
                ],
                "source_account": fb_acc["uid"],
                "platform": "FACEBOOK",
                "interface": "FB_WEB",
            }),
            "server_timestamps": "true",
            "doc_id": "9388416374608398",
        }, is_accounts_center=True, is_instagram=False)
        
        # Check for errors
        if fb_result.get("errors") or fb_result.get("data", {}).get("fxim_sync_resources_v2", {}).get("error"):
            error_msg = (
                fb_result.get("data", {}).get("fxim_sync_resources_v2", {}).get("error", {}).get("description") or
                fb_result.get("errors", [{}])[0].get("message") or
                "Unknown error"
            )
            raise Exception(f"Facebook sync failed: {error_msg}")
        
        print("\n" + "🎉" * 20)
        print(f"🎉 SUCCESS: Name changed to \"{new_name}\"")
        print("🎉 Changes applied to both Facebook and Instagram!")
        print("🎉" * 20)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
