
# generate extreme cases
import random
print("120 40")

names = ['p{}'.format(i) for i in range(120)]
for i in range(120):
    gender = 'F' if i % 3 == 0 else 'M'
    target = ""
    if random.random() < 0.9:
        target = names[random.randint(0, 119)]
    print ('{} {} {}'.format(names[i], gender, target))

for _ in range(40):
    i, j = random.randint(0, 119), random.randint(0, 119)
    print('{} {}'.format(names[i], names[j]))
