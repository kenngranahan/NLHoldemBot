from NLHoldemEngine import NLHoldemEngine
from NLHoldemGUI import holdem_table, widget, card, text_input_box, player_ticket

import pygame, sys

from pygame.locals import *

import yaml

pygame.init()


with open('config/default/config.yaml') as file:
    
    config = yaml.load(file, Loader = yaml.FullLoader)


players = ['player1', 'player2']

buyins = [200, 200]


card_scale = 0.1

table_scale = 0.4


  
screen_color = config['screen']['color']

screen_size = config['screen']['size']

screen_width, screen_height = screen_size



active_player_fill_color = config['gameplay']['active_player_fill_color']

active_player_font = config['gameplay']['active_player_font']

active_player_font_color = config['gameplay']['active_player_font_color']

active_player_font_size = config['gameplay']['active_player_font_size']



current_player_fill_color = config['gameplay']['current_player_fill_color']

current_player_font = config['gameplay']['current_player_font']

current_player_font_color = config['gameplay']['current_player_font_color']

current_player_font_size = config['gameplay']['current_player_font_size']



folded_player_fill_color = config['gameplay']['folded_player_fill_color']

folded_player_font = config['gameplay']['folded_player_font']

folded_player_font_color = config['gameplay']['folded_player_font_color']

folded_player_font_size = config['gameplay']['folded_player_font_size']



pot_fill_color = config['gameplay']['pot_fill_color']

pot_font = config['gameplay']['pot_font']

pot_font_color = config['gameplay']['pot_font_color']

pot_font_size = config['gameplay']['pot_font_size']



text_box_center = config['gameplay']['text_box_center']

text_box_size = config['gameplay']['text_box_size']

text_box_fill_color = config['gameplay']['text_box_fill_color']

text_box_font = config['gameplay']['text_box_font']

text_box_font_color = config['gameplay']['text_box_font_color']

text_box_font_size = config['gameplay']['text_box_font_size']



ticket_player_fill_color = config['ticket']['player_fill_color']

ticket_player_font_color = config['ticket']['player_font_color']

ticket_player_font = config['ticket']['player_font']

ticket_player_font_size = config['ticket']['player_font_size']



ticket_position_fill_color = config['ticket']['position_fill_color']

ticket_position_font_color = config['ticket']['position_font_color']

ticket_position_font = config['ticket']['position_font']

ticket_position_font_size = config['ticket']['position_font_size']



ticket_stack_fill_color = config['ticket']['stack_fill_color']

ticket_stack_font_color = config['ticket']['stack_font_color']

ticket_stack_font = config['ticket']['stack_font']

ticket_stack_font_size = config['ticket']['stack_font_size']



ticket_status_fill_color = config['ticket']['status_fill_color']

ticket_status_font_color = config['ticket']['status_font_color']

ticket_status_font = config['ticket']['status_font']

ticket_status_font_size = config['ticket']['status_font_size']



ticket_width = screen_width * config['ticket']['ticket_width']

ticket_height = screen_height * config['ticket']['ticket_height']

ticket_spacing = screen_height * config['ticket']['ticket_spacing']

ticket_top_margin = screen_height * config['ticket']['ticket_top_margin']

ticket_left_margin = screen_width * config['ticket']['ticket_left_margin']



ticket_player_font = pygame.font.Font('fonts/' + ticket_player_font + '.ttf', ticket_player_font_size)

ticket_stack_font = pygame.font.Font('fonts/' + ticket_stack_font + '.ttf', ticket_stack_font_size)

ticket_status_font = pygame.font.Font('fonts/' + ticket_status_font + '.ttf', ticket_status_font_size)

ticket_position_font = pygame.font.Font('fonts/' + ticket_position_font + '.ttf', ticket_position_font_size)



pot_font = pygame.font.Font('fonts/' + pot_font + '.ttf', pot_font_size)

active_player_font = pygame.font.Font('fonts/' + active_player_font + '.ttf', active_player_font_size)

current_player_font = pygame.font.Font('fonts/' + current_player_font + '.ttf',current_player_font_size)

folded_player_font = pygame.font.Font('fonts/' + folded_player_font + '.ttf', folded_player_font_size)

text_box_font = pygame.font.Font('fonts/' + text_box_font + '.ttf', text_box_font_size)



player_fill_color = {'active': active_player_fill_color,
                     'current': current_player_fill_color,
                     'folded': folded_player_fill_color}


