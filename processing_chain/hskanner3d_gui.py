# Purpose
#   This script controls the generation and filtering of 2D as well as 3D data, offering an easy to use graphical user interface. For that, it uses the class and methods defined in hskanner3d_script.py, and though it, all the other scripts.
####
# Usage
#   python3.7 hskanner3d_gui.py
# this script has no additional arguments.
# It is recommended to run the GUI from a terminal, since all the (debug) output is displayed there.

#!/usr/bin/env python
import tkinter as tk
from tkinter import *
from tkinter import ttk
from hskanner3d_script import *
import configparser
from time import sleep


class hska3d_gui:
    def __init__(self):
        # this constructor does the gui layout
        padx_setting = 5
        pady_setting = 5
        stick_labels = E    # stick labels to > east, < west (E, W)
        stick_entry = W
        stick_task_buttons = W
        entry_width = 40

        # main window
        root = tk.Tk()
        program_title = "HSkanner3D control"
        root.title(program_title)

        # add tabs
        tabControl = ttk.Notebook(root)
        tab_tasks = ttk.Frame(tabControl)
        tab_settings = ttk.Frame(tabControl)
        tabControl.add(tab_tasks, text ='Tasks')
        tabControl.add(tab_settings, text ='Settings') 

        # tasks tab content
        cc = 0 # column counter
        rr = 0 # row counter
        btn_single_cap_hq = Button(tab_tasks, text = 'Single Capture (2D + 3D, high quality)', command = self.single_capture_hq).grid(column = cc, row = rr, padx = padx_setting, pady = pady_setting, sticky = stick_task_buttons)
        rr += 1
        btn_single_cap_fast = Button(tab_tasks, text = 'Single Capture (2D + 3D, faster processing)', command = self.single_capture_fast).grid(column = cc, row = rr, padx = padx_setting, pady = pady_setting, sticky = stick_task_buttons)
        rr += 1
        btn_image_cap = Button(tab_tasks, text = 'Only capture images', command = self.image_capture).grid(column = cc, row = rr, padx = padx_setting, pady = pady_setting, sticky = stick_task_buttons)
        rr += 1
        btn_program_quit = Button(tab_tasks, text = 'Close ' + program_title, command = root.destroy).grid(column = cc, row = rr, padx = padx_setting, pady = pady_setting, sticky = stick_task_buttons)
        
        # settings tab content
        tabControl.pack(expand = 1, fill ="both") 
        cc = 0 # column counter
        rr = 0 # row counter

        # arrays for saving config data
        self.entry_field_array = []
        self.key_array = [] # array that contains variable names ('keys')

        # load config to get number and names of variables to open up to the gui to configure
        self.load_config_from_file()
        for key in self.config_obj["custom"]:   # for every variable defined under the [custom] block in the config file, do this:
            # create text label (consisting of variable name)
            ttk.Label(tab_settings, text = key).grid(column = cc, row = rr, padx = padx_setting, pady = pady_setting, sticky = stick_labels)
            # create entry box for variable and arrange it on the grid
            entry_field = Text(tab_settings, wrap = WORD, height = 1, width = entry_width)
            entry_field.grid(column = cc+1, row = rr, padx = padx_setting, pady = pady_setting, sticky = stick_entry)
            # append current textlabel and entry fields to their arrays
            self.entry_field_array.append(entry_field)
            self.key_array.append(key)
            # advance row by one
            rr += 1
        self.number_variables = rr
        
        # fill input fields with last custom config from file
        self.load_custom()
        
        # loading and saving buttons
        btn_load_default = Button(tab_settings, text = 'Load defaults', command = self.load_defaults).grid(column = cc, row = rr, padx = padx_setting, pady = pady_setting)
        btn_check_save_settings = Button(tab_settings, text = 'Check and Save Settings', command = self.save_custom).grid(column = cc+1, row = rr, padx = padx_setting, pady = pady_setting)
        rr +=1
        
        # feedback box
        ttk.Label(tab_settings, text ="Errors,\nWarnings,\nFeedback->").grid(column = cc, row = rr, padx = padx_setting, pady = pady_setting, sticky = stick_labels)
        self.settings_output = Text(tab_settings, wrap = WORD, height = 5, width = entry_width)
        self.settings_output.grid(column = cc+1, row = rr, padx = padx_setting, pady = pady_setting, sticky = stick_entry)

        # init scanner and start GUI
        self.init_scanning_interface()

        root.mainloop()
    
    # functions for file I/O
    def check_type(self, string_under_test):
        # typecast will throw an exception if you try to typecast a str (that is not a number) to int. Same with other data types.
        try:
            int(string_under_test)
            return "Integer"
        except:
            try:
                float(string_under_test)
                return "Float"
            except:
                return "String"       

    def load_config_from_file(self):
        workpath = path[0]  # get absolute path of script
        self.config_obj = configparser.ConfigParser()
        self.config_obj.read(workpath + "/hskanner3d.config")

    def write_config_to_textboxes(self, default_or_custom):
        for nn in range(self.number_variables):
            self.entry_field_array[nn].delete(0.0, END) # clear entry fields
            self.entry_field_array[nn].insert(END, self.config_obj[default_or_custom][self.key_array[nn]]) # fill them with the contents of the variables

    def write_textboxes_to_config(self, default_or_custom):
        self.settings_output.delete(0.0, END)
        self.error_count = 0
        for nn in range(self.number_variables):
            textbox_type = self.check_type(self.entry_field_array[nn].get(0.0, END))
            config_type = self.check_type(self.config_obj[default_or_custom][self.key_array[nn]])
            if textbox_type == config_type:
                self.config_obj[default_or_custom][self.key_array[nn]] = self.entry_field_array[nn].get(0.0, END) 
            else:
                self.error_count += 1
                self.entry_field_array[nn].delete(0.0, END)
                self.settings_output.insert(END, "Variable \'" + self.key_array[nn] + "\' not applicable. It should be of type \'" + config_type + "\'.\n")

        if self.error_count == 0:
            self.settings_output.insert(END, "Successfully saved variables. Note that only the types (Integer, Float and String) are checked.")    

    def save_config_to_file(self):
        workpath = path[0]  # get absolute path of script
        with open(workpath + "/hskanner3d.config", 'w') as configfile:
            self.config_obj.write(configfile)

    def load_defaults(self):
        self.write_config_to_textboxes("default")
        self.save_custom()

    def load_custom(self):
        self.load_config_from_file()
        self.write_config_to_textboxes("custom")

    def save_custom(self):
        self.write_textboxes_to_config("custom")
        self.save_config_to_file()
        if self.error_count == 0:
            self.hs.apply_settings()
            self.hs = hska3d()

    # functions for scanning. Due to how Tk buttons work, you can't pass values to your function when a button is pressed, you can only call the function like this: 'function()'.
    def init_scanning_interface(self):
        self.hs = hska3d()
        self.hs.apply_settings()

    def single_capture_hq(self):
        self.hs = hska3d()
        self.hs.run("hq")

    def single_capture_fast(self):
        self.hs = hska3d()
        self.hs.run("fast")

    def image_capture(self):
        self.hs = hska3d()
        self.hs.gen_2d()

def main():
    hs_gui = hska3d_gui()

if __name__ == "__main__":
    main()

    


