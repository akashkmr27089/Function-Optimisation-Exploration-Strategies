import matplotlib.pyplot as plt
import numpy as np
import random
from GeneticNeuralNetwork import *

class Population:
    def __init__(self, calculate_fitness, network):
        print("Population Class Initialised")
        self.calculate_fitness = calculate_fitness
        self.network = network
    
    def calculate_set_fitness(self, data):
        return [self.calculate_fitness(x, self.network) for x in data]

    def calucluate_score(self, data):
        return self.calculate_fitness(data, self.network)

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
        if(single): ## single crossver selected 
            selection_index = random.choices([x for x in range(self.size)], k = self.pop_size)
            j = 0
            final_population = []
            for i in range(0, self.pop_size-1, 2):
                final_population += list(self.crossover_single(population[i],population[i+1],
                                    selection_index[j]))
                j+= 1
        else:
            pass 
            #Write fuction for double crossover
        return final_population

class Selection:
    def __init__(self, nos_selection, population, number_of_selected_population, network):
        print("Selection Initialised")
        self.replace = nos_selection
        self.pop_control = population
        self.nos_pop_out = number_of_selected_population
        self.network = network

    def population_to_probability(self, population):
        fitness_score = self.pop_control.calculate_set_fitness(population)
        sum_val = sum(fitness_score)
        selection_prob = [self.pop_control.calculate_fitness(x, self.network)/sum_val for x in population]
        return selection_prob
    
    def selection(self, population, type='default'): 
        #function responsible for rearrangements 
        if(type == 'default'):
            new_population = population[:-self.replace] + population[:self.replace]
        elif(type == 'roulette'):
            self.probability_population = self.population_to_probability(population)
            new_population = random.choices(population, weights=self.probability_population, k = self.nos_pop_out)
        return new_population

#mutation is used so that if every member of population is same then itdoesnt stop improving
class Mutation:
    def __init__(self, top):
        print("Mutaion Initialised")
        self.top = top

    def single_bit_mutation(self, data):
        pos = random.randint(0, len(data)-1)
        data[pos] = np.random.randn()
        return data

    def set_mutation(self, data, single=True):
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
        number_top_population, selection_population, population_generation, calculate_fitness, network, limits):

        replacement = number_top_population
        self.max_score = 0
        self.best_model = None
        self.calculate_fitness = calculate_fitness
        self.population_cal = Population(self.calculate_fitness, network)
        self.selection = Selection(replacement, self.population_cal, selection_population, network)
        self.crossover = Crossover(size_of_each_population, selection_population)
        self.population = population_generation(network, population_batch_size)   #population_generation
        self.mutation = Mutation(number_top_population)
        self.multiplot = MultiPlot(population_batch_size)
        self.top_population = number_top_population
        self.population_batch_size = population_batch_size
        self.network = network
        self.limits = limits

    def train(self, iteration, type_selection='roulette'):
        for i in range(iteration):
            print("Iteration Number {} with current Maximum score of {}".format(i, self.max_score))
            sorted_pop = sorted(self.population, key=self.population_cal.calucluate_score, reverse=True)[:self.population_batch_size]
            self.multiplot.append_data(self.population_cal.calculate_set_fitness(sorted_pop))
            current_max_score = self.population_cal.calucluate_score(sorted_pop[0])
            if(current_max_score > self.max_score):
                self.max_score = current_max_score
                self.best_model = sorted_pop[0]
            if(self.limits <= self.max_score): break
            selected_pop = self.selection.selection(sorted_pop, type_selection)
            crossover_pop = self.crossover.crossover_set(selected_pop)
            muted_pop = self.mutation.set_mutation(crossover_pop)
            muted_pop += sorted_pop
            self.population = muted_pop
        print("Trainig Over")

    def display(self):
        self.multiplot.multi_plot()
