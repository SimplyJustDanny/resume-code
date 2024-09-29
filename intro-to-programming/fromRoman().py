def fromRoman(rmn):
  arb = 0
  while rmn:
    if "M" in rmn:
      if "CM" in rmn:
        rmn = rmn.replace("C","",1)
        arb -= 100
      rmn = rmn.replace("M","",1)
      arb += 1000
    if "D" in rmn:
      if "CD" in rmn:
        rmn = rmn.replace("C","",1)
        arb -= 100
      rmn = rmn.replace("D","",1)
      arb += 500
    if "C" in rmn:
      if "XC" in rmn:
        rmn = rmn.replace("X","",1)
        arb -= 10
      rmn = rmn.replace("C","",1)
      arb += 100
    if "L" in rmn:
      if "XL" in rmn:
        rmn = rmn.replace("X","",1)
        arb -= 10
      rmn = rmn.replace("L","",1)
      arb += 50
    if "X" in rmn:
      if "IX" in rmn:
        rmn = rmn.replace("I","",1)
        arb -= 1
      rmn = rmn.replace("X","",1)
      arb += 10
    if "V" in rmn:
      if "IV" in rmn:
        rmn = rmn.replace("I","",1)
        arb -= 1
      rmn = rmn.replace("V","",1)
      arb += 5
    if "I" in rmn:
      rmn = rmn.replace("I","",1)
      arb += 1
    if "\n" in rmn:
      rmn = rmn.replace("\n","")
  return str(arb)
