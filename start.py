import random

def clear_file(file_name):
    with open(file_name, 'w') as f:
        f.truncate(0)

clear_file("Population.txt")
weights = [
    -15,
    12,
    -8.1,
    -8.1,
    -10.7,
    -8.0
]
def random_number():
    if random.randint(1,2) == 1:
        return -random.random()
    else:
        return random.random()

with open("Population.txt", 'a') as f:
    for i in range(45):
        for j in range(6):
            w = weights[j] + 25 * random_number()
            f.write(str(w) + '\n')

