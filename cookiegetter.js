const axios = require('axios');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Facebook Android App ID for EAAAU tokens
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

        const headers = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'cookie': cookie
        };

        // Method 1: Facebook Android OAuth (EAAAU)
        console.log('📌 Method 1: Facebook Android OAuth...');
        try {
            const oauthParams = new URLSearchParams({
                client_id: FB_ANDROID_APP_ID,
                redirect_uri: 'fbconnect://success',
                scope: 'email,public_profile',
                response_type: 'token'
            });

            const response = await axios.get(`https://www.facebook.com/dialog/oauth?${oauthParams.toString()}`, {
                headers: headers,
                maxRedirects: 0,
                validateStatus: (status) => status >= 200 && status < 400
            });

            if (response.headers.location?.includes('access_token=')) {
                const token = response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token && token.startsWith('EAAAU')) {
                    console.log('\n✅ EAAAU Token:', token);
                    rl.close();
                    return;
                }
            }
        } catch (e) {
            if (e.response?.headers?.location?.includes('access_token=')) {
                const token = e.response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token && token.startsWith('EAAAU')) {
                    console.log('\n✅ EAAAU Token:', token);
                    rl.close();
                    return;
                }
            }
        }

        // Method 2: Get any token first, then convert to EAAAU
        console.log('📌 Method 2: Convert to EAAAU...');
        let initialToken = null;

        // Try different app IDs to get initial token
        const appIds = [
            { id: '124024574287414', redirect: 'https://www.facebook.com/connect/login_success.html' },
            { id: '350685531728', redirect: 'fbconnect://success' },
            { id: '145634995501895', redirect: 'https://developers.facebook.com/tools/explorer/callback' }
        ];

        for (const app of appIds) {
            try {
                const params = new URLSearchParams({
                    client_id: app.id,
                    redirect_uri: app.redirect,
                    scope: 'email,public_profile',
                    response_type: 'token'
                });

                const response = await axios.get(`https://www.facebook.com/dialog/oauth?${params.toString()}`, {
                    headers: headers,
                    maxRedirects: 0,
                    validateStatus: (status) => status >= 200 && status < 400
                });

                if (response.headers.location?.includes('access_token=')) {
                    initialToken = response.headers.location.match(/access_token=([^&]+)/)?.[1];
                    if (initialToken) break;
                }
            } catch (e) {
                if (e.response?.headers?.location?.includes('access_token=')) {
                    initialToken = e.response.headers.location.match(/access_token=([^&]+)/)?.[1];
                    if (initialToken) break;
                }
            }
        }

        if (initialToken) {
            console.log('Got initial token, converting to EAAAU...');
            
            // Convert to EAAAU using auth.getSessionforApp
            try {
                const sessionResponse = await axios.post('https://api.facebook.com/method/auth.getSessionforApp',
                    new URLSearchParams({
                        access_token: initialToken,
                        format: 'json',
                        new_app_id: FB_ANDROID_APP_ID,
                        generate_session_cookies: '1'
                    })
                );

                if (sessionResponse.data.access_token) {
                    console.log('\n✅ EAAAU Token:', sessionResponse.data.access_token);
                    rl.close();
                    return;
                }
            } catch (e) {
                console.log('Conversion failed, trying alternative...');
            }
        }

        // Method 3: Direct password grant (using fb_dtsg)
        console.log('📌 Method 3: Password Grant Method...');
        try {
            // First get fb_dtsg
            const homeResponse = await axios.get('https://www.facebook.com/', { headers });
            const dtsgMatch = homeResponse.data.match(/\["DTSGInitData",\[\],\{"token":"([^"]+)"/);
            
            if (dtsgMatch) {
                const fb_dtsg = dtsgMatch[1];
                
                // Try token exchange
                const tokenResponse = await axios.post('https://graph.facebook.com/oauth/client_code', 
                    new URLSearchParams({
                        access_token: `${FB_ANDROID_APP_ID}|${FB_ANDROID_APP_SECRET}`,
                        client_id: FB_ANDROID_APP_ID,
                        redirect_uri: 'fbconnect://success',
                        scope: 'email,public_profile'
                    })
                );

                if (tokenResponse.data.access_token) {
                    console.log('\n✅ EAAAU Token:', tokenResponse.data.access_token);
                    rl.close();
                    return;
                }
            }
        } catch (e) {}

        // Method 4: Mobile User Agent OAuth
        console.log('📌 Method 4: Mobile OAuth...');
        try {
            const mobileHeaders = {
                ...headers,
                'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 12; SM-G991B Build/SP1A.210812.016) [FBAN/FB4A;FBAV/435.0.0.36.110;FBBV/516239178;FBDM/{density=2.75,width=1080,height=2400};FBLC/en_US;FBRV/518082198;FBCR/;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-G991B;FBSV/12;FBOP/1;FBCA/arm64-v8a:;]'
            };

            const mobileParams = new URLSearchParams({
                client_id: FB_ANDROID_APP_ID,
                redirect_uri: 'fb6628568379://authorize',
                scope: 'email,public_profile',
                response_type: 'token',
                auth_type: 'rerequest'
            });

            const response = await axios.get(`https://m.facebook.com/dialog/oauth?${mobileParams.toString()}`, {
                headers: mobileHeaders,
                maxRedirects: 0,
                validateStatus: (status) => status >= 200 && status < 400
            });

            if (response.headers.location?.includes('access_token=')) {
                const token = response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ EAAAU Token:', token);
                    rl.close();
                    return;
                }
            }
        } catch (e) {
            if (e.response?.headers?.location?.includes('access_token=')) {
                const token = e.response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ EAAAU Token:', token);
                    rl.close();
                    return;
                }
            }
        }

        // Method 5: API login method
        console.log('📌 Method 5: API Login...');
        try {
            // Extract credentials from cookie for login
            const xs = cookie.match(/xs=([^;]+)/)?.[1];
            
            if (xs) {
                const decodedXs = decodeURIComponent(xs);
                
                const loginResponse = await axios.get('https://b-api.facebook.com/method/auth.getSessionforApp', {
                    params: {
                        format: 'json',
                        access_token: `${FB_ANDROID_APP_ID}|${FB_ANDROID_APP_SECRET}`,
                        new_app_id: FB_ANDROID_APP_ID,
                        generate_session_cookies: '1',
                        uid: id
                    },
                    headers: {
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12)',
                        'Cookie': cookie
                    }
                });

                if (loginResponse.data.access_token) {
                    console.log('\n✅ EAAAU Token:', loginResponse.data.access_token);
                    rl.close();
                    return;
                }
            }
        } catch (e) {}

        // Method 6: Checkpoint bypass using cookie session
        console.log('📌 Method 6: Session Exchange...');
        try {
            // Get any working token first via different endpoint
            const wwwParams = new URLSearchParams({
                client_id: FB_ANDROID_APP_ID,
                redirect_uri: 'fbconnect://success',
                response_type: 'token,signed_request,graph_domain',
                scope: 'openid,email,public_profile',
                nonce: Math.random().toString(36).substring(7),
                state: JSON.stringify({ challenge: Math.random().toString(36) })
            });

            const response = await axios.get(`https://www.facebook.com/v18.0/dialog/oauth?${wwwParams.toString()}`, {
                headers: headers,
                maxRedirects: 0,
                validateStatus: (status) => status >= 200 && status < 400
            });

            if (response.headers.location?.includes('access_token=')) {
                const token = response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ EAAAU Token:', token);
                    rl.close();
                    return;
                }
            }
        } catch (e) {
            if (e.response?.headers?.location?.includes('access_token=')) {
                const token = e.response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ EAAAU Token:', token);
                    rl.close();
                    return;
                }
            }
        }

        console.log('\n❌ Không thể lấy được EAAAU token.');
        console.log('💡 Nguyên nhân có thể:');
        console.log('   - Cookie đã hết hạn');
        console.log('   - Tài khoản bị checkpoint');
        console.log('   - Cần đăng nhập lại và lấy cookie mới');

    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        rl.close();
    }
});
