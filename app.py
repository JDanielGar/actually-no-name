from interfase import main
import database
import logic as lg
import tkinter

root = tkinter.Tk()
App = main.App(root, database.db)
Product = lg.inventory.inventory_product
