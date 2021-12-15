import math
a = int(input("Ievadi preces daudzums: "))
print("Vienas precfes cena ir 2.35Ls")
print(math.floor(a * 2.35))

if a * 2.35 > 4.7:
  print("jums būs atlaide 10%!")
  print(math.floor(a * 2.35 / 10.0))
else:
  if a == 2.35 < 4.7:
    print("Nav atlaides!")
