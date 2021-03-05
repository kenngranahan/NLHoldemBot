# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 08:01:29 2021

@author: Kenneth
"""

import yaml


black = (0, 0, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
red = (255, 0, 0)


game_sprites = {
                'table': 'table.jpeg',
                'call': 'widgets/Call(Check).jpeg',
                'fold': 'widgets/Fold.jpeg',
                '2_bet': 'widgets/2 Bet.jpeg',
                '3_bet': 'widgets/3 Bet.jpeg',
                'raise': 'widgets/Raise.jpeg',
                'card_folder': 'custom_cards/',
                'card_file_extension': '.jpeg'
                }


screen = {
          'color': white,
          'size': (1200, 800)
          }


gameplay = {
            'active_player_font': 'Comic Sans MS',
            'active_player_font_size': 12,
            'active_player_font_color': black,
            'active_player_fill_color': white,
            
            'current_player_font': 'Comic Sans MS',
            'current_player_font_size': 12,
            'current_player_font_color': red,
            'current_player_fill_color': white,
            
            'folded_player_font': 'Comic Sans MS',
            'folded_player_font_size': 12,
            'folded_player_font_color': grey,
            'folded_player_fill_color': white,
            
            'pot_font': 'Comic Sans MS', 
            'pot_font_size': 12,
            'pot_font_color': white,
            'pot_fill_color': black,
            
            'text_box_font': 'Comic Sans MS', 
            'text_box_font_size': 12,
            'text_box_font_color': black,
            'text_box_fill_color': grey,
            'text_box_center': (200, 300),
            'text_box_size': (300, 100)
            }



ticket = {
                'player_font': 'Comic Sans MS', 
                'player_font_size': 12,
                'player_font_color': white,
                'player_fill_color': grey,
                
                'position_font': 'Comic Sans MS', 
                'position_font_size': 12,
                'position_font_color': white,
                'position_fill_color': grey,
                
                'stack_font': 'Comic Sans MS', 
                'stack_font_size': 12,
                'stack_font_color': white,
                'stack_fill_color': grey,
                
                'status_font': 'Comic Sans MS', 
                'status_font_size': 12,
                'status_font_color': white,
                'status_fill_color': grey,
                }


config = {
          'game_sprites': game_sprites,
          'screen': screen,
          'ticket': ticket,
          'gameplay': gameplay
          }

file = open('config/default/config.yaml', 'w')
yaml.dump(config, file)

file = open('config/default/config.yaml', 'r')
test = yaml.load(file, Loader = yaml.Loader)
print(test)