player_font = {'active': active_player_font,
               'current': current_player_font,
               'folded': folded_player_font}


player_font_color = {'active': active_player_font_color,
                     'current': current_player_font_color,
                     'folded': folded_player_font_color}


ticket_font_color = {'position':ticket_position_font_color,
                     'status': ticket_status_font_color,
                     'stack': ticket_stack_font_color,
                     'player': ticket_player_font_color}


ticket_font = {'position': ticket_position_font,
               'status': ticket_status_font,
               'stack': ticket_stack_font,
               'player': ticket_player_font}


ticket_fill_color = {'position': ticket_position_fill_color,
                     'status': ticket_status_fill_color,
                     'stack': ticket_stack_fill_color,
                     'player': ticket_player_fill_color}


card_folder = config['game_sprites']['card_folder']

card_file_extension = config['game_sprites']['card_file_extension']



call = widget(pygame.image.load(config['game_sprites']['call']), 'C')

fold = widget(pygame.image.load(config['game_sprites']['fold']), 'F')

twobet = widget(pygame.image.load(config['game_sprites']['2_bet']), '2BB')

threebet = widget(pygame.image.load(config['game_sprites']['3_bet']), '3BB')

raise_ = widget(pygame.image.load(config['game_sprites']['raise']), 'R')

widgets = [call, fold, twobet, threebet, raise_]


  

for widget in widgets:
    
    scale_factor = screen_width/widget.get_image().get_width()
    
    widget.rescale(scale_factor/len(widgets))
    
    
widget_width, widget_height = widgets[0].get_image().get_size()
    
for idx, widget in enumerate(widgets):

    widget.recenter((widget_width*(idx + 1/2), widget_height/2))
    


screen = pygame.display.set_mode(screen_size, flags = RESIZABLE)

screen.fill(screen_color)

poker_table = holdem_table(pygame.image.load(config['game_sprites']['table']))

poker_table.recenter(screen.get_rect().center)

screen.blit(poker_table.get_image(), poker_table.get_rect())

pot_rect = poker_table.pot_rect((100, 70), screen.get_rect().center)


text_box = text_input_box(600, 100, 20, 20, text_box_font)


GameEngine = NLHoldemEngine(players = players, buyins = buyins, max_buyin = 400, min_buyin = 50, BB = 2)

community_cards = pygame.sprite.Group()

tickets = {}

player_info = GameEngine.get_player_info()

for idx, position in enumerate(GameEngine.get_positions()):

    
    player = player_info[position]['player']
    
    stack = str(player_info[position]['stack'])
    
    status = str(player_info[position]['stake'])
    
    
    ticket = player_ticket(player, ticket_width, ticket_height, ticket_font, ticket_font_color, ticket_fill_color)
    
    ticket.set_stack(stack)
    
    ticket.set_position(position)
    
    ticket.set_status(status)
    
    
    ticket.recenter(ticket_left_margin + ticket_width, ticket_top_margin + (ticket_spacing + ticket_height/2)*(1 + idx))
    
    tickets[player] = ticket




running = True

screen_resizing = False


hands_have_not_been_dealt = True

play_selected_was_valid = True

play_selected = None

deal_community_cards = False

showdown = False

winner_decided = False

position_to_end_the_round_of_betting = 'SB'


