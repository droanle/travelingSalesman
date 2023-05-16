import random
import math

class Environment:
    cartesian_size = 10
    number_of_points = 0
    coordinate_list = {}
    distance_matrix = []
    trains_points = []
    index_numbers_list = []

    def __init__(self, number_of_points, cartesian_size = 10, seed = None):

        if(seed == None):
            seed = random.randrange(1,1000)
            
        random.seed(seed)

        self.number_of_points = number_of_points
        self.cartesian_size = cartesian_size

    def print(self):

        print("Lista de coordenadas: {")
        for key, value in self.coordinate_list.items():
            print(f"   {key:3}: [{value[0]:2},{value[1]:2}]")
        print("}\n")

        print("Matriz de distancias: ")
        for linha in self.distance_matrix:
            print("   |", end="")
            for val in linha:
                print('{:3}  |'.format(val), end="")
            print("")
        print("\n")

        print("Local inicial dos trens: ", end="")
        print(self.trains_points)
        print("\n")

        print("Lista de índices: ")
        print("   |", end="")
        for linha in self.index_numbers_list:
            print('{:3}  |'.format(linha), end="")
        print("\n")
    
    # Cria um ambiente com dados aleatórios.
    def create_environment(self):
        min_x, max_x = 0, self.cartesian_size
        min_y, max_y = 0, self.cartesian_size

        for i in range(self.number_of_points):
            x = round(random.uniform(min_x, max_x))
            y = round(random.uniform(min_y, max_y))

            self.index_numbers_list.append(i)
            self.coordinate_list[i] = [x, y]

        for i in self.coordinate_list:
            coordinate_row = []
            x1, y1 = self.coordinate_list[i][0], self.coordinate_list[i][1]

            for e in self.coordinate_list:
                x2, y2 = self.coordinate_list[e][0], self.coordinate_list[e][1]

                coordinate_row.append(
                    round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2)))

            self.distance_matrix.append(coordinate_row)


        self.trains_points = random.sample(self.coordinate_list.keys(), 3)

