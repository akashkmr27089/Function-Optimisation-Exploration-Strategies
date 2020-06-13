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
    def __init__(self, size, pop_size, selected_max):
        print("Crossover Class Initialised")
        self.size = size
        self.pop_size = pop_size - selected_max
        self.selected_top = selected_max
    
    def crossover_single(self,a,b,key):
        new_a = a[:key] + b[key:]
        new_b = b[:key] + a[key:]
        return new_a,new_b

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
        self.population_process = Population()

    def selection_to_probability(self, data):
        sum_val = sum(data)
        for i,j in enumerate(data):
            data[i] = data[i]/sum_val
        return data
    
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

    # def set_mutation(self, data , single=True):
    #     final = []
    #     if(single):
    #         final = [x[:self.top] + self.single_bit_mutation(x[self.top:]) for x in data]
    #     else:
    #         pass
    #     return final
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

            
SIZE = 11    #Size of each population
POP = 12    #Population in each batch
NOS_TOP = 4 #Number of top selected population per population
ITERATION = 10 #Number of Iteration 

def main():
    replacement = NOS_TOP
    population_cal = Population()
    selection = Selection(replacement)
    crossover = Crossover(SIZE,POP, NOS_TOP)
    population = population_generation(SIZE, POP)
    mutation = Mutation(NOS_TOP)
    multiplot = MultiPlot(POP)
    for i in range(ITERATION):
        sorted_pop = sorted(population, key=calculate_fitness, reverse=True)  #sort according to fitness
        multiplot.append_data(population_cal.calculate_set_fitness(sorted_pop))
        print("Current Population Fitness :{}".format(population_cal.calculate_set_fitness(sorted_pop)))
        selected_pop = selection.selection(sorted_pop)
        crossover_pop = crossover.crossover_set(selected_pop)
        muted_pop = mutation.set_mutation(crossover_pop)
        population = muted_pop
    multiplot.multi_plot()

if __name__ == "__main__":
    main()

