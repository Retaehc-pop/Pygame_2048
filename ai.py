import neat
import os
import pygame as pg
from Board import Board
import pickle

WIDTH = 800
HEIGHT = 600
DIMENSION = 4
SQUARE_SIZE = HEIGHT // DIMENSION

def run_best_genome(genome,config):
  net = genome
  # neat.nn.FeedForwardNetwork.create(genome, config)
  run = True
  clock = pg.time.Clock()
  board = Board(DIMENSION)
  screen = pg.display.set_mode((WIDTH, HEIGHT))
  while run:
    clock.tick(60)
    for event in pg.event.get():
      if event.type == pg.QUIT:
        run = False
        break
      
    in_neurons = [i for row in board.grid for i in row]
    output = net.activate(in_neurons)
    
    output_moves = [(map_neuron_to_move(i), output[i]) for i in range(len(output))]
    output_moves = sorted(output_moves, key=lambda x: x[1])
    
    for output_move in output_moves:
      board.grid, move = board.push(output_move[0], board.grid)
      if move:
        break
    
    board.draw(screen)
    pg.display.update()
    



def map_neuron_to_move(neuron):
    if neuron == 0:
        return "u"
    elif neuron == 1:
        return "d"
    elif neuron == 2:
        return "l"
    elif neuron == 3:
        return "r"
      

def eval_genome(genome_id, genome, config):
    genome.fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    board = Board(DIMENSION)
    while board.check_game_over() == False:
      in_neurons = [i for row in board.grid for i in row]
      output = net.activate(in_neurons)
      output_moves = [(map_neuron_to_move(i), output[i]) for i in range(len(output))]
      output_moves = sorted(output_moves, key=lambda x: x[1])
      
      for output_move in output_moves:
        board.grid, move = board.push(output_move[0], board.grid)
        if move:
          break
        
      genome.fitness = score_fitness_calculation(board)


def score_fitness_calculation(board):
    score = 0
    score += board.score
    # zeros = 0
    
    # for row in board.grid:
    #   zeros += row.count(0)  
    # score += zeros*10
    
    # max_tile = max([max(row) for row in board.grid])
    # incorner = False
    # for i,row in enumerate(board.grid):
    #   for j,col in enumerate(row):
    #     if i == 0 or i == 3:
    #       if j == 0 or j == 3:
    #         score += max_tile
    #         incorner = True
            
    # if incorner == False:
    #   score -= max_tile
    
    # score -= board.move
            
    return score



def eval_genomes(genomes, config):
  for genome_id, genome in genomes:
      eval_genome(genome_id, genome, config)


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    
    # pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-0')
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    best = pop.run(eval_genomes, 200)
    print('\nBest genome:\n{!s}'.format(best))
    
    best_net = neat.nn.FeedForwardNetwork.create(best, config)
    with open('best_genome.pickle', 'wb') as output:
      pickle.dump(best_net, output)
  
      

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    # run(config_path)
    
    with open('best_genome.pickle', 'rb') as output:
      best = pickle.load(output)
    run_best_genome(best, config_path)
