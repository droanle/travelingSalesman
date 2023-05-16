
from Environment import Environment
from HillClimb import HillClimb

environment = Environment(6, 10, 351, 150)

environment.create_environment()

hillClimb = HillClimb(environment)

hillClimb.hill_climb()

hillClimb.print()