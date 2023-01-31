import telepot
from time import sleep
from CredentialManagement import CredentialManagement
from tools.AccountData import AccountEnumeration
from alpaca.trading.client import TradingClient


""" CREDENTIALS """
keyfile = "/server/administrator/.credentials/.key"
database = "/server/administrator/.credentials/credentials.db"

# Gather the administrators telegram user id so the bot only responds to him.
telegramID =  CredentialManagement.SingleKeyAPICredentials(
  platform="telegram_admin",
  credabase=database,
  keyfile=keyfile
)

# Initialize the Telegram bot with the platforms API key.
bot = telepot.Bot(
  CredentialManagement.SingleKeyAPICredentials(
    platform="telegram",
    credabase=database,
    keyfile=keyfile
  )
)

# Unlock the Alpaca.Markets API key and secret.
credentials = CredentialManagement.MultiKeyAPICredentials(
  platform="alpaca", credabase=database, keyfile=keyfile
)

# Pull the credentials from the dictionary.
key = credentials['key']; secret = credentials['secret']


# Initialize the trade client with key and secret.
brokerage_account = AccountData(TradingClient(key, secret, paper=False))


""" End-User Interface """
def BrokerBot(message):
  """
  The Broker Bot manages communications between the user and the daemon.
  """
  packet_data = message["text"].split(" ")
  command = str(packet_data[0])

  # Get all account data.
  if command == "/account": bot.sendMessage(telegramID, brokerage_account.GetAccount())

  # Enumerate all current positions. 
  if command == "/positions": bot.sendMessage(telegramID, brokerage_account.GetAllPositions())

  # List all assets offered by the broker.
  if command == "/getassets": bot.sendMessage(telegramID, brokerage_account.ListAssets())


if __name__ == "__main__":
  bot.message_loop(BrokerBot)
  while True:
    sleep(1)
