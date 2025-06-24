import aiohttp
import asyncio
import json

with open("guest_accounts.json") as f:
    accounts = json.load(f)["accounts"]

async def login_guest(uid, password):
    async with aiohttp.ClientSession() as session:
        url = "https://ff.garena.com/api/guest_login"  # mocked login URL
        data = {"uid": uid, "password": password}
        async with session.post(url, json=data) as resp:
            return await resp.json()

async def send_like(token, target_uid):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"target_uid": target_uid}
    async with aiohttp.ClientSession() as session:
        url = "https://ff.garena.com/api/like"  # mocked like URL
        async with session.post(url, json=data, headers=headers) as resp:
            return await resp.json()