// Facebook Name Changer Terminal Tool (Fixed for Termux)
// by RIYO - Optimized for JSON appstate paste

const axios = require("axios");
const crypto = require("crypto");
const readline = require("readline");

// ========== UTILITIES ==========
const util = {};

util.fbUserAgent = "facebookexternalhit/1.1";

util.getUID = (cookie) => {
  if (!cookie) return null;
  const cUserMatch = cookie.match(/(?:^|;)\s*c_user=([^;]+)/);
  const iUserMatch = cookie.match(/(?:^|;)\s*i_user=([^;]+)/);
  return (cUserMatch && cUserMatch[1]) || (iUserMatch && iUserMatch[1]) || null;
};

util.isInstagram = (cookie) =>
  cookie && (cookie.includes("sessionid") || cookie.includes("csrftoken") || cookie.includes("rur"));

util.generateMutationID = () =>
  crypto.randomUUID ? crypto.randomUUID() : crypto.randomBytes(8).toString("hex");

util.getFrom = (str, startToken, endToken) => {
  if (!str) return null;
  const start = str.indexOf(startToken);
  if (start === -1) return null;
  const startIndex = start + startToken.length;
  const lastHalf = str.substring(startIndex);
  const end = lastHalf.indexOf(endToken);
  if (end === -1) return null;
  return lastHalf.substring(0, end);
};

util.getFbData = async (cookie, isInstagram) => {
  try {
    const headers = {
      "user-agent": util.fbUserAgent,
      cookie: cookie,
      "cache-control": "max-age=0",
      "upgrade-insecure-requests": "1",
      referer: `https://www.${isInstagram ? "instagram" : "facebook"}.com/`,
      origin: `https://www.${isInstagram ? "instagram" : "facebook"}.com`,
    };

    const fb = await axios.get(`https://www.${isInstagram ? "instagram" : "facebook"}.com`, { 
      headers,
      timeout: 10000 
    });
    
    const userID = util.getUID(cookie);
    const fb_dtsg = util.getFrom(fb.data, '["DTSGInitData",[],{"token":"', '","');
    
    let req = 1;
    let jazoest = "2";
    if (fb_dtsg) {
      for (let i = 0; i < fb_dtsg.length; i++) jazoest += fb_dtsg.charCodeAt(i);
    }

    return {
      data: {
        fb_dtsg: fb_dtsg || "",
        jazoest,
        lsd: util.getFrom(fb.data, '["LSD",[],{"token":"', '"}') || "",
        av: userID,
        __a: 1,
        __user: userID,
        __req: (req++).toString(36),
      },
      userID,
      headers,
    };
  } catch (error) {
    console.error("Error getting FB data:", error.message);
    throw error;
  }
};

util.execGraph = async (cookie, data, isAccountsCenter, isInstagram) => {
  try {
    const { data: form, headers } = await util.getFbData(cookie, isInstagram);
    const url = `https://${isAccountsCenter ? "accountscenter" : "www"}.${
      isInstagram ? "instagram" : "facebook"
    }.com/api/graphql`;

    const res = await axios.post(url, new URLSearchParams({ ...form, ...data }), {
      headers: {
        ...headers,
        "content-type": "application/x-www-form-urlencoded",
      },
      timeout: 15000,
    });
    return res.data;
  } catch (error) {
    console.error("Graph API error:", error.message);
    throw error;
  }
};

util.getAccountsCenter = async (cookie) => {
  try {
    const getinsta = await util.execGraph(cookie, {
      fb_api_caller_class: "RelayModern",
      fb_api_req_friendly_name: "FXAccountsCenterProfilesPageV2Query",
      variables: JSON.stringify({
        device_id: "device_id_fetch_datr",
        flow: "FB_WEB_SETTINGS",
        interface: "FB_WEB",
        platform: "FACEBOOK",
        scale: 2
      }),
      server_timestamps: "true",
      doc_id: "7683343698455923",
    }, true);

    const linked = [
      ...(getinsta?.data?.fx_identity_management?.identities_and_central_identities?.linked_identities_to_pci || []),
      ...(getinsta?.data?.fx_identity_management?.identities_and_central_identities?.business_identities || []),
    ];

    if (!linked.length) return [];
    
    return linked
      .filter((x) => x.identity_type !== "FB_ADDITIONAL_PROFILE")
      .map((x) => ({
        name: x.full_name,
        username: x.username,
        uid: x.canonical_id || x.administering_account_id,
        type: x.account_type,
        id_type: x.detailed_identity_type,
        id_type2: x.identity_type,
      }));
  } catch (error) {
    console.error("Error getting accounts center:", error.message);
    return [];
  }
};

