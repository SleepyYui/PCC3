from aiohttp import ClientSession
from websockets import connect
from asyncio import wait_for
from orjson import loads, dumps as dump

dumps = lambda a:str(dump(a), "utf-8")
PROMOCODE_DB = "wss://pc-creator-2-b499e-default-rtdb.firebaseio.com/.ws?ns=pc-creator-2-b499e-default-rtdb&v=5"
CHAT_WS = "ws://83.229.84.175:8081/Chat"
EXCHANGE_WS = "ws://83.229.84.175:8082/CurrencyRate"
TRADING_WS = "ws://83.229.84.175:8082/TradingPlatform"
FILE_STORAGE = "https://kamatera.creaty.me/storage/pc-creator-two/Localizations/production.json"
SESSION_MANAGER = "ws://83.229.84.175:8082/SessionManager"
definitions = {
  FILE_STORAGE: "File Storage",
  PROMOCODE_DB: "Promocode Validation",
  CHAT_WS: "Ingame Chat",
  EXCHANGE_WS: "Currency Exchange",
  TRADING_WS: "Trading Platform",
  SESSION_MANAGER: "Session Manager"
}
USER_ID = 466664
TIMEOUT = 10
WORKING_CODE = "TEST00"  # change it to a new code later!
USERAGENT = "BestHTTP 1.11.2"  # pcc2 uses it


async def check_ws(url: str) -> bool:
  try:
    async with connect(url, extra_headers={"User-Agent": USERAGENT}) as socket:
      await (await socket.ping())
      await socket.close()
    return True
  except:
    return False


async def check_promocode(
) -> bool:  # this code isnt very good but i think it works
  try:
    async with connect(
        "wss://pc-creator-2-b499e-default-rtdb.firebaseio.com/.ws?ns=pc-creator-2-b499e-default-rtdb&v=5",
        extra_headers={
          "User-Agent": "Firebase/5/20.1.0/30/Android",
          "X-Firebase-AppCheck": "null"
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
                  "p": "RestoreCodes/" + WORKING_CODE,
                  "h": ""
                }
              }
            }))
        elif msg["t"] == "d":
          msg = msg["d"]["b"]
          if msg.get("p") != None:
            return True
          elif msg["d"] == {}:
            print("please change WORKING_CODE as it likely expired!")
            return False
          await socket.close()
        else:
          continue
  except:
    return False


async def check_chat() -> bool:
  try:
    recvd = 0
    async with connect(CHAT_WS, extra_headers={"User-Agent":
                                               USERAGENT}) as socket:
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
    async with connect(EXCHANGE_WS, extra_headers={"User-Agent":
                                                   USERAGENT}) as socket:
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
                       extra_headers={"User-Agent": USERAGENT}) as ws:
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
      result = await session.get(url, headers={"User-Agent": USERAGENT})
    return not str(result.status).startswith("5")
  except:
    return False


def format_msg(url: str, status: bool) -> str:
  return f"{'✅' if status else '❌'} | {definitions[url]} is {'online' if status else 'down!'}\n"


async def checker_wrapper(coro):
  try:
    status = await wait_for(coro, timeout=TIMEOUT)
  except:
    status = False
  return status


async def check_all() -> str:
  result = ""
  result += format_msg(FILE_STORAGE, await
                       checker_wrapper(check_http(FILE_STORAGE)))
  result += format_msg(PROMOCODE_DB, await checker_wrapper(check_promocode()))
  result += format_msg(EXCHANGE_WS, await checker_wrapper(check_exchange()))
  result += format_msg(CHAT_WS, await checker_wrapper(check_chat()))
  result += format_msg(TRADING_WS, await checker_wrapper(check_trading()))
  result += format_msg(SESSION_MANAGER, await
                       checker_wrapper(check_ws(SESSION_MANAGER)))
  return result.strip()
