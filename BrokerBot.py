import telepot
from time import sleep
import logging
import argparse
from CredentialManagement import CredentialManagement
from AlpacaAccountData.AccountData import AccountEnumeration


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-K", "--keyfile", help="Designate a file containing an ssh key for encryption.")
  parser.add_argument("-D", "--database", help="Designate a sqlite3 database file.")

  arguments = parser.parse_args()

  logfile = "/server/administrator/logs/Broker-Bot.log"
  with open(logfile, 'w') as clearing_log: clearing_log.write("")
  logging.basicConfig(filename=logfile, level=logging.DEBUG)


  """ CREDENTIALS """
  if arguments.keyfile: keyfile = arguments.keyfile
  else: keyfile = "/server/administrator/.credentials/.key"
  logging.info(f"Keyfile: {keyfile}")

  if arguments.database: database = arguments.database
  else: database = "/server/administrator/.credentials/credentials.db"
  logging.info(f"Database: {database}")

  # Gather the administrators telegram user id so the bot only responds to him.
  telegramID =  CredentialManagement.SingleKeyAPICredentials(
    platform="telegram_admin",
    credabase=database,
    keyfile=keyfile
  )
 
  # Initialize the Telegram bot with the platforms API key.
  logging.debug(f"Creating Telegram bot.")
  bot = telepot.Bot(
    CredentialManagement.SingleKeyAPICredentials(
      platform="telegram",
      credabase=database,
      keyfile=keyfile
    )
  )
  logging.debug(f"Bot\n{bot}\nCreated.")


  """ End-User Interface """
  def BrokerBot(message):
    """
    The Broker Bot manages communications between the user and the daemon.
    """
  
    logging.debug("Contacting Alpaca brokerage.")
    brokerage_account = AccountEnumeration(keyfile, database)
    logging.debug(f"Got details for brokerage.")
  
    logging.debug("Recieving incoming transmission:")
    packet_data = message["text"].split(" ")
    command = str(packet_data[0])
    logging.debug(f"Recieved command: {command}")
  
    # Get all account data.
    if command == "/account": bot.sendMessage(telegramID, brokerage_account.GetAccount())
  
    # Enumerate all current positions. 
    if command == "/positions": bot.sendMessage(telegramID, brokerage_account.GetAllPositions())
  
    # List all assets offered by the broker.
    if command == "/assets": bot.sendMessage(telegramID, brokerage_account.ListAssets())


  bot.message_loop(BrokerBot)
  while True:
    sleep(1)
