# Made by Daniel J. Febles Bustillo
blc = "Placeholder"
dpt = 0
dpn = 0
wst = 0
wsn = 0
wft = 0
wfn = 0
pnl = 0
pnn = 0
ext = 0
nam = str(input("Insert name, please: "))
blc = int(float(input("\nWhat will be your starting balance?\n").replace("$",""))* 100) / 100
while ext == 0:
  print("\nAccount Name: " + nam + "\nCurrent Balance: $" + str(blc) + "\n 1) Deposit Funds \n 2) Withdraw Funds \n 3) Log Out\n")
  pck = int(input("Select a number for the desired action: "))
  if pck == 1:
    dps = int(float(input("\nHow much would you like to deposit?\n").replace("$","")) * 100)
    blc = int((blc * 100))
    print("\nProcessing...\n$" + str(blc / 100) + "\n+ $" + str(dps / 100) + "\n$" + str((blc+dps) / 100) + "\nDeposit succeeded.")
    blc = float(str((blc+dps) / 100))
    dpt += dps
    dpn += 1
  elif pck == 2:
    wtd = int(float(input("\nHow much would you like to withdraw?\n").replace("$","")) * 100)
    blc = int((blc * 100))
    if wtd > blc:
      print("\nMalicious withdrawal detected. A penalty of $5 applied to the account. \nProcessing...\n$" + str(blc / 100) + "\n- $5.0\n$" + str(blc / 100 - 5))
      blc = float(str((blc-500) / 100))
      wft += wtd 
      wfn += 1
      pnn += 500
      pnl += 1
    else:
      print("\nProcessing...\n$" + str(blc / 100) + "\n- $" + str(wtd / 100) + "\n$" + str((blc-wtd)/ 100) + "\nWithdrawal succeeded.")
      blc = float(str((blc-wtd) / 100))
      wst += wtd
      wsn += 1
  elif pck == 3:
    print("\n" + nam + " - Actions this session:\n> Final Balance: $" + str(blc) + "\n> Deposits Made: " + str(dpn) + "\n> Funds Deposited: $" + str(dpt / 100) + "\n> Successful Withdrawals Made: " + str(wsn) + "\n> Funds Successfully Withdrawn: $" + str(wst / 100) + "\n> Unsuccessful Withdrawals Made: " + str(wfn) + "\n> Funds Unsuccessfully Withdrawn: $" + str(wft / 100) + "\n> Penalties Made: " + str(pnl) + "\n> Penalties Applied: $" + str(pnn / 100) + "\nGood Day!\nSigning out...")
    ext += 1
  else:
    print("\nInvalid input: must be a number between 1 and 3. Try again")
