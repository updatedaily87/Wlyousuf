from fastapi import FastAPI, Query
import asyncio
from wlbittu_real_like import login_guest, send_like
import json

app = FastAPI()

with open("guest_accounts.json") as f:
    accounts = json.load(f)["accounts"]

@app.get("/like")
async def like(uid: str, key: str = Query(...)):
    if key != "wlbittu":
        return {"status": 0, "message": "Invalid API key."}

    success = 0
    for acc in accounts:
        try:
            token_data = await login_guest(acc["uid"], acc["password"])
            token = token_data.get("token")
            if token:
                res = await send_like(token, uid)
                if res.get("success"):
                    success += 1
            await asyncio.sleep(0.5)
        except:
            continue

    return {
        "status": 1,
        "message": f"✅ {success} Likes Sent to {uid}",
        "from": "WLBittu Bot",
        "likes_success": success,
        "failed": len(accounts) - success
    }