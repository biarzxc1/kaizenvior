const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Nhập Cookie: ', async (cookie) => {
    try {
        const id = cookie.split('c_user=')[1].split(';')[0];
        
        const headers1 = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'dpr': '1.25',
            'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
            'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'viewport-width': '1038',
            'Cookie': cookie
        };

        const params = {
            'redirect_uri': 'fbconnect://success',
            'scope': 'email,public_profile',
            'response_type': 'token,code',
            'client_id': '350685531728',
        };

        const response1 = await axios.get('https://www.facebook.com/v2.3/dialog/oauth', {
            headers: headers1,
            params: params
        });

        const responseText = response1.data.replace(/\[\]/g, '');
        const fb_dtsg_match = responseText.match(/DTSGInitData",,{"token":"(.+?)"/);
        
        if (!fb_dtsg_match) {
            throw new Error('Không tìm thấy fb_dtsg - Cookie có thể đã hết hạn');
        }
        
        const fb_dtsg = fb_dtsg_match[1];

        const headers2 = {
            'authority': 'www.facebook.com',
            'accept': '*/*',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://www.facebook.com',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
            'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'x-fb-friendly-name': 'useCometConsentPromptEndOfFlowBatchedMutation',
            'Cookie': cookie
        };

        const postData = new URLSearchParams({
            'fb_dtsg': fb_dtsg,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useCometConsentPromptEndOfFlowBatchedMutation',
            'variables': JSON.stringify({
                "input": {
                    "client_mutation_id": "4",
                    "actor_id": id,
                    "config_enum": "GDP_READ",
                    "device_id": null,
                    "experience_id": uuidv4(),
                    "extra_params_json": JSON.stringify({
                        "app_id": "350685531728",
                        "display": "\"popup\"",
                        "kid_directed_site": "false",
                        "logger_id": `"${uuidv4()}"`,
                        "next": "\"read\"",
                        "redirect_uri": "\"https:\\/\\/www.facebook.com\\/connect\\/login_success.html\"",
                        "response_type": "\"token\"",
                        "return_scopes": "false",
                        "scope": "[\"email\",\"public_profile\"]",
                        "sso_key": "\"com\"",
                        "steps": "{\"read\":[\"email\",\"public_profile\"]}",
                        "tp": "\"unspecified\"",
                        "cui_gk": "\"[PASS]:\"",
                        "is_limited_login_shim": "false"
                    }),
                    "flow_name": "GDP",
                    "flow_step_type": "STANDALONE",
                    "outcome": "APPROVED",
                    "source": "gdp_delegated",
                    "surface": "FACEBOOK_COMET"
                }
            }),
            'server_timestamps': 'true',
            'doc_id': '6494107973937368'
        });

        const response2 = await axios.post('https://www.facebook.com/api/graphql/', postData, {
            headers: headers2
        });

        console.log('GraphQL Response:', JSON.stringify(response2.data, null, 2));

        const uri = response2.data.data.run_post_flow_action.uri;
        
        // Follow the consent complete URL to get the actual redirect with token
        const response3 = await axios.get(uri, {
            headers: {
                'authority': 'www.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                'Cookie': cookie
            },
            maxRedirects: 0,
            validateStatus: (status) => status >= 200 && status < 400
        });

        let access_token = null;

        // Check if response has redirect location
        if (response3.headers.location) {
            const redirectUrl = response3.headers.location;
            console.log('Redirect URL:', redirectUrl);
            
            // Try to extract token from redirect URL
            if (redirectUrl.includes('access_token=')) {
                const tokenMatch = redirectUrl.match(/access_token=([^&]+)/);
                if (tokenMatch) {
                    access_token = tokenMatch[1];
                }
            } else if (redirectUrl.includes('#')) {
                const fragment = redirectUrl.split('#')[1];
                const fragmentParams = new URLSearchParams(fragment);
                access_token = fragmentParams.get('access_token');
            }
        }

        // If not found in redirect, check response body
        if (!access_token && response3.data) {
            const bodyStr = typeof response3.data === 'string' ? response3.data : JSON.stringify(response3.data);
            
            // Try to find access_token in response body
            const tokenMatch = bodyStr.match(/access_token[=:][\s"]*([^"&\s]+)/);
            if (tokenMatch) {
                access_token = tokenMatch[1];
            }
            
            // Try to find close_uri in response
            const closeUriMatch = bodyStr.match(/close_uri[=:][\s"]*([^"&\s]+)/);
            if (closeUriMatch) {
                try {
                    const decodedCloseUri = decodeURIComponent(closeUriMatch[1]);
                    if (decodedCloseUri.includes('access_token')) {
                        const fragment = decodedCloseUri.split('#')[1];
                        if (fragment) {
                            const fragmentParams = new URLSearchParams(fragment);
                            access_token = fragmentParams.get('access_token');
                        }
                    }
                } catch (e) {}
            }
        }

        if (!access_token) {
            // Alternative method: Try direct OAuth approach
            console.log('\nTrying alternative method...');
            
            const oauthResponse = await axios.get('https://www.facebook.com/v2.3/dialog/oauth', {
                headers: headers1,
                params: {
                    'redirect_uri': 'https://www.facebook.com/connect/login_success.html',
                    'scope': 'email,public_profile',
                    'response_type': 'token',
                    'client_id': '350685531728',
                },
                maxRedirects: 5
            });
            
            // Check final URL for token
            if (oauthResponse.request && oauthResponse.request.res && oauthResponse.request.res.responseUrl) {
                const finalUrl = oauthResponse.request.res.responseUrl;
                if (finalUrl.includes('access_token=')) {
                    const fragment = finalUrl.split('#')[1] || finalUrl.split('?')[1];
                    if (fragment) {
                        const params = new URLSearchParams(fragment);
                        access_token = params.get('access_token');
                    }
                }
            }
        }

        if (access_token) {
            console.log('\n✅ Access Token:', access_token);
            
            // Convert to EAAG token
            try {
                const sessionResponse = await axios.post('https://api.facebook.com/method/auth.getSessionforApp', new URLSearchParams({
                    'access_token': access_token,
                    'format': 'json',
                    'new_app_id': '275254692598279',
                    'generate_session_cookies': '1'
                }));
                
                if (sessionResponse.data.access_token) {
                    console.log('\n✅ EAAG Token:', sessionResponse.data.access_token);
                } else {
                    console.log('\n⚠️ Session Response:', sessionResponse.data);
                }
            } catch (sessionError) {
                console.log('\n⚠️ Could not convert to EAAG token:', sessionError.message);
            }
        } else {
            console.log('\n❌ Không thể lấy access token. Thử phương pháp khác...');
            
            // Last resort: Business Suite token method
            console.log('\nTrying Business Suite method...');
            
            const bsResponse = await axios.get('https://business.facebook.com/content_management', {
                headers: {
                    ...headers1,
                    'Cookie': cookie
                }
            });
            
            const eaagMatch = bsResponse.data.match(/EAAG[a-zA-Z0-9]+/);
            if (eaagMatch) {
                console.log('\n✅ EAAG Token (Business Suite):', eaagMatch[0]);
            } else {
                console.log('\n❌ Không thể lấy token từ Business Suite');
            }
        }

    } catch (error) {
        if (error.response) {
            console.error('Error Response:', error.response.status, error.response.data);
        } else {
            console.error('Error:', error.message);
        }
    } finally {
        rl.close();
    }
});
