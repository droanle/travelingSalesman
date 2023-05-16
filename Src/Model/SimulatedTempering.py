import random
import math
from copy import deepcopy

class SimulatedTempering:
    def __init__(self, environment):
        self.current_environment = environment
        self.list_of_solutions = [] 

    def print(self):
        self.current_environment.print()
        print("List of solutions:")
        for solution in self.list_of_solutions:
            path, value, temp, gain = solution
            print(f"Solution final : {path}, Best value: {value}, Temperature: {temp}, Ganho: {gain}")
        print("\n")

    def export_json(self):

        current_environment = self.current_environment
        trains_infos = {}

        for i in range(len(current_environment.trains_points)):
            solution, value, temp, gain = self.list_of_solutions[i]

            solution_coordinates = {}
            
            for e in range(len(solution)):
                solution_coordinates[e] = current_environment.coordinate_list[solution[e]]
            
            trains_infos[i] = {
                "init_point": current_environment.coordinate_list[current_environment.trains_points[i]],
                "solution_value": value,
                "temp": temp,
                "gain": gain,
                "solution": solution_coordinates
            }
        
        json = {
            "cartesian_size": current_environment.cartesian_size,
            "number_of_points": current_environment.number_of_points,
            "coordinate_list": current_environment.coordinate_list,
            "distance_matrix": current_environment.distance_matrix,
            "trains_infos": trains_infos
        }

        return json

    # Inicia a base de operações para o algoritmo
    def base_simulated_tempering(self, initial_temperature, reducing_factor, iterations):
        list_of_solutions = []

        for trains_point in self.current_environment.trains_points:

            [solution, value, temp, gain] = self.simulated_tempering(initial_temperature, reducing_factor, iterations)
            

            if len(list_of_solutions) > 0:
                solution = self.solve_oblique_paths(solution, list_of_solutions)

            list_of_solutions.append([solution, value, temp, gain])

        self.list_of_solutions = list_of_solutions

    # Verifica se há conflitos no caminho percorrido e corrige-os, se necessário.
    def solve_oblique_paths(self, solution, otherSolutions, init=0):
        for i in range(init, len(solution) - 1):
            e = i + 1
            pointStart = solution[i]
            pointEnd = solution[e]

            for otherSolution in otherSolutions:
                if pointStart == otherSolution[0][i] and pointEnd == otherSolution[0][e]:
                    return self.solve_oblique_paths(self.slope(solution),
                                                    otherSolutions, i)

        return solution
    
    def simulated_tempering(self, initial_temperature, reducing_factor, iterations):
        current_solution = self.init_solution(self.current_environment.trains_points)
        current_value = self.evaluate_solution(current_solution)
        best_solution = deepcopy(current_solution)
        final_value = current_value

        

        temperature = initial_temperature

        for i in range(iterations):
            new_solution = self.slope(deepcopy(current_solution))
            new_value = self.evaluate_solution(new_solution)

            delta_expo = new_value - current_value

            if delta_expo < 0 or random.random() < math.exp(-delta_expo / temperature):
                current_solution = deepcopy(new_solution)
                current_value = new_value

            if new_value < final_value:
                best_solution = deepcopy(new_solution)
                final_value = new_value
            
            temperature *= reducing_factor

        gain = (current_value-final_value)/current_value
        return (best_solution, final_value, temperature, gain);
    

    def init_solution(self, locked_positions):
        index_numbers_list = list(set(self.current_environment.index_numbers_list) - set(locked_positions))
        return locked_positions + random.sample(index_numbers_list, len(index_numbers_list))

    def slope(self, solution):

        print(solution)
        index1 = random.randint(0, len(solution) - 1)
        index2 = random.randint(0, len(solution) - 1)

        while index1 == index2:
            index2 = random.randint(0, len(solution) - 1)

        print(solution[index2], solution[index1])

        solution[index1], solution[index2] = solution[index2], solution[index1]
        return solution

    def evaluate_solution(self, solution):
        travel_value = 0

        for i in range(len(solution) - 1):
            travel_value += self.current_environment.distance_matrix[solution[i]][solution[i + 1]]

        return travel_value
