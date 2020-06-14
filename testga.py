import Genetic_Algorithm as ga
import random

# def calculate_fitness(data):  #change the value as per as need
#     sum_val = 0
#     for i,j in enumerate(reversed(data)):
#         sum_val += ((-2)**i)*j
#     return sum_val

# def population_generation(size, nos_pop): 
#     return [random.choices([0,1], k=size) for _ in range(nos_pop)]

def calculate_fitness(data):  #change the value as per as need
    sum_val = 0
    for i,j in enumerate(reversed(data)):
        sum_val += j
    return sum_val

def population_generation(size, nos_pop): 
    return [random.choices([x for x in range(10)], k=size) for _ in range(nos_pop)]

SIZE = 10    #Size of each population
POP = 120    #Population in each batch
NOS_TOP = 20 #Number of top selected population per population
ITERATION = 100 #Number of Iteration 

genetic_algo = ga.GeneticAlgorithm(SIZE, POP, NOS_TOP, 9, population_generation, calculate_fitness)
genetic_algo.train(ITERATION)
genetic_algo.display()
print(genetic_algo.population[0:NOS_TOP])
print(genetic_algo.population_cal.calculate_set_fitness(genetic_algo.population))