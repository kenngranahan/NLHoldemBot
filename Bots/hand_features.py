# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 15:52:42 2021

@author: Kenneth
"""


max_value = 13
min_value = 2
max_cards = 52
suits = [0, 1, 2, 3]

from pokerhands import showdown, best_hand


def pocket_hand_win_rates(hand):
    
    value0, suit0 = hand[0]
    value1, suit1 = hand[1]
    
    lose = 0                
    tie = 0
    win = 0
    
    if value0 == value1:
        
        # Lose to all pairs greater than our pair. There are 4 choose 2 (which equals 6)
        # combinations of suits for each pair of numbers
        lose = (max_value - value0)*6
        
        # Only tie with the remaining pair 
        tie = 1
        
        # We beat everything else. The number of 2 card hands from the 
        # remaining 50 card deck are computed as 50 choose 2 (which equals 1225)        
        win = 1225 - lose - tie
         
    
    else:
        our_high_card = max(value0, value1)
        
        for opp_value0 in range(max_value+1):
            
            for opp_value1 in range(max_value+1):
            
                opp_high_card = max(opp_value0, opp_value1)
                
                
                # Lose to any pair or a larger high card
                if (opp_value0 == opp_value1) or opp_high_card > our_high_card: 
                    lose+=1
                
                # Tie with equal high cards
                elif our_high_card == opp_high_card: 
                    tie+=1
            
                # Otherwise we win
                else: 
                    win+=1
    
    total = win + lose + tie
    
    return win/total, lose/total, tie/total





def hand_strength(hand, board):
    
    deck = [(value, suit) for value in range(max_value) for suit in suits]
    
    for card in (hand + board):
        deck.remove(card)
    
    win = 0
    lose = 0
    tie = 0
    
    deck_copy = deck.copy()
    
    for first_card in deck:
        
        deck_copy.remove(first_card)
        
        for second_card in deck_copy:   
    
            tmp_hand = [first_card, second_card]
        
            winner = showdown(hand, tmp_hand, board)

            if winner == hand:
                win+=1
            
            elif winner == tmp_hand:
                lose+=1
            
            else:
                tie+=1
    

    total = win + lose + tie

    return win/total, lose/total, tie/total




def hand_potential(our_hand, board):
    
    deck = [(value, suit) for value in range(max_value) for suit in suits]
    
    for card in (our_hand + board):
        deck.remove(card)
    
    look_ahead = 5-len(board)
    
    total_count = {'ahead': 0, 'behind': 0, 'tied': 0}
    win_count = {'ahead': 0, 'behind': 0, 'tied': 0}
    lose_count = {'ahead': 0, 'behind': 0, 'tied': 0}
    tie_count = {'ahead': 0, 'behind': 0, 'tied': 0}
    
    win_rate = {}
    lose_rate = {}
    tie_rate = {}

    first_deck_copy = deck.copy()
    
    
    for card1 in first_deck_copy:
        
        first_deck_copy.remove(card1)
        
        second_deck_copy = first_deck_copy.copy()
        
        
        for card2 in second_deck_copy:
        
            second_deck_copy.remove(card2)
            
            third_deck_copy = second_deck_copy.copy()
        
            opponent_hand = [card1, card2]
        
        
            if board == []:
                
        
                opponent_value0, _ = opponent_hand[0]
                
                opponent_value1, _ = opponent_hand[1]
                
                
                our_value0, _ = our_hand[0]
        
                our_value1, _ = our_hand[1]
        
                
        
                if opponent_value0 == opponent_value1:
                    
                    if our_value0 == our_value1:
                        
                        
                        if our_value0 > opponent_value0:
                            
                            winning_hand = our_hand
                        
                        
                        elif our_value0 < opponent_value0:
                            
                            winning_hand = opponent_hand
                            
                        
                        else:
                            
                            winning_hand = []
        
        
                elif our_value0 == our_value1:
                    
                    winning_hand = our_hand
        
                    
                else:
                    
                    our_high_card = max(our_value0, our_value1)
                    
                    opponent_high_card = max(opponent_value0, opponent_value1)
                    
                    
                    if our_high_card > opponent_high_card:
                        
                        winning_hand = our_hand
                        
                        
                    elif our_high_card > opponent_high_card:
                        
                        winning_hand = opponent_hand
                    
                    
                    else:
                        
                        winning_hand = []
                
                    
            #If we're executing this block of code then board != []    
            else:
                
                winning_hand = showdown(our_hand, opponent_hand, board)
                
                
            
            if winning_hand == our_hand:
                index = 'ahead'
    
            elif winning_hand == opponent_hand:
                index = 'behind'
            
            else:
                index = 'tied'
            
            
            total_count[index] += 1
            
            
            
            
            
            if look_ahead == 1:
            
                for river in third_deck_copy:
                
                    new_board = board + [river]
                    
                    
            elif look_ahead == 2:
                
                fourth_deck_copy = third_deck_copy.copy()
                
                for turn in third_deck_copy:
                
                    fourth_deck_copy.remove(turn)
                    
                    for river in fourth_deck_copy:
                        new_board = board + [turn, river]
                  
                        
            elif look_ahead == 5:
                
                fourth_deck_copy = third_deck_copy.copy()
                
                for flop1 in third_deck_copy:
                
                    fourth_deck_copy.remove(flop1)
                    
                    fifth_deck_copy = fourth_deck_copy.copy()
                    
                    
                    for flop2 in fourth_deck_copy:
                    
                        fifth_deck_copy.remove(flop2)
                        
                        sixth_deck_copy = fifth_deck_copy.copy()
                    
                    
                        for flop3 in fifth_deck_copy:
                    
                            sixth_deck_copy.remove(flop3)
                            
                            seventh_deck_copy = sixth_deck_copy.copy()
                            
                            
                            for turn in sixth_deck_copy:
                                
                                seventh_deck_copy.remove(turn)
                            
        
                                for river in seventh_deck_copy:
                                    new_board = [flop1, flop2, flop3, turn, river]
                                    

            
            winning_hand = showdown(our_hand, opponent_hand, new_board)
            
            new_board = board
            
            if winning_hand == our_hand:
                win_count[index] += 1
            
            elif winning_hand == opponent_hand:
                lose_count[index] += 1
            
            else:
                tie_count[index] += 1
        
    
    for key in win_count.keys():
        
        win_count[key] /= total_count
        
        lose_count[key] /= total_count
        
        tie_count[key] /= total_count
    
    return win_count, lose_count, tie_count

