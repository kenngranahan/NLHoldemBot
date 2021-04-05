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
                'table': 'table/table.jpeg',
                'call': 'widgets/Call(Check).jpeg',
                'fold': 'widgets/Fold.jpeg',
                '2_bet': 'widgets/2 Bet.jpeg',
                '3_bet': 'widgets/3 Bet.jpeg',
                'raise': 'widgets/Raise.jpeg',
                'card_folder': 'custom_cards/',
                'card_file_extension': '.jpeg',
                'card_scale': 0.1,
                'table_scale': 0.4,
                }


screen = {
          'color': white,
          'size': (1200, 800)
          }


gameplay = {
            'active_player_font': 'comic',
            'active_player_font_size': 12,
            'active_player_font_color': black,
            'active_player_fill_color': white,
            
            'current_player_font': 'comic',
            'current_player_font_size': 12,
            'current_player_font_color': red,
            'current_player_fill_color': white,
            
            'folded_player_font': 'comic',
            'folded_player_font_size': 12,
            'folded_player_font_color': grey,
            'folded_player_fill_color': white,
            
            'pot_font': 'comic', 
            'pot_font_size': 12,
            'pot_font_color': white,
            'pot_fill_color': black,
            'pot_top_margin': 0.42,
            'pot_left_margin':0.50,
            'pot_width': 0.1,
            'pot_height': 0.04,
            
            'text_box_font': 'comic', 
            'text_box_font_size': 12,
            'text_box_font_color': black,
            'text_box_fill_color': grey,
            'text_box_top_margin': 0.2,
            'text_box_left_margin': 0.3,
            'text_box_width': 0.2,
            'text_box_height': 0.1,
            }



ticket = {
                'player_font': 'comic', 
                'player_font_size': 12,
                'player_font_color': black,
                'player_fill_color': grey,
                
                'position_font': 'comic', 
                'position_font_size': 12,
                'position_font_color': black,
                'position_fill_color': grey,
                
                'stack_font': 'comic', 
                'stack_font_size': 12,
                'stack_font_color': black,
                'stack_fill_color': red,
                
                'status_font': 'comic', 
                'status_font_size': 12,
                'status_font_color': black,
                'status_fill_color': red,
                
                
                'ticket_width': 0.06,
                'ticket_height': 0.08,
                'ticket_spacing': 0.05,
                'ticket_top_margin': 0.1,
                'ticket_left_margin': 0.0125,
                
                }


config = {
          'game_sprites': game_sprites,
          'screen': screen,
          'ticket': ticket,
          'gameplay': gameplay
          }

file = open('default/config.yaml', 'w')
yaml.dump(config, file)

file = open('default/config.yaml', 'r')
test = yaml.load(file, Loader = yaml.Loader)
