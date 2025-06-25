import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from datetime import datetime, timedelta
import aiohttp

API_TOKEN = "7359445506:AAElzP9Bb_uPrkXiqRxm7npe3-uqhIFfmpY"
ALLOWED_GROUP_ID = -1002837440798
VIP_USER_ID = 5490613126

bot = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

user_usage = {}
like_usage = {"BD": 0, "IND": 0}

def join_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Join Channel", url="https://t.me/wlbittu")],
    ])

def vip_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Join Channel", url="https://t.me/wlbittu")],
        [InlineKeyboardButton(text="🤖 Use VIP Bot", url="https://t.me/wlbittu_bot")],
    ])

def verify_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Join Group To Get Likes", url="https://t.me/wlbittu")],
    ])

def reset_daily_limits():
    user_usage.clear()
    like_usage["BD"] = 0
    like_usage["IND"] = 0
    print("✅ Daily limits reset.")

async def daily_reset_scheduler():
    while True:
        now = datetime.now()
        next_reset = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
        wait_seconds = (next_reset - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        reset_daily_limits()

async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                return await r.json()
    return None

def group_only(func):
    async def wrapper(msg: Message):
        if msg.chat.id != ALLOWED_GROUP_ID:
            return
        return await func(msg)
    return wrapper

@dp.message(Command("like"))
@group_only
async def like_handler(msg: Message):
    parts = msg.text.split()
    if len(parts) != 3:
        await msg.reply("❗ Correct format: /like bd uid", reply_markup=join_keyboard())
        return
    region, uid = parts[1].upper(), parts[2]
    if region not in ["BD", "IND"]:
        await msg.reply("❗ Only BD or IND regions are supported!", reply_markup=join_keyboard())
        return

    user_id = msg.from_user.id
    if user_id != VIP_USER_ID:
        count = user_usage.get(user_id, {}).get("like", 0)
        if count >= 1:
            await msg.reply("🚫 You have already used your like command today!", reply_markup=verify_keyboard())
            return

    if like_usage[region] >= 150 and user_id != VIP_USER_ID:
        await msg.reply(
            f"⚠️ Daily like limit reached for {region} region. Please try again tomorrow.",
            reply_markup=join_keyboard()
        )
        return

    wait = await msg.reply("⏳ Sending Likes, Please Wait.....")
    url = f"https://wlyousuf.onrender.com"
    data = await fetch_json(url)

    if not data:
        await wait.edit_text("❌ Failed to send request. Check UID or try later.", reply_markup=join_keyboard())
        return

    await wait.edit_text(
        f"✅ Likes Sent Successfully!

"
        f"🆔 UID: {uid}
"
        f"🎯 Likes Sent By WLBittu Bot: {data.get('LikesGivenByAPI', 'N/A')}",
        reply_markup=join_keyboard()
    )

    if user_id != VIP_USER_ID:
        user_usage.setdefault(user_id, {})["like"] = 1
        like_usage[region] += data.get("LikesGivenByAPI", 0)

async def main():
    print("🤖 WLBittu Like Bot is running...")
    asyncio.create_task(daily_reset_scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
