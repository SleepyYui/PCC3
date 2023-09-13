from aiohttp import ClientSession
from websockets import connect
from asyncio import wait_for
from orjson import loads, dumps as dump
from discord import Embed

dumps = lambda a:str(dump(a), "utf-8")
PROMOCODE_DB = "wss://pc-creator-2-b499e-default-rtdb.firebaseio.com/.ws?ns=pc-creator-2-b499e-default-rtdb&v=5"
CHAT_WS = "ws://83.229.84.175:8081/Chat"
EXCHANGE_WS = "ws://83.229.84.175:8082/CurrencyRate"
TRADING_WS = "ws://83.229.84.175:8082/TradingPlatform"
FILE_STORAGE = "https://kamatera.creaty.me/storage/pc-creator-two/Localizations/production.json"
SESSION_MANAGER = "ws://83.229.84.175:8082/SessionManager"
LEADERBOARD = "https://kamatera.creaty.me/leaderboard"
USER_ID = 466664
TIMEOUT = 10
WORKING_CODE = "B4GF1X"  # change it to a new code later!
HTTP_HEADERS = {"User-Agent": "UnityPlayer/2021.3.3f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)", "X-Unity-Version": "2021.3.3f1"}
WS_HEADERS = {"User-Agent": "BestHTTP 1.11.2"}  # pcc2 uses it
ITEM_DB = {
  "PCCase.1105": '"Blue Panda" PC Case',
  "PCCase.1133": '"Matrix" PC Case'
}
PUBLIC_PROMOCODE_LIST = [
  "B4GF1X"
]
FIELD_NAMES = {
  "ads": "No Ads",
  "ads_ultimate": "No Ads + X2",
  "subscribe": "VIP",
  "btc": "Bitcoin",
  "usd": "USD",
  "dgc": "Dogecoin",
  "eth": "Ethereum",
  "gem": "Gems",
  "cards": "Hacking Cards",
  "ids": "Items"
}
CURRENCIES = {
  "Bitcoin": 1,
  "Ethereum": 2,
  "Dogecoin": 3
}
LEADERBOARD_TITLES = {
  1: "🥇",
  2: "🥈",
  3: "🥉"
}
LOADING = "<a:Loading:867450712887918632>"


async def check_ws(url: str) -> bool:
  try:
    async with connect(url, extra_headers=WS_HEADERS) as socket:
      await (await socket.ping())
      await socket.close()
    return True
  except:
    return False


async def _get_promocode(code: str):
  code = code.upper()
  try:
    async with connect(
        "wss://pc-creator-2-b499e-default-rtdb.firebaseio.com/.ws?ns=pc-creator-2-b499e-default-rtdb&v=5",
        extra_headers={
          "User-Agent": "Firebase/5/20.1.0/30/Android",
          "X-Firebase-AppCheck": "null",
        },
        max_size=99999999999999999) as socket:
      async for msg in socket:
        try:
          msg = loads(msg)
        except:
          continue
        if type(msg) != dict:
          continue
        elif msg["t"] == "c":
          await socket.send(
            dumps({
              "t": "d",
              "d": {
                "a": "s",
                "r": 0,
                "b": {
                  "c": {
                    "sdk.android.20-1-0": 1
                  }
                }
              }
            }))
          await socket.send(
            dumps({
              "t": "d",
              "d": {
                "a": "q",
                "r": 1,
                "b": {
                  "p": "RestoreCodes/" + code,
                  "h": ""
                }
              }
            }))
        elif msg["t"] == "d":
          msg = msg["d"]["b"]
          if msg.get("p") != None:
            return msg
          elif msg["d"] == {}:
            return None
          await socket.close()
        else:
          continue
  except:
    return "err"


async def get_promocode(code: str, retry: int = 3): # _get_promocode but with retries as the websocket sometimes fails with 1005
  attempts = 0
  while attempts < retry:
    result = await _get_promocode(code)
    if result != "err":
      return result
    attempts += 1
  raise RecursionError


