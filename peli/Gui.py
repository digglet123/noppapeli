# coding=UTF-8
'''
Created on Apr 10, 2016

@author: mikko
'''
import tkinter as tk
import tkinter.messagebox

class Gui():
        
    def __init__(self, logic):
        self.game = logic
        self.anim_frame = 1
        self.ui_lock = False
        self.play_animation = False
        
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.resizable(0, 0)
        self.root.title("Noppapeli")
        self.create_widgets()
        self.update()
        self.root.mainloop()
        
    def create_widgets(self):
        #Create Menubar
        self.menubar = tk.Menu(self.root)
        self.menubar.add_command(label="Poistu", command=self.root.quit)
        self.menubar.add_command(label="Ohje", command=self.show_help)
        
        self.root.config(menu=self.menubar)
        self.root.configure(bg = "#a3a3a3")
        
        #Create Frame-objects to contain all other widgets
        self.top_frame = tk.Frame(self.root, bg = "#a3a3a3")
        self.top_frame.pack()
        
        self.frame = tk.Frame(self.root, bg = "#a3a3a3")
        self.frame.pack()
        
        self.bottom_frame = tk.Frame(self.root, bg = "#a3a3a3")
        self.bottom_frame.pack()
        
        #Top frame widgets
        self.text_label = tk.Label(self.top_frame, pady = 50, padx = 10, font = ("Helvetica", 20), fg = "blue", text = "Arvauksesi:", bg = "#a3a3a3")
        self.text_label.pack(side = "left")
        
        self.error_img = tk.PhotoImage(file = "error.png")
        self.ok_img = tk.PhotoImage(file = "ok.png")
        self.indicator = tk.Label(self.top_frame, image = self.error_img, bg = "#a3a3a3")
        self.indicator.pack(side = "right")
        
        self.input_text = tk.Entry(self.top_frame, width = 2, font = ("Helvetica", 20))
        self.input_text.pack(side = "right")
        
        #Create a PhotoImage-object for every frame in the gif file
        self.sequence_array = []
        for i in range (0,25):
            self.sequence_array.append(tk.PhotoImage(file = "dice_roll.gif", format = "gif -index %i" %i))
        
        #Create PhotoImage-objects for still images
        self.still_array = []
        for i in range (1,7):
            self.still_array.append(tk.PhotoImage(file = "dice_%i.png" %i))
        
        #Middle frame widgets
        self.dice_l = tk.Label(self.frame, image = self.sequence_array[0], bg = "#a3a3a3")
        self.dice_l.pack(side = "left")
        
        self.dice_r = tk.Label(self.frame, image = self.sequence_array[0], bg = "#a3a3a3")
        self.dice_r.pack(side = "right")
        
        #Bottom frame widgets
        self.cast_button = tk.Button(self.bottom_frame, text = "Heitä nopat", font = ("Helvetica", 20), fg = "blue", command = self.call_command)
        self.cast_button.pack(side = "top")
        
        #Pop up information windows
        self.root.after(500, self.show_help)
            
    #Method for checking if the random generator was initialized correctly    
    def check_dice_init(self):
        if(not self.game.init_success):
            tkinter.messagebox.showwarning("Virhe", "Järjestelmän aikaan perustuva nopan alustaminen epäonnistui.\nSiirrytään käyttämään vakio-arvoa")
    
    #Method for showing help pop up window
    def show_help(self):
        tkinter.messagebox.showinfo("info", "Yritä arvata noppien silmälukujen yhteenlaskettu tulos ja heitä nopat.")
        self.check_dice_init() 
    
    #Method for retrieving text from the input field
    def retrieve_input(self):
        retrieved = self.input_text.get()
        return retrieved
    
    #Method for showing right message after dices have been cast 
    def show_message(self):
        result = self.game.add_result()
        resultString = "Tulos oli %i. " % result
        if(self.game.check_guess()):
            tkinter.messagebox.showinfo("info", resultString + "Arvauksesi oli OIKEIN!")
        else:
            tkinter.messagebox.showinfo("info",  resultString + "Arvauksesi oli VÄÄRIN.")
        self.enable_ui()
        self.play_animation = False
        self.anim_frame = 1
    
    #Method for handling cast dice button events 
    def call_command(self):
        self.disable_ui()
        self.game.cast_dice()
        self.play_animation = True
        self.root.after(2000, self.show_message)
       
    #Method for disabling UI elements 
    def disable_ui(self):
        self.ui_lock = True
        self.input_text.configure(state = "disabled")
        self.input_text.configure(bg = "light gray")
        self.cast_button.configure(state = "disabled")
    
    #Method for enabling UI elements
    def enable_ui(self):
        self.ui_lock = False
        self.input_text.configure(state = "normal")
        self.input_text.configure(bg = "white")
        self.cast_button.configure(state = "normal")
           
    #Method for changing dice images       
    def animate(self):
        if(self.anim_frame < 23):
            self.anim_frame += 1
            self.dice_l.configure(image = self.sequence_array[self.anim_frame]) 
            self.dice_r.configure(image = self.sequence_array[self.anim_frame])
        else:
            dice_left_value = self.game.results[0]
            dice_right_value = self.game.results[1]
            self.dice_l.configure(image = self.still_array[dice_left_value - 1])
            self.dice_r.configure(image = self.still_array[dice_right_value - 1])
                               
    def update(self):
        #Update current gif animation frame and set it visible
        if(self.play_animation):
            self.animate()  
        
        #Delete excess characters
        self.input_text.delete(2, "end") 
        
        #Try to set input field value as guess and give indication symbol to user
        if(not self.ui_lock):
            try:
                self.game.set_guess(self.retrieve_input())
                self.cast_button.configure(state = "normal")
                self.indicator.configure(image = self.ok_img)
            except:
                self.cast_button.configure(state = "disabled")
                self.indicator.configure(image = self.error_img)
            
        self.root.after(40, self.update)