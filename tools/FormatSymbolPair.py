def FormatSymbolPair(position):
  if position[-1] == AssetClass.CRYPTO:

    anchor = position[5][-3:]

    if anchor == "USD" or "BTC": symbol = f"{position[5][:-3]}/{position[5][-3:]}"
    elif anchor == "SDT": symbol = f"{position[5][:-4]}/{position[5][-4:]}"
    
    return symbol