#!/usr/bin/env python3
"""
Create Facebook Page - Python Version
"""

import requests
import json
import uuid
import random
import time

def generate_page_name():
    """
    Generate a random page name
    
    Returns:
        str: Random page name
    """
    adjectives = [
        "Amazing", "Awesome", "Creative", "Digital", "Elite", "Epic", "Fresh",
        "Global", "Grand", "Great", "Happy", "Innovative", "Inspiring", "Modern",
        "Premium", "Professional", "Smart", "Stellar", "Supreme", "Ultimate",
        "Unique", "Vibrant", "Bright", "Dynamic", "Prime", "Quantum", "Rising",
        "Stellar", "Trendy", "Urban", "Vivid", "Bold", "Classic", "Cosmic"
    ]
    
    nouns = [
        "Media", "Hub", "Network", "Studio", "Agency", "Group", "Solutions",
        "Ventures", "Innovations", "Creations", "Designs", "Productions",
        "Services", "Concepts", "Ideas", "Vision", "Digital", "Tech",
        "Marketing", "Business", "Enterprise", "Company", "Brand", "Team",
        "Community", "Collective", "Platform", "Center", "Zone", "Space",
        "World", "Universe", "Galaxy", "Realm"
    ]
    
    categories = [
        "Tech", "Gaming", "Food", "Travel", "Fashion", "Fitness", "Music",
        "Art", "Photography", "Business", "Education", "Health", "Lifestyle",
        "Sports", "Entertainment", "News", "Design", "Science", "Nature",
        "Pets", "Books", "Movies", "Comedy", "Beauty", "Auto", "Real Estate"
    ]
    
    # Generate different name patterns
    patterns = [
        f"{random.choice(adjectives)} {random.choice(categories)} {random.choice(nouns)}",
        f"{random.choice(categories)} {random.choice(adjectives)} {random.choice(nouns)}",
        f"{random.choice(adjectives)} {random.choice(nouns)}",
        f"The {random.choice(adjectives)} {random.choice(categories)}",
        f"{random.choice(categories)} {random.choice(nouns)} {random.randint(100, 999)}",
    ]
    
    return random.choice(patterns)


def create_facebook_page(access_token, page_name):
    """
    Create a Facebook page using the Graph API
    
    Args:
        access_token (str): Access token of main profile
        page_name (str): Full name of page to create
    
    Returns:
        dict: Response containing success status and message
    """
    
    # Generate unique client trace ID
    client_trace_id = str(uuid.uuid4())
    
    # Build the nested JSON structure properly
    client_input_params = {
        "cp_upsell_declined": 0,
        "category_ids": ["2214"],
        "profile_plus_id": "0",
        "page_id": "0"
    }
    
    server_params = {
        "INTERNAL__latency_qpl_instance_id": random.randint(40000000000000, 50000000000000),
        "screen": "category",
        "referrer": "pages_tab_launch_point",
        "name": page_name,
        "creation_source": "android",
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "variant": 5
    }
    
    inner_params = {
        "client_input_params": client_input_params,
        "server_params": server_params
    }
    
    middle_params = {
        "params": json.dumps(inner_params)
    }
    
    outer_params = {
        "params": json.dumps(middle_params),
        "bloks_versioning_id": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec",
        "app_id": "com.bloks.www.additional.profile.plus.creation.action.category.submit"
    }
    
    nt_context = {
        "styles_id": "e6c6f61b7a86cdf3fa2eaaffa982fbd1",
        "using_white_navbar": True,
        "pixel_ratio": 1.5,
        "is_push_on": True,
        "bloks_version": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec"
    }
    
    variables = {
        "params": outer_params,
        "scale": "1.5",
        "nt_context": nt_context
    }
    
    # Prepare POST data
    post_data = {
        'method': 'post',
        'pretty': 'false',
        'format': 'json',
        'server_timestamps': 'true',
        'locale': 'en_US',
        'purpose': 'fetch',
        'fb_api_req_friendly_name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
        'fb_api_caller_class': 'graphservice',
        'client_doc_id': '11994080423068421059028841356',
        'variables': json.dumps(variables),
        'fb_api_analytics_tags': '["GraphServices"]',
        'client_trace_id': client_trace_id
    }
    
    # Prepare headers
    headers = {
        'x-fb-request-analytics-tags': '{"network_tags":{"product":"350685531728","purpose":"fetch","request_category":"graphql","retry_attempt":"0"},"application_tags":"graphservice"}',
        'x-fb-ta-logging-ids': f'graphql:{client_trace_id}',
        'x-fb-rmd': 'state=URL_ELIGIBLE',
        'x-fb-sim-hni': '31016',
        'x-fb-net-hni': '31016',
        'authorization': f'OAuth {access_token}',
        'x-graphql-request-purpose': 'fetch',
        'user-agent': '[FBAN/FB4A;FBAV/417.0.0.33.65;FBBV/480086274;FBDM/{density=1.5,width=720,height=1244};FBLC/en_US;FBRV/0;FBCR/T-Mobile;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-N976N;FBSV/7.1.2;FBOP/1;FBCA/x86:armeabi-v7a;]',
        'content-type': 'application/x-www-form-urlencoded',
        'x-fb-connection-type': 'WIFI',
        'x-fb-background-state': '1',
        'x-fb-friendly-name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
        'x-graphql-client-library': 'graphservice',
        'x-fb-privacy-context': '3643298472347298',
        'x-fb-device-group': '3543',
        'x-tigon-is-retry': 'False',
        'priority': 'u=3,i',
        'x-fb-http-engine': 'Liger',
        'x-fb-client-ip': 'True',
        'x-fb-server-cluster': 'True'
    }
    
    url = "https://graph.facebook.com/graphql"
    
    try:
        # Make the request
        response = requests.post(
            url,
            data=post_data,
            headers=headers,
            timeout=30,
            verify=True
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        response_json = response.json()
        
        # Check for success
        if 'data' in response_json and response_json['data']:
            success_res = str(response_json['data'].get('fb_bloks_action', {}).get('root_action', {}).get('action', {}).get('action_bundle', {}).get('bloks_bundle_action', ''))
            
            if 'Cannot create Page: You have created too many Pages in a short time' in success_res:
                return {
                    'success': False,
                    'message': f"Rate limit reached!",
                    'rate_limited': True
                }
            else:
                return {
                    'success': True,
                    'message': "Page created successfully!",
                    'response': response_json,
                    'rate_limited': False
                }
        else:
            return {
                'success': False,
                'message': f"Unexpected response format",
                'rate_limited': False
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'message': f"Request error: {str(e)}",
            'rate_limited': False
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'message': f"JSON decode error: {str(e)}",
            'rate_limited': False
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}",
            'rate_limited': False
        }


