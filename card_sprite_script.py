# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 15:40:16 2021

@author: Kenneth
"""

from PIL import ImageFont, ImageDraw, Image

white = (250,250,250)
black = (0, 0, 0)
red = (220, 20, 60)

aspect_ratio = 60/90
height = 330
font_size = 100
font_file = 'C:\Windows\Fonts\Arial.ttf'

make_card_front = False
make_card_back = False
make_buttons = True

card_size = (int(height*aspect_ratio), height)
blank_card = Image.new(mode = 'RGB', size = card_size, color=white)
draw = ImageDraw.Draw(blank_card, mode = 'RGB')

draw.line([(0, 0), (0, height)], fill = black)
draw.line([(0, 0), (int(height*aspect_ratio)-1, 0)], fill = black)
draw.line([(int(height*aspect_ratio)-1, 0), (int(height*aspect_ratio)-1, height)], fill = black)
draw.line([(int(height*aspect_ratio)-1, height-1), (0, height-1)], fill = black)


button_height = 100
button_width = 300
button_size = (button_width, button_height)
blank_button = Image.new(mode = 'RGB', size = button_size, color=white)

draw.line([(0, 0), (0, button_height-1)], fill = black)
draw.line([(0, 0), (button_width-1, 0)], fill = black)
draw.line([(button_width-1, 0), (button_width-1, button_height-1)], fill = black)
draw.line([(button_width-1, button_height-1), (0, button_height-1)], fill = black)



if make_card_front:
    
    font = ImageFont.truetype(font_file, size =100)
    blank_card_copy = blank_card.copy()
    draw_copy = ImageDraw.Draw(blank_card_copy, mode = 'RGB')
    
    suit_colors = {'h': red, 'd': red, 'c': black, 's':black}
    
    for i in list(range(9)):
        for key in suit_colors.keys():    
            
            text = str(i+2) + key
            text_width, text_height = font.getsize(text)
            
            draw_copy.text((height*aspect_ratio/2-text_width/2, height/2 - text_height/2), 
                           text, font = font, fill = suit_colors[key], anchor = 'mm')
    
            blank_card_copy.save('custom_cards/' + text +'.jpeg')
            
            blank_card_copy = blank_card.copy()
            draw_copy = ImageDraw.Draw(blank_card_copy, mode = 'RGB')
      
            
    for picture in ['J', 'Q', 'K', 'A']:
        for key in suit_colors.keys():    
            
            text = picture + key
            text_width, text_height = font.getsize(text)
            
            draw_copy.text((height*aspect_ratio/2-text_width/2, height/2 - text_height/2), 
                           text, font = font, fill = suit_colors[key], anchor = 'mm')
    
            blank_card_copy.save('custom_cards/' + text +'.jpeg')
            
            blank_card_copy = blank_card.copy()
            draw_copy = ImageDraw.Draw(blank_card_copy, mode = 'RGB')
        
if make_card_back:
    
    checkerboard_size = 10
    
    number_of_height_squares = int(height/checkerboard_size)
    number_of_width_squares = int(height*aspect_ratio/checkerboard_size)
    
    for i in range(number_of_height_squares):
        for j in range(number_of_width_squares):
            if (i % 2 == j % 2):
                color = red
            else:
                color = black
            draw.rectangle([(j*checkerboard_size, i*checkerboard_size), ((j+1)*checkerboard_size, (i+1)*checkerboard_size)],
                           fill = color)
    
    
    blank_card.save('custom_cards/card_back.jpeg')
    
    
    
if make_buttons:
    
    font = ImageFont.truetype(font_file, size =50)
    blank_button_copy = blank_button.copy()
    draw_copy = ImageDraw.Draw(blank_button_copy, mode = 'RGB')
    
    texts = ['Fold', 'Call(Check)',  '2 Bet', '3 Bet', 'Raise']
    
    for text in texts:
        
        text_width, text_height = font.getsize(text)
        
        draw_copy.text((button_width/2-text_width/2, button_height/2 - text_height/2), 
                       text, font = font, fill = black, anchor = 'mm')

        blank_button_copy.save('widgets/' + text +'.jpeg')
        
        blank_button_copy = blank_button.copy()
        draw_copy = ImageDraw.Draw(blank_button_copy, mode = 'RGB')
  
   