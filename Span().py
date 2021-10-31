def Span(y1,m1,d1,y2,m2,d2):
  dt1 = 0
  dt2 = 0
  #DATE 1 YEAR-TO-DAY CALCULATOR
  for i in range(y1):
    if i % 4 == 0:
      if i % 100 == 0:
        if i % 400 == 0:
          dt1 += 366
        else:
          dt1 += 365
      else:
        dt1 += 366
    else:
      dt1+= 365
  #DATE 1 MONTH-TO-DAY CALCULATOR
  for i in range(m1 - 1):
    i += 1
    if i > 7:
      if i % 2 == 0:
        dt1 += 31
      else:
        dt1 += 30
    else:
      if i == 2:
        if y1 % 4 == 0:
          if y1 % 100 == 0:
            if y1 % 400 == 0:
              dt1 += 29
            else:
              dt1 += 28
          else:
            dt1 += 29
        else:
          dt1 += 28
      elif i % 2 == 0:
        dt1 += 30
      else:
        dt1 += 31
  #DATE 1 DAY REMAINDER
  dt1 += d1
  #DATE 1 YEAR-TO-DAY CALCULATOR
  for i in range(y2):
    if i % 4 == 0:
      if i % 100 == 0:
        if i % 400 == 0:
          dt2 += 366
        else:
          dt2 += 365
      else:
        dt2 += 366
    else:
      dt2+= 365
   #DATE 2 MONTH-TO-DAY CALCULATOR
  for i in range(m2 - 1):
    i += 1
    if i > 7:
      if i % 2 == 0:
        dt2 += 31
      else:
        dt2 += 30
    else:
      if i == 2:
        if y2 % 4 == 0:
          if y2 % 100 == 0:
            if y2 % 400 == 0:
              dt2 += 29
            else:
              dt2 += 28
          else:
            dt2 += 29
        else:
          dt2 += 28
      elif i % 2 == 0:
        dt2 += 30
      else:
        dt2 += 31
  #DATE 1 DAY REMAINDER
  dt2 += d2
  #RETURN VALUE
  return abs(dt1 - dt2)
