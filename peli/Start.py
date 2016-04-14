# coding=UTF-8
'''
Created on Apr 13, 2016

@author: mikko
'''
from Logic import Logic
from Gui import Gui

#Creates game logic and starts game
def main():
    game = Logic()
    Gui(game)
main()