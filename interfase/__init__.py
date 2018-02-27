import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.main_menu()

    def main_menu(self):
        self.billings = tk.Button(self, 
            bd="3",
            cursor="hand",
            text="Facturación",
            height="10",
            width='20'
        ).pack(side='left', fill='y')
        self.inventory = tk.Button(self, 
            cursor = "hand",     
            height = "10",
            text = "Inventario",
            width = "20"
        ).pack(side='right', expand='yes', fill='x')

root = tk.Tk()
no_name = App(master=root)
no_name.master.title('No Name')
no_name.master.minsize(800, 600)
no_name.master.maxsize(1800, 1200)
no_name.mainloop()