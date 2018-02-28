import shelve

from tkinter import Tk, Frame, Label, Button, Entry, StringVar, OptionMenu, Toplevel
from tkinter import ttk
from logic import Product

shelve.open('Productos')

class App(Frame):
    def __init__(self, master=None, database=None):
        super().__init__(master)
        self.database = database
        self.master.title('App')
        self.master.minsize(800, 600)
        self.master.maxsize(800, 600)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing())
        self.pack(side="top", fill="both", expand=True, pady=100)
        self.main_menu()
        self.mainloop()

    def main_menu(self):
        self.main_title = Label(self, text='Panel de Control', font=("Helvetica", 35), width=100)
        self.main_title.pack()
        self.billings = Button(self, 
            cursor="hand",
            text="Facturación",
            height="10",
            width='20'
        )
        self.billings.place(x=420, y=130, height=160, width=160)
        self.inventory = Button(self,
            command=lambda:self.delete_main(0),
            cursor = "hand",     
            height = "10",
            text = "Inventario",
            width = "20"
        )
        self.inventory.place(x=210, y=130, height=160, width=160)

    def inventory_menu(self):
        # TODO self.inventory_menu = tk.Toplevel(self) // This is for the new window when we create that shit.
        self.main_inventory_text = Label(self, text='Bienvenido', font=("Helvetica", 35))
        self.main_inventory_text.pack(pady=10)

        # Search Input
        self.search_input = Entry(self, width=55)
        self.search_input.place(x=50, y=100)

        self.search_button = Button(self, text='Buscar')
        self.search_button.place(x=570, y=98, height=30, width=60)

        # Filter
        self.option_filter = ('Nombre', 'Codigo', 'Cantidad')
        self.filter_variable = StringVar(self)
        self.filter_variable.set(self.option_filter[0])
        self.search_filter = OptionMenu(self, self.filter_variable, *self.option_filter)
        self.search_filter.place(x=640, y=100)

        # Self buttons
        self.add_button = Button(self, text='+', height='2', width='4', command=self.register_product)
        self.modify_button = Button(self, text='M', height='2', width='4')
        self.delete_button = Button(self, text='-', height='2', width='4')

        # Pack buttons in order
        self.add_button.place(x=330, y=150)
        self.modify_button.place(x=380, y=150)
        self.delete_button.place(x=430, y=150)

        # Add list of items
        self.item_list()

    def item_list(self):
        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('Nombre', 'Compra', 'Venta', 'Stock')

        self.tree.heading('#0', text='Id')
        self.tree.column("#0", width=100)

        self.tree.heading('Nombre', text='Nombre')
        self.tree.column("Nombre", width=200)

        self.tree.heading('Compra', text='Compra')
        self.tree.column("Compra", width=120)

        self.tree.heading('Venta', text='Venta')
        self.tree.column("Venta", width=120)
        
        self.tree.heading('Stock', text='Stock')
        self.tree.column("Stock", width=80)
        
        self.tree.place(x=75, y=200)

    def delete_main(self, command):
        self.main_title.destroy()
        self.billings.destroy()
        self.inventory.destroy()
        if command == 0:
            # Should open inventory menu
            self.inventory_menu()

    def register_product(self):
        Register_Product(Toplevel(self))

    def on_closing(self):
        print('Helloooooooooooooooo')

class Register_Product(Frame):
    def __init__(self, master=None, database=None):
        super().__init__(master)
        self.database = database
        self.master.title('Producto')
        self.master.minsize(300, 420)
        self.master.maxsize(500, 420)
        self.init_inputs()
        self.init_buttons()
    def init_inputs(self):
        self.text('Registra tu producto:')
        self.text('ID Producto:')
        self.product_id = self.input('...') 
        self.product_id.focus()
        self.text('Nombre Producto')    
        self.product_name = self.input('...')
        self.text('Valor de compra del Producto')
        self.sale_value = self.input('...')
        self.text('Venta de venta del Producto')
        self.purchase_value = self.input('...')
        self.text('Cantidad del Producto')
        self.stock = self.input('...')
    def init_buttons(self):
        self.multiple_buttons = ttk.Checkbutton(
            self.master,
            text='Varios'
        )
        self.multiple_buttons.pack(pady='5')
        self.multiple_buttons.state(['!alternate'])        
        self.cancel_button = Button(
            self.master, 
            command=self.quit,
            height=2,
            text='Cancelar', 
            width=8)
        self.cancel_button.pack(pady='5')
        self.save_button = Button(
            self.master,
            command=self.validate_fields, 
            height=2,
            text='Salvar',
            width=8)
        self.save_button.pack(pady='5')
    def input(self, text):
        inputer = Entry(self.master)
        inputer.pack()
        return inputer
    def text(self, text):
        label = Label(self.master, text=text)
        label.pack()
    def quit(self):
        self.master.quit()
    def validate_fields(self):
        a = self.product_id.get() != ''
        b = self.product_name.get() != ''
        c = self.sale_value.get() != ''
        d = self.purchase_value.get() != ''
        e = self.stock.get() != ''
        if a and b and c and d and e:
            if self.multiple_buttons.instate(['selected']):
                pass
            else:
                save_product((Product(
                    self.product_id.get(), 
                    self.product_name.get(), 
                    self.sale_value.get(), 
                    self.purchase_value.get(),
                    self.stock.get()
                )))
                self.master.destroy()
        else:
            self.error_popup('Hacen falta campos.')
    def error_popup(self, text):
        pop_up = Toplevel(self)
        pop_up.wm_title('Error')
        pop_up.minsize(200, 100)
        pop_up.maxsize(200, 100)
        
        label = Label(pop_up, text=text)
        label.pack(pady=10)
        exit_button = Button(pop_up, text="Aceptar", command=pop_up.destroy, height=2, width=8)
        exit_button.pack()

def save_product(product):
    db = shelve.open('Productos')
    if len(db) > 0:
        persistence = db['Productos']
        persistence.append(product)
        db['Productos'] = persistence
        print('Correcto')    
    else:
        db['Productos'] = []
        db['Productos'] = [product]
        print('Incorrecto')
    print(db['Productos'])
        
    db.close()

root = Tk()
myapp = App(root)