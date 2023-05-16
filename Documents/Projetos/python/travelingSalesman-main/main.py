
from Environment import Environment
from HillClimb import HillClimb
from SimulatedTempering import SimulatedTempering

environment = Environment(6, 10, 15)

environment.create_environment()

hillClimb = HillClimb(environment)

hillClimb.hill_climb()

hillClimb.print()

simulatedTempering = SimulatedTempering(environment)
initial_temperature = 900.0
cooling_rate = 0.94
iterations = 20000000
simulatedTempering.simulated_tempering(initial_temperature, cooling_rate, iterations)
simulatedTempering.print()