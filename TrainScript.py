# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 06:33:43 2021

@author: Kenneth
"""

from NLHoldemEngine import NLHoldemEngine
from Bots.Bot import TexasHoldemBot


buyings = [100, 100]

players = ['Bot1', 'Bot2']


GameEngine = NLHoldemEngine(players=players, buyins=buyins, max_buyin=200, min_buyin=50, BB=2)

order_of_play = GameEngine.get_order_of_play()



Bot1 = TexasHoldemBot(GameEngine.get_positions(), buyins, 2, 1)

Bot2 = TexasHoldemBot(GameEngine.get_positions(), buyins, 2, 1)

bots = {'Bot1': Bot1, 'Bot2': Bot2} 




def get_player_features(our_player, engine)
    

    idx = players.index(our_player)
    
    list_of_players_starting_with_our_player = players[idx:] + players[:idx]


    tablefeatures = engine.get_player_info()
    
    positions =  []
    
    stacks = []
        
    stakes = []
        
    in_play = []

    hand = []    

    
    for player in list_of_players_starting_with_our_player:
        
        for position in order_of_play:
        
            if tablefeatures[position]['player'] == player:
            
                positions.append(position)     
                
                stacks.append(tablefeatures[position]['stacks'])
            
                stakes.append(tablefeatures[position]['stakes'])
            
                in_play.append(tablefeatures[position]['in play'])
                        
    
    for position in order_of_play:
        
        if tablefeatures[position]['player'] == our_player:
            
            hand = tablefeatures[position]['hand']
    
    
    
    return positions, stacks, stakes, in_play, hand
    


def make_a_move(player, engine):

    bot = bots[player]

    positions, stacks, stakes, in_play, hand = get_player_features(player)    


    bot.set_positions(positions)    

    bot.set_stacks(stacks)
    
    bot.set_stakes(stakes)
    
    bot.set_player_active(in_play)
    
    bot.set_hand(hand)
    
    bot.set_pot_size(engine.get_pot())
    
    flop = engine.get_flop()

    turn = engine.get_turn()

    river = engine.get_river()    
    
    board = flop + turn + river

    
    if len(board) == 0:
        bot.pre_flop(True)
        
    elif len(board) == 3:
        bot.flop(True)
        
    elif len(board) == 4:
        bot.turn(True)
        
    else:
        bot.river(True)
    
    
    
    
GameEngine.pay_in_blinds_and_deal()



current_player = GameEngine.get_player(GameEngine.get_current_position())

player_features = get_player_features(current_player)

print(GameEngine.get_player_info())




