#!/usr/bin/env python3
"""
Create Facebook Page - Python Version
"""

import requests
import json
import uuid

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
        'variables': json.dumps({
            "params": {
                "params": json.dumps({
                    "params": json.dumps({
                        "client_input_params": {
                            "cp_upsell_declined": 0,
                            "category_ids": ["2214"],
                            "profile_plus_id": "0",
                            "page_id": "0"
                        },
                        "server_params": {
                            "INTERNAL__latency_qpl_instance_id": 40168896100127,
                            "screen": "category",
                            "referrer": "pages_tab_launch_point",
                            "name": page_name,
                            "creation_source": "android",
                            "INTERNAL__latency_qpl_marker_id": 36707139,
                            "variant": 5
                        }
                    })
                }),
                "bloks_versioning_id": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec",
                "app_id": "com.bloks.www.additional.profile.plus.creation.action.category.submit"
            },
            "scale": "1.5",
            "nt_context": {
                "styles_id": "e6c6f61b7a86cdf3fa2eaaffa982fbd1",
                "using_white_navbar": True,
                "pixel_ratio": 1.5,
                "is_push_on": True,
                "bloks_version": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec"
            }
        }),
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
            success_res = response_json['data'].get('fb_bloks_action', {}).get('root_action', {}).get('action', {}).get('action_bundle', {}).get('bloks_bundle_action', '')
            
            if 'Cannot create Page: You have created too many Pages in a short time' in str(success_res):
                return {
                    'success': False,
                    'message': f"Failed to create page!\n{success_res}"
                }
            else:
                return {
                    'success': True,
                    'message': "Page created successfully!",
                    'response': response_json
                }
        else:
            return {
                'success': False,
                'message': f"Unexpected response format: {response.text}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'message': f"Request error: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'message': f"JSON decode error: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}"
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
    
    # Prompt for page name
    PAGE_NAME = input("Enter the page name you want to create: ").strip()
    
    if not PAGE_NAME:
        print("\n✗ Error: Page name cannot be empty")
        exit(1)
    
    # Confirmation
    print(f"\n{'─' * 50}")
    print(f"Creating Facebook page: '{PAGE_NAME}'")
    print(f"{'─' * 50}\n")
    
    # Create the page
    result = create_facebook_page(ACCESS_TOKEN, PAGE_NAME)
    
    # Display result
    print()
    if result['success']:
        print(f"✓ {result['message']}")
    else:
        print(f"✗ {result['message']}")
    
    print()
