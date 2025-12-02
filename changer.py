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
            # Validate cookie has required fields
            if is_instagram:
                if not any(x in cookie for x in ['sessionid', 'csrftoken']):
                    raise Exception("Invalid Instagram cookie - missing sessionid or csrftoken")
            else:
                if 'c_user' not in cookie and 'i_user' not in cookie:
                    raise Exception("Invalid Facebook cookie - missing c_user or i_user")
            
            platform = "instagram" if is_instagram else "facebook"
            headers = {
                "user-agent": FBUtil.FB_USER_AGENT,
                "cookie": cookie,
                "cache-control": "max-age=0",
                "upgrade-insecure-requests": "1",
                "referer": f"https://www.{platform}.com/",
                "origin": f"https://www.{platform}.com",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.9",
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"https://www.{platform}.com", headers=headers, allow_redirects=True) as response:
                    html = await response.text()
                    
                    # Check if we got redirected to login
                    if "login" in str(response.url) or response.status == 302:
                        raise Exception("Cookies are invalid or expired - redirected to login")
            
            user_id = FBUtil.get_uid(cookie)
            if not user_id:
                raise Exception("Could not extract user ID from cookies")
            
            fb_dtsg = FBUtil.get_from(html, '["DTSGInitData",[],{"token":"', '","')
            if not fb_dtsg:
                print("⚠️  Warning: Could not find fb_dtsg token in response")
                # Try alternative pattern
                fb_dtsg = FBUtil.get_from(html, '"DTSGInitialData",[],"', '"')
            
            # Calculate jazoest
            jazoest = "2"
            if fb_dtsg:
                for char in fb_dtsg:
                    jazoest += str(ord(char))
            
            lsd_token = FBUtil.get_from(html, '["LSD",[],{"token":"', '"}')
            if not lsd_token:
                # Try alternative pattern
                lsd_token = FBUtil.get_from(html, '"LSDToken",[],"', '"')
            
            return {
                "data": {
                    "fb_dtsg": fb_dtsg or "",
                    "jazoest": jazoest,
                    "lsd": lsd_token or "",
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
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-fb-friendly-name": data.get("fb_api_req_friendly_name", ""),
                "x-fb-lsd": form_data.get("lsd", ""),
            }
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, data=urlencode(post_data), headers=headers_post) as response:
                    # Get response text first
                    response_text = await response.text()
                    
                    # Check if response is JSON
                    if response.content_type and 'json' in response.content_type:
                        return json.loads(response_text)
                    elif response_text.strip().startswith('{') or response_text.strip().startswith('['):
                        # Try to parse as JSON even if content-type is wrong
                        return json.loads(response_text)
                    else:
                        # Not JSON, probably HTML error page
                        print(f"❌ Server returned HTML instead of JSON")
                        print(f"Response status: {response.status}")
                        print(f"Response preview: {response_text[:500]}")
                        
                        # Check for common Facebook errors
                        if "login" in response_text.lower() or "checkpoint" in response_text.lower():
                            raise Exception("Invalid or expired cookies. Please get fresh appstate.")
                        elif "rate limit" in response_text.lower():
                            raise Exception("Rate limited by Facebook. Please wait and try again.")
                        else:
                            raise Exception(f"Facebook returned error page. Check your cookies.")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            raise
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
    
    # Debug mode
    import sys
    debug = '--debug' in sys.argv
    
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
        
        if debug:
            print(f"\n[DEBUG] FB Cookie length: {len(appstate_fb)}")
            print(f"[DEBUG] IG Cookie length: {len(appstate_ig)}")
            print(f"[DEBUG] FB has c_user: {'c_user' in appstate_fb}")
            print(f"[DEBUG] IG has sessionid: {'sessionid' in appstate_ig}")
        
        # Validate Instagram appstate
        if not FBUtil.is_instagram(appstate_ig):
            print("❌ Invalid Instagram appstate! Make sure it contains sessionid or csrftoken")
            return
        
        print("\n🔍 Fetching account data...")
        
        try:
            # Get linked accounts
            accounts = await FBUtil.get_accounts_center(appstate_fb)
            if not accounts:
                raise Exception("No accounts found. Check your Facebook appstate.")
            
            if debug:
                print(f"[DEBUG] Found {len(accounts)} accounts")
                for acc in accounts:
                    print(f"[DEBUG] Account: {acc['type']} - {acc['name']}")
        except Exception as e:
            print(f"\n❌ Failed to get accounts: {e}")
            print("\n💡 Troubleshooting:")
            print("1. Make sure your Facebook cookie is fresh (not expired)")
            print("2. Try getting new appstate from browser")
            print("3. Ensure Facebook and Instagram accounts are linked")
            print("4. Check if your account needs security verification")
            raise
        
        # Find Facebook and Instagram accounts
        fb_acc = next((acc for acc in accounts if acc["type"] == "FACEBOOK"), None)
        ig_acc = next((acc for acc in accounts if acc["type"] == "INSTAGRAM"), None)
        
        if debug:
            print(f"\n[DEBUG] Facebook Account: {fb_acc}")
            print(f"[DEBUG] Instagram Account: {ig_acc}")
        
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
        
        if debug:
            print(f"[DEBUG] IG Result: {json.dumps(ig_result, indent=2)}")
        
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
        
        if debug:
            print(f"[DEBUG] FB Result: {json.dumps(fb_result, indent=2)}")
        
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
        if debug:
            import traceback
            print("\n[DEBUG] Full traceback:")
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
