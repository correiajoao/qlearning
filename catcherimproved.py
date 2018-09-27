import random
import operator
from PyGameLearningEnvironment.ple.games import Catcher
from PyGameLearningEnvironment.ple import PLE

#Variáveis globais
q_table = [[0 for i in range(4)] for j in range(4)]
reward = 0.0

epsilon = 1	
alpha = 0.1
gama = 0.9

info = False

missed = 0 
win = 0

#Função de atualização do reforço naquele estado
def updateQTable(fruit_x, new_fruit_x, action, reward):
	qsa = q_table[fruit_x][action]
	rsa = reward 
	qlmax = max(q_table[new_fruit_x])
	q_table[fruit_x][action] = qsa + alpha*(rsa + gama*(qlmax) - qsa)

	if(info):
		print("Estado: ",fruit_x, action, " -- Recompensa: ",q_table[fruit_x][action])

#Função de escolha da melhor ação para aquele estado
def chooseBestAction(fruit_x):
	index, value = max(enumerate(q_table[fruit_x]), key = operator.itemgetter(1))
	return index

def getFruitPosition(player_x, fruit_x):
	if(player_x < fruit_x):
		return 0
	elif(player_x > fruit_x):
		return 1
	else:
		return 2

def updatePoints(reward):
	global win
	global missed
	if(reward == -1.0):
		missed = missed +1
	elif(reward == 1.0):
		win = win + 1

		if (info):
			print("Missed:", missed, "Win:", win)


for i in range(0,2):
	game = None;
	p = None;

	if(i == 0):
		print("Treinando ... ")
		frames = 100
		info = False

		game = Catcher(width=600, height=600, init_lives=1000000000)
		p = PLE(game, fps=30, display_screen=False, force_fps=False)
	else:

		info = True
		frames = 1000000

		game = Catcher(width=600, height=600, init_lives=1000000000)
		p = PLE(game, fps=30, display_screen=True, force_fps=True)	

	p.init()

	for f in range(frames):
		if p.game_over(): #check if the game is over
			p.reset_game()

		previous_state = game.getGameState()
		previous_state_discrete = getFruitPosition(previous_state['player_x'], previous_state['fruit_x'])

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
			current_state_discrete = getFruitPosition(current_state['player_x'], current_state['fruit_x'])
			
		else:
		#Caso não explore, executa a ação com maior reforço já conhecida
			action = chooseBestAction(previous_state_discrete)
			if(action == 0):
				reward = p.act(97)
			elif (action == 1):
				reward = p.act(100)
			else:
				reward = p.act(None)

			current_state = game.getGameState()
			current_state_discrete = getFruitPosition(current_state['player_x'], current_state['fruit_x'])

		if(info):
			print(previous_state)
			print(current_state)

		epsilon = epsilon - 0.01
		updatePoints(reward)
		updateQTable(previous_state_discrete, current_state_discrete, action, reward)	

