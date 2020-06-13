import matplotlib.pyplot as plt
import numpy as np
import random

class Population:
    def __init__(self, calculate_fitness):
        print("Population Class Initialised")
        self.calculate_fitness = calculate_fitness
    
    def calculate_set_fitness(self, data):
        return [self.calculate_fitness(x) for x in data]

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
    def __init__(self, nos_selection):
        print("Selection Initialised")
        self.replace = nos_selection
    
    def selection(self, population, type='default'): 
        #function responsible for rearrangements 
        if(type == 'default'):
            new_poplation = population[:-self.replace] + population[:self.replace]
        return new_poplation

#mutation is used so that if every member of population is same then itdoesnt stop improving
class Mutation:
    def __init__(self):
        print("Mutaion Initialised")
    
    def single_bit_mutation(self, data):
        pos = random.randint(0, len(data)-1)
        if(data[pos] == 1): data[pos] = 0
        else: data[pos] = 1
        return data

    def set_mutation(self, data, single=True):
        final = []
        if(single):
            final = [self.single_bit_mutation(x) for x in data]
        else:
            pass
        return final

class MultiPlot:
    def __init__(self, number_of_population):
        self.pop_nos = number_of_population
        self.pop_fitness = [[] for _ in range(self.pop_nos)]
        print("Plotting Initialised")

    def append_data(self, data):
        for i,j in enumerate(data):
            self.pop_fitness[i].append(j)

    def multi_plot(self):

        for i in range(self.pop_nos):
            plt.plot(self.pop_fitness[i])
        plt.legend()
        plt.show()

class GeneticAlgorithm:
    def __init__(self, size_of_each_population, population_batch_size,
        number_top_population, iteration, population_generation, calculate_fitness):

        replacement = size_of_each_population - number_top_population
        self.calculate_fitness = calculate_fitness
        self.population_cal = Population(self.calculate_fitness)
        self.selection = Selection(replacement)
        self.crossover = Crossover(size_of_each_population,population_batch_size)
        self.population = population_generation(size_of_each_population, population_batch_size)
        self.mutation = Mutation()
        self.multiplot = MultiPlot(population_batch_size)