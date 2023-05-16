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
            path, value, temp = solution
            print(f"Solution: {path}, Best value: {value}, Temperature: {temp}")
        print("\n")

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

        self.list_of_solutions.append((best_solution, final_value, temperature))

    def init_solution(self, locked_positions):
        index_numbers_list = list(set(self.current_environment.index_numbers_list) - set(locked_positions))
        return locked_positions + random.sample(index_numbers_list, len(index_numbers_list))

    def slope(self, solution):
        index1 = random.randint(0, len(solution) - 1)
        index2 = random.randint(0, len(solution) - 1)

        while index1 == index2:
            index2 = random.randint(0, len(solution) - 1)

        solution[index1], solution[index2] = solution[index2], solution[index1]
        return solution

    def evaluate_solution(self, solution):
        travel_value = 0

        for i in range(len(solution) - 1):
            travel_value += self.current_environment.distance_matrix[solution[i]][solution[i + 1]]

        return travel_value
