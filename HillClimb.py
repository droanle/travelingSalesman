import Environment
import math
import random
import copy


class HillClimb:
    current_environment = None
    list_of_solutions = []


    def __init__(self,  environment:Environment):
        self.current_environment = environment

    def print(self):
        self.current_environment.print()

        print("Lista de soluções: ")
        for solution in self.list_of_solutions:
            path, value = solution
            print(f"Solução: {path}, Valor: {value}")
        print("\n")


    # Inicia a base de operações para o algoritmo
    def hill_climb(self):
        list_of_solutions = []

        for trains_point in self.current_environment.trains_points:

            solution = self.slope(self.init_solution([trains_point]),
                                  0)

            if len(list_of_solutions) > 0:
                solution = self.solve_oblique_paths(solution, list_of_solutions)

            list_of_solutions.append(solution)

        self.list_of_solutions = list_of_solutions

    def init_solution(self, locked_positions):
        number_of_indexes = len(self.current_environment.index_numbers_list)
        number_of_locked_positions = len(locked_positions)

        index_numbers_list = list(
            set(self.current_environment.index_numbers_list) - set(locked_positions))

        return (locked_positions +
                random.sample(index_numbers_list,
                              (number_of_indexes - number_of_locked_positions)))

    # Implementa o algoritmo de subida de encosta.
    def slope(self, solution, locked_position = 0):
        travel_value = self.evaluate_solution(solution)

        new_travel_value = travel_value
        new_solution = copy.deepcopy(solution)

        attempts = 1

        while True:
            i = random.randint(locked_position + 1, len(solution) - 1)

            for e in range(locked_position + 1, len(solution) - 1):
                aux_solution = copy.deepcopy(solution)
                aux_solution[e] = solution[i]
                aux_solution[i] = solution[e]

                aux_travel_value = self.evaluate_solution(aux_solution)

                if aux_travel_value < new_travel_value:
                    new_travel_value = aux_travel_value
                    new_solution = copy.deepcopy(aux_solution)
                
                

            if new_travel_value < travel_value:
                attempts == 1
                travel_value = new_travel_value
                solution = copy.deepcopy(new_solution)
            elif attempts < self.current_environment.maximum_attempts:
                attempts += 1
            else:
                return [solution, travel_value]
    
    # Verifica se há conflitos no caminho percorrido e corrige-os, se necessário.
    def solve_oblique_paths(self, solution, otherSolutions, init=0):
        for i in range(init, len(solution) - 1):
            e = i + 1
            pointStart = solution[i]
            pointEnd = solution[e]
            for otherSolution in otherSolutions:
                if pointStart == otherSolution[
                        i] and pointEnd == otherSolution[e]:
                    return self.solve_oblique_paths(self.slope(solution, i),
                                                    otherSolutions, i)

        return solution
    
    # Avalia a solução.
    def evaluate_solution(self, solution):
        travel_value = 0

        for i in range(len(solution) - 1):
            travel_value += self.current_environment.distance_matrix[solution[i]][solution[i + 1]]

        return travel_value



