# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 11:38:08 2021

@author: Kenneth
"""


import torch.nn as nn
from torch.optim import SGD

from random import randint, random

class DQN():
    
    def __init__(self, number_of_features, number_of_actions, epsilon, learning_rate, discount_factor):
        
        
        self.epsilon = epsilon
        
        self.learning_rate = learning_rate

        self.discount_factor = discount_factor
        

        self.current_state = []
        
        self.action = 0
        
        self.reward = 0 

        self.next_state = []

        self.experience = []

        
        self.prediction_network = self.network_architecture(number_of_features, number_of_actions)
        
        self.target_network = self.network_architecture(number_of_features, number_of_actions)        

        self.target_network.requires_grad_(False)
        
       
        self.optim = SGD(self.prediction_network.parameters(), lr = self.learning_rate)
        
        self.loss = nn.MSELoss()
        
        
        
    class network_architecture(nn.Module):
          
         def __init__(self, number_of_features, number_of_actions):
                 super(Opponent, self).__init__()
        
        
            self.model = nn.Sequential(
             
             nn.Linear(number_of_features, (number_of_features + number_of_actions)/2),
             nn.Tanh(),
             
             nn.Linear((number_of_features + number_of_actions)/2, (number_of_features + number_of_actions)/2),
             nn.Tanh(),
             
             nn.Linear((number_of_features + number_of_actions)/2, number_of_actions),
             nn.Tanh()
            )
            
            
        def forward(self, game_state):
            
            Q_values = self.model(game_state)
            
            return Q_values
            
       

    def initalize_game_state(self, game_state):
        
        self.current_state = game_state
    
    
    
    
    def choose_action(self):
        
        predicted_Q_values = self.prediction_network.forward(self.current_state)
        
        maximum_predicted_Q_value = max(predicted_Q_values)
              
        
        random_float = random()
        
        if random_float <= self.epsilon:
            
            action = randomint(0, len(self.actions)-1) 
            
        else:
            
            action = predicted_Q_values.index(maximum_predicted_Q_value)
            
        self.action = action
        
        
        return self.action
        
    
    
    def set_reward_and_new_game_state(self, reward, new_game_state):
        
        self.next_state = new_game_state
        
        self.reward = reward
        
        self.experience.append([self.current_state, self.action, self.reward, self.next_state])
        
        
        self.current_state = self.next_state
        
        
        
    def train(self):
        
        
        for experience in self.experience:
            
            
            state, action, reward, new_state = experience
            
            
            Q_values_of_new_state = self.target_network(new_state)
            
            target = reward + self.discount_factor*max(Q_values_of_new_state)
            
            
            Q_values_of_current_state = self.prediction_network(state)
            
            Q_value_of_action_taken = Q_values_of_current_state[action]
            
            
            error = self.loss(target, Q_value_of_action_taken)
            
            error.backward()
            
            self.optim.step()
            
    
    def update_target_network(self):
        
        self.target_network.load_state_dict(self.prediction_network.state_dict())
        
        self.target_network.requires_grad_(False)
          
        
    
    def save(self, f):
         
        try:
            torch.save(self.prediction_network, f)
        
        except OSError as err:
            
            print("OS Error: {0}".format(err))
            print('Attempting to write to DQN_prediction_network.pt')
            
            try:
                
                torch.save(self.prediction_network, 'DQN_prediction_network.pt')
                print("Successfully writen")
            
            except:
                print('Failed')
    
    
    
    def load(self, f):
        
        try:
            self.prediction_network = torch.load(f)
        
            self.update_target_network()
        
        except OSError as err:
            print("OS Error: {0}".format(err))
            
        except:
            print('Unknown error occured when loading')
            
    
    