if __name__ == "__main__":
    print("=" * 50)
    print("Facebook Page Creator")
    print("=" * 50)
    print()
    
    # Prompt for access token
    ACCESS_TOKEN = input("Enter your Facebook access token: ").strip()
    
    if not ACCESS_TOKEN:
        print("\n✗ Error: Access token cannot be empty")
        exit(1)
    
    # Prompt for number of pages
    while True:
        try:
            num_pages = int(input("How many pages do you want to create? ").strip())
            if num_pages <= 0:
                print("✗ Please enter a number greater than 0")
                continue
            break
        except ValueError:
            print("✗ Please enter a valid number")
    
    # Ask for naming method
    print("\nPage naming options:")
    print("  1. Manual - Enter each page name yourself")
    print("  2. Auto-generate - Automatically create random page names")
    
    while True:
        naming_choice = input("\nChoose option (1 or 2): ").strip()
        if naming_choice in ['1', '2']:
            break
        print("✗ Please enter 1 or 2")
    
    print()
    
    # Store page names
    page_names = []
    
    if naming_choice == '1':
        # Manual naming
        if num_pages == 1:
            PAGE_NAME = input("Enter the page name: ").strip()
            if not PAGE_NAME:
                print("\n✗ Error: Page name cannot be empty")
                exit(1)
            page_names.append(PAGE_NAME)
        else:
            print(f"Enter {num_pages} page names:\n")
            for i in range(num_pages):
                while True:
                    PAGE_NAME = input(f"  Page {i+1} name: ").strip()
                    if PAGE_NAME:
                        page_names.append(PAGE_NAME)
                        break
                    else:
                        print("  ✗ Page name cannot be empty. Try again.")
    else:
        # Auto-generate names
        print(f"Generating {num_pages} random page names...\n")
        for i in range(num_pages):
            generated_name = generate_page_name()
            page_names.append(generated_name)
            print(f"  Page {i+1}: {generated_name}")
        
        print()
        confirm = input("Use these names? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\nOperation cancelled.")
            exit(0)
    
    # Add delay option
    print()
    use_delay = input("Add delay between requests to avoid rate limits? (y/n): ").strip().lower()
    delay_seconds = 0
    
    if use_delay == 'y':
        while True:
            try:
                delay_seconds = int(input("Enter delay in seconds (recommended 2-5): ").strip())
                if delay_seconds < 0:
                    print("✗ Delay cannot be negative")
                    continue
                break
            except ValueError:
                print("✗ Please enter a valid number")
    
    # Confirmation
    print(f"\n{'─' * 50}")
    print(f"Creating {num_pages} Facebook page(s)...")
    if delay_seconds > 0:
        print(f"Delay between requests: {delay_seconds} seconds")
    print(f"{'─' * 50}\n")
    
    # Track results
    successful = 0
    failed = 0
    rate_limited_count = 0
    
    # Create the pages
    for idx, page_name in enumerate(page_names, 1):
        print(f"[{idx}/{num_pages}] Creating page: '{page_name}'")
        
        result = create_facebook_page(ACCESS_TOKEN, page_name)
        
        if result['success']:
            print(f"  ✓ {result['message']}\n")
            successful += 1
        else:
            print(f"  ✗ {result['message']}\n")
            failed += 1
            
            if result.get('rate_limited', False):
                rate_limited_count += 1
                
                # If rate limited, ask if user wants to continue
                if idx < num_pages:
                    cont = input("  Rate limit reached. Continue trying remaining pages? (y/n): ").strip().lower()
                    if cont != 'y':
                        print("\n  Stopping page creation...")
                        break
                    print()
        
        # Add delay between requests (except for the last one)
        if delay_seconds > 0 and idx < num_pages:
            print(f"  ⏳ Waiting {delay_seconds} seconds before next request...")
            time.sleep(delay_seconds)
            print()
    
    # Summary
    print("=" * 50)
    print("Summary:")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")
    if rate_limited_count > 0:
        print(f"  ⚠ Rate Limited: {rate_limited_count}")
    print(f"  Total Attempted: {successful + failed}")
    print("=" * 50)
    print()
