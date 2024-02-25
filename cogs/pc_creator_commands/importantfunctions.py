from aiohttp import ClientSession
from websockets import connect
from asyncio import wait_for
from orjson import loads, dumps as dump
from discord import Embed
import base64
from decouple import config
from enum import Enum

# Copied from the game
# Some lines are commented out since those rarities are not used for any items but they are still in the game
class Rarity(Enum):
	Ancient = 0
	Normal = 1
	Rare = 2
	# UnReal = 3
	Exclusive = 4
	Innovation = 5
	# Secret = 6
	Gold = 7
	# DEBUG = 8
	# Card = 9
	Hacking = 10
	Relict = 11
	# Halloween = 12
	Epic = 13
	Season = 14

dumps = lambda a:str(dump(a), "utf-8")

TIMEOUT = 10
SERVER = config("GAME_SERVER")
SESSION_MANAGER = f"wss://{SERVER}/ws/sessionmanager"
FILE_STORAGE = f"https://{SERVER}/api/storage/pc-creator-two/Localizations/production.json"
HTTP_HEADERS = {"User-Agent": "UnityPlayer/2022.3.14f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)", "X-Unity-Version": "2022.3.14f1"}
WS_HEADERS = {"User-Agent": "websocket-sharp/1.0"}

PUBLIC_PROMOCODE_LIST = [
  "X5XKEY",
  "R5RKEY",
  "LNY024",
]
LEADERBOARDS = {
  "PC Score": "PCPower",
  "Bitcoin": "BTC",
  "Ethereum": "ETH",
  "Dogecoin": "DOGE"
}
LEADERBOARD_TITLES = {
  1: "🥇",
  2: "🥈",
  3: "🥉"
}
LOADING = "<a:Loading:867450712887918632>"

ONLINE_USERS = "0"

TOKEN = ""

# Do not edit this file by hand, I can easily generate it whenever an update drops
with open("json_files/items.json") as file:
  items = loads(file.read())

async def authed_post(*args, **kwargs):
  global TOKEN
  newHeaders = dict(HTTP_HEADERS)
  if "headers" in kwargs:
    newHeaders = kwargs["headers"]
  if TOKEN == "":
    TOKEN = await get_token()
  newHeaders["Authorization"] = "Bearer "+TOKEN
  kwargs["headers"] = newHeaders

  async with ClientSession() as session:
    while True:
      result = await session.post(*args, **kwargs)

      await result.text() # some things break without this for some reason haha
      #print(args, kwargs, TOKEN, result.status, await result.text())

      if result.status == 401:
        TOKEN = await get_token()
        newHeaders["Authorization"] = "Bearer "+TOKEN
      else:
        return result
  

async def get_trader(id="", code=""):
  result = await authed_post(f"https://{SERVER}/api/trading/trader/get", json={"traderID": id, "traderCode": code})

  if result.status != 204:
    return await result.json(loads=loads)

async def get_account(userid):
  async with ClientSession() as session:
    result = await session.get(f"https://{SERVER}/api/storage/pc-creator-two/PlayerSaves/{userid}.json?alt=media", headers=HTTP_HEADERS)

    return await result.json(loads=loads)
  
async def upload_account(userid, account):
  return await authed_post(f"https://{SERVER}/api/storage/pc-creator-two/PlayerSaves/{userid}.json?alt=media", json=account)

async def get_userid(email):
  async with ClientSession() as session:
    result = await session.post(f"https://us-central1-pc-creator-test.cloudfunctions.net/getUserUUID?email={email}")

    if result.status == 200:
      return await result.text()

async def get_token():
  async with ClientSession() as session:
      result = await session.post(f"https://{SERVER}/api/auth/token", json={
        "UserID": "pc-creator-2-discord-bot",
        "ProjectID": "pc-creator-two",
        "Country": "TV",
        "Version": "1.12.0"
      }, headers=HTTP_HEADERS)
      return (await result.json(loads=loads))["token"]

async def check_main_server():
  global ONLINE_USERS, TOKEN
  try:
    if TOKEN == "":
      TOKEN = await get_token()

    async with connect(SESSION_MANAGER, extra_headers=WS_HEADERS) as socket:
      await socket.send(dumps({"method": "authorize", "args": TOKEN}))
      async for msg in socket:
        break
      await socket.send(dumps({"method": "Subscribe"}))
      async for msg in socket:
        msg = loads(msg)
        ONLINE_USERS = str(msg["response"]["sessionCount"])
        await socket.close()
    return True
  except:
    return False

