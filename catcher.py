import random
import operator
from PyGameLearningEnvironment.ple.games import Catcher
from PyGameLearningEnvironment.ple import PLE

#Variáveis globais
q_table = [[[0 for i in range(3)] for j in range(128)] for k in range(128)]
reward = 0.0

epsilon = 1	
alpha = 0.1
gama = 0.9

info = False

#Função de atualização do reforço naquele estado
def updateQTable(player_x, fruit_x, action, reward, new_player_x):
	qsa = q_table[player_x][fruit_x][action]
	rsa = reward 
	qlmax = max(q_table[new_player_x][fruit_x])
	q_table[player_x][fruit_x][action] = qsa + alpha*(rsa + gama*(qlmax) - qsa)

	if(info):
		print("Estado: ", player_x, fruit_x, action, " -- Recompensa: ",q_table[player_x][fruit_x][action])

#Função de escolha da melhor ação para aquele estado
def chooseBestAction(player_x, fruit_x):
	index, value = max(enumerate(q_table[player_x][fruit_x]), key = operator.itemgetter(1))
	return index



for i in range(0,2):
	game = None;
	p = None;

	if(i == 0):
		print("Treinando ... ")
		frames = 1000
		info = False

		game = Catcher(width=128, height=128, init_lives=1000000000)
		p = PLE(game, fps=30, display_screen=False, force_fps=False)
	else:

		info = True
		frames = 1000000

		game = Catcher(width=128, height=128, init_lives=1000000000)
		p = PLE(game, fps=30, display_screen=True, force_fps=True)	

	p.init()

	for f in range(frames):
		if p.game_over(): #check if the game is over
			p.reset_game()

		previous_state = game.getGameState()
		#Escolhe baseado no episilon se irá explorar ou não
		rand = random.random()
		if(rand < epsilon):
			#Escolhe qual ação irá tomar
			action = random.randint(0,2)
			if(action == 0):
				reward = p.act(97) #Mover para a esquerda			
			elif (action == 1):
				reward = p.act(100) #Mover para a direita
			else:
				reward = p.act(None) #Não fazer nada
			
			current_state = game.getGameState()
			
		else:
		#Caso não explore, executa a ação com maior reforço já conhecida
			action = chooseBestAction(previous_state['player_x'], previous_state['fruit_x'])
			if(action == 0):
				reward = p.act(97)
			elif (action == 1):
				reward = p.act(100)
			else:
				reward = p.act(None)

			current_state = game.getGameState()

		if(info):
			print(previous_state)
			print(current_state)

		epsilon = epsilon - 0.0001
		updateQTable(previous_state['player_x'], previous_state['fruit_x'], action, reward, current_state['player_x'])	
