# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 15:44:27 2021

@author: Kenneth
"""

class TexasHoldemBot():
    
    from Opponent_modelling import Opponent_V1
    from DeepRL import DQN
    
    
    def __init__(self, player_positions, player_stacks, big_blind, small_blind):

        self.actions = ['C', 'F', 'A', '2BB', '3BB']
        
        self.number_of_players = len(player_positions)
        
        self.players = []
        
        for idx in range(self.number_of_players):
            
            player = Opponent_V1()
            
            self.players.append(player)
        
        
        self.position_encoding = {'UTG': 0, 'MP':1, 'CO': 2, 'D': 3, 'SB':4, 'BB': 5}
        self.player_positions = self.encode_positions(player_positions)
        
        
        self.player_stacks = player_stacks
        self.player_stakes = [0]*self.number_of_players
        self.player_active = [1]*self.number_of_players
        
        self.big_blind = big_blind
        self.small_blind = small_blind
        
        self.pot_size = 0
        
        self.pre_flop = 1
        self.flop = 0
        self.turn = 0
        self.river = 0
        
        self.board = []
        self.hand = []
        
        self.win_probability = 0
        self.lose_probability = 0
        self.tie_probability = 0
        
        

        self.hand_state = [self.win_probability, self.lose_probability, self.tie_probability]



        self.board_state = [self.number_of_players,
                            self.big_blind, 
                            self.small_blind,
                            self.pot_size,
                            self.pre_flop,
                            self.flop,
                            self.turn,
                            self.river]
        
        self.board_state += self.stakes + self.stacks + self.player_active + player_positions


        self.player_state = []

        for player in self.players:
            
            self.player_state += player.get_features()
            
            
        self.game_state = self.hand_state + self.board_state + self.player_state
        
        
        self.AI = DQN(len(self.game_state), len(self.actions), 0.1, 0.001, 0.99)
        
     
    def encode_positions(self, positions):
        
        encoded_positions = []
        
        for postion in positions:
            
            encoded_positions.append(self.position_encoding[position])  

    
    def set_hand(self, hand):
        
        self.hand = hand
        
        if self.hand != []:
        
            ahead_prob, behind_prob, tied_prob = hand_features.pocket_hand_win_rates(self.hand)
                
            self.win_probability = ahead_prob
            
            self.lose_probability = behind_prob
            
            self.tie_probability = tied_prob
        
        

        
    def set_board(self, board):
        
        self.board = board
        
        
        if self.board != []:
            
            ahead_prob, behind_prob, tied_prob = hand_features.hand_strength(self.hand, self.board)
            
            win_rate, lose_rate, tie_rate = hand_features.hand_potential(self.hand, self.board)
            
            
            self.win_probability = win_rate['ahead']*ahead_prob + win_rate['behind']*behind_prob + win_rate['tied']*tied_prob
            
            self.lose_probability = lose_rate['ahead']*ahead_prob + lose_rate['behind']*behind_prob + lose_rate['tied']*tied_prob
            
            self.tie_probability = tie_rate['ahead']*ahead_prob + tie_rate['behind']*behind_prob + tie_rate['tied']*tied_prob
        
        
    def set_stacks(self, stacks):
        self.stack = stacks
    
    
    def set_stakes(self, stakes):
        self.stakes = stakes
    
    
    def set_player_active(self, player_active):
        self.player_active = player_active
    
    
    def set_pot_size(self, pot_size):
        self.pot_size = pot_size
    
    
    def pre_flop(self, pre_flop = True):
        self.pre_flop = 1
        self.flop = 0
        self.turn = 0
        self.river = 0
        
        
    def flop(self, flop = True):
        self.pre_flop = 0
        self.flop = 1
        self.turn = 0
        self.river = 0
        
        
    def turn(self, turn = True):
        self.pre_flop = 0
        self.flop = 0
        self.turn = 1
        self.river = 0
    
    
    def river(self, river = True):
        self.pre_flop = 0
        self.flop = 0
        self.turn = 0
        self.river = 1
        
   
    
    