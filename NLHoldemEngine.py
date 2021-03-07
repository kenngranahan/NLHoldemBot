from itertools import cycle
from random import shuffle
import copy

class NLHoldemEngine:
    """
    A Class used to run a game of No Limit Texas Holdem
    
    The maximum number of supported players is 6
    
    
    Attributes
    ---------------
    
    min_players : int
        The minmimum number of players supported
        
    max_players : int
        The maximum number of players supported
        
    player_order : list
        A list of positions arranged in order of play
    
    deal_order : list
        A list of positions arranged in the order to be dealt
    
    position : list
        The list of positions. this has been ordered such that slicing returns
        the correct positions, e.g. positions[:3] gives the positions for a 3 player game
        
    plays : list
        The plays available to a player during their turn, only 6 plays are implemented
        'C' -> Call/Check
        'F' -> Fold
        'A' -> All In
        '2BB' -> Bet 2 * Big Blind
        '3BB' -> Bet 3 * Big Blind
        'R' -> Raise some other amount
    
    hand_type : dict
        A dict that maps integer ranks to different hands. 
    
    max_rank : int
        The maximum hand rank. In a standard 52 card deck this is 12
        
        
        
    Methods
    
    ----------------
    
    deal(number_of_cards) :  list
        deals number_of_cards and returns them as a list
        
    deal_flop() : None
        deals the flop
    
    deal_turn() : None
        deals the turn
        
    deal_river() : None
        deals the river
  
    get_flop() : list
        returns the formatted flop cards 
        
    get_turn() : list
        returns the formatted turn cards 
    
    get_river() : list
        returns the formatted river cards
        
    reset_deck() : None
        reset self.deck
        
    format_cards(cards) : list
        returns a list of formatted cards e.g. (0, 0) returns '2h' 
        
        
    
    
    get_current_position() : str
        returns the current position
    
    set_current_position(position) : None
        set the current postion to position
        
    get_positions() : list
        returns a list of positions in the game
    
    get_player(position) : str
        get the name of the player in position
        
    get_players() : list
        return the list of players in the game
    
    
    get_player_info() : dict
        return a dict of dicts that stores the player information
    
    
    
               
    get_position_who_raised() : str
        return the postion who raised. If no one has raise then is returns 'BB'
    
    get_amount_to_call() : float
        returns the amount to needed to call. This does not include the amount already paid in by the current position
    
    all_folded() : bool
        returns True if all of the players have folded
        
    get_pot() : float
        returns the pot size
    
    get_BB() : float
        returns the big blind
    
    get_SB(): float
        returns the small blind
        
        
        
        
    pay_in_blinds_and_deal() : None
        pay in the blinds and deal pocket cards to each player. This should be called to start a new game
  
    pay_out_winner_and_reset_table() : None
        pay out to the winner and reset the table. This is called at the end of the game after a player has won
    
    set_play(play) : None
        used to input the play made by the current player. The list of possible plays can be found in the .plays class 
        attribute
    
    set_raise(amount_raised) : None
        used to input the amount raised if the palyer chose raise as their play
            
    update_game_and_move_to_next_active_position() : bool
        this is called after the current player has submitted their play. This method checks if the play submitted is valid.
        If so, then the game state is updated. Returns True/False if the game state was update successfully.
    
    end_round_of_betting() : None
        This method is called when the round of betting is over
    
    
    
    
    best_hand(position) : (int, list)
        returns the best 5 card hand of the player sitting in position. Returns a tuple of an int encoding the type of hand
        and a list of cards in the best 5 card hand. The integers used to encode the hand type are corresponds to the mapping
        given in the .hand_type class attribute
    
    get_best_hand(position) : list
        returns the best formatted 5 card hand held by the player sitting in position 
    
    winning_set_of_cards(hand1, hand2, set_number) : list
        Returns the hand with the winning set. Returns [] if it's a tie
    
    winning_two_pair(hand1, hand2) : list
        Returns the hand with the winning two pair. Returns [] if it's a tie
    
    winning_high_card(hand1, hand2) : list
        Returns the hand with the winning high card. Returns [] if it's a tie
    
    winning_straight(hand1, hand2): list
       Returns the hand with the winning high card. Returns [] if it's a tie
    
    winning_flush(hand1, hand2): list
        Returns the hand with the winning high card. Returns [] if it's a tie
    
    showdown() : None
        Determines the winner if the game goes to showdown
    
    get_showdown_winner() : list / str
        returns the best formatted 5 card hand held by the showdowns winner. If the result is a split pot then a list of winners
        is returned
    
    """
    min_players = 2    
    max_players = 6

    play_order = ['UTG','MP','CO', 'D', 'SB','BB']
    deal_order = ['SB','BB', 'UTG','MP','CO', 'D']
    
  
    positions = ['BB', 'SB', 'D', 'UTG','CO', 'MP']
    
    
 
    plays = ['C', 'F', 'A', '2BB', '3BB', 'R']
    
    
    #This maps integers to different hand types so that comparing different has is easier
    hand_type = {0: 'High Card', 1: 'Pair', 2: 'Two Pair', 3: 'Three of a Kind',
                 4: 'Straight', 5: 'Flush', 6: 'Full House', 7: 'Four of a Kind',
                 8: 'Straight Flush'}

    max_rank = 12
    
    def __init__(self, players, buyins, max_buyin, min_buyin, BB, SB = None):
        


        
        #Assign the player names, stacks and deck
        self.player_names = players
        self.stacks = buyins
        self.max_buyin = max_buyin
        self.min_buyin = min_buyin
        
        #Encode the deck as a list of tuples
        self.deck_ranks = range(NLHoldemEngine.max_rank+1)
        self.deck_suits = range(4)
        self.deck = [(rank, suit) for rank in self.deck_ranks for suit in self.deck_suits]
        
        
        self.rank_mapping = {}
        for rank in self.deck_ranks:
            self.rank_mapping[rank] = str(rank+2)
        
        self.rank_mapping[NLHoldemEngine.max_rank] = 'A'
        self.rank_mapping[NLHoldemEngine.max_rank-1] = 'K'
        self.rank_mapping[NLHoldemEngine.max_rank-2] = 'Q'
        self.rank_mapping[NLHoldemEngine.max_rank-3] = 'J'
        
    
        self.suit_mapping = {0: 'd', 1: 'h', 2: 'c', 3: 's'}    
    
        #Assign the positions according to the number of players
        self.positions = NLHoldemEngine.positions[:len(players)]
        
        #Initalize the blinds
        self.BB = BB
        if SB is None:
            SB = BB/2
        self.SB = SB
        
        
        #Initalize other attributes that get updated after every hand/play
        self.pot = 0
        self.showdown_winner = []
        
        self.position_who_raised = 'BB'
        self.amount_to_call = self.BB
        
        self.current_position = 'BB'
        self.current_play = ''
        self.rotation_of_play = [pos for pos in NLHoldemEngine.play_order if pos in self.positions]
        self.rotation_iter = cycle(iter(self.rotation_of_play))
            
        self.flop = []
        self.turn = []
        self.river = []


        # A dict of dicts which stores the player information. 
        # The structure is {'position': dict()} where dict() is
        # {'stack': float,   the player's current chip stack 
        # 'player': string,  the player's name
        # 'hand': list,      the player's pocket hand
        # 'stake': float,    the amount the player has payed into the pot this round
        # 'in play': bool}   bool to flag if a player has folded
        
        self.table = {}
        for position, stack, player in zip(self.positions,self.stacks,self.player_names):
            self.table[position] = {'stack': stack, 'player': player,\
                                  'hand': [], 'stake': 0, 'in play': True}
        
        #This dictionary maps the amount paid into the pot based
        #on the play made. amount_paid['C'] and amount_paid['A']
        #get updated after each play in the update_game_state() method
        self.amount_paid = {'C': self.amount_to_call - self.table[self.current_position]['stake'],
                            'F': 0,
                            'A': self.table[self.current_position]['stack'],
                            '2BB': self.BB * 2,
                            '3BB': self.BB * 3,
                            'R': 0}



    #Methods for cards
    def deal(self, number_of_cards):
        
        if number_of_cards < len(self.deck):
            
            cards_drawn = self.deck[:number_of_cards]
        
            self.deck = self.deck[number_of_cards:]
            
        else:
            
            cards_drawn = self.deck
            
            self.deck = []
            
        return cards_drawn
        
    
    def deal_flop(self):
       self.flop = self.deal(3)
    
    
    def deal_turn(self):
        self.turn = self.deal(1)
    
    
    def deal_river(self):
        self.river = self.deal(1)
    
        
    def reset_deck(self):
        self.deck = shuffle([(rank, suit) for rank in self.deck_ranks for suit in self.deck_suits])   
        
        
    def formatted_cards(self, cards):
        
        formatted_cards = []
        
        if cards != []:    
        
            for card in cards:
            
                rank, suit = card
                
                formatted_card = self.rank_mapping[rank] + self.suit_mapping[suit]
                
                formatted_cards.append(formatted_card)
            
        return formatted_cards
    
    
    def get_flop(self):
        return self.formatted_cards(self.flop)
    
    def get_turn(self):
        return self.formatted_cards(self.turn)
    
    def get_river(self):
        return self.formatted_cards(self.river)
       
            
       
        
       
    def get_player_info(self):
    
        dict_deepcopy = copy.deepcopy(self.table)
        
        for key in self.table.keys():
        
            dict_deepcopy[key]['hand'] = self.formatted_cards(self.table[key]['hand'])
        
        return dict_deepcopy        


    def get_positions(self):
        return self.positions
        
    def get_position_who_raised(self):
        return self.position_who_raised
    
    def get_amount_to_call(self):
        return self.amount_to_call
    
    def get_current_position(self):
        return self.current_position
    
    def set_current_position(self, position):
        self.current_position = position
        while next(self.rotation_iter) != position:
            continue
    
    def get_player(self, position):
        player = self.table[position]['player']
        return player
    
    def get_players(self):
        return self.players   
  
    
    def all_folded(self):

        total = 0

        for pos in self.positions:

            total += self.table[pos]['in play']

        return (total == 1)        
  

    def get_pot(self):
        return self.pot
    
    def get_BB(self):
        return self.BB
    
    def get_SB(self):
        return self.SB
  


    

    def pay_in_blinds_and_deal(self):

        shuffle(self.deck)

        self.pot = self.BB + self.SB


        self.table['BB']['stack'] -= self.BB

        self.table['BB']['stake'] += self.BB

        
        self.table['SB']['stack'] -= self.SB

        self.table['SB']['stake'] += self.SB
        

        for pos in NLHoldemEngine.deal_order:

            if pos in self.positions:

                self.table[pos]['hand'] = self.deal(2)


        self.current_position = next(self.rotation_iter)


        
    def pay_out_winner_and_reset_table(self):
        
        for winner in self.showdown_winner:

            self.table[winner]['stack'] += self.pot/len(self.showdown_winner)

    
        for pos in self.positions:
    
            self.table[pos]['hand'] = []
            
            self.table[pos]['stake'] = 0
            
            self.table[pos]['in play'] = True
            
            
        self.pot = 0
       
        self.position_who_raised = 'BB'
        
        self.amount_to_call = self.BB
        
        self.current_play = ''
        
        self.showdown_winner = []
        
        
        self.flop = []
        
        self.turn = []
        
        self.river = []
        
        
        self.reset_deck()
        
        
  
        tmp_dict = self.table[self.rotation_of_play[0]]
        
        for idx, pos in enumerate(self.rotation_of_play[:-1]):
        
            self.table[pos] = self.table[self.rotation_of_play[idx+1]]
        
        self.table[self.rotation_of_play[-1]] = tmp_dict
        
        


    def set_play(self, play):
        self.current_play = play

        
    def set_raise(self, amount_raised):
        if self.current_play == 'R':
            self.amount_paid[self.current_play] = amount_raised
        

    
    def update_game_and_move_to_next_active_position(self):
        
        
        self.amount_paid['C'] = self.amount_to_call - self.table[self.current_position]['stake']
        
        self.amount_paid['A'] = self.table[self.current_position]['stack']
        
        
        
        bet_placed = self.amount_paid[self.current_play]

        
        if self.current_play == 'R':

            if bet_placed < self.amount_to_call - self.table[self.current_position]['stake']:

                return False
            
            
        if bet_placed > self.table[self.current_position]['stack']:
            return False
        
        else:
                  
            #Check if the player has raised, if so update the amount to call 
            if bet_placed > self.amount_to_call:

                self.amount_to_call += bet_placed

                self.position_who_raised = self.current_position
        
        
                    
            self.pot += bet_placed

            self.table[self.current_position]['stake'] += bet_placed

            self.table[self.current_position]['stack'] -= bet_placed
        
                
        
            #If a player Folded we need to update their 'in play' flag
            if self.current_play == 'F':

                self.table[self.current_position]['in play'] = False
         
            
         
            self.current_position = next(self.rotation_iter)
    
    
            return True



    def end_round_of_betting(self):
        
        self.amount_to_call = 0
        
        self.amount_paid['C'] = 0
        
        for position in self.positions:
            
            self.table[position]['stake'] = 0
            
            
        self.current_position = 'SB'
      
        for position in self.rotation_iter:
            if position == self.current_position:
                break
                
                
        
       
    def best_hand(self, player_pos):
        #Different hand types are encoded using 
        #(max_rank_count, (max_suit_count>=5), hand_identifier)
        #where:
        
        #max_rank_count is the highest number of matching ranks in a hand,
        #(max_suit_count>=5) is a boolean for if the number of matching suits is >= 5
        #hand_identifier is a condition used to distinguish 2 hands where max_rank_count
        #and (max_suit_count>=5) can't.
        
        #e.g. a hand with max_rank_count==2 and (max_suit_count>=5) == False 
        #is either a pair or 2 pair. hand_identifier == 0 and hand_identifier == 1
        #distinguishes these two cases respectively.
        
        hand_mapping = {(1, 0, 0): 0, #high card 
                        (2, 0, 0): 1, #pair
                        (2, 0, 1): 2, #2 pair
                        (3, 0, 0): 3, #3 of a kind
                        (1, 0, 1): 4, #straight
                        (1, 1, 0): 5, #flush
                        (3, 0, 1): 6, #full house
                        (4, 0, 1): 7, #4 of a kind
                        (1, 1, 1): 8} #straight flush
        
        if player_pos in self.positions:
            
            #Initalize some variables
            final_hand = []
            best_hand_ranks = []
            max_rank_count = 1
            max_suit_count = 2
            hand_identifer = 0
            max_rank = NLHoldemEngine.max_rank
            
            #Read in the full 7 card hand
            full_hand = self.table[player_pos]['hand'] + self.flop \
                        + self.turn + self.river
            
            suits_in_hand = []
            ranks_in_hand = []
            
            for card in full_hand:
            
                rank, suit = card
                
                ranks_in_hand.append(rank)
                
                suits_in_hand.append(suit)
            
            
            #Count how many of each suit is in the full hand. Take the maximum
            #suit count
            suit_count = [suits_in_hand.count(suit) for suit in self.deck_suits]
            max_suit_count = max(suit_count)            
            
            
            
            
            if max_suit_count < 5:
                
                #Create a list of numbers [12,.., ] sorted descending
                decending_number_list = list(max_rank+1)
                decending_number_list.reverse()
                
                #Create a list of card ranks(e.g. 'J' has a rank of 11) sorted 
                #in descending order. Then count how many of each rank we have. 
                #Take the maximum count
                ranks_in_hand.sort(reverse = True)
                rank_count = [ranks_in_hand.count(number) for number in decending_number_list]
                max_rank_count = max(rank_count)
                
                
                #This is a handy function internal to this method. It returns
                #the first set (pair, 3 of a kind, 4 of a kind) found in the hand.
                #Since this has been sorted in descending order, the first set has
                #the highest rank
                def find_set(rank_count, set_number):
                    
                    number = max_rank - rank_count.index(set_number)
                    
                    return [number]*set_number
                
                #This function is internal to this method. It returns a list of
                #ranks to complete our hand (Ace high, King high, etc.)
                def find_kickers(full_hand, cards_used, number_of_kickers):
                    
                    kickers = []
                    
                    for card in full_hand[:5]:    
                    
                        if len(kickers)== number_of_kickers:
                            break
                        
                        elif (card not in cards_used):
                            kickers.append(card)
                    
                    return kickers
  
                
                #Here we check all combinations of pairs, 3 of a kind and 4 of a kind  
                if max_rank_count <= 4:
                    
                    best_hand_ranks = find_set(rank_count, max_rank_count)
                    
                    
                    if max_rank_count == 3:
                        
                        hand_identifer = int(2 in rank_count)
                        
                        if hand_identifer == 1:
                            best_hand_ranks = best_hand_ranks + find_set(rank_count, 2)
                    
                    elif max_rank_count == 2:
                        
                        idx = max_rank - best_hand_ranks[0]
                        
                        if idx < (len(rank_count)- 1):
                            
                            hand_identifer = int(2 in rank_count[idx+1:])
                            
                            if hand_identifer == 1:
                                
                                second_idx = rank_count[idx+1:].index(2)
                                
                                full_idx = second_idx + idx + 1
                                
                                best_hand_ranks = best_hand_ranks + ([max_rank - full_idx]*2)
                    
                    #Add any kickers to complete the hand(if needed)
                    best_hand_ranks = best_hand_ranks + find_kickers(ranks_in_hand, best_hand_ranks, 5-len(best_hand_ranks))
                
                
                #Here we check for straight and high card
                else:
                    
                    best_hand_ranks = ranks_in_hand[:5]
                    
                    
                    for idx in range(len(ranks_in_hand) - 4):
                        
                        hand_identifer = int(ranks_in_hand[idx] == (ranks_in_hand[idx+4] + 4))
                        
                        if hand_identifer == 1:
                        
                            best_hand_ranks = ranks_in_hand[idx:idx+5]
                            break
                    
                    #This is a special case where we check [A,5,4,3,2]
                    if ranks_in_hand[0] == max_rank:
                        
                        for idx in range(len(ranks_in_hand) - 3):
                        
                            hand_identifer = int((ranks_in_hand[idx+1] == 3) and(ranks_in_hand[idx+3] == 0))
                            
                            if hand_identifer == 1:
                            
                                best_hand_ranks = ranks_in_hand[0] + ranks_in_hand[idx+1:idx+5]
                                break
                            
                                
                        
                
                
                #If we've reached here, then we have prepared a hand.
                #So now we need to assign the correct 
                #suit to each card to get the final_hand
                unique_list = []
                
                for rank in best_hand_ranks:
                
                    if rank not in unique_list:
                    
                        unique_list.append(rank)
                
                for rank in unique_list:
                    
                    suits = [s for (v, s) in full_hand if v==rank]
                    
                    cards = [(rank, s) for s in suits]
                    
                    final_hand = final_hand + cards
    
    
    
            #If we're executing this code block, then we have >= 5 cards with the
            #same suit, i.e. we have a straight flush or a flush
            else:
                
                
                #Find out the matching suit, then pick out all the cards
                #with this suit. Then map these cards to their ranks
                suit = self.deck_suits[suit_count.index(max(suit_count))]
                
                ranks_in_hand = [v for (v, s) in full_hand if s == suit]
                
                ranks_in_hand.sort(reverse = True)
            
        
                best_hand_ranks = ranks_in_hand[:5]
                    
                    
                for idx in range(len(ranks_in_hand) - 4):
                    
                    hand_identifer = int(ranks_in_hand[idx] == (ranks_in_hand[idx+4] + 4))
                    
                    if hand_identifer == 1:
                    
                        best_hand_ranks = ranks_in_hand[idx:idx+5]
                        break
                
                #This is a special case where we check [A,5,4,3,2]
                if ranks_in_hand[0] == max_rank:
                    
                    for idx in range(len(ranks_in_hand) - 3):
                    
                        hand_identifer = int((ranks_in_hand[idx+1] == 3) and(ranks_in_hand[idx+3] == 0))
                        
                        if hand_identifer == 1:
                        
                            best_hand_ranks = ranks_in_hand[0] + ranks_in_hand[idx+1:idx+5]
                            break
                        

                
                #If we've reached here, then we have prepared a hand.
                #So now we need to assign the correct 
                #suit to each card to get the final_hand
                unique_list = []
                
                for rank in best_hand_ranks:
                
                    if rank not in unique_list:
                    
                        unique_list.append(rank)
                
                
                for rank in unique_list:
                    
                    final_hand.append((rank,suit))
                    

                
            #Map the hand_type using characeristics of the hand determined during
            #run time
            hand_type = hand_mapping[(max_rank_count, max_suit_count>=5, hand_identifer)]    
            
            #Done
            return (hand_type, final_hand)
        
        #Return this if player argument passed fails the check 
        else:    
            return (-1, [])
    
    
    def winning_set_of_cards(self, hand1, hand2, set_number):
        
        _set1 = 0
        _set2 = 0
        
        for rank in hand1:
            if hand1.count(rank) == set_number:
                _set1 = rank
        
        for rank in hand2:
            if hand2.count(rank) == set_number:
                _set2 = rank
        
        
        if _set1 > _set2:
            return hand1
        
        elif _set1 < _set2:
            return hand2
        
        else:
            return []
        
        
    def winning_two_pair(self, hand1, hand2):
        
        rank1 = 0
        rank2 = 0
        
        for rank in hand1:
            if hand1.count(rank) == 2:
                rank1 = rank
                break
        
        for rank in hand2:
            if hand2.count(rank) == 2:
                rank2 = rank
                break

        if rank1 > rank2:
            return hand1
        
        elif rank1 < rank2:
            return hand2
        
        else:
            
            hand1.remove(rank1)
            hand1.remove(rank1)
            
            hand2.remove(rank2)
            hand2.remove(rank2)
            
            
            for rank in hand1:
                if hand1.count(rank) == 2:
                    rank1 = rank
                    break
            
            for rank in hand2:
                if hand2.count(rank) == 2:
                    rank2 = rank
                    break
        
            if rank1 > rank2:
                return hand1
        
            elif rank1 < rank2:
                return hand2
            
            else:
                return []

    def winning_high_card(self, hand1, hand2):
        
        winner = []
        
        for rank1, rank2 in zip(hand1, hand2):
           
            if winner == []:
                
                if rank1 > rank2:
                    winner = hand1
                
                elif rank1 < rank2:
                    winner = hand2
        
        return winner
                
    def winning_straight(self, hand1, hand2):
       
        if min(hand1) < min(hand2):
            return hand2
        
        elif min(hand1) > min(hand2):
            return hand1
        
        else:
            return []
        
    def winning_flush(self, hand1, hand2):
        
        if max(hand1) > max(hand2):
            return hand1
        
        elif max(hand1) < max(hand2):
            return hand2
        
        else:
            return []

    def showdown(self):
        
        best_hand_type = ''
        
        positions = [position for position in self.positions if self.table[position]['in play'] == True]
        
        
        def winning_pair(hand1, hand2):
        
            return self.winning_set_of_cards(hand1, hand2, 2)
        
        
        def winning_triple(hand1, hand2):
            
            return self.winning_set_of_cards(hand1, hand2, 3)
        
        
        def winning_four(hand1, hand2):
            
            return self.winning_set_of_cards(hand1, hand2, 4)
        
        
        #The way we compare 2 matching hands depends of the hand type.
        #This dictionary stores the list of comparisons we make based on the 
        #hand type. If all comparisons results in a tie, 
        #then the overall result is a tie
        hand_type_comparisions = {0: [self.winning_high_card], #High Card
                                  1: [winning_pair, self.winning_high_card], #Pair
                                  2: [self.winning_two_pair, self.winning_high_card], #2 Pair
                                  3: [winning_triple, self.winning_high_card], #3 of a Kind
                                  4: [self.winning_straight], #Straight
                                  5: [self.winning_flush], #Flush
                                  6: [winning_triple, winning_pair], #Full House
                                  7: [winning_four, self.winning_high_card], #4 of a Kind
                                  8: [self.winning_straight]} #Striaght Flush
         
               
        for current_position in positions:
            
            current_hand_type, current_hand = self.best_hand(current_position)
            
            current_hand_ranks = []
            
            for (rank, suit) in current_hand:
                
                current_hand_ranks.append(rank)
            
            
            
            if (best_hand_type == '') or (current_hand_type > best_hand_type):
                
                best_hand_type = current_hand_type
                
                best_hand = current_hand
                
                best_hand_ranks = current_hand_ranks
                
                winning_players = [current_position]
                
                best_hand_sorted = False
            
           
            elif best_hand_type == current_hand_type:
                
                
                if best_hand_sorted == False:
           
                    best_hand_ranks.sort(reverse = True)
                    
                    best_hand_sorted = True
            
                    
                current_hand_ranks.sort(reverse = True)
                
                winning_players.append(current_position)
                
                comparisions = hand_type_comparisions[best_hand_type]
                
                
                for comparision in comparisions:
                    
                    winning_hand_ranks = comparision(best_hand_ranks, current_hand_ranks)
                    
                    
                    if winning_hand_ranks == best_hand_ranks:
                    
                        winning_players.remove(current_position)
                        
                        break
                    
                    
                    elif winning_hand_ranks == current_hand_ranks:
                    
                        best_hand_ranks = current_hand_ranks
                        
                        best_hand_sorted = True
                        
                        winning_players = [current_position]
                        
                        break
                    
                    else:
                        continue
                
        self.showdown_winner = winning_players

    def get_best_hand(self, position):
        
        best_hand_type, best_hand = self.best_hand(position)
        
        
        if best_hand_type == -1:
            
            return None, None
        
        
        else:
            
            best_hand_type_mapped = NLHoldemEngine.hand_type[best_hand_type]
            
            formatted_best_hand = self.formatted_cards(best_hand)
        
        
        return best_hand_type_mapped, formatted_best_hand
        
    
    def get_showdown_winner(self):
        return self.showdown_winner
        