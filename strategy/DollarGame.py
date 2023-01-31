def DollarGame():
  positions = GetAllPositions(cmdline=False)


  for position in positions:
    symbol = FormatSymbolPair(positions[position])


    # Calculate current profit.
    if float(positions[position][3]) - float(positions[position][1]) > 1:
      amount = float(float(positions[position][2]) + 1)

      limit_order_data = LimitOrderRequest(
        symbol=f"{symbol}",
        limit=amount,
        notional=1,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.GTC
      )

      trading_client.submit_order(order_data=limit_order_data)
      message = (f"Creating new limit order for $1 at {amount}.")
      return bot.sendMessage(telegramID, message)