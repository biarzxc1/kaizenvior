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

        console.log(response2.data);

        const uri = response2.data.data.run_post_flow_action.uri;
        const url = new URL(uri);
        const close_uri = url.searchParams.get('close_uri');
        const decoded_close_uri = decodeURIComponent(close_uri);
        const fragment = new URL(decoded_close_uri).hash.substring(1);
        const fragment_params = new URLSearchParams(fragment);
        const access_token = fragment_params.get('access_token');

        console.log(access_token);

        // Uncomment if needed:
        // const sessionResponse = await axios.post('https://api.facebook.com/method/auth.getSessionforApp', new URLSearchParams({
        //     'access_token': access_token,
        //     'format': 'json',
        //     'new_app_id': '275254692598279',
        //     'generate_session_cookies': '1'
        // }));
        // const token_new = sessionResponse.data.access_token;
        // console.log(token_new);

    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        rl.close();
    }
});
