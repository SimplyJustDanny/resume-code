#Daniel J. Febles Bustillo - Project #2
def Project2():
  
  cmd_bed = 'b'
  cmd_close = 'c'
  cmd_die = 'd'
  cmd_east = 'e'
  cmd_feed = 'f'
  cmd_get = 'g'
  cmd_inv = 'i'
  cmd_lock = 'l'
  cmd_map = 'm'
  cmd_north = 'n'
  cmd_open = 'o'
  cmd_put = 'p'
  cmd_quit = 'q'
  cmd_south = 's'
  cmd_tv = 't'
  cmd_unlock = 'u'
  cmd_west = 'w'

  room_names = ("Front Porch", "Living Room", "The Kitchen", "Office Desk", "The Bedroom")
  room_front = 0
  room_living = 1
  room_kitchen = 2
  room_office = 3
  room_bed = 4

  flag_me_awake = True
  flag_tv_on = False
  flag_first_kitchen = True
  flag_first_office = True
  flag_first_bedroom = True
  flag_safe_open = False
  flag_pantry_open = False
  flag_pantry_locked = True
  flag_inv_key = False
  flag_inv_bone = False
  flag_inv_spam = False
  flag_stella_fed = False
  flag_spam_put = False
  flag_deltarune = False

  room = 0
  turn = 0

  print("Well, today was horrendous as usual! Your body is literally dysfunctional, and the only way to repair it is to pass out and collapse on the matress. Fortunately, that is much easier said than done…\n")
  print("Welcome to... Febles's Fair of Fortuitous Folly.")

  while flag_me_awake:
    print("\nCurrent Location:", room_names[room])
    cmd = input("> ")
    turn += 1

    if cmd == cmd_quit:
      print("\nFine, leave then. Didn't even want you to play my stupid game.")
      return False

    if cmd == cmd_map:
      print("\n            +-----------+")
      print(("            |The Bedroom|             \n+-----------+-----------+-----------+\n|Front Porch|Living Room|Office Desk|\n+-----------+-----------+-----------+\n            |The Kitchen|").replace(room_names[room],"You're Here"))
      print("            +-----------+")
      continue

    if cmd == cmd_inv:
      print("\nCurrent inventory:")
      if flag_inv_key:
        print(" - Pantry Key")
      if flag_inv_bone:
        print(" - Elder Bone")
      if flag_inv_spam:
        print(" - Lovely Spam")
      if not (flag_inv_key or flag_inv_bone or flag_inv_spam):
        print(" - Nothing")
      continue

    if cmd == cmd_die:
      print('\nBy virtue of your own sheer will to live, or lack thereof, you have propmptly collapsed on the floor and died. Excellent.')
      return False



    if room == room_front:
      if cmd == cmd_east:
        print("\nYou have entered your pathetic abode. They charge you money to live here! The audacity of those absurd landlords... At least there's someplace to lie down on.")
        print("\nThe TV is off and Stella is in the way to your bedroom.")
        room = room_living
        continue
	


    if room == room_living:
      if cmd == cmd_tv:
        if flag_tv_on:
          print("\nYou turn off the TV. You then realize that you're forced to come with the consequences of your own actions for having put off your responsibilities for far too long. You're too tired to care. Moving on!")
          flag_tv_on = False
        else:
          print("\nYou turn on the TV. To your befuddling amusement, the screen showcases a group of teenagers being slaughtered by Michael Myers. How adorable, yet more precious to you is some much needed zeds.")
          flag_tv_on = True
        continue

      if cmd == cmd_feed:
        if flag_stella_fed:
          print('\nThe wishes of the Great Old One have already been sated. She is no longer in need of sustenance. For now...')
        else:
          if flag_inv_bone:
            if flag_tv_on:
              print("\nThe frantic screams of the actors is enough to soothe Stella, and at last she is able to enjoy her bone in peace.")
              flag_stella_fed = True
              flag_inv_bone = False
            else:
              print("\nUnfortunately, it seems like Stella is unable to eat much without her much beloved sound of human torment. Perhaps something could replicate it?")
          else:
            print("\nYou wish to feed your humble monster, but there's nothing you can give her right now.")
        continue

      if cmd == cmd_west:
        print("\nAs enthusiastic as you are to kill yourself in the monotonous grind of life again, you physically cannot bring yourself to leave your little safe haven. Maybe another day...")
        continue
      
      if cmd == cmd_south:
        if flag_first_kitchen:
          print("\nAllured by the fragrance of the undead living, you enter the kitech, thinking about catching a midnight snack from your well of souls. Alas, you remember that it is Lent friday, and that you need to fast in order to not displease the invisible crowd of God by commiting less crimes against humanity. Still, there must be something here of use to you, no?")
          flag_first_kitchen = False
        else:
          print("\nYou moved to the kitchen.")
        if flag_pantry_open:
          if not (flag_inv_bone or flag_stella_fed):
            print("\nYour pantry is on the counter, displaying an elder bone.")
          elif flag_spam_put:
            print("\nYour pantry is on the counter, displaying lovely spam.")
          else:
            print("\nYour pantry is on the counter, open and hideous.")
        else:
          print("\nYour pantry is on the counter, closed.")
        room = room_kitchen
        continue

      if cmd == cmd_east:
        if flag_first_office:
          print("\nAh yes, your war room. Here, you commit common milquetoast activities, such as coding infrastructure that will never be used, pretending to write stories until giving up 3 sentences in, and, of course, tax evasion. Perhaps there's something of notice here that you can use to your advantage...")
          flag_first_office = False
        else:
          print("\nYou moved to the office.")
        if flag_safe_open:
          if flag_inv_key:
            print("\nYou notice that there's a safe here, left open and unrestrained")
          else:
            print("\nYou notice that there's a safe here, left open and unrestrained, with a dastardly key lying inside")
        else:
          print("\nYou notice that there's a safe here.")
        room = room_office
        continue

      if cmd == cmd_north:
        if flag_stella_fed:
          if flag_first_bedroom:
            print("\nFinally, your comfortable abode! How long you have wished to get to this place. However, before you go to bed, you need to make sure that everything is tucked away and tidy.")
            flag_first_bedroom = False
          else:
            print("\nYou moved to the bedroom.")
          if not (flag_inv_spam or flag_spam_put):
            print('\nLovely spam on the counter.')
          else:
            print('\nThe bed lies before you.')
          room = room_bed
        else:
          print('\nYour pet Great Old One, Stella, is blocking the way. It seems that she wants a treat.')
        continue



    if room == room_office:
      if cmd == cmd_open:
        if flag_safe_open:
          print("\nIt's already been opened, you aloofus doofus!")
          continue
        else:
          print("\nAs you approach the safe, you put your hands steady on the dial. Of course, your password is only the most heinous and despicable black magic of all, the Collatz conjecture. Your starting offset, of course, is 42. The code should be calculating the nex 3 steps after that")
          x = int(input("\nThe First Seal: "))
          y = int(input("The Second Seal: "))
          z = int(input("The Final Seal: "))
          if (x == 21) and (y == 64) and (z == 32):
            if flag_inv_key:
              print("\nWith all your might, you successfully unlock the dreaded safe. Your prize within, a key to the pantry, lies in the wake of its belly.")
              flag_safe_open = True
              continue
            else:
              print("\nWith all your might, you successfully unlock the dreaded safe.")
              flag_safe_open = True
              continue
          else:
            print("\nTry as you might with your display of power, even the great Collatz have bested you. You can hear his cackle in the distance, mocking you with his infinite 4-2-1 loop")
            continue
          
      if cmd == cmd_get:
        if flag_safe_open:
          if flag_inv_key:
            print("\nThere is nothing here to obtain. Look elsewere, eldritch being.")
            continue
          else:
            print("\nPulling out your right, acid-damaged hand, you grab the ethereal key of the pantry.")
            flag_inv_key = True
            continue
        else:
          print("\nPerhaps you should open the safe first before trying to pick up what's inside. Remember, your Glove of Phasing is broken.")
          continue
          
      if cmd == cmd_put:
        if flag_inv_key:
          if flag_safe_open:
            print("\nFinding no use for it as of now, you stow away the ancient treasure within the cold confines of the metallic pocket.")
            flag_inv_key = False
            continue
          else:
            print("\nThe key can't be put away now. You need to unseal the seal's seal that you sealed, lying behind the teal veil of the unreal reel you feel.")
            continue
        else:
          print("\nThe key is not in your hands. It lies still within the endless walls of the cage before you.")
          continue
        
      if cmd == cmd_close:
        if flag_safe_open:
          print("\nOnce more, the coffin of horrendous atrocities is sealed, with the 3 ancient numbers of the beast of Collatz.")
          flag_safe_open = False
          continue
        else:
          print("\nFortunaltely, the jaws of Pandora's box lie locked and hinged, unable to do all but obey to your command.")
          continue
        
      if cmd == cmd_west:
        print("\nYou moved to the living room.")
        if flag_stella_fed:
          if flag_tv_on:
            print('\nThe TV is on and Stella is eating her elder bone.')
          else:
            print('\nThe TV is off and Stella is eating her elder bone.')
        else:
          if flag_tv_on:
            print('\nThe TV is on and Stella is in the way to your bedroom.')
          else:
            print('\nThe TV is off and Stella is in the way to your bedroom.')
        room = room_living
        continue



    if room == room_kitchen:
      if cmd == cmd_unlock:
        if flag_pantry_locked:
          if flag_inv_key:
            print("\nSliding in the ancient key, you turn the knob. You can hear something click from within the pantry. Also, the screaming, but that's standard.")
            flag_pantry_locked = False
          else:
            print("\nYou try to unlock the patry with all your tools, but it's not working. Perhaps a key is needed.")
        else:
          print("\nThe pantry's already been unlocked. Make of that what you will.")
        continue

      if cmd == cmd_open:
        if flag_pantry_locked:
          print("\nLifting as hard as you can, the pantry won't budge. It is sealed shut, awaiting a sinister key...")
        else:
          if not (flag_inv_bone or flag_stella_fed):
            print("\nYou unhinge the jaws of the pantry in order to behold a ghastly sight: a lone, eldritch, elder bone lies before you.")
          else:
            print("\nYou unhinge the jaws of the pantry in order to behold a ghastly sight: nothing. Looks like you need to stock up on food stamps again.")
          flag_pantry_open = True
        continue

      if cmd == cmd_get:
        if flag_pantry_open:
          if not (flag_inv_bone or flag_stella_fed):
            print("\nYou decide to grab the abominable bone with your left, skeleton hand and put it in your pocket. Just in case.")
            flag_inv_bone = True
          elif flag_spam_put:
            print("\nYou try to grab the spam from the pantry, but the pantry bites you in the process. It would be unwise to do that again.")
          else:
            print("\nYou try to grab something from the pantry, but there's nothing there at all. Maybe you should start making that shopping grimoire.")
        else:
          print("\nYou try to grab something from the pantry, but the pantry needs to be open first.")
        continue

      if cmd == cmd_put:
        if flag_pantry_open:
          if flag_inv_bone:
            print("\nFor some asinine reason, you've decided to put the bone back in the pantry, which I'm pretty sure bit you.")
            flag_inv_bone = False
          elif flag_inv_spam:
            print("\nThe spam has been put in its rightful throne. The pantry is pleased.")
            flag_inv_spam = False
            flag_spam_put = True
          else:
            print("\nYou have nothing to please the pantry at the moment.")
        else:
          print("\nYou try to put something into the pantry, but the pantry needs to be open first.")
        continue
          
      if cmd == cmd_close:
        if flag_pantry_open:
          print("\nYou shut the pantry once more, fighting against its jerky, wrathful movements.")
          flag_pantry_open = False
        else:
          print("\nThe pantry is closed...")
        continue

      if cmd == cmd_lock:
        if flag_pantry_open:
          print("\nThe pantry cannot be locked, as it is still open.")
        else:
          if flag_pantry_locked:
            print("\nThe pantry is sealed tight and shut.")
          else:
            print("\nFearful of what might come out of it, you lock the pantry once more, containing the evil within...")
            flag_pantry_locked = True
        continue

      if cmd == cmd_north:
        print("\nYou moved to the living room.")
        if flag_stella_fed:
          if flag_tv_on:
            print('\nThe TV is on and Stella is eating her elder bone.')
          else:
            print('\nThe TV is off and Stella is eating her elder bone.')
        else:
          if flag_tv_on:
            print('\nThe TV is on and Stella is in the way to your bedroom.')
          else:
            print('\nThe TV is off and Stella is in the way to your bedroom.')
        room = room_living
        continue

    if room == room_bed:
      if cmd == cmd_bed:
        if flag_tv_on:
          print('\nThe noise of the TV is keeping you awake.')
        elif flag_pantry_open:
          print('\nThe screams of agony coming from the pantry are keeping you awake.')
        elif not flag_pantry_locked:
          print("\nThe aura of unlocked evils coming from the pantry are keeping you awake.")
        elif flag_inv_key:
          print('\nThe horrendous hissing coming from the pantry key in your pocket is keeping you awake.')
        elif flag_safe_open:
          print('\nThe horrendous hissing coming from the pantry key in the safe is keeping you awake.')
        elif not (flag_inv_spam or flag_spam_put):
          print('\nKris, get the spam.')
          flag_deltarune = True
        elif not flag_spam_put:
          print('\nThe heavenly sounds of lovely spam are keeping you awake. Put it back in the pantry.')
        else:
          print('\nFinally. Peace.')
          break
        continue

      if cmd == cmd_get:
        if not (flag_inv_spam or flag_spam_put):
          if flag_deltarune:
            print('\nPotassium.')
            flag_deltarune = False
          else:
            print('\nPulling out your third, spam-loving hand, you grab the lovely spam.')
          flag_inv_spam = True
        else:
          print("\nThere's nothing here.")
        continue

      if cmd == cmd_south:
        print("\nYou moved to the living room.")
        if flag_tv_on:
          print('\nThe TV is on and Stella is eating her elder bone.')
        else:
          print('\nThe TV is off and Stella is eating her elder bone.')
        room = room_living
        continue



    if cmd == cmd_north or cmd_east or cmd_south or cmd_west:
      print("\nIt seems that you have no sense of direction. Try pulling out a map next time before you start going places.")
      continue

    print("\nInvalid command. Try again.")

  print("You win!")
  print(turn, "turns wasted.")
  return True
