# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 16:32:33 2021

@author: Kenneth
"""


class Opponent_V1():
    
    def __init__(self):
    
    self.number_of_opponent_features = 6

    self.number_of_observed_plays = 0
    
    self.number_of_folds = 0
    
    self.number_of_calls = 0
    
    self.average_call = 0
    
    self.number_of_raises = 0
    
    self.average_raise = 0

    self.number_of_checks = 0
    
    
    if self.number_of_observed_plays != 0:
        
        self.opponent_features = [self.number_of_folds / self.number_of_observed_plays,
                                  self.number_of_calls / self.number_of_observed_plays,
                                  self.number_of_raises / self.number_of_observed_plays,
                                  self.number_of_checks / self.number_of_observed_plays,
                                  self.average_call,
                                  self.average_raise]
    
    else:
        
        self.opponent_features = [0]*self.number_of_features

   
    def observe_play(self, play, amount):
        
        
        if play == 'R':
             
            self.average_raise*self.number_of_raises += amount
            
            self.number_of_raises += 1
           
            self.average_raise /= self.number_of_raises 
           
            
        elif play == 'F':
            
            self.number_of_folds += 1
        
        
        elif (play == 'C') and (amount != 0) :
            
            self.average_call*self.number_of_calls += amount
            
            self.number_of_calls += 1
            
            self.average_call /= self.number_of_calls 
            
            
        elif play == 'C':
            
            self.number_of_checks += 1
            
            
        self.number_of_observed_plays += 1
        
        
        
    def update_features(self):
        
        if self.number_of_observed_plays != 0:
        
            self.opponent_features = [self.number_of_folds / self.number_of_observed_plays,
                                      self.number_of_calls / self.number_of_observed_plays,
                                      self.number_of_raises / self.number_of_observed_plays,
                                      self.number_of_checks / self.number_of_observed_plays,
                                      self.average_call,
                                      self.average_raise]
        
        else:
        
            self.opponent_features = [0]*self.number_of_features
        
    
   
    def get_features(self):
        return self.features
        
        
        