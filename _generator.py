
# generate extreme cases
import random

total = random.randint(80, 120)
names = ['p{}'.format(i) for i in range(total)]

# generate
lines = []
for i in range(total):
    target = ""
    if random.random() < 0.9:
        j = random.randint(0, total - 2)
        if j >= i: j += 1 
        lines.append((names[i], names[j]))
    else:
        lines.append((names[i],))

# print
print(total)
for l in lines:
    print(" ".join(l))


