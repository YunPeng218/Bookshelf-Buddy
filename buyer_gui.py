import tkinter as tk
import tkinter.ttk as ttk
import json
from tkinter.messagebox import *

def buyer_panel(root, current_username):

    def main_page():
        for widgets in root.winfo_children():
            widgets.destroy()

        # To checkout book(s) in shopping cart
        def checkout():
            with open ('cart.json', 'r') as infile:
                cart = json.load (infile)
            infile.close()
            with open ('books.json', 'r') as infile:
                books = json.load (infile)
            infile.close()
            with open ('account.json', 'r') as infile:
                account = json.load (infile)
            infile.close()
            with open ('paid_books.json', 'r') as infile:
                paid = json.load (infile)
            infile.close()
            user_money = 0
            total_price = 0
            for i in account:
                if i['Username'] == current_username:
                    user_money = i['Money']
            for i in cart:
                if i['Buyer Name'] == current_username:
                    total_price += i['Price']*i['Quantity']
            if total_price!=0:
                ans = askyesno('Confirmation', 'Are you sure to check out book(s) in shopping cart?')
                if ans:
                    if user_money >= total_price:
                        user_money -= total_price
                        for i in account:
                            if i['Username'] == current_username:
                                i['Money'] = user_money
                        with open ('account.json', 'w') as infile:
                            json.dump (account, infile, indent=2)
                        infile.close()
                        while True:
                            for i in cart:
                                if i['Buyer Name'] == current_username:
                                    paid.append(i)
                                    for x in books:
                                        if x['ID'] == i['ID']:
                                            x['Quantity'] -= i['Quantity']
                                    cart.remove(i)
                                    break
                            else:
                                break
                        with open ('books.json', 'w') as infile:
                            json.dump (books, infile, indent=2)
                        infile.close()
                        with open ('paid_books.json', 'w') as infile:
                            json.dump (paid, infile, indent=2)
                        infile.close()
                        with open ('cart.json', 'w') as infile:
                            json.dump (cart, infile, indent=2)
                        infile.close()
                        showinfo ('Successful', 'Thank you for your order.')
                        for widgets in root.winfo_children():
                            widgets.destroy()
                        main_page()
                    else:
                        showerror('Error', 'The wallet balance of your account is not sufficient to make payment.')
            else:
                showerror('Error', 'There is no book in cart. Please add book into the cart before making payment.')   

        # To redeem gift card
        def redeem():
            with open ('code.json', 'r') as infile:
                code = json.load (infile)
            infile.close()
            with open ('account.json', 'r') as infile:
                account = json.load (infile)
            infile.close()
            if ent_redeem.get() == '':
                window_title='Error'
                window_msg=f'Please enter gift card code before proceeding.'
                showerror(window_title, window_msg)
            else:
                for i in code:
                    if i['Status'] == 'Unused' and i['Code'] == ent_redeem.get():
                        gift_value=i['Value']
                        i['Status'] = 'Used'
                        with open ('code.json', 'w') as infile:
                            json.dump (code, infile, indent = 2)
                        infile.close()
                        for i in account:
                            if current_username == i['Username']:
                                i['Money']+=gift_value
                                with open ('account.json', 'w') as infile:
                                    json.dump (account, infile, indent = 2)
                                infile.close()
                                for widgets in root.winfo_children():
                                    widgets.destroy()
                                main_page()
                                showinfo ('Successful', 'Gift card has been redeemed successfully.')
                                break
                        break
                else:
                    showerror ('Error', 'Gift card code is not valid.')

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
                    showerror('Error', 'Please make sure you filled in your password before proceeding.')
                else:
                    for i in all_accounts:
                        if ent_password.get() == i['Password'] and current_username == i['Username']:
                            window_title='Confirmation'
                            window_msg=f'Are you sure to delete your account? All data regarding it will be erased.'
                            answer = askyesno(window_title, window_msg)
                            if answer:
                                all_accounts.remove(i)
                                with open ('account.json', 'w') as infile:
                                    json.dump (all_accounts, infile, indent = 2)
                                infile.close()
                                showinfo('Deleted','Your account has been deleted.')
                                root.destroy()
                            break
                    else:
                        window_title='Error'
                        window_msg=f'Incorrect password'
                        showerror(window_title, window_msg)
            btn_delete['command'] = delete
            btn_back['command'] = main_page

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
                        if ent_newpassword.get() == i['Password'] and current_username==i['Username']:
                            window_title='Error'
                            window_msg=f'Your new password cannot be the same as your old password'
                            showerror(window_title, window_msg)
                            break
                        elif i['Username'] == current_username and ent_oldpassword.get() == i['Password']:
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
                        window_msg=f'Incorrect password'
                        showerror(window_title, window_msg)
            
            ##### Widget command #####
            btn_change['command'] = change_pw
            btn_back['command'] = main_page

        # To logout
        def logout():
            ans = askyesno('Confirmation','Are you sure you want to logout?')
            if ans:
                root.destroy()

        # To delete seleted book in from shopping cart
        def delete():
            with open ('cart.json', 'r') as infile:
                cart = json.load (infile)
            infile.close()
            try:
                item2
            except NameError:
                showerror ('Error', 'Please select a book before proceeding.')
            else:
                for i in cart:
                    if current_username == i['Buyer Name'] and item2 == i['ID']:
                        ans = askyesno('Confirmation','Are you sure you want to remove selected book from cart?')
                        if ans:
                            cart.remove(i)
                            with open ('cart.json', 'w') as infile:
                                json.dump (cart, infile, indent=2)
                            infile.close()
                            update_cart_tv()

        # To refresh treeview for shopping cart after a book is added to cart
        def update_cart_tv():
            with open ('cart.json', 'r') as infile:
                cart = json.load (infile)
            infile.close()
            tv2.delete(*tv2.get_children())
            for i in range(len(cart)):
                if cart[i]['Buyer Name'] == current_username:
                    tv2.insert('', 'end', values=(cart[i]['ID'], cart[i]['Book Title'], cart[i]['Author'], cart[i]['Category'], cart[i]['Year Published'], cart[i]['Price'], cart[i]['Quantity']))

        # To add selected book into cart
        def add_to_cart():
            with open ('books.json', 'r') as infile:
                books = json.load (infile)
            infile.close()
            try:
                item
            except NameError:
                showerror ('Error', 'Please select a book before proceeding.')
            else:
                if combo_quantity.get() == '':
                    showerror('Error', 'Please select a quantity.')
                else:
                    with open ('cart.json', 'r') as infile:
                        cart = json.load (infile)
                    infile.close()
                    for i in books:
                        if i['ID'] == item and int(combo_quantity.get()) > i['Quantity']:
                            showerror('Error', 'Quantity selected exceeded stock quantity.')
                        elif i['ID'] == item:
                            i['Buyer Name']=current_username
                            i['Quantity']=int(combo_quantity.get())
                            cart.append(i)    
                            with open ('cart.json', 'w') as infile:
                                json.dump (cart, infile, indent=2)
                            infile.close()
                            update_cart_tv()
                            combo_quantity.set('')

        # To make selection in book list
        def select(a):
            global item
            item = tv.item(tv.focus())
            item = item['values'][0]

        # To make selection in shopping cart
        def select2(a):
            global item2
            item2 = tv2.item(tv2.focus())
            item2 = item2['values'][0]

        # To Search book in book list
        def search():
            with open ('books.json', 'r') as infile:
                books = json.load (infile)
            infile.close()
            if ent_search_title.get().isspace() == False and ent_search_title.get() != '':
                for i in books:
                    for i in books:
                        if ent_search_title.get().lower()==i['Book Title'].lower():
                            tv.delete(*tv.get_children())
                            for data in books:
                                if i['Book Title']==data['Book Title']:
                                    tv.insert('', 'end', values=(i['ID'], i['Book Title'], i['Author'], i['Category'], i['Year Published'], i['Price'], i['Quantity']))
                            btn_search['text'] = 'Clear'
                            ent_search_title['state'] = tk.DISABLED
                            btn_search['command'] = clear
                            break
                    else:
                        showerror('Error', 'The book is not available.')
                        break
            else:
                showerror('Error', 'Please enter a value.')

        # To clear book list treeview after the book has been searched 
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

    
        wrapper1 = ttk.LabelFrame(root, text='Book List')
        wrapper2 = ttk.LabelFrame(wrapper1, text='Search')
        wrapper3 = ttk.LabelFrame(wrapper1, text='Add to cart')
        wrapper4 = ttk.LabelFrame(root, text='Shopping Cart')
        wrapper5 = ttk.LabelFrame(root, text='More Options')
        wrapper6 = ttk.LabelFrame(wrapper5, text='Redeem Gift Card')

        wrapper1.pack(fill='both', expand='yes', padx=10, pady=30)
        wrapper2.place(x=50, y=196)
        wrapper3.place(x=400, y=196)
        wrapper4.pack(fill='both', expand='yes', padx=10, pady=10)
        wrapper5.pack(fill='both', expand='yes', padx=10, pady=10)
        wrapper6.place(x=0, y=40)

        # Book Treeview section
        with open ('books.json', 'r') as infile:
            books = json.load (infile)
        infile.close()
        tv = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height="8", selectmode='browse')
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
        tv.heading(7, text='Stock Quantity')
        tv.column(7, minwidth=0, width=100, anchor=tk.CENTER)
        for i in range(len(books)):
            tv.insert('', 'end', values=(books[i]['ID'], books[i]['Book Title'], books[i]['Author'], books[i]['Category'], books[i]['Year Published'], books[i]['Price'], books[i]['Quantity']))
        
        # Search section
        lbl_search_title = tk.Label(wrapper2, text='Book Title:')
        lbl_search_title.pack(side=tk.LEFT, padx=10)
        ent_search_title = tk.Entry(wrapper2)
        ent_search_title.pack(side=tk.LEFT, padx=6)
        btn_search = tk.Button(wrapper2, text='Search')
        btn_search.pack(side=tk.LEFT, padx=6)
        btn_search['command'] = search

        # Add to cart section
        lbl_quantity = tk.Label(wrapper3, text='Quantity')
        lbl_quantity.pack(side=tk.LEFT, padx=10)
        combo_quantity = ttk.Combobox(wrapper3, state='readonly', width=3)
        quantity_value=[]
        for i in range(1,1000):
            quantity_value.append(i)
        combo_quantity['values']=quantity_value
        combo_quantity.pack(side=tk.LEFT)
        btn_add = tk.Button(wrapper3, text='Add')
        btn_add.pack(side=tk.LEFT, padx=10)
        btn_add['command']=add_to_cart

        # Shopping cart section
        with open ('cart.json', 'r') as infile:
            cart = json.load (infile)
        infile.close()
        with open ('account.json', 'r') as infile:
            account = json.load (infile)
        infile.close()
        for i in account:
            if current_username == i['Username']:
                wallet = i['Money']
        tv2 = ttk.Treeview(wrapper4, columns=(1, 2, 3, 4, 5, 6, 7), show='headings', height="5")
        tv2.pack()
        vsb2 = ttk.Scrollbar(wrapper4, orient="vertical", command=tv2.yview)
        vsb2.place(x=795+150+2, y=0, height=110+20)
        tv2.configure(yscrollcommand=vsb2.set)
        tv2.bind('<ButtonRelease-1>', select2)
        tv2.heading(1, text='ID')
        tv2.column(1, minwidth=0, width=55, anchor=tk.CENTER)
        tv2.heading(2, text='Book Title')
        tv2.column(2, minwidth=0, width=250, anchor=tk.CENTER)
        tv2.heading(3, text='Author')
        tv2.column(3, minwidth=0, width=150, anchor=tk.CENTER)
        tv2.heading(4, text='Category')
        tv2.column(4, minwidth=0, width=120, anchor=tk.CENTER)
        tv2.heading(5, text='Year Published')
        tv2.column(5, minwidth=0, width=120, anchor=tk.CENTER)
        tv2.heading(6, text='Price (RM)')
        tv2.column(6, minwidth=0, width=120, anchor=tk.CENTER)
        tv2.heading(7, text='Quantity')
        tv2.column(7, minwidth=0, width=100, anchor=tk.CENTER)
        btn_delete = tk.Button(wrapper4, text='Delete', anchor=tk.NE, command=delete)
        btn_delete.place(x=835, y=130)
        btn_checkout = tk.Button(wrapper4, text='Check out', command=checkout)
        btn_checkout.place(x=885, y=130)
        lbl_wallet = tk.Label(wrapper4, text=f'Wallet balance: RM{wallet:.2f}')
        lbl_wallet.place(x=30, y=130)
        for i in cart:
            if current_username == i['Buyer Name']:
                tv2.insert('', 'end', values=(i['ID'], i['Book Title'], i['Author'], i['Category'], i['Year Published'], i['Price'], i['Quantity']))

        # More options
        lbl_redeem = tk.Label(wrapper6, text='Gift card code:')
        ent_redeem = tk.Entry(wrapper6)
        btn_redeem = tk.Button(wrapper6, text='Redeem')
        lbl = tk.Label(wrapper5, text='*Gift card can be purchased at bookshop.')
        btn_change_pass = tk.Button(wrapper5, text='Change Password')
        btn_delete_acc = tk.Button(wrapper5, text='Delete Account')
        btn_logout = tk.Button(wrapper5, text='Logout')
        lbl_redeem.pack(side=tk.LEFT, padx=6)
        ent_redeem.pack(side=tk.LEFT, padx=6)
        btn_redeem.pack(side=tk.LEFT, padx=6)
        lbl.place(x=0, y=85)
        btn_change_pass.grid(row=0, column=1, padx=6)
        btn_delete_acc.grid(row=0, column=2, padx=6)
        btn_logout.grid(row=0, column=3, padx=6)
        btn_redeem['command'] = redeem
        btn_change_pass['command'] = change_password_screen
        btn_delete_acc['command'] = delete_account_screen
        btn_logout['command'] = logout

    main_page()