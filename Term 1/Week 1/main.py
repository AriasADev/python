# age = 22
# print(f"My age is {age}") 

try:
  myAge = int(input("How old are you? "))
  if myAge == 69:
    print("Hehe funny number :3")
  elif myAge > 116:
    print("Why are you lying to a random computer program? There's no way you're older than the worlds oldest person! haha")
  elif myAge > 69:
      print("Damn! You're old!")
  else:
    print(f"Hey, that's cool! just wait {69 - myAge} years!")
except ValueError:
  print("Please enter just an integer for your age. (in years) [Value Error]")