// ========== IMPROVED APPSTATE HANDLER ==========
util.parseAppstate = (input) => {
  try {
    // If input is already a cookie string, return it
    if (typeof input === 'string' && input.includes('=') && input.includes(';')) {
      return input;
    }

    // Try to parse as JSON
    let jsonStr = input.trim();
    
    // Fix common JSON issues
    if (!jsonStr.startsWith('[')) {
      // If it starts with random text, find the first [
      const startBracket = jsonStr.indexOf('[');
      if (startBracket !== -1) {
        jsonStr = jsonStr.substring(startBracket);
      }
    }

    // Find the complete JSON array by matching brackets
    let bracketCount = 0;
    let endIndex = -1;
    
    for (let i = 0; i < jsonStr.length; i++) {
      if (jsonStr[i] === '[') bracketCount++;
      if (jsonStr[i] === ']') bracketCount--;
      if (bracketCount === 0 && i > 0) {
        endIndex = i;
        break;
      }
    }

    if (endIndex !== -1) {
      jsonStr = jsonStr.substring(0, endIndex + 1);
    }

    const appstate = JSON.parse(jsonStr);
    
    if (Array.isArray(appstate)) {
      const cookieString = appstate
        .map(cookie => `${cookie.name}=${cookie.value}`)
        .join('; ');
      console.log(`✅ Converted ${appstate.length} cookies to string`);
      return cookieString;
    }
    
    throw new Error("Invalid appstate format");
  } catch (error) {
    console.log("❌ Failed to parse appstate as JSON, using as raw string");
    // Return as is, might be cookie string
    return input;
  }
};

