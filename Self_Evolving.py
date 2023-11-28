import os, random, time

random.seed(float(time.time()))


def clear_file(file_name):
    with open(file_name, 'w') as f:
        f.truncate(0)


# Read the populations stored in POPULATIONS.TXT
def read_weights():
    pop = []
    with open("Population.txt", 'r') as f:
        data_lines = f.readlines()
        # print(data_lines)
        count = 0
        weights = []
        for data in data_lines:
            weights.append(float(data.strip('\n')))
            count += 1
            if count > 5:
                pop.append(weights.copy())
                count = 0
                weights.clear()
    return pop

# Output the generated populations to the POPULATIONS.TXT
def output_weights(POPULATIONS):
    with open("Population.txt", 'w') as f:
        for weights in POPULATIONS:
            for i in weights:
                f.write(str(i) + '\n')


# Set the weights for the autoplayer
def set_weights(weights):
    with open("Weight.txt", 'w') as f:
        for i in weights:
            f.write(str(i) + '\n')


# Read the results from SCORES.TXT
def read_results():
    RESULTS = []
    with open("Score.txt", 'r') as f:
        data_lines = f.readlines()
        count = 0
        current_result = []
        for data in data_lines:
            current_result.append(float(data.strip('\n')))
            count += 1
            if count > 6:
                RESULTS.append(current_result.copy())
                count = 0
                current_result.clear()
    return RESULTS



# According to the new the population, generate next geretion

def random_number():
    if random.randint(1, 2) == 1:
        return -random.random()
    else:
        return random.random()

results = []
mid_generation = []
new_weights = []
while True:
    clear_file("Score.txt")
    populations = read_weights()
    for weights in populations:
        set_weights(weights)
        os.system("python visual-pygame.py")
    results.clear()
    results = read_results()
    results.sort(key = lambda x: float(-x[6]))
    for i in results:
        print(i)
    with open("Weights_over_17000.txt", 'a') as records_file:
        for weight in results:
            if weight[6] > 17000:
                for i in weight:
                    records_file.write(str(i) + ' ')
                records_file.write('\n')
    mid_generation.clear()
    new_weights.clear()
    weights_width = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    for i in range(10 - 1):
        current_generation = []
        for j in range(1, 9 - i + 1):
            for k in range(6):
                current_generation.append((results[i][k] + results[i + j][k]) / 2)
                if (abs(results[i][k] - results[i + j][k]) > weights_width[k]):
                    weights_width[k] = abs(results[i][k] - results[i + j][k])
            mid_generation.append(current_generation.copy())
            current_generation.clear()
    for weights in mid_generation:
        current_generation = []
        for i in range(6):
            current_generation.append(weights[i] + random_number() * weights_width[i])
        new_weights.append(current_generation.copy())
        current_generation.clear()
    with open("Population.txt", 'w') as populations_file:
        for weights in new_weights:
            for i in weights:
                populations_file.write(str(i) + '\n')