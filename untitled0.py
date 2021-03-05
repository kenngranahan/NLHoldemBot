from NLHoldemEngine import HLHoldemEngine
from NLHoldemGUI import holdem_table, widget, card, text_input_box, player_ticket

import pygame, sys

import yaml

pygame.init()


with open('config/default/config.yaml') as file:
    
    config = yaml.load(file, Loader = yaml.FullLoader)

    
    
screen_color = config['screen']['color']

screen_size = config['screen']['size']



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



card_folder = config['gameplay']['card_folder']

card_file_extension = config['gameplay']['card_file_extension']



screen = pygame.display.set_mode(screen_size, flags = pygame.RESIZEABLE)

    
call = widget(pygame.image.load(config['game_sprites']['call']), 'C')

fold = widget(pygame.image.load(config['game_sprites']['fold']), 'F')

2_bet = widget(pygame.image.load(config['game_sprites']['2_bet']), '2BB')

3_bet = widget(pygame.image.load(config['game_sprites']['3_bet']), '3BB')

_raise = widget(pygame.image.load(config['game_sprites']['raise']), 'R')

poker_table = holdem_table(pygame.image.load(config['game_sprites']['table']))





















