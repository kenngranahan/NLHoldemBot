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



card_folder = config['game_sprites']['card_folder']

card_file_extension = config['game_sprites']['card_file_extension']


    
call = widget(pygame.image.load(config['game_sprites']['call']), 'C')

fold = widget(pygame.image.load(config['game_sprites']['fold']), 'F')

twobet = widget(pygame.image.load(config['game_sprites']['2_bet']), '2BB')

threebet = widget(pygame.image.load(config['game_sprites']['3_bet']), '3BB')

_raise = widget(pygame.image.load(config['game_sprites']['raise']), 'R')

widgets = [call, fold, twobet, threebet, _raise]


    
screen_color = config['screen']['color']

screen_size = config['screen']['size']



screen = pygame.display.set_mode(screen_size, flags = RESIZABLE)

screen.fill(screen_color)

poker_table = holdem_table(pygame.image.load(config['game_sprites']['table']))

poker_table.recenter(screen.get_rect().center)

screen.blit(poker_table.get_image(), poker_table.get_rect())



GameEngine = NLHoldemEngine(players = players, buyins = buyins, max_buyin = 400, min_buyin = 50, BB = 2)

running = True

hands_have_not_been_dealt = True

screen_updating = False

while running:
    
    for event in pygame.event.get():
         
        if event.type == pygame.QUIT:
            pygame.quit()


    if hands_have_not_been_dealt:
        
        hands_have_not_been_dealt = False
        
        GameEngine.pay_in_blinds_and_deal()
        
        player_info = GameEngine.get_player_info()
                
        hands_dealt_sprite = {}

        for idx, position in enumerate(GameEngine.get_positions()):
        
            
            hand_dealt = player_info[position]['hand']
            
            sprites = pygame.sprite.Group()
            
            center0, center1 = poker_table.hand_centers(idx, card_size)
        
            for card_dealt in hand_dealt:
                
                card_sprite = card(pygame.image.load(card_folder+card_dealt+card_file_extension), 
                                   pygame.image.load(card_folder + 'card_back' + card_file_extension))
                
                sprites.add(card_sprite)
        
            
            hands_dealt_sprites[position] = sprites                
        
        
        
    if not(screen_updating()):
        
        
        for position in GameEngine.get_positions():
            
            hands_dealt_sprites[position].draw()
                
                
            
        
    pygame.display.flip()










