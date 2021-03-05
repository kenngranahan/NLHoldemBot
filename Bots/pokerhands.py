#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 14:16:46 2020

@author: kenneth
"""

   
def best_hand(hand, board):
    #Different hand types are encoded using 
    #(max_value_count, (max_suit_count>=5), hand_identifier)
    #where:
    
    #max_value_count is the highest number of matching values in a hand,
    #(max_suit_count>=5) is a boolean for if the number of matching suits is >= 5
    #hand_identifier is a condition used to distinguish 2 hands where max_value_count
    #and (max_suit_count>=5) can't.
    
    #e.g. a hand with max_value_count==2 and (max_suit_count>=5) == False 
    #is either a pair or 2 pair. hand_identifier == 0 and hand_identifier == 1
    #distinguishes these two cases respectively.
    
    hand_mapping = {(1, 0, 0): 0, #high card 
                    (2, 0, 0): 1, #pair
                    (2, 0, 1): 2, #2 pair
                    (3, 0, 0): 3, #3 of a kind
                    (1, 0, 0): 4, #straight
                    (1, 1, 0): 5, #flush
                    (3, 0, 1): 6, #full house
                    (4, 0, 0): 7, #4 of a kind
                    (1, 1, 1): 8} #straight flush
   
    
    #Initalize some variables
    max_card_value = 12
    suits = [0, 1, 2, 3]
    
    final_hand = []
    best_hand_values = []
    max_value_count = 1
    max_suit_count = 2
    hand_identifer = 0
    
    full_hand = hand + board
    suits_in_hand = []
    values_in_hand = []
    
    
    
    
    for card in full_hand:
    
        value, suit = card
        
        values_in_hand.append(value)
        
        suits_in_hand.append(suit)

    
    #Count how many of each suit is in the full hand. Take the maximum
    #suit count
    suit_count = [suits_in_hand.count(suit) for suit in suits]
    
    max_suit_count = max(suit_count)            
    
    
    if max_suit_count < 5:
        

        decending_number_list = list(range(max_card_value+1))        
        decending_number_list.reverse()
        
        
        #Create a list of card values(e.g. 'J' has a value of 11) sorted 
        #in descending order. Then count how many of each value we have. 
        #Take the maximum count
        values_in_hand.sort(reverse = True)
    
        value_count = [values_in_hand.count(value) for value in decending_number_list]
        
        max_value_count = max(value_count)
        
        
        #This is a handy function. It returns
        #the first set (pair, 3 of a kind, 4 of a kind) found in the hand.
        #Since this has been sorted in descending order, the first set has
        #the highest value
        def find_set(value_count, set_number):
        
            number = max_card_value - value_count.index(set_number)
            
            return [number]*set_number
        
        
        #This function is internal to this method. It returns a list of
        #values to complete our hand (Ace high, King high, etc.)
        def find_kickers(full_hand, cards_used, number_of_kickers):
        
            kickers = []
            
            for card in full_hand[:5]:    
            
                if len(kickers) == number_of_kickers:
                    break
                
                elif (card not in cards_used):
                    kickers.append(card)
            
            return kickers
  
        
        #Here we check all combinations of pairs, 3 of a kind and 4 of a kind  
        if max_value_count <= 4:
            
            best_hand_values = find_set(value_count, max_value_count)
            
            
            if max_value_count == 3:
                
                #This varible determines if there is a pair in our in hand. In which
                #case we have a full house
                hand_identifer = int(2 in value_count)
            
                if hand_identifer == 1:
                    best_hand_values = best_hand_values + find_set(value_count, 2)
            
            
            elif max_value_count == 2:
                
                #Find the index of the first pair in the value_count list
                idx = max_card_value - best_hand_values[0]
                
                if idx < (len(value_count) - 1):
            
                    #This varible determines if there is another pair in our in hand. In which
                    #case we have two pair
                    hand_identifer = int(2 in value_count[idx+1:])
                    
                    if hand_identifer == 1:
                        
                        second_idx = value_count[idx+1:].index(2)
                        
                        full_idx = second_idx + idx + 1
                        
                        best_hand_values = best_hand_values + ([max_card_value - full_idx]*2)
            
            #Add any kickers to complete the hand(if needed)
            best_hand_values = best_hand_values + find_kickers(values_in_hand, best_hand_values, 5-len(best_hand_values))
        
        
        #Here we check for straight and high card
        else:
            
            
            best_hand_values = values_in_hand[:5]
            
            
            for idx in range(len(values_in_hand) - 4):
                
                #This variable determines if we have a straight or not
                hand_identifer = int(values_in_hand[idx] == (values_in_hand[idx+4] + 4))
                
                if hand_identifer == 1:
                
                    best_hand_values = values_in_hand[idx:idx+5]
                    
                    break
            
            
            #This is a special case where we check for [A,5,4,3,2] which has been encoded as [12,3,2,1,0]
            if values_in_hand[0] == max_card_value:
                
                for idx in range(len(values_in_hand) - 3):
                    
                hand_identifer = int((values_in_hand[idx+1] == 3) and(values_in_hand[idx+3] == 0))
                
                if hand_identifer == 1:
                
                    best_hand_values = values_in_hand[0] + values_in_hand[idx+1:idx+5]
                    break
                
                #This variable determines if we have a straight or not
                hand_identifer = int((values_in_hand[1] == 3) and (values_in_hand[4] == 0))
                
                if hand_identifer == 1:
                
                    best_hand_values = values_in_hand[:5]
        
        
        
        #If we've reached here, then we have identified the best hand.
        #So now we need to assign the correct 
        #suit to each card to get the final_hand
        unique_list = []
        
        for value in best_hand_values:
        
            if value not in unique_list:
        
                unique_list.append(value)
        
        
        for value in unique_list:
            
            suits = [s for (v, s) in full_hand if v == value]
            
            cards = [(value, s) for s in suits]
            
            final_hand = final_hand + cards



    #If we're executing this code block, then we have >= 5 cards with the
    #same suit, i.e. we have a straight flush or a flush
    else:
        
        
        #Find the matching suit, then pick out all the cards
        #with this suit. Then map these cards to their values
        suit = suits[suit_count.index(max_suit_count)]
        
        values_in_hand = [value for (value, s) in full_hand if s == suit]
        
        values_in_hand.sort(reverse = True)
    
    
        #Take high card if there are no straights
        best_hand_values = values_in_hand[:5]
        
        
        for idx in range(len(values_in_hand) - 4):
            
            #This variable determines if we have a straight or not
            hand_identifer = int(values_in_hand[idx] == (values_in_hand[idx+4] + 4))
            
            if hand_identifer == 1:
            
                best_hand_values = values_in_hand[idx:idx+5]
                
                break
        
        
        #This is a special case where we check [A,5,4,3,2] which has been encoded as [12,3,2,1,0]    
        if values_in_hand[0] == max_card_value:
            
            for idx in range(len(values_in_hand) - 3):
                    
                hand_identifer = int((values_in_hand[idx+1] == 3) and(values_in_hand[idx+3] == 0))
                
                if hand_identifer == 1:
                
                    best_hand_values = values_in_hand[0] + values_in_hand[idx+1:idx+5]
                    break
       
        
           
            
        for value in best_hand_values:
                
            final_hand.append((value,suit))
        
        if final_hand == []:
            
            print(best_hand_values, full_hand)
        
        
    #Map the hand_type using characeristics of the hand determined during
    #run time
    hand_type = hand_mapping[(max_value_count, int(max_suit_count>=5), hand_identifer)]    
        
    
    return (hand_type, final_hand)




def winning_set_of_cards(hand1, hand2, set_number):
    
    _set1 = 0
    _set2 = 0
    
    for value in hand1:
        if hand1.count(value) == set_number:
            _set1 = value
    
    for value in hand2:
        if hand2.count(value) == set_number:
            _set2 = value
    
    
    if _set1 > _set2:
        return hand1
    
    elif _set1 < _set2:
        return hand2
    
    else:
        return []
    
    
def winning_two_pair(hand1, hand2):
    
    value1 = 0
    value2 = 0
    
    for value in hand1:
        
        if hand1.count(value) == 2:
        
            value1 = value
            
            break
    
    for value in hand2:
        
        if hand2.count(value) == 2:
        
            value2 = value
            
            break

    if value1 > value2:
        
        return hand1
    
    elif value1 < value2:
        
        return hand2
    
    
    else:
        
        hand1.remove(value1)
        hand1.remove(value1)
        
        hand2.remove(value2)
        hand2.remove(value2)
        
        
        for value in hand1:
            if hand1.count(value) == 2:
                value1 = value
                break
        
        for value in hand2:
            if hand2.count(value) == 2:
                value2 = value
                break
    
        if value1 > value2:
            return hand1
    
        elif value1 < value2:
            return hand2
        
        else:
            return []


def winning_high_card(hand1, hand2):
    
    winner = []
    
    for value1, value2 in zip(hand1, hand2):
       
        if winner == []:
            
            if value1 > value2:
                winner = hand1
            
            elif value1 < value2:
                winner = hand2
    
    return winner

            
def winning_straight(hand1, hand2):
   
    if min(hand1) < min(hand2):
        return hand2
    
    elif min(hand1) > min(hand2):
        return hand1
    
    else:
        return []

    
def winning_flush(hand1, hand2):
    
    if max(hand1) > max(hand2):
        return hand1
    
    elif max(hand1) < max(hand2):
        return hand2
    
    else:
        return []



def showdown(hand1, hand2, board):
    
    winning_hand = [hand1, hand2]
    
 
    def winning_pair(hand1, hand2):
    
        return winning_set_of_cards(hand1, hand2, 2)
    
    
    def winning_triple(hand1, hand2):
        
        return winning_set_of_cards(hand1, hand2, 3)
    
    
    def winning_four(hand1, hand2):
        
        return winning_set_of_cards(hand1, hand2, 4)
    
    
    #The way we compare 2 matching hands depends of the hand type.
    #This dictionary stores the list of comparisons we make based on the 
    #hand type. If all comparisons results in a tie, 
    #then the overall result is a tie
    hand_type_comparisions = {0: [winning_high_card], #High Card
                              1: [winning_pair, winning_high_card], #Pair
                              2: [winning_two_pair, winning_high_card], #2 Pair
                              3: [winning_triple, winning_high_card], #3 of a Kind
                              4: [winning_straight], #Straight
                              5: [winning_flush], #Flush
                              6: [winning_triple, winning_pair], #Full House
                              7: [winning_four, winning_high_card], #4 of a Kind
                              8: [winning_straight]} #Striaght Flush
     
           
    
    hand1_type, best_hand1 = best_hand(hand1, board)
    
    hand2_type, best_hand2 = best_hand(hand2, board)
    
    
    if hand1_type > hand2_type:
        
        winning_hand.remove(hand2)
        
    elif hand1_type < hand2_type:
        
         winning_hand.remove(hand1)
   
    
    else:
        
        hand1_values = []
        
        hand2_values = []
        
        
        for value, suit in best_hand1:
            
            hand1_values.append(value)
            
        for value, suit in best_hand2:
            
            hand2_values.append(value)
            
            
        hand1_values.sort(reverse = True)
        
        hand2_values.sort(reverse = True)
        
        comparisions = hand_type_comparisions[hand1_type]
        
        
        for comparision in comparisions:
            
            winning_hand_values = comparision(hand1_values, hand2_values)
            
            
            if winning_hand_values == hand1_values:
            
                winning_hand.remove(hand2)
                
                break
            
            
            
            elif winning_hand_values == hand2_values:
                
                winning_hand.remove(hand1)
                
                break
            
            else:
                continue
    
        
    if len(winning_hand) == 1:
        return winning_hand[0]
    
    else:
        return winning_hand
