import json
import random
from tkinter.messagebox import *

# Id generator for book id
def id_generator():
    with open ('books.json', 'r') as infile:
        all_books = json.load (infile)
    infile.close()
    id=[]
    while True:
        id=int(''.join(random.sample('0123456789', 5)))
        for i in all_books:
            if i['ID']!=id:
                return id

# Function for creating new book record
def create_book_record(book_title, author, category, year, price, quantity):
    with open ('books.json', 'r') as infile:
        all_books = json.load (infile)
    infile.close()
    for i in all_books:
        if book_title.lower() == i['Book Title'].lower() and author.lower() == i['Author'].lower():
            window_title='Error'
            window_msg=f'Book titled \'{book_title}\' is not created successfully as it already exists in the database.'
            showerror(window_title, window_msg)
            break
    else:
        id=id_generator()
        new_book = {"Book Title":book_title, "Author":author, "Category":category, "Year Published":year, "Price":price, 'Quantity':quantity, 'ID':id}
        all_books.append(new_book)
        with open ('books.json', 'w') as infile:
            json.dump (all_books, infile, indent=2)
        infile.close()
        window_title='Successful'
        window_msg=f'Book titled \'{book_title}\' has been created successfully in the database.'
        showinfo(window_title, window_msg)

# Function for updating selected book record
def update_book_record(item, new_book_title, new_author, new_category, new_year, new_price, new_quantity):
    with open ('books.json', 'r') as infile:
        all_books = json.load (infile)
    infile.close()
    for i in all_books:
        if i['ID'] == item:
            i['Book Title']=new_book_title
            i['Author']=new_author
            i['Category']=new_category
            i['Year Published']=new_year
            i['Price']=new_price
            i['Quantity']=new_quantity
            with open ('books.json', 'w') as infile:
                json.dump (all_books, infile, indent=2)
            infile.close()
            window_title='Update Successful'
            window_msg="Book has been successfully updated in the database."
            showinfo(window_title, window_msg)

# Function for deleting selected book record
def delete_book_record(delete_id):
    with open ('books.json', 'r') as infile:
        all_books = json.load (infile)
    infile.close()
    for i in range (len(all_books)):
        if delete_id == all_books[i]['ID']:
            del all_books[i]
            with open ('books.json', 'w') as infile:
                json.dump (all_books, infile, indent=2)
            infile.close()
            showinfo('Successful', 'Book deleted.')
            break
    else:
        showerror('Error', 'Book not found.')

# Function for adding new gift code
def add_code(code, value):
    with open ('code.json', 'r') as infile:
        current_code = json.load (infile)
    infile.close()
    new_code = {"Code":code, "Value":value, "Status":'Unused'}
    current_code.append(new_code)
    with open ('code.json', 'w') as infile:
        json.dump (current_code, infile, indent=2)
    infile.close()