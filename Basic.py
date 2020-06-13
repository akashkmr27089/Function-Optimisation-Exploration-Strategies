import matplotlib.pyplot as plt
import numpy as np
import random

#user defined functions start
def calculate_fitness(data):  #change the value as per as need
    sum_val = 0
    for i,j in enumerate(reversed(data)):
        sum_val += (2**i)*j
    return sum_val

def population_generation(size, nos_pop): 
    return [random.choices([0,1], k=size) for _ in range(nos_pop)]

#user defined function over

class Population:
    def __init__(self):
        print("Population Class Initialised")
        global calculate_fitness
        self.calculate_fitness = calculate_fitness
    
    def calculate_set_fitness(self, data):
        return [calculate_fitness(x) for x in data]

class Crossover:
    def __init__(self, size, pop_size):
        print("Crossover Class Initialised")
        self.size = size
        self.pop_size = pop_size
    
    def crossover_single(self,a,b,key):
        new_a = a[:key] + b[key:]
        new_b = b[:key] + a[key:]
        return new_a,new_b

    def crossover_double(self,a,b,key1, key2, inner = True):
        if inner == True:
            new_a = a[:key1] + b[key1:key2] + a[key2:]
            new_b = b[:key1] + a[key1:key2] + b[key2:]
        else:
            new_a = b[:key1] + a[key1:key2] + b[key2:]
            new_b = a[:key1] + b[key1:key2] + a[key2:]
        return new_a, new_b

    def crossover_set(self, population, single=True):
        final_population = []
        if(single): ## single crossver selected 
            selection_index = random.choices([x for x in range(self.size)], k = self.pop_size//2)
            for i in range(0,self.pop_size, 2):
                final_population += list(self.crossover_single(population[i],population[i+1],
                                    selection_index[i//2]))
        else:
            pass 
            #Write fuction for double crossover
        return final_population
            

class Selection:
    def __init__(self):
        print("Selection")
    
    def selection(self, type='default'):
        if(type == 'default'):
            pass
            



def main():
    size = 5
    pop = 12
    population_cal = Population()
    crossover = Crossover(size, pop)
    population = population_generation(size, pop)
    sorted_pop = sorted(population, key=calculate_fitness)  #sort according to fitness
    print(population_cal.calculate_set_fitness(sorted_pop))

if __name__ == "__main__":
    main()