async def check_http(url):
  try:
    async with ClientSession() as session:
      result = await session.get(url, headers=HTTP_HEADERS)
    return result.status < 500 
  except:
    return False


async def get_lb(id, count=100):
  result = await authed_post(f"https://{SERVER}/api/leaderboard/get", json={"ID": id, "limit": count})

  return await result.json(loads=loads)

definitions = {
  FILE_STORAGE: {
    "name": "File Storage",
    "check": lambda: check_http(FILE_STORAGE)
  },
  SESSION_MANAGER: {
    "name": "Main Server",
    "check": check_main_server
  }
}


def format_msg(url, status):
  if status is True:
    data = f"✅ | {definitions[url]['name']} is online\n"
    if url == SESSION_MANAGER:
      data += f"\n{ONLINE_USERS} users online"
    return data
  if status is False:
    return f"❌ | {definitions[url]['name']} is down!\n"
  if status == "loading":
    return f"{LOADING} | Connecting to {definitions[url]['name']}...\n"

def bool_emoji(a):
    return "✅" if a else "❌"

def decrypt_currency(enc):
  try:
    value = base64.b64decode(enc["_encryptedValue"]).decode()
  except:
    return enc
  
  try:
    value = float(value)
  except:
    return value
  
  if str(value)[-2:] == ".0":
    return int(value)
  
  return value
async def checker_wrapper(coro):
  try:
    return await wait_for(coro, timeout=TIMEOUT)
  except:
    return False


async def live_check(index, item, checks, response):
  definition = definitions[item]
  data = await checker_wrapper(definition["check"]())
  checks[index] = format_msg(item, data)
  await response.edit_original_message(
    embed=Embed(title="Status", description=''.join(checks).strip()))
  return

# How much the currency actually weighs (based on how much a normal user might have)
def currency_factor(name):
  if name == "Usd":
    return 0.0005
  if name == "Btc":
    return 0.04
  if name == "Eth":
    return 0.03
  if name == "Doge":
    return 0.02
  if name == "Gem":
    return 1
  if name == "Sf":
    return 0.05
  if name == "Tlc":
    return 0.005
  
  return 1.0

# Same as above but for the rarity of items
def rarity_factor(item):
  try:
    rarity = Rarity(items[item["id"]])

    if rarity == Rarity.Ancient:
      return 0.0001
    if rarity == Rarity.Normal:
      return 0.0002
    if rarity == Rarity.Rare:
      return 0.0003
    if rarity == Rarity.Exclusive:
      return 0.0004
    if rarity == Rarity.Innovation:
      return 0.005
    if rarity == Rarity.Gold:
      return 2.5
    if rarity == Rarity.Relict:
      return 5.0
    if rarity == Rarity.Epic: # Most often, cheaters use the most basic apk mods, where you have lots of gems, so they open lots of crates and receive lots of epic items/gold and below
      return 10.0
    if rarity == Rarity.Season:
      return 4.0
    if rarity == Rarity.Hacking:
      return 2.0
    
    return 1.0
  except:
    return 1.0

# Maybe not the best formula but it works alright
def suspect_confidence(account, currencies, visual_inventory, item_limit):
  result_factor = 0
  total_currency_factor = 0
  total_item_factor = 0

  has_payment = account["accountInfo"]["hasSubscription"] or account["adsRemoved"] or account["adsRemovedUltimate"]

  for currency in currencies:
    total_currency_factor += currency_factor(currency) * currencies[currency]
  
  total_currency_factor /= len(currencies)
  total_currency_factor /= account["level"]
  result_factor += total_currency_factor

  for item in account["inventory"]["itemReferences"]:
    total_item_factor += rarity_factor(item)
  
  result_factor += total_item_factor


  if "IPhone" in account["platform"]: # It is still possible to cheat even on apple devices but I have never seen someone do that so its likely very rare
    result_factor *= 0.75
  elif account["suspect"]:
    result_factor *= 1.25

  if has_payment:
    result_factor *= 0.75

  if len(visual_inventory) > 1.25 * item_limit:
    result_factor *= 1.25
  
  result_factor /= 100

  result_factor *= 70 / account["level"]

  return result_factor