from flask import Blueprint, render_template, request, jsonify
from Src.Model.Environment import Environment
from Src.Model.SimulatedTempering import SimulatedTempering
from Src.Model.HillClimb import HillClimb
from Src.Model.GeneticAlgorithm import GeneticAlgorithm

Execute = Blueprint('Execute', __name__)


@Execute.route('/hillclimb/')
def hillclimb():
  nPlano = request.args.get('nPlano', type=int)
  nPontos = request.args.get('nPontos', type=int)
  seed = request.args.get('seed', type=int)

  if seed == 0:
    environment = Environment(nPontos, nPlano)
  else:
    environment = Environment(nPontos, nPlano, seed)

  environment.create_environment()

  hillClimb = HillClimb(environment)

  hillClimb.hill_climb()

  return jsonify(hillClimb.export_json())


@Execute.route('/hillclimb/alternating')
def hillclimbAlternating():
  nPlano = int(request.args.get('nPlano'))
  nPontos = int(request.args.get('nPontos'))
  seed = int(request.args.get('seed'))
  attempts = int(request.args.get('attempts'))

  if seed == 0:
    environment = Environment(nPontos, nPlano, None, attempts)
  else:
    environment = Environment(nPontos, nPlano, seed, attempts)

  environment.create_environment()

  hillClimb = HillClimb(environment)

  hillClimb.hill_climb()

  return jsonify(hillClimb.export_json())


@Execute.route('/simulatedseasoning')
def simulatedseasoning():
  nPlano = int(request.args.get('nPlano'))
  nPontos = int(request.args.get('nPontos'))
  seed = int(request.args.get('seed'))
  initial_temperature = int(request.args.get('initial_temperature'))
  cooling_rate = int(request.args.get('cooling_rate'))
  iterations = int(request.args.get('iterations'))

  if seed == 0:
    environment = Environment(nPontos, nPlano)
  else:
    environment = Environment(nPontos, nPlano, seed)

  environment.create_environment()

  simulatedTempering = SimulatedTempering(environment)
  simulatedTempering.base_simulated_tempering(initial_temperature,
                                              cooling_rate, iterations)
  return jsonify(simulatedTempering.export_json())


# this doesnt actually work yet 20/06/2023
@Execute.route('/genetic_algorithm')
def genetic_algorithm_execution():
  nPlano = int(request.args.get('nPlano'))
  nPontos = int(request.args.get('nPontos'))
  seed = int(request.args.get('seed'))
  # population_size = int(request.args.get('population_size'))
  # mutation_rate = float(request.args.get('mutation_rate'))
  # generations = int(request.args.get('generations'))

  gene_size = int(request.args.get('gene_size'))
  population_size = int(request.args.get('population_size'))
  number_generations = int(request.args.get('number_generations'))
  crossbreeding_rate = float(request.args.get('crossbreeding_rate'))
  mutation_rate = float(request.args.get('mutation_rate'))
  generation_interval = float(request.args.get('generation_interval'))

  if seed == 0:
    environment = Environment(nPontos, nPlano)
  else:
    environment = Environment(nPontos, nPlano, seed)

  environment = Environment(10)

  environment.create_environment()
  geneticAlgorithm = GeneticAlgorithm(environment, gene_size, population_size,
                                      number_generations, crossbreeding_rate,
                                      mutation_rate, generation_interval)

  # current_population, generational_fitness =
  geneticAlgorithm.run()

  return jsonify(geneticAlgorithm.export_json())
