from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

from CredentialManagement import CredentialManagement


class AccountEnumeration:
  def __init__(self, keyfile, database, paperage=False):

    # Unlock the Alpaca.Markets API key and secret.
    credentials = CredentialManagement.MultiKeyAPICredentials(
      platform="alpaca", credabase=database, keyfile=keyfile
    )

    # Pull the credentials from the dictionary.
    key = credentials['key']; secret = credentials['secret']


    # Initialize the trade client with key and secret.
    self.client = TradingClient(key, secret, paper=paperage)


  def GetAccount(self, cmdline=True):
  
    account = self.client.get_account()
  
    account_data = {
      "account blocked": account.account_blocked,
      "account number": account.account_number,
      "accrued fees": account.accrued_fees,
      "buying power": account.buying_power,
      "cash": account.cash,
      "created at": account.created_at,
      "crypto status": account.crypto_status,
      "currency": account.currency,
      "daytrade count": account.daytrade_count,
      "daytrading buying power": account.daytrading_buying_power,
      "equity": account.equity,
      "id": account.id,
      "initial margin": account.initial_margin,
      "last equity": account.last_equity,
      "last maintenance margin": account.last_maintenance_margin,
      "long market value": account.long_market_value,
      "maintenance margin": account.maintenance_margin,
      "multiplier": account.multiplier,
      "non-marginable buying power": account.non_marginable_buying_power,
      "pattern day trader": account.pattern_day_trader,
      "pending transfer in": account.pending_transfer_in,
      "pending transfer out": account.pending_transfer_out,
      "portfolio value": account.portfolio_value,
      "regt buying power": account.regt_buying_power,
      "short market value": account.short_market_value,
      "shorting enabled": account.shorting_enabled,
      "sma": account.sma,
      "status": account.status,
      "trade suspended by user": account.trade_suspended_by_user,
      "trading blocked": account.trading_blocked,
      "transfers blocked": account.transfers_blocked
    }
  
    if cmdline is True: return ( f"Account Details:"
                                 f"\n\n  Account Number: {account_data['account number']}"
                                 f"\n  Account Fees: {account_data['accrued fees']}"
                                 f"\n  Currency: {account_data['currency']}"
                                 f"\n  Buying Power: ${account_data['buying power']}"
                                 f"\n  Cash: ${account_data['cash']}"
                                 f"\n  Equity: ${account_data['equity']}"
                                 f"\n  Portfolio Value: ${account_data['portfolio value']}" )
    else: return account_data
  
  
  # Gather positional data.
  def GetAllPositions(self, cmdline=True):
    """
    Collect a readout of all of our currently held positions.
    Can either be used in an interactive setting or a programmatic setting.
  
    For interactivity, a string 'message' is constructed enumerating the most
    relevant-at-a-glance endpoints in a human readable format to be distributed
    by a telegram bot.
  
    For programmatic usage, the entire result is returned to the caller.
    """
  
  
    # Make the API call requesting positions.
    positions = self.client.get_all_positions()
  
    # Establish data structure for collections.
    positional_data = {}
  
    # Populate the structure.
    for position in positions:
      positional_data[position.symbol] = {
        "symbol": position.symbol,
        "exchange": position.exchange,
        "asset class": position.asset_class,
        "average entry price": position.avg_entry_price,
        "quantity": position.qty,
        "side": position.side,
        "market value": position.market_value,
        "cost basis": position.cost_basis,
        "unrealized profit/loss": position.unrealized_pl,
        "unrealized profit/loss percent": position.unrealized_plpc,
        "unrealized intraday profit/loss": position.unrealized_intraday_pl,
        "unrealized intraday profit/loss percent": position.unrealized_intraday_plpc,
        "current price": position.current_price,
        "last day price": position.lastday_price,
        "change today": position.change_today
      }

  
     
    # For interactive usage.
    if cmdline is True:
      message = "Your positions:"
      for position in positional_data:
        message += f"\n\nSymbol: {positional_data[position]['symbol']}"
        message += f"\nClass: {positional_data[position]['asset class']}"
        message += f"\nCurrent Price: {positional_data[position]['current price']}"
        message += f"\nSide: {positional_data[position]['side']}"
        message += f"\nQuantity: {positional_data[position]['quantity']}"
        message += f"\nValue: {positional_data[position]['market value']}"
        message += f"\nBuy-In: {positional_data[position]['cost basis']}"
      return message
  
    # For programmatic usage.
    else: return positional_data
  
  
  def ListAssets(self):
    """
    Curate a list of offerings available on the Alpaca market.
  
    Currently, we only display the cryptocurrency assets, as there are over
    31,000 us_equity assets maintained by Alpaca.
  
    To display equity assets, the 31,000 should be broken up alphabetically
    and given by the broker bot individually, piece by piece.
    """
  
    message = ("Cryptocurrency Assets:")
  
    # Query the market for asset lists.
    search_params = GetAssetsRequest(asset_class=AssetClass.CRYPTO)
    assets = self.client.get_all_assets(search_params)
    print(assets)
      
  
    return message
