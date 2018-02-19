import tkinter as tk
from tkinter import Entry, StringVar

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_buttons()

    def create_buttons(self):
        '''
        self.billings = tk.Button(self, 
            bd="3",
            cursor="hand",
            text="Facturación",
            height="10",
            width='20'
        ).pack(side='left', expand=200)
        '''
        self.inventory = tk.Button(self, 
            cursor = "hand",     
            height = "10",
            text = "Inventario",
            width = "20"
        )
        self.inventory.place(
            relx=.5,
            rely=.5,
            anchor='nw'
        )
        self.inventory.pack(expand=0)

root = tk.Tk()
no_name = App(master=root)
no_name.master.title('No Name')
no_name.master.minsize(800, 600)
no_name.master.maxsize(1800, 1200)
no_name.mainloop()