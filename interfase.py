# Initialice Shelve for data persistence
import shelve

# Initialice tkinter interfase
from tkinter import Tk, Frame, Label, Button, Entry, StringVar, OptionMenu, Toplevel
from tkinter import ttk

# Open Productos database.
shelve.open('Productos')

# Products class for load items.
class Product(object):
    '''
    Product class to play with data. 
    Content: 
        Id
        Name 
        Sale 
        Purchase
        Stock 
    '''
    def __init__(self, product_id, product_name, sale_value, purchase_value, stock):
        self.product_id = product_id
        self.product_name = product_name
        self.sale_value = sale_value
        self.purchase_value = purchase_value
        self.stock = stock
    def change_id(self, product_id):
        self.product_id = product_id
    def change_name(self, product_name):
        self.product_name = product_name
    def change_sale_value(self, sale_value):
        self.sale_value = sale_value
    def change_purchase_value(self, purchase_value):
        self.purchase_value = purchase_value
    def change_stock(self, stock):
        self.stock = stock
    def __str__(self):
        return "<{0} => {1}>".format(self.__class__.__name__, self.product_id)


# Create the main class
class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.init_properties()
        self.main_menu()
        self.mainloop() # Main Loop of app.

    def init_properties(self):
        '''
        Initialice the initial properties of master and app
        '''
        self.master.title('App')
        self.choice = 'Nombre' # Current Choice of OptionMenu TODO Change This shit
        self.master.minsize(800, 600)
        self.master.maxsize(800, 600)
        self.pack(side="top", fill="both", expand=True, pady=100)

    def main_menu(self):
        '''
        Initialice FIRST menu of program
        '''
        self.main_title = Label(self, text='Panel de Control', font=("Helvetica", 35), width=100)
        self.main_title.pack()
        self.billings = Button(self, 
            command=lambda:self.delete_main(0),
            cursor="hand",
            text="Facturación",
            height="10",
            width='20'
        )
        self.billings.place(x=420, y=130, height=160, width=160)
        self.inventory = Button(self,
            command=lambda:self.delete_main(1),
            cursor = "hand",     
            height = "10",
            text = "Inventario",
            width = "20"
        )
        self.inventory.place(x=210, y=130, height=160, width=160)

    def delete_main(self, command):
        '''
        Delete FIRST menu to open Billings/Inventory SECOND menu.
        '''
        self.main_title.destroy()
        self.billings.destroy()
        self.inventory.destroy()
        if command == 0:
            self.billings_menu()
        else:
            self.inventory_menu()
    
    def inventory_menu(self):
        '''
        Create the inventory menu to see the list of items. SECOND menu.
        '''
        # Label
        self.main_inventory_text = Label(self, text='Bienvenido', font=("Helvetica", 35))
        self.main_inventory_text.pack(pady=10)

        # Search input
        self.search_input = Entry(self, width=55)
        self.search_input.place(x=50, y=100)

        # Search button.
        self.search_button = Button(self, text='Buscar', command=self.search_item)
        self.search_button.place(x=570, y=98, height=30, width=60)

        # Filter
        self.option_filter = ('Nombre', 'Codigo', 'Cantidad')
        self.filter_variable = StringVar(self)
        self.filter_variable.set(self.option_filter[0])
        self.search_filter = OptionMenu(self, self.filter_variable, *self.option_filter, command=self.get_choice)
        self.search_filter.place(x=640, y=100)

        # Self buttons
        self.add_button = Button(self, text='+', height='2', width='4', command=self.register_product)
        self.modify_button = Button(self, text='M', height='2', width='4', command=self.modify_product)
        self.delete_button = Button(self, text='-', height='2', width='4', command=self.delete_product)

        # Pack buttons in order
        self.add_button.place(x=330, y=150)
        self.modify_button.place(x=380, y=150)
        self.delete_button.place(x=430, y=150)

        # Add list of items
        self.inventory_items()

    def inventory_items(self):
        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('Nombre', 'Compra', 'Venta', 'Stock')
        self.tree.bind('<ButtonRelease-1>', self.select_tree)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=700, y=200, height=200)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

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

        self.load_items(load_products())


    # Functions to search items and comunicate with the interfase

    def search_item(self):
        '''
        Search item from DB and send choices to tree
        '''
        db = shelve.open('Productos')
        choices = []
        if self.choice == 'Nombre':
            for product in db['Productos']:
                if product.product_name == self.search_input.get():
                    choices.append(product)
        elif self.choice == 'Codigo':
            for product in db['Productos']:
                if product.product_id == self.search_input.get():
                    choices.append(product)
                    break
        else:
            for product in db['Productos']:
                if product.stock == self.search_input.get():
                    choices.append(product)
        if len(choices) == 0:
            self.popup('Error', 'No se encontro el '+self.choice)
        else:
            self.tree.delete(*self.tree.get_children())
            self.return_button = Button(self, text='Mostrar todos', height='2', width='11', command=self.return_products)
            self.return_button.place(x=600, y=150)
            self.load_items(choices)

    def return_products(self):
        '''
        Return Tree product to original state
        '''
        self.tree.delete(*self.tree.get_children())
        self.load_items(load_products())
        self.return_button.destroy()
        
    def get_choice(self, value):
        '''
        Get the choice from the OptionMenu ( self.search_filter )
        '''
        self.choice = value

    # Billings Menu

    def billings_menu(self): # TODO
        print('On boarding')

    # Tree Functions

    def select_tree(self, a):
        self.current_item = self.tree.item(self.tree.focus())
    
    def load_items(self, value):
        '''
        Load items according to a product schema (value) to the Tree (self.tree)
        '''
        products_list = value
        for product in products_list:
            self.tree.insert(
                "", 
                "end", 
                text=product.product_id, 
                values = (
                    product.product_name,
                    product.sale_value,
                    product.purchase_value,
                    product.stock
                )
            )


    def modify_product(self):
        if self.tree.item(self.tree.focus())['text'] == '':
            self.popup('Advertencia', 'Nada seleccionado')
        else:
            Register_Product(Toplevel(self), is_modify=True, tree=self.tree)

    def register_product(self):
        Register_Product(Toplevel(self), tree=self.tree)
    
    def delete_product(self):
        if self.tree.item(self.tree.focus())['text'] == '':
            self.popup('Advertencia', 'Nada seleccionado')
        else:
            self.sure_advertise()

    def delete_instance(self):
        delete_product(self.tree.item(self.tree.focus())['text'])
        self.tree.delete(self.tree.focus())
        self.pop_up.destroy()

    def sure_advertise(self):
        self.pop_up = Toplevel(self)
        self.pop_up.wm_title('Advertencia')
        self.pop_up.minsize(200, 100)
        self.pop_up.maxsize(200, 100)
        label = Label(self.pop_up, text='¿Está seguro de eliminar')
        label.pack(pady=10)
        label_2 = Label(self.pop_up, text='el producto?')
        label_2.place(x=54,y=28)
        acept = Button(self.pop_up, text="Aceptar", command=self.delete_instance, height=2, width=8)
        decline = Button(self.pop_up, text="Cancelar", command=self.pop_up.destroy, height=2, width=8)
        acept.place(x=100, y=50)
        decline.place(x=25, y=50)
    
    def popup(self, title, text):
        pop_up = Toplevel(self)
        pop_up.wm_title(title)
        pop_up.minsize(200, 100)
        pop_up.maxsize(200, 100)
        
        label = Label(pop_up, text=text)
        label.pack(pady=10)
        exit_button = Button(pop_up, text="Aceptar", command=pop_up.destroy, height=2, width=8)
        exit_button.pack()


