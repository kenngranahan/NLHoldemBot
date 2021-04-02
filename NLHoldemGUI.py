#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 18:00:58 2020

@author: kenneth
"""
import pygame, sys
from pygame.locals import *


class card(pygame.sprite.Sprite):
    """
    Class used to reprsent card sprites
    
    Methods
    ----------------
    rescale(scale_factor) : None
        rescales the card size. the aspect ration is preserved
        
    flip() : None
        the card image is flipped
    
    recenter((x, y)) : None
        recenter the card on (x, y)
    
    get_image() : Surface
        gets the image of the card. This is either the card front or card back depending depending if  hidden == True.
        Call the flip() method to change
    
    is_hidden() : bool
        returns a bool, depending if the card is hidden or not
        
    get_size() : (width, height)
        returns the size of the card
    
    """    
    def __init__(self, front_image, back_image, hidden = True):
        pygame.sprite.Sprite.__init__(self)
        
        self.card_front = front_image
        self.card_back = back_image
        self.card_size = self.card_front.get_size()
        self.rect = self.card_front.get_rect()
        
        self.width, self.height =  self.card_size
      
    
        self.hidden = hidden
        
        if self.hidden:
            self.image = self.card_back
        else:
            self.image = self.card_front
  
    
    def rescale(self, scale_factor):
        self.width *=  scale_factor 
        self.height *=  scale_factor
        
        self.card_size = (int(self.width), int(self.height))
        self.card_front = pygame.transform.scale(self.card_front, self.card_size)
        self.card_back = pygame.transform.scale(self.card_back, self.card_size)
        self.image =  pygame.transform.scale(self.image, self.card_size)
        
        self.rect = self.card_front.get_rect()
        
        
    def flip(self):
        
        if self.hidden:
            self.image = self.card_front
            self.hidden = False
        
        else:
            self.image = self.card_back
            self.hidden = True
        
            
    def recenter(self,  pos):
        self.rect.center = pos
        
    def get_image(self):
        return self.image
    
    def is_hidden(self):
        return self.hidden

    def get_size(self):
        return self.card_size



class holdem_table(pygame.sprite.Sprite):
    """
    A class to represent of table for No Limit Texas Holdem. This class also repreents where players are seated at the table 
    and where cards are dealt to.
    
    Methods
    -----------------
    
    get_image() : Surface
        returns the image of the poker table
    
    get_rect() : Rect
        returns the rect of the poker table
        
    hand_centers(hand_number, card_size) : ((x0, y0), (x1, y1))
        returns the center of both cards held by the player sitting at the position indexed by hand_number
        
    player_title_rect(hand_number, card_size) : Rect
        returns a rect for drawing the player's name sitting at the position indexed by hand_number
    
    pot_rect(size) : Rect
        returns a Rect for drawing the pot
        
    pot_image(self, pot, size, font, font_color, fill_color) : Surface
        returns the pot image
       
    flop_center() : ((x0, y0), (x1, y1), (x2, y2))
        returns the centers for the flop
    
    turn_center() : (x0, y0)
        returns the center for the turn
        
    river_center() : (x0, y0)
        returns the center for the turn
     
    rescale(scale) : None
        rescales the poder table, preserves the aspect ratio 
    
    recenter((x, y)) : None
        recenters the table on (x, y)
            
    
    """
    
    
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.size =  self.image.get_size()
        (self.width, self.height) = self.size
        
        self.card_spacing = self.rect.width/200
        self.xhand = [self.rect.width*0.65/2, self.rect.width/2, 
                      self.rect.width*0.65/2, -self.rect.width*0.65/2, 
                      -self.rect.width/2, -self.rect.width*0.65/2]
        
        self.yhand = [-self.rect.height/2, 0, self.rect.height/2, 
                      self.rect.height/2, 0, -self.rect.height/2]
    
    
    def get_rect(self):
        return self.rect
    
    def get_image(self):
        return self.image
    
    def hand_centers(self, hand_number, card_size):
        
        x, y = self.rect.center 
        
        x = x + self.xhand[hand_number]
        y = y + self.yhand[hand_number]
        
        width , _ = card_size
        
        offset = (width + self.card_spacing)/2
        
        if hand_number == 1:
            center1 = (x + offset + width, y)
            center2 = (x - offset + width, y)
        
        elif hand_number == 4:
            center1 = (x + offset - width, y)
            center2 = (x - offset - width, y)
            
        else:  
            center1 = (x + offset, y)
            center2 = (x - offset, y)
            
        return center1, center2
     
        
    def player_title_rect(self, hand_number, card_size):
        (x1, y1), (x2, y2) = self.hand_centers(hand_number, card_size)
        
        x = (x1 + x2)/2
        w, h = card_size
        
        rect =  pygame.Rect(x-self.card_spacing/2 - w, y1 - 3*h/2 - self.card_spacing + w, x1 + x2 + self.card_spacing, w)
        
        return rect
    
    def player_hand_rect(self, hand_number, card_size):
        
        title_rect = self.player_title_rect(hand_number, card_size)
        
        width, height = title_rect.size
        
        x, y = title_rect.center
        
        rect =  pygame.Rect(x - width/2, y - 3*height/2 -self.card_spacing, x + width/2, y - 5*height/2 - self.card_spacing)
        
        return rect
     
        
    def pot_image(self, pot, size, font, font_color, fill_color):
        
        w, h = size
        
        pot_surface = pygame.Surface((w, h))
        
        pygame.Surface.fill(pot_surface, fill_color)
        
        pot_characters = font.render(pot, True, font_color, fill_color)
        
        pot_surface.blit(pot_characters, pot_characters.get_rect())
        
        return pot_surface
        
    
    def pot_rect(self, size, center):
        
        w, h = size
        
        rect = pygame.Rect(0, 0, w, h)
        
        rect.center = center
        
        return rect    
        
    
    def flop_center(self, card_size):
        x, y = self.rect.center 
        width, _ = card_size
        
        center1 = (x - (self.card_spacing+width)*2, y)
        center2 = (x - (self.card_spacing+width), y)
        center3 = (x , y)
        
        return center1, center2, center3
    
    def turn_center(self, card_size):
        x, y = self.rect.center 
        width, _ = card_size
        return (x + (self.card_spacing+width), y)


    def river_center(self, card_size):        
        x, y = self.rect.center 
        width, _ = card_size
        return (x + (self.card_spacing+width)*2, y)
    
   
    def rescale(self, scale_factor):
        self.width *=  scale_factor
        self.height *=  scale_factor
        
        self.size = (int(self.width), int(self.height))
        self.image = pygame.transform.scale(self.image, self.size)
        
        self.rect = self.image.get_rect()
    
    def recenter(self, pos):
        self.rect.center = pos
        


class widget(pygame.sprite.Sprite):
    
    """
    A class used to represent a widget.
    
    
    Methods
    ----------------------------
    
    rescale(scale_factor) : None 
        rescales the widget, preserves the aspect ratio
    
    recenter((x, y)) : None
        recenters the widget on (x, y)
    
    clicked(mouse_pos) : bool
        returns True if the mouse clicked on the widget
    
    get_binding() :  str
        returns the str binding to the widget
        
    get_image() : Surface
        returns the image of the widget
    
    """
    
    def __init__(self, image, binding = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        
        self.width , self.height = self.size
   
        self.binding = binding    
    
        
    def rescale(self, scale_factor):
    
        self.width *=  scale_factor 
        self.height *=  scale_factor
        
        self.size = (int(self.width), int(self.height))
        
        self.image = pygame.transform.scale(self.image, self.size)
         
        self.rect = self.image.get_rect()
        
    def recenter(self, pos):
        self.rect.center = pos
        
    
    def clicked(self, mouse_pos):
        centerx, centery = self.rect.center
        mousex, mousey = mouse_pos
        
        if (abs(mousex - centerx) <= self.width/2) and (abs(mousey - centery) <= self.height/2):
            return True
        else:
            return False
    
    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect

    def get_binding(self):
        return self.binding


class text_input_box(pygame.sprite.Sprite):
    
    """
    A Class used to represent a text box used to read string inputs from the user
    
    Methods
    ---------------
    
    read_text(event) : None
        reads text from the user based on the pygame.event module
        
    render_text() : Surface
        renders the text on a surface
    
    clear_text() : None
        clears the text stored in the text box
    
    get_text() : str
        returns the text stored on the text box
    
    rescale(scale_factor) : None 
        rescales the widget, preserves the aspect ratio
    
    recenter((x, y)) : None
        recenters the widget on (x, y)
        
   is_active() :  bool
       returns True if th etext box is active
        
    
   set_active(active): None
        set the text box as active         
    
    
    
    """
    
    
    def __init__(self, xcenter, ycenter, w, h, font, text_color = (0,0,0), background_color = (255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        
        self.center = (xcenter, ycenter)
        self.width = w
        self.height = h
        self.font = font
        self.text = ''
        self.text_color = text_color
        self.background_color = background_color
        self.active = False
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (xcenter, ycenter)
        
        
    def read_text(self, event):
    
        if (event.type == MOUSEBUTTONDOWN) and not(self.active):
            
            self.active = self.rect.collidepoint(event.pos)
            
    
        if (event.type == KEYDOWN) and self.active:
            
            if event.key == K_RETURN:
                
                self.active = False
                
            elif event.key == K_BACKSPACE:
                
                self.text = self.text[:-1]
                
            else:
                
                self.text += event.unicode
            
                
    def render_text(self):
        
        
        text_box_surface = pygame.Surface((self.width, self.height))
        
        text_box_surface.fill(self.background_color)
    
        if self.text != '':
        
            text_box_characters = self.font.render(self.text, True, self.text_color, self.background_color)
            
            text_box_surface.blit(text_box_characters, text_box_surface.get_rect())
       
        
        return text_box_surface
        

        
    def clear_text(self):
        self.text = ''
        
    def get_text(self):
        return self.text
        
        
    def rescale(self, scale_factor):
        
        self.width *=  scale_factor 
        self.height *=  scale_factor
        
        self.size = (int(self.width), int(self.height))
        self.image = pygame.transform.scale(self.image, self.size)
        
        self.rect = self.image.get_rect()
        
    def recenter(self, pos):
        self.rect.center = pos
        
    def is_active(self):
        return self.active
    
    def set_active(self, active):
        self.active = active
        
    def get_rect(self):
        return self.rect
        
        
        
        
class player_ticket(pygame.sprite.Group):
    """
    A Class for displaying player information
    
    Methods
    ---------------
    
    set_position(position) : None
        set the position to be displayed on the ticket
        
    set_stack(stack) : None
        set the stack to be displayed on the ticket
        
    set_status(starus) : None
        set the status to be displayed on the ticket
    
    recenter((xcenter, ycenter)) : None
        recenter the ticket
    
    draw(surface) : None
        draw the ticket onto the surface
    
    
    """
    
    
    def __init__(self, player_name, w, h, fonts, text_colors, background_colors):
        pygame.sprite.Group.__init__(self)
        
        
        self.fonts = fonts
        self.text_colors = text_colors
        self.background_colors = background_colors
        self.player_name = player_name
        
        
        self.width = int(w)
        self.height = int(h)
        
        
        self.position_surface = pygame.Surface((self.width, int(self.height/2)))
        self.player_surface = pygame.Surface((self.width, int(self.height/2)))
        self.stack_surface = pygame.Surface((int(1.1*self.width), int(0.45*self.height)))
        self.status_surface = pygame.Surface((int(1.1*self.width), int(0.45*self.height)))
        
        pygame.Surface.fill(self.position_surface, self.background_colors['position'])
        pygame.Surface.fill(self.player_surface, self.background_colors['player'])
        pygame.Surface.fill(self.stack_surface, self.background_colors['stack'])
        pygame.Surface.fill(self.status_surface, self.background_colors['status'])
        
        
        self.position_rect = self.position_surface.get_rect()
        self.player_rect = self.player_surface.get_rect()
        self.stack_rect = self.stack_surface.get_rect()
        self.status_rect = self.status_surface.get_rect()
    
        
        self.player_characters = self.fonts['player'].render(self.player_name, True, self.text_colors['player'], self.background_colors['player'])
        self.position_characters = None
        self.stack_characters = None
        self.status_characters = None
        
        self.player_surface.blit(self.player_characters, self.player_surface.get_rect())
        
    def set_position(self, position):
         
        pygame.Surface.fill(self.position_surface, self.background_colors['position'])
        
        self.position_characters = self.fonts['position'].render(position, True, self.text_colors['position'], self.background_colors['position'])

        self.position_surface.blit(self.position_characters, self.position_surface.get_rect())
        
        
    def set_stack(self, stack):
        
        pygame.Surface.fill(self.stack_surface, self.background_colors['stack'])
        
        self.stack_characters = self.fonts['stack'].render(stack, True, self.text_colors['stack'], self.background_colors['stack'])
        
        self.stack_surface.blit(self.stack_characters, self.stack_surface.get_rect())
    
    
    def set_status(self, status):
        
        pygame.Surface.fill(self.status_surface, self.background_colors['status'])
        
        self.status_characters = self.fonts['status'].render(status, True, self.text_colors['status'], self.background_colors['status'])
        
        self.status_surface.blit(self.status_characters, self.status_surface.get_rect())
        
        
        
    def recenter(self, xcenter, ycenter):
        
        self.position_rect.center = (xcenter - self.width/2, ycenter-self.height/4)
        
        self.player_rect.center = (xcenter - self.width/2, ycenter + self.height/4)
        
        self.stack_rect.center = (xcenter + 1.1*self.width/2, ycenter - 0.45*self.height/2)
        
        self.status_rect.center = (xcenter + 1.1*self.width/2, ycenter + 0.45*self.height/2)
        
        
        
    
    def get_player_surface(self):
        return self.player_surface
    
    def get_player_rect(self):
        return self.player_rect
    
    
    def get_position_surface(self):
        return self.position_surface
    
    def get_position_rect(self):
        return self.position_rect
    
    
    def get_stack_surface(self):
        return self.stack_surface
    
    def get_stack_rect(self):
        return self.stack_rect
    
    
    def get_status_surface(self):
        return self.status_surface
    
    def get_status_rect(self):
        return self.status_rect
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        