import Genetic_Algorithm as ga
import random

def calculate_fitness(data):  #change the value as per as need
    sum_val = 0
    for i,j in enumerate(reversed(data)):
        sum_val += (2**i)*j
    return sum_val

def population_generation(size, nos_pop): 
    return [random.choices([0,1], k=size) for _ in range(nos_pop)]



SIZE = 10    #Size of each population
POP = 12    #Population in each batch
NOS_TOP = 4 #Number of top selected population per population
ITERATION = 50 #Number of Iteration 

genetic_algo = ga.GeneticAlgorithm(SIZE, POP, NOS_TOP, population_generation, calculate_fitness)
genetic_algo.train(ITERATION)
genetic_algo.display()
print(genetic_algo.population)