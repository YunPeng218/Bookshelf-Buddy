import tkinter as tk
import tkinter.ttk as ttk
import json
from admin import *
from tkinter.messagebox import *

def admin_panel(root, current_username):
    # Admin Mainpage
    def main_page():
        for widgets in root.winfo_children():
                widgets.destroy()

        # To change account password
        def change_password_screen():
            for widgets in root.winfo_children():
                widgets.destroy()
            wrapper = tk.LabelFrame(root, text='Change Account Password')
            wrapper.pack(expand='yes', padx=10, pady=10)
            lbl_oldpassword = ttk.Label(wrapper, text='Current password: ')
            lbl_newpassword = ttk.Label(wrapper, text='New password:')
            lbl_r_newpassword = ttk.Label(wrapper, text='Re-type new password:')
            ent_oldpassword = ttk.Entry(wrapper, show='*')
            ent_newpassword = ttk.Entry(wrapper, show='*')
            ent_r_newpassword = ttk.Entry(wrapper, show='*')
            btn_change = ttk.Button(wrapper, text='Change password')
            btn_back = ttk.Button(wrapper, text='Back')
            lbl_oldpassword.grid(row=1, column=0)
            ent_oldpassword.grid(row=1, column=1)
            lbl_newpassword.grid(row=2, column=0)
            ent_newpassword.grid(row=2, column=1)
            lbl_r_newpassword.grid(row=3, column=0)
            ent_r_newpassword.grid(row=3, column=1)
            btn_change.grid(row=4, column=1, columnspan=2)
            btn_back.grid(row=4, column=0, columnspan=1)

            def change_pw():
                if ent_oldpassword.get() == '' or ent_newpassword.get() == '' or ent_r_newpassword.get() =='':
                    window_title='Error'
                    window_msg=f'Please make sure all fields are filled in before proceeding.'
                    showerror(window_title, window_msg)
                elif ent_newpassword.get() != ent_r_newpassword.get():
                    showerror('Error', 'Please make sure the new password and re-type password are the same.')
                else:
                    with open ('account.json', 'r') as infile:
                        all_accounts = json.load (infile)
                    infile.close()
                    for i in all_accounts:
                        if ent_newpassword.get() == i['Password'] and current_name==i['Username']:
                            window_title='Error'
                            window_msg=f'Your new password cannot be the same as your old password.'
                            showerror(window_title, window_msg)
                            break
                        elif i['Username'] == current_name and ent_oldpassword.get() == i['Password']:
                            window_title='Confirmation'
                            window_msg=f'Are you sure to change your account password? '
                            answer = askyesno(window_title, window_msg)
                            if answer:
                                i['Password'] = ent_newpassword.get()
                                with open ('account.json', 'w') as infile:
                                    json.dump (all_accounts, infile, indent = 2)
                                infile.close()
                                showinfo ('Successful', 'Your account password has been changed successfully.')
                                ent_oldpassword.delete(0, 'end')
                                ent_newpassword.delete(0, 'end')
                                ent_r_newpassword.delete(0, 'end')
                            break
                    else:
                        window_title='Error'
                        window_msg=f'Incorrect password.'
                        showerror(window_title, window_msg)
            btn_change['command'] = change_pw
            btn_back['command'] = main_page
        
        # To delete account
        def delete_account_screen():
            for widgets in root.winfo_children():
                widgets.destroy()
            wrapper = tk.LabelFrame(root, text='Delete Account')
            wrapper.pack(expand='yes', padx=10, pady=10)
            lbl_password = ttk.Label(wrapper, text='Please enter your password:')
            ent_password = ttk.Entry(wrapper, show="*")
            btn_delete = ttk.Button(wrapper, text='Delete')
            btn_back = ttk.Button(wrapper, text='Back')
            lbl_password.grid(row=0, column=0)
            ent_password.grid(row=0, column=1)
            btn_delete.grid(row=1, column=1, columnspan=2)
            btn_back.grid(row=1, column=0, columnspan=1)

            def delete():
                with open ('account.json', 'r') as infile:
                    all_accounts = json.load (infile)
                infile.close()
                if ent_password.get() == '':
                    showerror('Error', 'Please fill in your password before proceeding.')
                else:
                    for i in all_accounts:
                        if ent_password.get() == i['Password'] and current_name == i['Username']:
                            window_title='Confirmation'
                            window_msg=f'Are you sure to delete your account? All data regarding it will be erased.'
                            answer = askyesno(window_title, window_msg)
                            if answer:
                                all_accounts.remove(i)
                                with open ('account.json', 'w') as infile:
                                    json.dump (all_accounts, infile, indent = 2)
                                infile.close()
                                showinfo('Account Deleted','Your account has been deleted.')
                                root.destroy()
                            break
                    else:
                        window_title='Error'
                        window_msg=f'Incorrect password.'
                        showerror(window_title, window_msg)
            btn_delete['command'] = delete
            btn_back['command'] = main_page

        # To logout
        def logout():
            ans = askyesno('Confirmation','Are you sure you want to logout?')
            if ans:
                root.destroy()
        
        # To manage gift card
        def gift():
            def update_screen():
                with open ('code.json', 'r') as infile:
                    code = json.load (infile)
                infile.close()
                tv.delete(*tv.get_children())
                for i in code:
                    tv.insert('', 'end', values=(i['Code'], i['Value'], i['Status']))

            def submit_code():
                with open ('code.json', 'r') as infile:
                    code = json.load (infile)
                infile.close()
                if ent_code.get() == '' or ent_value.get() == '':
                    window_title='Error'
                    window_msg=f'Please make sure all fields are filled before proceeding.'
                    showerror(window_title, window_msg)
                elif ent_code.get().isspace() == True or ent_value.get().isspace() == True:
                    showerror('Error', 'Please make sure all fields are fiiled with a correct value.')
                elif ent_value.get().replace('.','').isdigit() == False and ent_value.get().isdigit() == False:
                    window_title='Error'
                    window_msg=f'Please enter a valid value for code value.'
                    showerror(window_title, window_msg)
                else:
                    for i in code:
                        if ent_code.get() == i['Code']:
                            showerror('Error', 'A gift card with a same code is exist.')
                            break
                    else:
                        code = ent_code.get()
                        value = float(ent_value.get())
                        add_code(code, value)
                        update_screen()
                        showinfo ('New Code Added', 'A new code has added.')

            for widgets in root.winfo_children():
                widgets.destroy()
            wrapper1 = ttk.LabelFrame(root, text="Gift Card")
            wrapper1.pack(fill='both', expand='yes', padx=10, pady=10)
            wrapper2 = ttk.LabelFrame(wrapper1, text='Add Gift Card')
            wrapper2.place(x=380, y=200)
            with open ('code.json', 'r') as infile:
                code = json.load (infile)
            infile.close()
            tv = ttk.Treeview(wrapper1, columns=(1, 2, 3), show="headings", height="8", selectmode='none')
            tv.pack()
            vsb = ttk.Scrollbar(wrapper1, orient="vertical", command=tv.yview)
            vsb.place(x=467+150+2, y=0, height=165+20)
            tv.configure(yscrollcommand=vsb.set)
            tv.heading(1, text='Gift Card Code')
            tv.column(1, minwidth=0, width=150, anchor=tk.CENTER)
            tv.heading(2, text='Value')
            tv.column(2, minwidth=0, width=55, anchor=tk.CENTER)
            tv.heading(3, text='Status')
            tv.column(3, minwidth=0, width=55, anchor=tk.CENTER)
            for i in code:
                tv.insert('', 'end', values=(i['Code'], i['Value'], i['Status']))
            lbl_code = tk.Label(wrapper2, text='Gift Card Code:')
            ent_code = tk.Entry(wrapper2)
            lbl_value = tk.Label(wrapper2, text='Value (RM):')
            ent_value = tk.Entry(wrapper2)
            btn_submit = tk.Button(wrapper2, text='Submit')
            btn_back = tk.Button(root, text='Back To Mainpage')
            lbl_code.grid(row=0, column=0)
            ent_code.grid(row=0, column=1)
            lbl_value.grid(row=1, column=0)
            ent_value.grid(row=1, column=1)
            btn_submit.grid(row=2, column=1)
            btn_back.place(x=440, y=320)
            btn_submit['command'] = submit_code
            btn_back['command'] = main_page

        # To show paid history
        def view():
            def update_search(i):
                with open ('paid_books.json', 'r') as infile:
                    paid_books = json.load (infile)
                infile.close()
                tv.delete(*tv.get_children())
                for data in paid_books:
                    if i['Buyer Name']==data['Buyer Name']:
                        tv.insert('', 'end', values=(i['Buyer Name'], i['ID'], i['Book Title'], i['Author'], i['Category'], i['Year Published'], i['Price'], i['Quantity']))
            # Search a specific buyer's paid history
            def search():
                with open ('paid_books.json', 'r') as infile:
                    paid_books = json.load (infile)
                infile.close()
                if ent_search_buyer.get().isspace() == False and ent_search_buyer.get() != '':
                    for i in paid_books:
                        for i in paid_books:
                            if ent_search_buyer.get().lower()==i['Buyer Name'].lower():
                                update_search(i)
                                btn_search['text'] = 'Clear'
                                ent_search_buyer['state'] = tk.DISABLED
                                btn_search['command'] = clear
                                break
                        else:
                            showerror('Error', 'This buyer has not purchased any book.')
                            break
                else:
                    showerror('Error', 'Please enter a value.')
            # Refresh treeview after the searching a book
            def clear():
                with open ('paid_books.json', 'r') as infile:
                    paid_books = json.load (infile)
                infile.close()
                btn_search['text'] = 'Search'
                ent_search_buyer['state'] = tk.NORMAL
                tv.delete(*tv.get_children())
                ent_search_buyer.delete(0, 'end')
                for i in range(len(paid_books)):
                    tv.insert('', 'end', values=(paid_books[i]['Buyer Name'], paid_books[i]['ID'], paid_books[i]['Book Title'], paid_books[i]['Author'], paid_books[i]['Category'], paid_books[i]['Year Published'], paid_books[i]['Price'], paid_books[i]['Quantity']))
                btn_search['command'] = search

            for widgets in root.winfo_children():
                widgets.destroy()
            wrapper1 = ttk.LabelFrame(root, text="Paid Books History")
            wrapper1.pack(fill='both', expand='yes', padx=10, pady=10)
            wrapper2 = ttk.LabelFrame(wrapper1, text='Search')
            wrapper2.place(x=18, y=195)
            with open ('paid_books.json', 'r') as infile:
                paid_books = json.load (infile)
            infile.close()
            tv = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height="8", selectmode='none')
            tv.pack()
            vsb = ttk.Scrollbar(wrapper1, orient="vertical", command=tv.yview)
            vsb.place(x=797+150+2, y=0, height=165+20)
            tv.configure(yscrollcommand=vsb.set)
            tv.heading(1, text='Buyer Name')
            tv.column(1, minwidth=0, width=130, anchor=tk.CENTER)
            tv.heading(2, text='Book ID')
            tv.column(2, minwidth=0, width=55, anchor=tk.CENTER)
            tv.heading(3, text='Book Title')
            tv.column(3, minwidth=0, width=230, anchor=tk.CENTER)
            tv.heading(4, text='Author')
            tv.column(4, minwidth=0, width=150, anchor=tk.CENTER)
            tv.heading(5, text='Category')
            tv.column(5, minwidth=0, width=80, anchor=tk.CENTER)
            tv.heading(6, text='Year Published')
            tv.column(6, minwidth=0, width=85, anchor=tk.CENTER)
            tv.heading(7, text='Price')
            tv.column(7, minwidth=0, width=80, anchor=tk.CENTER)
            tv.heading(8, text='Quantity Purchased')
            tv.column(8, minwidth=0, width=110, anchor=tk.CENTER)
            for i in paid_books:
                tv.insert('', 'end', values=(i['Buyer Name'], i['ID'], i['Book Title'], i['Author'], i['Category'], i['Year Published'], i['Price'], i['Quantity']))
            lbl_search_buyer = tk.Label(wrapper2, text='Buyer Name:')
            lbl_search_buyer.pack(side=tk.LEFT, padx=10)
            ent_search_buyer = tk.Entry(wrapper2)
            ent_search_buyer.pack(side=tk.LEFT, padx=6)
            btn_search = tk.Button(wrapper2, text='Search')
            btn_search.pack(side=tk.LEFT, padx=6)
            btn_search['command'] = search
            btn_back = tk.Button(root, text='Back To Mainpage')
            btn_back.place(x=29, y=275)
            btn_back['command'] = main_page

        # Popup message box for filling in the new info of selected book
        def update_record():
            try:
                item
            except NameError:
                showerror ('Error', 'Please select a book before proceeding.')
            else:
                popup = tk.Tk()
                popup.wm_title('Update')
                popup.wm_geometry('250x180')
                popup.resizable(False, False)
                # Pass in entry values into another function in module2.py
                def pass_in_value():
                    if ent_book_title.get() == '' or ent_author.get() == '' or ent_category.get() == '' or combo_year.get() == '' or ent_price.get() == '' or combo_quantity.get() == '':
                        window_title='Error'
                        window_msg=f'Please make sure all fields are filled before proceeding.'
                        showerror(window_title, window_msg)
                    elif ent_book_title.get().isspace() == True or ent_author.get().isspace() == True or ent_category.get().isspace() == True or ent_price.get().isspace() == True:
                        showerror('Error', 'Please make sure all fields are fiiled with a correct value.')
                    elif ent_price.get().replace('.','').isdigit() == False and ent_price.get().isdigit() == False:
                        window_title='Error'
                        window_msg=f'Please enter a correct value for price.'
                        showerror(window_title, window_msg)
                    else:
                        new_book_title=ent_book_title.get()
                        new_author=ent_author.get()
                        new_category=ent_category.get().capitalize()
                        new_year=int(combo_year.get())
                        new_price=float(ent_price.get())
                        new_quantity=int(combo_quantity.get())
                        popup.destroy()
                        update_book_record(item, new_book_title, new_author, new_category, new_year, new_price, new_quantity)
                        update_screen()

                # UI Widgets
                year=[]
                for i in range(1900, 2022):
                    year.append(i)
                year=year[::-1]
                quantity=[]
                for i in range(1,1000):
                    quantity.append(i)
                lbl_id = ttk.Label(popup, text=f'Book ID:')
                lbl_id_value = ttk.Label(popup, text=f'{item}')
                lbl_book_title = ttk.Label(popup, text='Book Title:')
                ent_book_title = ttk.Entry(popup)
                lbl_author = ttk.Label(popup, text='Author:')
                ent_author = ttk.Entry(popup)
                lbl_category = ttk.Label(popup, text='Book Category:')
                ent_category = ttk.Entry(popup)
                lbl_year = ttk.Label(popup, text='Year Published:')
                combo_year = ttk.Combobox(popup, state="readonly", width=4)
                combo_year['values']=year
                lbl_price = ttk.Label(popup, text='Price:')
                ent_price = ttk.Entry(popup)
                lbl_quantity = ttk.Label(popup, text='Quantity:')
                combo_quantity = ttk.Combobox(popup, state='readonly', width=3)
                combo_quantity['values']=quantity
                btn_close = ttk.Button(popup, text='Close', command = popup.destroy)
                btn_submit = ttk.Button(popup, text='Submit', command = pass_in_value)

                # UI Layouts
                lbl_id.grid(row=0, column=0)
                lbl_id_value.grid(row=0, column=1)
                lbl_book_title.grid(row=1, column=0)
                ent_book_title.grid(row=1, column=1)
                lbl_author.grid(row=2, column=0)
                ent_author.grid(row=2, column=1)
                lbl_category.grid(row=3, column=0)
                ent_category.grid(row=3, column=1)
                lbl_year.grid(row=4, column=0)
                combo_year.grid(row=4, column=1, sticky='w')
                lbl_price.grid(row=5, column=0)
                ent_price.grid(row=5, column=1)
                lbl_quantity.grid(row=6, column=0)
                combo_quantity.grid(row=6, column=1, sticky='w')
                btn_close.grid(row=7, column=0)
                btn_submit.grid(row=7, column=1, sticky='nsew')
                popup.mainloop()

        # To select item in treeview
        def select(a):
            global item
            item = tv.item(tv.focus())
            item = item['values'][0]

        # To delete selected item
        def delete():
            try:
                item
            except NameError:
                showerror('Error', 'Please select a book before proceeding.')
            else:
                permission = askyesno('Confirmation', 'Are you sure?')
                if permission:
                    delete_book_record(item)
                    update_screen()

        # To refresh Treeview after search is clear or new book is created
        def update_screen():
            with open ('books.json', 'r') as infile:
                books = json.load (infile)
            infile.close()
            tv.delete(*tv.get_children())
            for i in books:
                tv.insert('', 'end', values=(i['ID'], i['Book Title'], i['Author'], i['Category'], i['Year Published'], i['Price'], i['Quantity']))

        # Update Treeview to show book searched
        def update_search(i):
            with open ('books.json', 'r') as infile:
                books = json.load (infile)
            infile.close()
            tv.delete(*tv.get_children())
            for data in books:
                if i['Book Title']==data['Book Title']:
                    tv.insert('', 'end', values=(i['ID'], i['Book Title'], i['Author'], i['Category'], i['Year Published'], i['Price'], i['Quantity']))

        # To search book
        def search():
            with open ('books.json', 'r') as infile:
                books = json.load (infile)
            infile.close()
            if ent_search_title.get().isspace() == False and ent_search_title.get() != '':
                for i in books:
                    for i in books:
                        if ent_search_title.get().lower()==i['Book Title'].lower():
                            update_search(i)
                            btn_search['text'] = 'Clear'
                            ent_search_title['state'] = tk.DISABLED
                            btn_search['command'] = clear
                            break
                    else:
                        showerror('Error', 'This book is not available.')
                        break
            else:
                showerror('Error', 'Please enter a book title before proceeding.')

        # To refresh treeview after the clear button is pressed
        def clear():
            with open ('books.json', 'r') as infile:
                books = json.load (infile)
            infile.close()
            btn_search['text'] = 'Search'
            ent_search_title['state'] = tk.NORMAL
            tv.delete(*tv.get_children())
            ent_search_title.delete(0, 'end')
            for i in range(len(books)):
                tv.insert('', 'end', values=(books[i]['ID'], books[i]['Book Title'], books[i]['Author'], books[i]['Category'], books[i]['Year Published'], books[i]['Price'], books[i]['Quantity']))
            btn_search['command'] = search

        # Create Function GUI
        def create():
            if ent_create_title.get() == '' or ent_create_author.get() == '' or ent_create_category.get() == '' or combo_create_year.get() == '' or ent_create_price.get() == '' or combo_create_quantity.get() == '':
                showerror('Error', 'Please make sure all fields are filled before proceeding.')
            elif ent_create_title.get().isspace() == True or ent_create_author.get().isspace() == True or ent_create_category.get().isspace() == True or ent_create_price.get().isspace() == True:
                showerror('Error', 'Please make sure all fields are fiiled with a correct value.')
            elif ent_create_price.get().replace('.','').isdigit() == False and ent_create_price.get().isdigit() == False:
                showerror('Error', 'Please enter a correct value for price.')
            else:
                book_title=ent_create_title.get()
                author=ent_create_author.get()
                category=ent_create_category.get().capitalize()
                year=int(combo_create_year.get())
                price=float(ent_create_price.get())
                quantity=int(combo_create_quantity.get())
                create_book_record(book_title, author, category, year, price, quantity)
                ent_create_title.delete(0, 'end')
                ent_create_author.delete(0, 'end')
                ent_create_category.delete(0, 'end')
                combo_create_year.set('')
                ent_create_price.delete(0, 'end')
                combo_create_quantity.set('')
                update_screen()

        # MainScreen GUI
        wrapper1 = ttk.LabelFrame(root, text="Book List")
        wrapper2 = ttk.LabelFrame(wrapper1, text="Search")
        wrapper3 = ttk.LabelFrame(root, text="Create New Book Record")
        wrapper4 = ttk.LabelFrame(root, text='More Options')
        wrapper1.pack(fill='both', expand='yes', padx=10, pady=10)
        wrapper2.place(x=18, y=195)
        wrapper3.pack(fill='both', expand='yes', padx=10, pady=10)
        wrapper4.pack(fill='both', expand='yes', padx=10, pady=10)

        # Book Treeview section GUI
        with open ('books.json', 'r') as infile:
            books = json.load (infile)
        infile.close()
        tv = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height="8")
        tv.pack()
        vsb = ttk.Scrollbar(wrapper1, orient="vertical", command=tv.yview)
        vsb.place(x=795+150+2, y=-1, height=170+20)
        tv.configure(yscrollcommand=vsb.set)
        tv.bind('<ButtonRelease-1>', select)
        tv.heading(1, text='ID')
        tv.column(1, minwidth=0, width=55, anchor=tk.CENTER)
        tv.heading(2, text='Book Title')
        tv.column(2, minwidth=0, width=250, anchor=tk.CENTER)
        tv.heading(3, text='Author')
        tv.column(3, minwidth=0, width=150, anchor=tk.CENTER)
        tv.heading(4, text='Category')
        tv.column(4, minwidth=0, width=120, anchor=tk.CENTER)
        tv.heading(5, text='Year Published')
        tv.column(5, minwidth=0, width=120, anchor=tk.CENTER)
        tv.heading(6, text='Price (RM)')
        tv.column(6, minwidth=0, width=120, anchor=tk.CENTER)
        tv.heading(7, text='Quantity')
        tv.column(7, minwidth=0, width=100, anchor=tk.CENTER)
        btn_update = tk.Button(wrapper1, text='Update', anchor=tk.NE, command=update_record)
        btn_update.place(x=850, y=190)
        btn_delete = tk.Button(wrapper1, text='Delete', anchor=tk.NE, command=delete)
        btn_delete.place(x=903, y=190)
        for i in range(len(books)):
            tv.insert('', 'end', values=(books[i]['ID'], books[i]['Book Title'], books[i]['Author'], books[i]['Category'], books[i]['Year Published'], books[i]['Price'], books[i]['Quantity']))
        
        # Search section GUI
        lbl_search_title = tk.Label(wrapper2, text='Book Title:')
        lbl_search_title.pack(side=tk.LEFT, padx=10)
        ent_search_title = tk.Entry(wrapper2)
        ent_search_title.pack(side=tk.LEFT, padx=6)
        btn_search = tk.Button(wrapper2, text='Search')
        btn_search.pack(side=tk.LEFT, padx=6)
        btn_search['command'] = search
        
        # Create section GUI
        year=[]
        for i in range(1900, 2022):
            year.append(i)
        year=year[::-1]
        quantity=[]
        for i in range(1,1000):
            quantity.append(i)
        lbl_create_title = tk.Label(wrapper3, text='Book Title:')
        lbl_create_title.grid(row=0, column=0, padx=5, pady=3)
        ent_create_title = tk.Entry(wrapper3)
        ent_create_title.grid(row=0, column=1, padx=5, pady=3)
        lbl_create_author = tk.Label(wrapper3, text='Author:')
        lbl_create_author.grid(row=1, column=0, padx=5, pady=3)
        ent_create_author = tk.Entry(wrapper3)
        ent_create_author.grid(row=1, column=1, padx=5, pady=3)
        lbl_create_category = tk.Label(wrapper3, text='Category:')
        lbl_create_category.grid(row=2, column=0, padx=5, pady=3)
        ent_create_category = tk.Entry(wrapper3)
        ent_create_category.grid(row=2, column=1, padx=5, pady=3)
        lbl_create_year = tk.Label(wrapper3, text='Year Published:')
        lbl_create_year.grid(row=3, column=0, padx=5, pady=3)
        combo_create_year = ttk.Combobox(wrapper3, state='readonly', width=4)
        combo_create_year['values'] = year
        combo_create_year.grid(row=3, column=1, padx=5, pady=3, sticky='w')
        lbl_create_price = tk.Label(wrapper3, text='Price:')
        lbl_create_price.grid(row=4, column=0, padx=5, pady=3)
        ent_create_price = tk.Entry(wrapper3)
        ent_create_price.grid(row=4, column=1, padx=5, pady=3)
        lbl_create_quantity = tk.Label(wrapper3, text='Quantity:')
        lbl_create_quantity.grid(row=5, column=0, padx=5, pady=3)
        combo_create_quantity = ttk.Combobox(wrapper3, state='readonly', width=3)
        combo_create_quantity['value'] = quantity
        combo_create_quantity.grid(row=5, column=1, padx=5, pady=3, sticky='w')
        btn_create = tk.Button(wrapper3, text='Create')
        btn_create.grid(row=6, columnspan=2, padx=5, pady=3)
        btn_create['command'] = create

        # More Options section GUI
        btn_view = tk.Button(wrapper4, text='Paid Books History')
        btn_gift = tk.Button(wrapper4, text='Manage Gift Card')
        btn_change_pass = tk.Button(wrapper4, text='Change Password')
        btn_delete_acc = tk.Button(wrapper4, text='Delete Account')
        btn_logout = tk.Button(wrapper4, text='Logout')
        btn_view.grid(row=0, column=0, padx=6)
        btn_gift.grid(row=0, column=1, padx=6)
        btn_change_pass.grid(row=0, column=2, padx=6)
        btn_delete_acc.grid(row=0, column=3, padx=6)
        btn_logout.grid(row=0, column=4, padx=6)
        btn_view['command'] = view
        btn_gift['command'] = gift
        btn_change_pass['command'] = change_password_screen
        btn_delete_acc['command'] = delete_account_screen
        btn_logout['command'] = logout
        current_name=current_username
    main_page()