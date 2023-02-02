from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass

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
      positional_data[position.symbol]["asset id"] = position.asset_id
      positional_data[position.symbol]["symbol"] = position.symbol
      positional_data[position.symbol]["exchange"] = position.exchange
      positional_data[position.symbol]["asset class"] = position.asset_class
      positional_data[position.symbol]["average entry price"] = position.avg_entry_price
      positional_data[position.symbol]["quantity"] = position.qty
      positional_data[position.symbol]["quantity available"] = position.qty_available
      positional_data[position.symbol]["side"] = position.side
      positional_data[position.symbol]["market value"] = position.market_value
      positional_data[position.symbol]["cost basis"] = position.cost_basis
      positional_data[position.symbol]["unrealized profit/loss"] = position.unrealized_pl
      positional_data[position.symbol]["unrealized profit/loss percent"] = position.unrealized_plpc
      positional_data[position.symbol]["unrealized intraday profit/loss"] = position.unrealized_intraday_pl
      positional_data[position.symbol]["unrealized intraday profit/loss percent"] = position.unrealized_intraday_plpc
      positional_data[position.symbol]["current price"] = position.current_price
      positional_data[position.symbol]["last day price"] = position.lastday_price
      positional_data[position.symbol]["change today"] = position.change_today
  
     
    # For interactive usage.
    if cmdline is True:
      message = "Your positions:"
      for position in positional_data:
        message += f"\n\nSymbol: {position['symbol']}"
        message += f"\nClass: {position['asset class']}"
        message += f"\nCurrent Price: {position['current price']}"
        message += f"\nSide: {position['side']}"
        message += f"\nQuantity: {position['quantity']}"
        message += f"\nValue: {position['market value']}"
        message += f"\nBuy-In: {position['cost basis']}"
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
    for asset in self.client.get_all_assets(
      GetAssetsRequest(
        asset_class=AssetClass.CRYPTO
      )
    ): message += f"\n    {asset.symbol}"
  
    return message
