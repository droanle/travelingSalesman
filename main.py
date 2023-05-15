
from Environment import Environment
from HillClimb import HillClimb

environment = Environment(6, 10, 15)

environment.create_environment()

hillClimb = HillClimb(environment)

hillClimb.hill_climb()

hillClimb.print()