// ========== MAIN PROGRAM ==========
(async () => {
  console.log("\n" + "=".repeat(50));
  console.log("   FB NAME CHANGER (TERMINAL TOOL)");
  console.log("=".repeat(50) + "\n");

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const ask = (question) => new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });

  try {
    console.log("📝 PASTE INSTRUCTIONS:");
    console.log("1. Copy your FULL Facebook appstate (entire JSON array)");
    console.log("2. Long press to paste in Termux");
    console.log("3. Wait for confirmation before pasting Instagram\n");
    
    const appstateFbInput = "datr=Et0uaRCzl-8h4cOeN3YsN5os; sb=Et0uaWmiCN2rnFzRZdEwVcgj; m_pixel_ratio=2; x-referer=eyJyIjoiL2NoZWNrcG9pbnQvMTUwMTA5MjgyMzUyNTI4Mi9sb2dvdXQvP25leHQ9aHR0cHMlM0ElMkYlMkZtLmZhY2Vib29rLmNvbSUyRiUzRmRlb2lhJTNEMSIsImgiOiIvY2hlY2twb2ludC8xNTAxMDkyODIzNTI1MjgyL2xvZ291dC8%2FbmV4dD1odHRwcyUzQSUyRiUyRm0uZmFjZWJvb2suY29tJTJGJTNGZGVvaWElM0QxIiwicyI6Im0ifQ%3D%3D; locale=en_US; vpd=v1%3B520x328x2; c_user=61569634753113; xs=49%3AhMnMtuJ4NzGVLQ%3A2%3A1764680571%3A-1%3A-1; pas=61552706407695%3AcWvsU0p8VD%2C61563790194125%3AcuWMERIFWk%2C61569634753113%3Absbily3KUw; wd=328x520; ps_l=1; ps_n=1; fr=0VpGcRBqSLhwISgWn.AWdjLEjtDKeOB6Ev7cM4PEUVbIpnpduJtVf8q0a4r1v5QqrM9Os.BpLt0S..AAA.0.0.BpLuqQ.AWfplluBJK7PZADFkjq4hJJSWls; fbl_st=101425388%3BT%3A29411373; wl_cbv=v2%3Bclient_version%3A3004%3Btimestamp%3A1764682384"
    const appstateIgInput = "datr=g84uaYu0GtBQ_HbfGV2D5Pnm; ig_did=716DE9F8-48CA-4060-9FB1-5BD62E59E237; wd=360x664; dpr=2; mid=aS7OgwABAAGuibVyE1uvJDhKIaaI; csrftoken=FRrzENKM8e2h2OiDPS3CaQHDtAFw12nn; ds_user_id=78648228706; sessionid=78648228706%3AaUyZy9WmTa7Y4w%3A19%3AAYjBm9kMjyq8U2keOG6P7lWRZpxlqXuSDXV51-5YTg; rur="CCO054786482287060541796218470:01fe601eb5f3be4bb1ed886bbaa11d3d9065dee7b235c2e4c3369e68da33e668102278b5";
    
    if (!appstateFbInput.trim()) {
      console.log("❌ No Facebook appstate provided!");
      rl.close();
      return;
    }
    if (!appstateIgInput.trim()) {
      console.log("❌ No Instagram appstate provided!");
      rl.close();
      return;
    }

    console.log("\n✅ Instagram appstate received!\n");

    const newName = "kendrick 󱢏"
    if (!newName.trim()) {
      console.log("❌ No name provided!");
      rl.close();
      return;
    }

    rl.close();

    console.log("\n🔄 Processing appstates...");
    
    // Parse appstates
    const appstateFb = appstateFbInput;
    const appstateIg = appstateIgInput;

    console.log("✅ Appstates processed successfully!");

    // Validate Instagram appstate
    if (!util.isInstagram(appstateIg)) {
      console.log("❌ Invalid Instagram appstate! Make sure it contains sessionid or csrftoken");
      return;
    }

    console.log("\n🔍 Fetching account data...");

    const accounts = await util.getAccountsCenter(appstateFb);
    if (!accounts.length) {
      throw new Error("No accounts found. Check your Facebook appstate.");
    }

    const fbAcc = accounts.find((a) => a.type === "FACEBOOK");
    const igAcc = accounts.find((a) => a.type === "INSTAGRAM");
    console.log(fbAcc)
    console.log(igAcc)
    if (!fbAcc || !igAcc) {
      throw new Error("Couldn't find connected Facebook and Instagram accounts.");
    }

    console.log(`✅ Facebook: ${fbAcc.name} (${fbAcc.uid})`);
    console.log(`✅ Instagram: ${igAcc.name} (${igAcc.uid})`);
    console.log(`\n🔄 Changing name to: ${newName}`);

    // Change IG Name
    console.log("\n📝 Updating Instagram name...");
    const igResult = await util.execGraph(appstateIg, {
      variables: JSON.stringify({
        client_mutation_id: util.generateMutationID(),
        family_device_id: "device_id_fetch_ig_did",
        identity_ids: [igAcc.uid],
        full_name: newName.trim(),
        first_name: null,
        middle_name: null,
        last_name: null,
        interface: "IG_WEB",
      }),
      fb_api_req_friendly_name: "useFXIMUpdateNameMutation",
      fb_api_caller_class: "RelayModern",
      server_timestamps: "true",
      doc_id: "28573275658982428",
    }, true, true);

    if (igResult?.errors || igResult?.data?.fxim_update_identity_name?.error) {
      const errorMsg = igResult?.data?.fxim_update_identity_name?.error?.description || 
                      igResult?.errors?.[0]?.message || "Unknown error";
      throw new Error(`Instagram update failed: ${errorMsg}`);
    }

    console.log("✅ Instagram name updated!");

    // Sync with Facebook
    console.log("🔄 Syncing with Facebook...");
    const fbResult = await util.execGraph(appstateFb, {
      fb_api_req_friendly_name: "useFXIMUpdateNameMutation",
      fb_api_caller_class: "RelayModern",
      variables: JSON.stringify({
        client_mutation_id: util.generateMutationID(),
        accounts_to_sync: [igAcc.uid, fbAcc.uid],
        resources_to_sync: ["NAME", "PROFILE_PHOTO"],
        source_of_truth_array: [
          { resource_source: "IG" },
          { resource_source: "FB" },
        ],
        source_account: fbAcc.uid,
        platform: "FACEBOOK",
        interface: "FB_WEB",
      }),
      server_timestamps: "true",
      doc_id: "9388416374608398",
    }, true, false);

    if (fbResult?.errors || fbResult?.data?.fxim_sync_resources_v2?.error) {
      const errorMsg = fbResult?.data?.fxim_sync_resources_v2?.error?.description ||
                      fbResult?.errors?.[0]?.message || "Unknown error";
      throw new Error(`Facebook sync failed: ${errorMsg}`);
    }

    console.log("\n" + "🎉".repeat(20));
    console.log(`🎉 SUCCESS: Name changed to "${newName}"`);
    console.log("🎉 Changes applied to both Facebook and Instagram!");
    console.log("🎉".repeat(20));

  } catch (error) {
    console.log("\n❌ Error:", error.message);
    if (error.response) {
      console.log("📡 Server response:", error.response.status, error.response.statusText);
    }
  } finally {
    rl.close();
  }
})();
