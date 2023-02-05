import telepot
from time import sleep
import logging
import argparse
from Lab93_Cryptogram import CredentialManagement
from Lab93_TradeClient.AccountData import AccountEnumeration


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-K", "--keyfile", help="Designate a file containing an ssh key for encryption.", required=True)
  parser.add_argument("-C", "--credential", help="Designate a credential database.", required=True)
  parser.add_argument("-l", "--log-level", action="count")
  parser.add_argument("-L", "--log-file", help="Designate a file for logging.")

  arguments = parser.parse_args()


  # Set log-level to INFO by default; otherwise DEBUG.
  if arguments.log_level == 0: loglevel = logging.INFO
  elif arguments.log_level > 0: loglevel = logging.DEBUG

  # Set logfile within directory unless specified.
  if arguments.log_file: logfile = arguments.log_file
  else: logfile = "./.log"

  # Rotate the log every time it's called.
  with open(logfile, 'w') as clearing_log: clearing_log.write("")
  logging.basicConfig(filename=logfile, level=loglevel)


  # Gather the administrators telegram user id so the bot only responds to him.
  telegramID =  CredentialManagement.SingleKeyAPICredentials(
    platform="telegram_admin",
    credabase=arguments.credential,
    keyfile=arguments.keyfile
  )

  # Gather Alpaca API credentials.
  alpacaAPI = CredentialManagement.MultiKeyAPICredentials(
    platform="alpaca",
    credabase=arguments.credential,
    keyfile=arguments.keyfile
  )
 
  # Initialize the Telegram bot with the platforms API key.
  bot = telepot.Bot(
    CredentialManagement.SingleKeyAPICredentials(
      platform="telegram",
      credabase=arguments.credential,
      keyfile=arguments.keyfile
    )
  )


  """ End-User Interface """
  def BrokerBot(message):
    """
    The Broker Bot manages communications between the user and the daemon.
    """
  
    brokerage_account = AccountEnumeration(key=alpacaAPI["key"], secret=alpacaAPI["secret"])
  
    packet_data = message["text"].split(" ")
    command = str(packet_data[0])
  
    # Get all account data.
    if command == "/account": bot.sendMessage(telegramID, brokerage_account.GetAccount())
  
    # Enumerate all current positions. 
    if command == "/positions": bot.sendMessage(telegramID, brokerage_account.GetAllPositions())
  
    # List all assets offered by the broker.
    if command == "/assets": bot.sendMessage(telegramID, brokerage_account.ListAssets())


  bot.message_loop(BrokerBot)
  while True:
    sleep(1)