while running:
    
    
    for event in pygame.event.get():
         
        if event.type == pygame.QUIT:
            
            running = False
            
            pygame.quit()
        
        elif event.type == VIDEORESIZE:
            
            screen_resizing = True
            
            screen_size = event.dict['size']
            
            
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            for widget in widgets:
                
                if widget.clicked(pygame.mouse.get_pos()):
                    
                    play_selected = widget.get_binding()
                    
                    if play_selected == 'R':
                    
                        text_box.set_active(True)
        
                        text_box.read_text(event)
                        
                      

    if hands_have_not_been_dealt:
        
        hands_have_not_been_dealt = False
        
        GameEngine.pay_in_blinds_and_deal()
        
        player_info = GameEngine.get_player_info()
                
        hand_dealt_sprites = {}


        for idx, position in enumerate(GameEngine.get_positions()):
            
            hand_dealt = GameEngine.formatted_cards(player_info[position]['hand'])
            
            hand_sprites = pygame.sprite.Group()
        
        
            for card_dealt in hand_dealt:
                
                card_sprite = card(pygame.image.load(card_folder + card_dealt + card_file_extension), 
                                   pygame.image.load(card_folder + 'card_back' + card_file_extension))
                
                card_sprite.rescale(card_scale)
                                
                hand_sprites.add(card_sprite)
        
        
            card_size = hand_sprites.sprites()[0].get_size()            
        
            center0, center1 = poker_table.hand_centers(idx, card_size)
        
            hand_sprites.sprites()[0].recenter(center0)
            
            hand_sprites.sprites()[1].recenter(center1)
        
            hand_dealt_sprites[position] = hand_sprites               
        
    
    if play_selected is not(None):
        
        GameEngine.set_play(play_selected)
        
        play_selected = None
        
        play_selected_was_valid = GameEngine.update_game_and_move_to_next_active_position()
    
        
        if play_selected_was_valid:
            
            if GameEngine.get_current_play() == 'R':
                
                position_to_end_the_round_of_betting = GameEngine.get_position_who_raised()
            
            
            elif GameEngine.all_folded():
                
                GameEngine.pay_out_winner_and_reset_table()
                
            elif GameEngine.get_current_position() == position_to_end_the_round_of_betting:
                
                GameEngine.end_round_of_betting()
                
                if len(community_cards) != 5:
                    
                    deal_community_cards = True
                
                else:
                
                    showdown = True
            
    
    if deal_community_cards:
        
        deal_community_cards = False
        
        if len(community_cards) == 0:
            
            GameEngine.deal_flop()
            
            cards_dealt = GameEngine.get_flop()
                 
            cards_dealt = GameEngine.formatted_cards(cards_dealt)
        
            
            for card_dealt in cards_dealt:
                    
                    card_sprite = card(pygame.image.load(card_folder + card_dealt + card_file_extension), 
                                       pygame.image.load(card_folder + 'card_back' + card_file_extension), hidden = False)
                    
                    card_sprite.rescale(card_scale)
                                    
                    community_cards.add(card_sprite)
            
            
            card_size = community_cards.sprites()[0].get_size()            
            
            center0, center1, center2 = poker_table.flop_center(card_size)
        
                
            community_cards.sprites()[0].recenter(center0)
            
            community_cards.sprites()[1].recenter(center1)
        
            community_cards.sprites()[2].recenter(center2)
        
 
        elif len(community_cards) == 3:
            
            GameEngine.deal_turn()
            
            cards_dealt = GameEngine.get_turn()
            
            cards_dealt = GameEngine.formatted_cards(cards_dealt)
        
            for card_dealt in cards_dealt:
                    
                card_sprite = card(pygame.image.load(card_folder + card_dealt + card_file_extension), 
                                   pygame.image.load(card_folder + 'card_back' + card_file_extension), hidden = False)
                
            card_sprite.rescale(card_scale)
                            
            community_cards.add(card_sprite)
    
            card_size = community_cards.sprites()[0].get_size()            
            
            center = poker_table.turn_center(card_size)
        
            community_cards.sprites()[3].recenter(center)

        
        else:
            
            GameEngine.deal_river()
            
            cards_dealt = GameEngine.get_river()
            
            cards_dealt = GameEngine.formatted_cards(cards_dealt)
        
            for card_dealt in cards_dealt:
                
                card_sprite = card(pygame.image.load(card_folder + card_dealt + card_file_extension), 
                                   pygame.image.load(card_folder + 'card_back' + card_file_extension), hidden = False)
                
            card_sprite.rescale(card_scale)
                            
            community_cards.add(card_sprite)
    
            card_size = community_cards.sprites()[0].get_size()            
            
            center = poker_table.river_center(card_size)
        
            community_cards.sprites()[4].recenter(center)



    if winner_decided:
        
        winner_decided = False
        
        GameEngine.pay_out_winner_and_reset_table()
        


    if showdown:
        
        showdown = False
        
        GameEngine.showdown()
        
        for position in GameEngine.get_positions():
            
            if not(GameEngine.has_folded(position)):
                
                for card_sprite in hand_dealt_sprites[position]:
                    
                    card_sprite.flip()

        winner_decided = True
    


        
    if not(screen_resizing):
        
        
        screen.fill(screen_color)
        
        screen.blit(poker_table.get_image(), poker_table.get_rect())
        
        screen.blit(poker_table.pot_image(str(GameEngine.get_pot()), (100, 50), pot_font, pot_font_color, pot_fill_color), 
                    pot_rect)
        
        for idx, position in enumerate(GameEngine.get_positions()):
            
            
            player = GameEngine.get_player(position)
            
            player_rect = poker_table.player_title_rect(idx, card_size)
            
            
            if position == GameEngine.get_current_position():
                
                player_status = 'current'
            
            elif GameEngine.has_folded(position):
                
                player_status = 'folded'   
                
            else:
                
                player_status = 'active'
            
            
            if winner_decided:
                
                if position in GameEngine.get_showdown_winners():
                    
                    player_status = 'current'
                
        
            fill_color = player_fill_color[player_status]
            
            font = player_font[player_status]
            
            font_color = player_font_color[player_status]
        
            
            player_name = font.render(player, True, font_color, fill_color)
            
            screen.blit(player_name, player_rect)
        
        
        for position in GameEngine.get_positions():
            
            hand_dealt_sprites[position].draw(screen)
                
             
        for widget in widgets:
            
            screen.blit(widget.get_image(), widget.get_rect())
        
        
        
        player_info = GameEngine.get_player_info()
        
        for position in GameEngine.get_positions():
            
            
            player = player_info[position]['player']
    
            stack = str(player_info[position]['stack'])
    
            status = str(player_info[position]['stake'])
    
    
            ticket = tickets[player]        
    
            ticket.set_stack(stack)
    
            ticket.set_position(position)
    
            ticket.set_status(status)
    
            
            screen.blit(ticket.get_player_surface(), ticket.get_player_rect())
            
            screen.blit(ticket.get_position_surface(), ticket.get_position_rect())
            
            screen.blit(ticket.get_status_surface(), ticket.get_status_rect())
            
            screen.blit(ticket.get_stack_surface(), ticket.get_stack_rect())
        
        
        if text_box.is_active():
            
            screen.blit(text_box.render_text(), text_box.get_rect())
        
        
        if len(community_cards) != 0:
            
            community_cards.draw(screen)
        
        
        pygame.display.flip()
    



    else:
        
        
        screen_resizing = False
        
        
        screen = pygame.display.set_mode(screen_size, flags = RESIZABLE)
        
        screen.fill(screen_color)
        
        screen_width, screen_height = screen.get_size()
        
        
        poker_table.recenter(screen.get_rect().center)
         
        pot_rect = poker_table.pot_rect((100, 70), screen.get_rect().center)
         
        
        
        ticket_width = screen_width * config['ticket']['ticket_width']

        ticket_height = screen_height * config['ticket']['ticket_height']

        ticket_spacing = screen_height * config['ticket']['ticket_spacing']

        ticket_top_margin = screen_height * config['ticket']['ticket_top_margin']

        ticket_left_margin = screen_width * config['ticket']['ticket_left_margin']

        for idx, key in enumerate(tickets.keys()):

            tickets[key].recenter(ticket_left_margin + ticket_width, ticket_top_margin + (ticket_spacing + ticket_height/2)*(1 + idx))
                                  
        
                                  
        for widget in widgets:
    
            scale_factor = screen_width/widget.get_image().get_width()
            
            widget.rescale(scale_factor/len(widgets))
            
        widget_width, widget_height = widgets[0].get_image().get_size()
            
        for idx, widget in enumerate(widgets):
        
            widget.recenter((widget_width*(idx + 1/2), widget_height/2))


        for idx, position in enumerate(GameEngine.get_positions()):
                  
            card_size = hand_sprites.sprites()[0].get_size()            
        
            center0, center1 = poker_table.hand_centers(idx, card_size)
        
            hand_dealt_sprites[position].sprites()[0].recenter(center0)
            
            hand_dealt_sprites[position].sprites()[1].recenter(center1)
        


        if len(community_cards) >= 3:
            
            card_size = community_cards.sprites()[0].get_size()            
            
            center0, center1, center2 = poker_table.flop_center(card_size)
        
                
            community_cards.sprites()[0].recenter(center0)
            
            community_cards.sprites()[1].recenter(center1)
        
            community_cards.sprites()[2].recenter(center2)
        
 
            if len(community_cards) >= 4:
            
                center = poker_table.turn_center(card_size)
            
                community_cards.sprites()[3].recenter(center)

        
            if len(community_cards) == 5:
                
                center = poker_table.river_center(card_size)
            
                community_cards.sprites()[4].recenter(center)
                
                
