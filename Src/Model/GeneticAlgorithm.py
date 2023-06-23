import csv
import Environment
import copy as cp
import numpy as np
import random
import math
from Environment import Environment

# N  =  [10,30,50,100]         # TAMANHO DO CROMOSSOMO

# TP =  [20,50,100,300,500]          # TAMANHO DA POPULAÇÃO
# NG =  [50,100,200,500]        # NÚMERO DE GERAÇÕES
# TC =  [0.4,0.6,0.8,0.9]        # TAXA DE CRUZAMENTO
# TM =  [0,0.05,0.1,0.2,0.5]        # TAXA DE MUTAÇÃO
# IG =  [0,0.1,0.2,0.5]        # INTERVALO DE GERAÇÃO


class GeneticAlgorithm:

  def __init__(self, environment, gene_size, population_size,
               number_generations, crossbreeding_rate, mutation_rate,
               generation_interval):
    self.environment = environment
    self.gene_size = gene_size
    self.population_size = population_size
    self.number_generations = number_generations
    self.crossbreeding_rate = crossbreeding_rate
    self.mutation_rate = mutation_rate
    self.generation_interval = generation_interval

    self.current_population = []
    self.generational_fitness = []

  def export_json(self): 

    current_environment = self.environment
    trains_infos = {}

    # for i in range(len(current_environment.trains_points)):
    #     solution, value = self.list_of_solutions[i]

    #     solution_coordinates = {}

    #     for e in range(len(solution)):
    #         solution_coordinates[e] = current_environment.coordinate_list[solution[e]]

    #     trains_infos[i] = {
    #         "init_point": current_environment.coordinate_list[current_environment.trains_points[i]],
    #         "solution_value": value,
    #         "solution_full": solution,
    #         "solution": solution_coordinates
    #     }

    print([self.current_population, self.generational_fitness])

    json = {
      "cartesian_size": current_environment.cartesian_size,
      "number_of_points": current_environment.number_of_points,
      "coordinate_list": current_environment.coordinate_list,
      "distance_matrix": current_environment.distance_matrix,
      "trains_infos": trains_infos
    }

    return json

  def initial_population(self):
    population = np.zeros((self.population_size, self.gene_size))

    for i in range(self.population_size):
      population[i] = np.random.permutation(self.gene_size)

    return population

  def fitness(self, population):
    fitness_values = np.zeros(self.population_size)

    for i in range(self.population_size):
      fitness_values[i] = self.evaluate_solution(population[i])

    return fitness_values

  def evaluate_solution(self, solution):
    travel_cost = 0

    for i in range(self.gene_size - 1):
      current_node = int(solution[i])
      next_node = int(solution[i + 1])
      graph_cost = self.environment.distance_matrix[current_node][next_node]

      travel_cost += graph_cost

    return travel_cost

  # uniform crossover rather than k-point crossover
  def uniform_choice(self, parent):
    gene = random.uniform(0, 1)
    individual = 0
    sum = parent[individual]

    while sum < gene:
      individual += 1
      sum += parent[individual]

    return individual

  def crossover(self, current_population, fitness):
    new_population = np.zeros((self.population_size, self.gene_size))

    for i in range(self.population_size):
      parent1 = self.uniform_choice(fitness)
      parent2 = self.uniform_choice(fitness)

      child = np.zeros(self.gene_size)

      for j in range(self.gene_size):
        if random.uniform(0, 1) < self.crossbreeding_rate:
          child[j] = current_population[parent1][j]
        else:
          child[j] = current_population[parent2][j]

      new_population[i] = child

    return new_population

  def mutation(self, current_population):
    max_mutations = int(self.mutation_rate * self.gene_size)
    children_amount = len(current_population)

    for _ in range(max_mutations):
      child = current_population[random.randint(0, children_amount - 1)]
      child_doppelganger = cp.deepcopy(child)

      gene1 = random.randint(0, self.gene_size - 1)
      gene2 = random.randint(0, self.gene_size - 1)

      gene_holder = child_doppelganger[gene1]
      child_doppelganger[gene1] = child_doppelganger[gene2]
      child_doppelganger[gene2] = gene_holder

      current_population = np.append(current_population, [child_doppelganger],
                                     axis=0)

    return current_population

  # iron lung method™ (survival of the fittest)
  def selection(self, current_population, fitness):
    # is this spelled right? i don't know, i don't speak french
    bourgeoisie = math.ceil(self.population_size * self.generation_interval)

    # sort by fitness
    current_population = current_population[np.argsort(fitness)]

    new_generation = 0

    for survivor in range(bourgeoisie):
      chosen_individual = cp.deepcopy(current_population[new_generation])

      current_population[survivor] = chosen_individual

      new_generation += 1

      if (new_generation >= self.population_size):
        break

    return current_population

  def run(self):
    current_population = self.initial_population()
    initial_fitness = np.min(self.fitness(current_population))
    generational_fitness = [{0: initial_fitness}]

    for generation in range(1, self.number_generations + 1):
      new_population = self.crossover(current_population,
                                      self.fitness(current_population))

      new_population = self.mutation(new_population)
      new_fitness = np.min(self.fitness(new_population))

      generational_fitness.append({generation: new_fitness})

      current_population = self.selection(new_population,
                                          self.fitness(new_population))
      initial_fitness = np.min(self.fitness(current_population))

    self.current_population = current_population
    self.generational_fitness = generational_fitness

    # return current_population, generational_fitness


# run with all possible parameters using a single environment
# possible_gene_size = [10, 30, 50, 100]

# possible_population_size = [20, 50, 100, 300, 500]
# possible_number_generations = [50, 100, 200, 500]
# possible_crossbreeding_rate = [0.4, 0.6, 0.8, 0.9]
# possible_mutation_rate = [0, 0.05, 0.1, 0.2, 0.5]
# possible_generation_interval = [0, 0.1, 0.2, 0.5]

# import itertools

# initial_path = None
# current_run = 0
# for gene_size, population_size, number_generations, crossbreeding_rate, mutation_rate, generation_interval in itertools.product(
#     possible_gene_size, possible_population_size, possible_number_generations,
#     possible_crossbreeding_rate, possible_mutation_rate,
#     possible_generation_interval):
#   environment = Environment(10)
#   environment.create_environment()
#   ga = GeneticAlgorithm(environment, gene_size, population_size,
#                         number_generations, crossbreeding_rate, mutation_rate,
#                         generation_interval)
#   current_population, generational_fitness = ga.run()

#   print("run: ", current_run)
#   print("gene_size: ", gene_size)
#   print("population_size: ", population_size)
#   print("number_generations: ", number_generations)
#   print("crossbreeding_rate: ", crossbreeding_rate)
#   print("mutation_rate: ", mutation_rate)
#   print("generation_interval: ", generation_interval)

#   if current_run == 0:
#     initial_path = current_population[0]
#     # calculate evaluation
#     initial_fitness = ga.evaluate_solution(initial_path)

#   generation_path = current_population[0]
#   # calculate evaluation
#   generation_fitness = ga.evaluate_solution(generation_path)

#   gain = (generation_fitness - initial_fitness) / initial_fitness
#   print("gain: ", gain)
#   print("----------------------")
#   current_run += 1
#   row = [
#     current_run, gene_size, population_size, number_generations,
#     crossbreeding_rate, mutation_rate, generation_interval, gain
#   ]
