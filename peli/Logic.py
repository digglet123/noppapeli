'''
Created on Apr 10, 2016

@author: mikko
'''
import random
import datetime

class Logic:
    
    def __init__(self):
        self.init_success = True
        self.initialize_dice() 
        self.guess = None
        self.results = (0,0)
    
    #Initialize random generator   
    def initialize_dice(self):
        try:
            random.seed(datetime.datetime.now())
        except:
            random.seed(1)
            self.init_success = False
            
    #Cast the dice and store values
    def cast_dice(self):
        self.results = ((random.randint(1, 6)), (random.randint(1, 6)))
    
    #Add dice results
    def add_result(self):
        return self.results[0] + self.results[1]       
    
    #Check if a quess is a valid integer
    def is_valid_guess(self):
        try:
            int(self.guess)
            return True
        except:
            return False    
            
    #Set current guess
    def set_guess(self, text):
        self.guess = int(text)
        
    #Check if current guess is right
    def check_guess(self):
        if(self.guess == self.add_result()):
            return True
        else:
            return False