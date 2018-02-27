import tkinter as tk
from tkinter import ttk
# Window to registter a product
class Register_Product(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Producto')
        self.master.minsize(300, 420)
        self.master.maxsize(500, 420)
        self.pack()
        self.init_inputs()
        self.init_buttons()
        self.mainloop()
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
        self.multiple_buttons = tk.ttk.Checkbutton(
            self.master,
            text='Varios'
        )
        self.multiple_buttons.pack(pady='5')
        self.multiple_buttons.state(['!alternate'])        
        self.cancel_button = tk.Button(
            self.master, 
            command=self.quit,
            height=2,
            text='Cancelar', 
            width=8)
        self.cancel_button.pack(pady='5')
        self.save_button = tk.Button(
            self.master,
            command=self.validate_fields, 
            height=2,
            text='Salvar',
            width=8)
        self.save_button.pack(pady='5')
    def input(self, text):
        inputer = tk.Entry(self.master)
        inputer.pack()
        return inputer
    def text(self, text):
        label = tk.Label(self.master, text=text)
        label.pack()
    def quit(self):
        self.master.quit()
    def validate_fields(self):
        print(self.multiple_buttons.instate(['selected']))
        a = self.product_id.get() != ''
        b = self.product_name.get() != ''
        c = self.sale_value.get() != ''
        d = self.purchase_value.get() != ''
        e = self.stock.get() != ''
        print(a, b, c, d, e)
        if a and b and c and d and e:
            print('Call back')
            if self.multiple_buttons.instate(['selected']):
                print('Fuck')
            else:
                self.quit()
root = tk.Tk()
register_interfase = Register_Product(root)
root.quit()