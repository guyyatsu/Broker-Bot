import telepot
from time import sleep
import logging
import argparse
from Lab93_Cryptogram import CredentialManagement
from AlpacaAccountData.AccountData import AccountEnumeration


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-K", "--keyfile", help="Designate a file containing an ssh key for encryption.", required=True)
  parser.add_argument("-C", "--credential", help="Designate a credential database.", required=True)
  parser.add_argument("-l", "--log-level", action="count")

  arguments = parser.parse_args()

  if arguments.log_level == 0: loglevel = logging.INFO
  elif arguments.log_level > 0: loglevel = logging.DEBUG

  logfile = "/server/administrator/logs/Broker-Bot.log"
  with open(logfile, 'w') as clearing_log: clearing_log.write("")
  logging.basicConfig(filename=logfile, level=loglevel)


  # Gather the administrators telegram user id so the bot only responds to him.
  telegramID =  CredentialManagement.SingleKeyAPICredentials(
    platform="telegram_admin",
    credabase=arguments.credential,
    keyfile=arguments.keyfile
  )
 
  # Initialize the Telegram bot with the platforms API key.
  logging.debug(f"Creating Telegram bot.")
  bot = telepot.Bot(
    CredentialManagement.SingleKeyAPICredentials(
      platform="telegram",
      credabase=arguments.credential,
      keyfile=arguments.keyfile
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
