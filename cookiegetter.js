const axios = require('axios');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Nhập Cookie: ', async (cookie) => {
    try {
        const id = cookie.split('c_user=')[1]?.split(';')[0];
        if (!id) {
            throw new Error('Cookie không hợp lệ - không tìm thấy c_user');
        }
        
        console.log('User ID:', id);
        console.log('\n🔄 Đang lấy token...\n');

        const headers = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
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

        // Method 1: Direct OAuth with login_success redirect
        console.log('📌 Method 1: Direct OAuth...');
        try {
            const oauthUrl = 'https://www.facebook.com/dialog/oauth';
            const oauthParams = new URLSearchParams({
                client_id: '124024574287414',
                redirect_uri: 'https://www.facebook.com/connect/login_success.html',
                scope: 'public_profile,email',
                response_type: 'token'
            });

            const response = await axios.get(`${oauthUrl}?${oauthParams.toString()}`, {
                headers: headers,
                maxRedirects: 0,
                validateStatus: (status) => status >= 200 && status < 400
            });

            if (response.headers.location) {
                const location = response.headers.location;
                if (location.includes('access_token=')) {
                    const token = location.match(/access_token=([^&]+)/)?.[1];
                    if (token) {
                        console.log('\n✅ Access Token (Method 1):', token);
                        await convertToEAAG(token);
                        rl.close();
                        return;
                    }
                }
            }
        } catch (e) {
            if (e.response?.headers?.location?.includes('access_token=')) {
                const token = e.response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ Access Token (Method 1):', token);
                    await convertToEAAG(token);
                    rl.close();
                    return;
                }
            }
        }

        // Method 2: Instagram app OAuth
        console.log('📌 Method 2: Instagram OAuth...');
        try {
            const igOauthParams = new URLSearchParams({
                client_id: '124024574287414',
                redirect_uri: 'https://www.instagram.com/accounts/signup/',
                scope: 'email',
                response_type: 'token'
            });

            const response = await axios.get(`https://www.facebook.com/dialog/oauth?${igOauthParams.toString()}`, {
                headers: headers,
                maxRedirects: 0,
                validateStatus: (status) => status >= 200 && status < 400
            });

            if (response.headers.location?.includes('access_token=')) {
                const token = response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ Access Token (Method 2):', token);
                    await convertToEAAG(token);
                    rl.close();
                    return;
                }
            }
        } catch (e) {
            if (e.response?.headers?.location?.includes('access_token=')) {
                const token = e.response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ Access Token (Method 2):', token);
                    await convertToEAAG(token);
                    rl.close();
                    return;
                }
            }
        }

        // Method 3: Business Suite EAAG extraction
        console.log('📌 Method 3: Business Suite...');
        try {
            const bsResponse = await axios.get('https://business.facebook.com/content_management', {
                headers: headers
            });

            const eaagMatch = bsResponse.data.match(/"accessToken":"(EAAG[^"]+)"/);
            if (eaagMatch) {
                console.log('\n✅ EAAG Token (Business Suite):', eaagMatch[1]);
                rl.close();
                return;
            }

            const eaagMatch2 = bsResponse.data.match(/EAAG[a-zA-Z0-9]{50,}/);
            if (eaagMatch2) {
                console.log('\n✅ EAAG Token (Business Suite):', eaagMatch2[0]);
                rl.close();
                return;
            }
        } catch (e) {}

        // Method 4: Ads Manager
        console.log('📌 Method 4: Ads Manager...');
        try {
            const adsResponse = await axios.get('https://www.facebook.com/adsmanager/manage/campaigns', {
                headers: headers
            });

            const eaagMatch = adsResponse.data.match(/"accessToken":"(EAAG[^"]+)"/);
            if (eaagMatch) {
                console.log('\n✅ EAAG Token (Ads Manager):', eaagMatch[1]);
                rl.close();
                return;
            }
        } catch (e) {}

        // Method 5: Graph API Explorer App
        console.log('📌 Method 5: Graph API Explorer...');
        try {
            const explorerParams = new URLSearchParams({
                client_id: '145634995501895',
                redirect_uri: 'https://developers.facebook.com/tools/explorer/callback',
                scope: 'public_profile,email',
                response_type: 'token'
            });

            const response = await axios.get(`https://www.facebook.com/dialog/oauth?${explorerParams.toString()}`, {
                headers: headers,
                maxRedirects: 0,
                validateStatus: (status) => status >= 200 && status < 400
            });

            if (response.headers.location?.includes('access_token=')) {
                const token = response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ Access Token (Method 5):', token);
                    await convertToEAAG(token);
                    rl.close();
                    return;
                }
            }
        } catch (e) {
            if (e.response?.headers?.location?.includes('access_token=')) {
                const token = e.response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ Access Token (Method 5):', token);
                    await convertToEAAG(token);
                    rl.close();
                    return;
                }
            }
        }

        // Method 6: Mobile app token
        console.log('📌 Method 6: Mobile App OAuth...');
        try {
            const mobileParams = new URLSearchParams({
                client_id: '6628568379',
                redirect_uri: 'fbconnect://success',
                scope: 'email,publish_actions',
                response_type: 'token'
            });

            const response = await axios.get(`https://www.facebook.com/dialog/oauth?${mobileParams.toString()}`, {
                headers: {
                    ...headers,
                    'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
                },
                maxRedirects: 0,
                validateStatus: (status) => status >= 200 && status < 400
            });

            if (response.headers.location?.includes('access_token=')) {
                const token = response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ Access Token (Method 6):', token);
                    await convertToEAAG(token);
                    rl.close();
                    return;
                }
            }
        } catch (e) {
            if (e.response?.headers?.location?.includes('access_token=')) {
                const token = e.response.headers.location.match(/access_token=([^&]+)/)?.[1];
                if (token) {
                    console.log('\n✅ Access Token (Method 6):', token);
                    await convertToEAAG(token);
                    rl.close();
                    return;
                }
            }
        }

        // Method 7: Page token from www
        console.log('📌 Method 7: WWW Token Extraction...');
        try {
            const wwwResponse = await axios.get('https://www.facebook.com/', {
                headers: headers
            });

            // Try to find any token in the page
            const dtsgMatch = wwwResponse.data.match(/\["DTSGInitData",\[\],\{"token":"([^"]+)"/);
            const lsdMatch = wwwResponse.data.match(/"LSD",\[\],\{"token":"([^"]+)"/);
            
            if (dtsgMatch) {
                console.log('fb_dtsg:', dtsgMatch[1]);
            }
            if (lsdMatch) {
                console.log('lsd:', lsdMatch[1]);
            }

            const tokenMatch = wwwResponse.data.match(/accessToken['":\s]+['"]([^'"]+)['"]/);
            if (tokenMatch) {
                console.log('\n✅ Access Token (WWW):', tokenMatch[1]);
                await convertToEAAG(tokenMatch[1]);
                rl.close();
                return;
            }
        } catch (e) {}

        // Method 8: Creator Studio
        console.log('📌 Method 8: Creator Studio...');
        try {
            const creatorResponse = await axios.get('https://business.facebook.com/creatorstudio/home', {
                headers: headers
            });

            const eaagMatch = creatorResponse.data.match(/EAAG[a-zA-Z0-9]{50,}/);
            if (eaagMatch) {
                console.log('\n✅ EAAG Token (Creator Studio):', eaagMatch[0]);
                rl.close();
                return;
            }
        } catch (e) {}

        console.log('\n❌ Không thể lấy được token. Cookie có thể đã hết hạn hoặc bị checkpoint.');
        console.log('💡 Hãy thử đăng nhập lại Facebook và lấy cookie mới.');

    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        rl.close();
    }
});

async function convertToEAAG(accessToken) {
    try {
        console.log('\n🔄 Converting to EAAG token...');
        
        const sessionResponse = await axios.post('https://api.facebook.com/method/auth.getSessionforApp', 
            new URLSearchParams({
                'access_token': accessToken,
                'format': 'json',
                'new_app_id': '275254692598279',
                'generate_session_cookies': '1'
            })
        );

        if (sessionResponse.data.access_token) {
            console.log('✅ EAAG Token:', sessionResponse.data.access_token);
        } else if (sessionResponse.data.error_msg) {
            console.log('⚠️ Conversion error:', sessionResponse.data.error_msg);
            console.log('ℹ️ Using original token instead');
        }
    } catch (error) {
        console.log('⚠️ Could not convert to EAAG:', error.message);
    }
}
