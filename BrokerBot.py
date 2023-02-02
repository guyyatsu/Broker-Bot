import telepot
from time import sleep
import argparse
from CredentialManagement import CredentialManagement
from tools.AccountData import AccountEnumeration


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-K", "--keyfile", help="Designate a file containing an ssh key for encryption.")
  parser.add_argument("-D", "--database", help="Designate a sqlite3 database file.")

  arguments = parser.parse_args()


  """ CREDENTIALS """
  if arguments.keyfile: keyfile = arguments.keyfile
  else: keyfile = "/server/administrator/.credentials/.key"

  if arguments.database: database = arguments.database
  else: database = "/server/administrator/.credentials/credentials.db"

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


  """ End-User Interface """
  def BrokerBot(message, keyfile, database):
    """
    The Broker Bot manages communications between the user and the daemon.
    """
  
    brokerage_account = AccountEnumeration(keyfile, database)
  
    packet_data = message["text"].split(" ")
    command = str(packet_data[0])
  
    # Get all account data.
    if command == "/account": bot.sendMessage(telegramID, brokerage_account.GetAccount())
  
    # Enumerate all current positions. 
    if command == "/positions": bot.sendMessage(telegramID, brokerage_account.GetAllPositions())
  
    # List all assets offered by the broker.
    if command == "/getassets": bot.sendMessage(telegramID, brokerage_account.ListAssets())


  bot.message_loop(BrokerBot, keyfile)
  while True:
    sleep(1)