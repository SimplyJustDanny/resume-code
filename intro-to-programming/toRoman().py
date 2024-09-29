def toRoman(arb):
  arb = int(arb)
  rmn = ""
  while arb > 0:
    if arb // 1000:
      arb -= 1000
      rmn += "M"
    elif arb // 500:
      arb -= 500
      rmn += "D"
      if "DCD" in rmn:
        arb += 1000
        rmn = rmn.replace("D","")
    elif arb // 100:
      arb -= 100
      rmn += "C"
      if "CCCC" in rmn:
        arb += 500
        rmn = rmn.replace("C","",3)
    elif arb // 50:
      arb -= 50
      rmn += "L"
      if "LXL" in rmn:
        arb += 100
        rmn = rmn.replace("L","")
    elif arb // 10:
      arb -= 10
      rmn += "X"
      if "XXXX" in rmn:
        arb += 50
        rmn = rmn.replace("X","",3)
    elif arb // 5:
      arb -= 5
      rmn += "V"
      if "VIV" in rmn:
        arb += 10
        rmn = rmn.replace("V","")
    else:
      arb -= 1
      rmn += "I"
      if "IIII" in rmn:
        arb += 5
        rmn = rmn.replace("I","",3)
  return rmn
