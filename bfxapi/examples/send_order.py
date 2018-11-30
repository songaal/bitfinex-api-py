import os
import sys
sys.path.append('../')

from bfxapi import Client

API_KEY=os.getenv("BFX_KEY")
API_SECRET=os.getenv("BFX_SECRET")

bfx = Client(
  API_KEY=API_KEY,
  API_SECRET=API_SECRET,
  logLevel='DEBUG'
)

@bfx.ws.on('order_snapshot')
async def close_all(data):
  await bfx.ws.close_all_orders()

@bfx.ws.on('order_confirmed')
async def trade_completed(order, trade):
  print ("Order confirmed.")
  print (order)
  print (trade)
  ## close the order
  # await order.close()
  # or
  # await bfx.ws.close_order(order.id)
  # or
  # await bfx.ws.close_all_orders()

@bfx.ws.on('error')
def log_error(msg):
  print ("Error: {}".format(msg))

@bfx.ws.on('authenticated')
async def submit_order(auth_message):
  await bfx.ws.submit_order('tBTCUSD', 19000, 0.01, 'EXCHANGE LIMIT')

# If you dont want to use a decorator
# ws.on('authenticated', submit_order)
# ws.on('error', log_error)

# You can also provide a callback
# await ws.submit_order('tBTCUSD', 0, 0.01,
# 'EXCHANGE MARKET', onComplete=trade_complete)

bfx.ws.run()