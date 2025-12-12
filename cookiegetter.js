const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Facebook Android App credentials
const FB_ANDROID_APP_ID = '6628568379';
const FB_ANDROID_APP_SECRET = 'c1e620fa708a1d5696fb991c1bde5662';

rl.question('Nhập Cookie: ', async (cookie) => {
    try {
        const id = cookie.split('c_user=')[1]?.split(';')[0];
        if (!id) {
            throw new Error('Cookie không hợp lệ - không tìm thấy c_user');
        }
        
        console.log('User ID:', id);
        console.log('\n🔄 Đang lấy EAAAU token...\n');

        // Common headers
        const desktopHeaders = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'cookie': cookie
        };

        const mobileHeaders = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 12; SM-G991B Build/SP1A.210812.016) [FBAN/FB4A;FBAV/435.0.0.36.110;FBBV/516239178;FBDM/{density=2.75,width=1080,height=2400};FBLC/en_US;FBRV/518082198;FBCR/;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-G991B;FBSV/12;FBOP/1;FBCA/arm64-v8a:;]',
            'cookie': cookie
        };

        // ============ METHOD 1: GraphQL Consent Flow ============
        console.log('📌 Method 1: GraphQL Consent Flow...');
        try {
            // Step 1: Get fb_dtsg
            const oauthUrl = `https://www.facebook.com/v2.3/dialog/oauth?redirect_uri=fbconnect://success&scope=email,public_profile&response_type=token&client_id=${FB_ANDROID_APP_ID}`;
            
            const response1 = await axios.get(oauthUrl, { headers: desktopHeaders });
            const responseText = response1.data.replace(/\[\]/g, '');
            
            const fb_dtsg_match = responseText.match(/DTSGInitData"[^{]*\{"token":"([^"]+)"/);
            if (!fb_dtsg_match) {
                throw new Error('fb_dtsg not found');
            }
            const fb_dtsg = fb_dtsg_match[1];
            console.log('   ✓ Got fb_dtsg');

            // Step 2: GraphQL mutation to approve consent
            const graphqlHeaders = {
                'authority': 'www.facebook.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.facebook.com',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'x-fb-friendly-name': 'useCometConsentPromptEndOfFlowBatchedMutation',
                'cookie': cookie
            };

            const postData = new URLSearchParams({
                'fb_dtsg': fb_dtsg,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'useCometConsentPromptEndOfFlowBatchedMutation',
                'variables': JSON.stringify({
                    "input": {
                        "client_mutation_id": "1",
                        "actor_id": id,
                        "config_enum": "GDP_READ",
                        "device_id": null,
                        "experience_id": uuidv4(),
                        "extra_params_json": JSON.stringify({
                            "app_id": FB_ANDROID_APP_ID,
                            "display": "\"popup\"",
                            "kid_directed_site": "false",
                            "logger_id": `"${uuidv4()}"`,
                            "next": "\"read\"",
                            "redirect_uri": "\"fbconnect:\\/\\/success\"",
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
                headers: graphqlHeaders
            });

            const uri = response2.data?.data?.run_post_flow_action?.uri;
            if (uri) {
                console.log('   ✓ Got consent URI');
                
                // Step 3: Follow the consent URL
                const response3 = await axios.get(uri, {
                    headers: desktopHeaders,
                    maxRedirects: 5,
                    validateStatus: () => true
                });

                // Check response text for token
                const responseBody = typeof response3.data === 'string' ? response3.data : JSON.stringify(response3.data);
                
                // Try to find access_token in various formats
                let token = null;
                
                // Check for direct token in response
                const tokenPatterns = [
                    /access_token=([^&"'\s]+)/,
                    /"access_token":"([^"]+)"/,
                    /access_token\\u0022:\\u0022([^\\]+)/,
                    /EAAAU[a-zA-Z0-9]+/
                ];

                for (const pattern of tokenPatterns) {
                    const match = responseBody.match(pattern);
                    if (match) {
                        token = match[1] || match[0];
                        break;
                    }
                }

                // Check final URL
                if (!token && response3.request?.res?.responseUrl) {
                    const finalUrl = response3.request.res.responseUrl;
                    const urlMatch = finalUrl.match(/access_token=([^&]+)/);
                    if (urlMatch) token = urlMatch[1];
                }

                if (token && token.startsWith('EAAAU')) {
                    console.log('\n✅ EAAAU Token:', token);
                    rl.close();
                    return;
                } else if (token) {
                    // Convert to EAAAU
                    const eaaau = await convertToEAAAU(token);
                    if (eaaau) {
                        console.log('\n✅ EAAAU Token:', eaaau);
                        rl.close();
                        return;
                    }
                }
            }
        } catch (e) {
            console.log('   ✗ Method 1 failed:', e.message);
        }

        // ============ METHOD 2: Direct b-api Mobile Auth ============
        console.log('📌 Method 2: Mobile b-api Auth...');
        try {
            const params = new URLSearchParams({
                adid: uuidv4(),
                format: 'json',
                device_id: uuidv4(),
                cpl: 'true',
                family_device_id: uuidv4(),
                credentials_type: 'device_based_login_password',
                generate_session_cookies: '1',
                generate_analytics_claim: '1',
                generate_machine_id: '1',
                currently_logged_in_userid: id,
                try_num: '1',
                enroll_misauth: 'false',
                meta_inf_fbmeta: 'NO_FILE',
                source: 'login',
                machine_id: uuidv4().replace(/-/g, ''),
                fb_api_req_friendly_name: 'authenticate',
                fb_api_caller_class: 'AuthOperations',
                api_key: '62f8ce9f74b12f84c123cc23437a4a32',
                access_token: `${FB_ANDROID_APP_ID}|${FB_ANDROID_APP_SECRET}`
            });

            const response = await axios.post('https://b-api.facebook.com/method/auth.login', params, {
                headers: {
                    ...mobileHeaders,
                    'content-type': 'application/x-www-form-urlencoded',
                    'x-fb-friendly-name': 'authenticate',
                    'x-fb-connection-type': 'WIFI'
                }
            });

            if (response.data?.access_token?.startsWith('EAAAU')) {
                console.log('\n✅ EAAAU Token:', response.data.access_token);
                rl.close();
                return;
            }
        } catch (e) {
            console.log('   ✗ Method 2 failed:', e.message);
        }

        // ============ METHOD 3: Touch Facebook OAuth ============
        console.log('📌 Method 3: Touch Facebook OAuth...');
        try {
            const touchUrl = `https://touch.facebook.com/dialog/oauth?client_id=${FB_ANDROID_APP_ID}&redirect_uri=fbconnect://success&response_type=token&scope=email,public_profile`;
            
            const response = await axios.get(touchUrl, {
                headers: mobileHeaders,
                maxRedirects: 0,
                validateStatus: () => true
            });

            const location = response.headers.location || '';
            if (location.includes('access_token=')) {
                const token = location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    if (token.startsWith('EAAAU')) {
                        console.log('\n✅ EAAAU Token:', token);
                        rl.close();
                        return;
                    } else {
                        const eaaau = await convertToEAAAU(token);
                        if (eaaau) {
                            console.log('\n✅ EAAAU Token:', eaaau);
                            rl.close();
                            return;
                        }
                    }
                }
            }
        } catch (e) {
            console.log('   ✗ Method 3 failed:', e.message);
        }

        // ============ METHOD 4: m.facebook OAuth ============
        console.log('📌 Method 4: Mobile Facebook OAuth...');
        try {
            const mUrl = `https://m.facebook.com/v19.0/dialog/oauth?client_id=${FB_ANDROID_APP_ID}&redirect_uri=fb${FB_ANDROID_APP_ID}://authorize&response_type=token&scope=email,public_profile`;
            
            const response = await axios.get(mUrl, {
                headers: mobileHeaders,
                maxRedirects: 0,
                validateStatus: () => true
            });

            const location = response.headers.location || '';
            if (location.includes('access_token=')) {
                const token = location.match(/access_token=([^&]+)/)?.[1];
                if (token?.startsWith('EAAAU')) {
                    console.log('\n✅ EAAAU Token:', token);
                    rl.close();
                    return;
                }
            }

            // Check response body for forms or redirects
            if (response.data) {
                const body = typeof response.data === 'string' ? response.data : '';
                const actionMatch = body.match(/action="([^"]+)"/);
                if (actionMatch) {
                    // There's a form, might need to submit it
                    const formUrl = actionMatch[1].replace(/&amp;/g, '&');
                    
                    // Extract hidden inputs
                    const inputs = {};
                    const inputMatches = body.matchAll(/name="([^"]+)"[^>]*value="([^"]*)"/g);
                    for (const match of inputMatches) {
                        inputs[match[1]] = match[2];
                    }

                    if (Object.keys(inputs).length > 0) {
                        const formResponse = await axios.post(
                            formUrl.startsWith('http') ? formUrl : `https://m.facebook.com${formUrl}`,
                            new URLSearchParams(inputs),
                            {
                                headers: {
                                    ...mobileHeaders,
                                    'content-type': 'application/x-www-form-urlencoded'
                                },
                                maxRedirects: 0,
                                validateStatus: () => true
                            }
                        );

                        const formLocation = formResponse.headers.location || '';
                        if (formLocation.includes('access_token=')) {
                            const token = formLocation.match(/access_token=([^&]+)/)?.[1];
                            if (token?.startsWith('EAAAU')) {
                                console.log('\n✅ EAAAU Token:', token);
                                rl.close();
                                return;
                            }
                        }
                    }
                }
            }
        } catch (e) {
            console.log('   ✗ Method 4 failed:', e.message);
        }

        // ============ METHOD 5: Get any token + Convert ============
        console.log('📌 Method 5: Token Conversion...');
        try {
            const apps = [
                { id: '124024574287414', redirect: 'https://www.facebook.com/connect/login_success.html' },
                { id: '350685531728', redirect: 'fbconnect://success' },
                { id: '145634995501895', redirect: 'https://developers.facebook.com/tools/explorer/callback' },
                { id: '256002347743983', redirect: 'https://www.facebook.com/connect/login_success.html' }
            ];

            for (const app of apps) {
                try {
                    const url = `https://www.facebook.com/dialog/oauth?client_id=${app.id}&redirect_uri=${encodeURIComponent(app.redirect)}&response_type=token&scope=email,public_profile`;
                    
                    const response = await axios.get(url, {
                        headers: desktopHeaders,
                        maxRedirects: 0,
                        validateStatus: () => true
                    });

                    const location = response.headers.location || '';
                    if (location.includes('access_token=')) {
                        const token = location.match(/access_token=([^&]+)/)?.[1];
                        if (token) {
                            console.log('   ✓ Got token from app', app.id);
                            const eaaau = await convertToEAAAU(token);
                            if (eaaau) {
                                console.log('\n✅ EAAAU Token:', eaaau);
                                rl.close();
                                return;
                            }
                        }
                    }
                } catch (e) {}
            }
        } catch (e) {
            console.log('   ✗ Method 5 failed:', e.message);
        }

        // ============ METHOD 6: Facebook Lite App ============
        console.log('📌 Method 6: Facebook Lite OAuth...');
        try {
            const liteAppId = '213546525407071'; // FB Lite app ID
            const liteHeaders = {
                ...mobileHeaders,
                'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 11; RMX3085 Build/RP1A.200720.011) [FBAN/FBLite;FBAV/336.0.0.10.99;FBBV/444746238;FBDM/{density=2.0,width=720,height=1560};FBLC/en_US;FBRV/446313429;FBCR/GLOBE;FBMF/realme;FBBD/realme;FBPN/com.facebook.lite;FBDV/RMX3085;FBSV/11;FBOP/1;FBCA/armeabi-v7a:armeabi;]'
            };

            const liteUrl = `https://m.facebook.com/dialog/oauth?client_id=${liteAppId}&redirect_uri=fbconnect://success&response_type=token&scope=email,public_profile`;
            
            const response = await axios.get(liteUrl, {
                headers: liteHeaders,
                maxRedirects: 0,
                validateStatus: () => true
            });

            const location = response.headers.location || '';
            if (location.includes('access_token=')) {
                const token = location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    const eaaau = await convertToEAAAU(token);
                    if (eaaau) {
                        console.log('\n✅ EAAAU Token:', eaaau);
                        rl.close();
                        return;
                    }
                }
            }
        } catch (e) {
            console.log('   ✗ Method 6 failed:', e.message);
        }

        // ============ METHOD 7: Messenger App ============
        console.log('📌 Method 7: Messenger OAuth...');
        try {
            const messengerAppId = '256002347743983'; // Messenger app ID
            const msgHeaders = {
                ...mobileHeaders,
                'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 12; SM-G991B Build/SP1A.210812.016) [FBAN/Orca-Android;FBAV/385.0.0.12.114;FBBV/452304528;FBDM/{density=2.75,width=1080,height=2400};FBLC/en_US;FBRV/453661983;FBCR/;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.orca;FBDV/SM-G991B;FBSV/12;FBOP/1;FBCA/arm64-v8a:;]'
            };

            const msgUrl = `https://m.facebook.com/dialog/oauth?client_id=${messengerAppId}&redirect_uri=fb${messengerAppId}://authorize&response_type=token&scope=email,public_profile`;
            
            const response = await axios.get(msgUrl, {
                headers: msgHeaders,
                maxRedirects: 0,
                validateStatus: () => true
            });

            const location = response.headers.location || '';
            if (location.includes('access_token=')) {
                const token = location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    const eaaau = await convertToEAAAU(token);
                    if (eaaau) {
                        console.log('\n✅ EAAAU Token:', eaaau);
                        rl.close();
                        return;
                    }
                }
            }
        } catch (e) {
            console.log('   ✗ Method 7 failed:', e.message);
        }

        console.log('\n❌ Không thể lấy được EAAAU token.');
        console.log('💡 Cookie có thể cần xác minh quyền cho ứng dụng.');
        console.log('💡 Thử truy cập link này trên trình duyệt đã đăng nhập:');
        console.log(`   https://www.facebook.com/dialog/oauth?client_id=${FB_ANDROID_APP_ID}&redirect_uri=fbconnect://success&response_type=token&scope=email,public_profile`);
        console.log('💡 Sau đó chấp nhận quyền và thử lại.');

    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        rl.close();
    }
});

async function convertToEAAAU(accessToken) {
    try {
        const response = await axios.post('https://api.facebook.com/method/auth.getSessionforApp',
            new URLSearchParams({
                access_token: accessToken,
                format: 'json',
                new_app_id: FB_ANDROID_APP_ID,
                generate_session_cookies: '1'
            }),
            {
                headers: {
                    'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 12; SM-G991B)'
                }
            }
        );

        if (response.data?.access_token?.startsWith('EAAAU')) {
            return response.data.access_token;
        }
        return null;
    } catch (e) {
        return null;
    }
}