class Register_Product(Frame):
    def __init__(self, master=None, tree=None, is_modify=False):
        super().__init__(master)
        self.tree = tree
        self.is_modify = is_modify
        self.master.title('Producto')
        if is_modify:
            self.master.minsize(300, 390)
            self.master.maxsize(500, 390)
        else:
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
        if self.is_modify:
            self.product_id.insert(0, self.tree.item(self.tree.focus())['text'])
            self.product_name.insert(0, self.tree.item(self.tree.focus())['values'][0])
            self.sale_value.insert(0, self.tree.item(self.tree.focus())['values'][1])
            self.purchase_value.insert(0, self.tree.item(self.tree.focus())['values'][2])
            self.stock.insert(0, self.tree.item(self.tree.focus())['values'][3])

    def init_buttons(self):
        if not self.is_modify:
            self.multiple_buttons = ttk.Checkbutton(
                self.master,
                text='Varios'
            )
            self.multiple_buttons.pack(pady='5')
            self.multiple_buttons.state(['!alternate'])        
        self.cancel_button = Button(
            self.master, 
            command=self.master.destroy,
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

    def validate_fields(self):
        a = self.product_id.get() != ''
        b = self.product_name.get() != ''
        c = self.sale_value.get() != ''
        d = self.purchase_value.get() != ''
        e = self.stock.get() != ''
        if a and b and c and d and e:
            if not self.is_modify:
                if is_existing_id(self.product_id.get()):
                    self.popup('Error', 'Ya existe ese ID')
                else:
                    product = Product(self.product_id.get(),
                    self.product_name.get(),
                    self.sale_value.get(),
                    self.purchase_value.get(),
                    self.stock.get())
                    if self.multiple_buttons.instate(['selected']):
                        save_product(product)
                        self.popup('Alerta', 'Producto añadido')
                        self.erase_fields()
                    else:
                        save_product(product)
                        self.popup('Alerta', 'Producto añadido')                
                        self.master.destroy()
                    self.load_last_item(product)
            else:
                if is_existing_id(self.product_id.get()) and self.tree.item(self.tree.focus())['text'] != self.product_id.get():
                    self.popup('Error', 'Ya existe ese ID')
                else: 
                    product_id = self.product_id.get()
                    product_name = self.product_name.get()
                    sale_value = self.sale_value.get()
                    purchase_value = self.purchase_value.get()
                    stock = self.stock.get()    
                    new_index = modify_product(
                        self.tree.item(self.tree.focus())['text'],
                        Product(
                            product_id, 
                            product_name, 
                            sale_value, 
                            purchase_value,
                            stock
                        )
                    )
                    self.tree.insert(
                        "", 
                        str(new_index), 
                        text=product_id, 
                        values = (
                            product_name, 
                            sale_value, 
                            purchase_value,
                            stock
                        )
                    )
                    self.tree.delete(self.tree.focus())
                    self.master.destroy()
        else:
            self.popup('Error', 'Hacen falta campos.')
    
    def load_last_item(self, product):
        product_list = load_products()
        for index in range(len(product_list)):
            if product_list[index].product_id == product.product_id:
                product_index = index
        self.tree.insert(
            "", 
            str(product_index), 
            text=product.product_id, 
            values = (
                product.product_name,
                product.sale_value,
                product.purchase_value,
                product.stock
            )
        )

    def erase_fields(self):
        self.product_id.delete('0', 'end')
        self.product_name.delete('0', 'end')
        self.sale_value.delete('0', 'end')
        self.purchase_value.delete('0', 'end')
        self.stock.delete('0', 'end')
    
    def popup(self, title, text):
        pop_up = Toplevel(self)
        pop_up.wm_title(title)
        pop_up.minsize(200, 100)
        pop_up.maxsize(200, 100)
        
        label = Label(pop_up, text=text)
        label.pack(pady=10)
        exit_button = Button(pop_up, text="Aceptar", command=pop_up.destroy, height=2, width=8)
        exit_button.pack()


############


def save_product(product):
    db = shelve.open('Productos')
    persistence = db['Productos']
    persistence.append(product)
    db['Productos'] = persistence
    db.close()

def load_products():
    db = shelve.open('Productos')
    if len(db) > 0:
        products = db['Productos']
        products = sorted(products, key=lambda product: int(product.product_id))
        db['Productos'] = products
        return products
    else:
        db['Productos'] = []
        return []

def modify_product(product_id, product):
    db = shelve.open('Productos')
    for index in range(len(db['Productos'])):
        if db['Productos'][index].product_id == product_id:
            products = db['Productos']
            products[index] = product
            break
    products = sorted(products, key=lambda product: int(product.product_id))
    db['Productos'] = products
    for index in range(len(products)):

        if products[index].product_id == product.product_id:
            new_index = index
            break
    db.close()
    return new_index

def delete_product(id):
    db = shelve.open('Productos')
    for index in range(len(db['Productos'])):
        if db['Productos'][index].product_id == id:
            persistence = db['Productos']
            del(persistence[index])
            db['Productos'] = persistence
            break
    
def is_existing_id(id):
    db = shelve.open('Productos')
    for product in db['Productos']:
        if id == product.product_id:
            db.close()
            return True
    db.close()
    return False

root = Tk()
myapp = App(root)