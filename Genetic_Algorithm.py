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
    def __init__(self, size, pop_size, selected_max):
        print("Crossover Class Initialised")
        self.size = size
        self.pop_size = pop_size - selected_max
        self.selected_top = selected_max
    
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
        final_population = [population[x] for x in range(self.selected_top)]
        if(single): ## single crossver selected 
            selection_index = random.choices([x for x in range(self.size)], k = self.pop_size)
            j = 0
            for i in range(self.selected_top, self.pop_size + self.selected_top, 2):
                final_population += list(self.crossover_single(population[i],population[i+1],
                                    selection_index[j]))
                j+= 1
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
    def __init__(self, top):
        print("Mutaion Initialised")
        self.top = top
    
    def single_bit_mutation(self, data):
        pos = random.randint(0, len(data)-1)
        if(data[pos] == 1): data[pos] = 0
        else: data[pos] = 1
        return data

    def set_mutation(self, data , single=True):
        final = []
        if(single):
            for i,j in enumerate(data):
                if(i<= self.top-1): final.append(j)
                else: final.append(self.single_bit_mutation(j))
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
        number_top_population, population_generation, calculate_fitness):

        replacement = number_top_population
        self.calculate_fitness = calculate_fitness
        self.population_cal = Population(self.calculate_fitness)
        self.selection = Selection(replacement)
        self.crossover = Crossover(size_of_each_population,population_batch_size, replacement)
        self.population = population_generation(size_of_each_population, population_batch_size)
        self.mutation = Mutation(number_top_population)
        self.multiplot = MultiPlot(population_batch_size)
        self.top_population = number_top_population

    def train(self, iteration):
        for _ in range(iteration):
            sorted_pop = sorted(self.population, key=self.calculate_fitness, reverse=True)
            self.multiplot.append_data(self.population_cal.calculate_set_fitness(sorted_pop))
            selected_pop = self.selection.selection(sorted_pop)
            crossover_pop = self.crossover.crossover_set(selected_pop)
            muted_pop = self.mutation.set_mutation(crossover_pop)
            self.population = muted_pop
        print("Trainig Over")

    def display(self):
        self.multiplot.multi_plot()

    def top_population(self):
        return self.population[:self.top_population]