async def check_promocode() -> bool:  # this code isnt very good but i think it works
  try:
    await get_promocode(WORKING_CODE)
    return True
  except:
    return False


async def check_chat() -> bool:
  try:
    recvd = 0
    async with connect(CHAT_WS, extra_headers=WS_HEADERS) as socket:
      await socket.send('{"method":"subscribe", "args":"PCC2.Main"}')
      async for msg in socket:
        recvd += 1
        if recvd == 30:  # server sends exactly 30 last messages
          break
      await socket.close()
    return True
  except:
    return False


async def check_exchange() -> bool:
  try:
    async with connect(EXCHANGE_WS, extra_headers=WS_HEADERS) as socket:
      msg = loads(await socket.recv())["response"]
      await wait_for(socket.recv(), timeout=msg["interval"])
      await socket.close()
    return True
  except:
    return False


async def check_trading() -> bool:
  try:
    async with connect(TRADING_WS,
                       max_size=99999999999,
                       extra_headers=WS_HEADERS) as ws:
      await ws.send(dumps({"method": "getTrader", "args": USER_ID}))
      msg = loads(await ws.recv())
      await ws.close()
      if msg["response"] != None:
        return True
      else:
        print("please change USER_ID as it likely doesnt work anymore!")
        return False
  except:
    return False


async def check_http(url: str) -> bool:
  try:
    async with ClientSession() as session:
      result = await session.get(url, headers=HTTP_HEADERS)
    return not str(result.status).startswith("5")
  except:
    return False


async def get_power_lb(count: int = 10) -> dict | list | None:
  async with ClientSession() as session:
    result = await session.post(LEADERBOARD, headers=HTTP_HEADERS, json={
      "method": "GetPowerLeaderboard",
      "id": -1, # your id
      "count": count,
      "page": 0
    })
    return await result.json(loads=loads)


async def get_crypto_lb(currency: int, count: int = 10) -> dict | list | None:
  async with ClientSession() as session:
    result = await session.post(LEADERBOARD, headers=HTTP_HEADERS, json={
      "method": "GetTopEntries",
      "currency": currency,
      "id": -1, # your id,
      "page": 0,
      "count": count
    })
    result = await result.json(loads=loads)
    return result["top"]


async def check_lb() -> bool:
  try:
    result = await get_power_lb(count=10)
    return len(result) == 10
  except:
    return False

definitions = {
  FILE_STORAGE: {
    "name": "File Storage",
    "check": lambda: check_http(FILE_STORAGE)
  },
  PROMOCODE_DB: {
    "name": "Promocode Validation",
    "check": check_promocode
  },
  CHAT_WS: {
    "name": "Ingame Chat",
    "check": check_chat
  },
  EXCHANGE_WS: {
    "name": "Currency Exchange",
    "check": check_exchange
  },
  TRADING_WS: {
    "name": "Trading Platform",
    "check": check_trading
  },
  SESSION_MANAGER: {
    "name": "Session Manager",
    "check": lambda: check_ws(SESSION_MANAGER)
  },
  LEADERBOARD: {
    "name": "Leaderboard",
    "check": check_lb
  }
}


def format_msg(url: str, status: bool | str) -> str:
  if status is True:
    return f"✅ | {definitions[url]['name']} is online\n"
  if status is False:
    return f"❌ | {definitions[url]['name']} is down!\n"
  if status == "loading":
    return f"{LOADING} | Connecting to {definitions[url]['name']}...\n"


async def checker_wrapper(coro) -> bool:
  try:
    return await wait_for(coro, timeout=TIMEOUT)
  except:
    return False


async def live_check(index: int, item: str, checks: list[str], response):
  definition = definitions[item]
  data = await checker_wrapper(definition["check"]())
  checks[index] = format_msg(item, data)
  await response.edit_original_message(
    embed=Embed(title="Status", description=''.join(checks).strip()))
  return
