import tkinter as tk
import tkinter.ttk as ttk
import json
from tkinter.messagebox import *
from admin_gui import *
from buyer_gui import *


# Login/Sign up screen
def login_panel(root):
    # Login screen
    def login_screen():
        for widgets in root.winfo_children():
                widgets.destroy()
        # Sign up screen
        def signup_screen():
            # Clear screen
            for widgets in root.winfo_children():
                widgets.destroy()

            ##### UI Widgets #####
            wrapper2 = tk.LabelFrame(root)
            wrapper2.pack(expand='yes', padx=10, pady=10)
            lbl_title = ttk.Label(wrapper2, text='Sign up', font='bold')
            lbl_username = ttk.Label(wrapper2, text='Username:')
            lbl_password = ttk.Label(wrapper2, text='Password:')
            lbl_r_password = ttk.Label(wrapper2, text='Re-type Password:')
            lbl_type = ttk.Label(wrapper2, text='User Type:')

            ent_username = ttk.Entry(wrapper2)
            ent_password = ttk.Entry(wrapper2, show="*")
            ent_r_password = ttk.Entry(wrapper2, show="*")
            combo_type = ttk.Combobox(wrapper2, state='readonly', width=17)
            combo_type['values'] = 'Buyer', 'Administrator'

            btn_signup = ttk.Button(wrapper2, text='Sign up')
            btn_login = ttk.Button(wrapper2, text="Already have an account? Login")

            ##### UI Layouts #####
            lbl_title.grid(row=0, column=0, columnspan=2)
            lbl_username.grid(row=1, column=0)
            ent_username.grid(row=1, column=1)
            lbl_password.grid(row=2, column=0)
            ent_password.grid(row=2, column=1)
            lbl_r_password.grid(row=3, column=0)
            ent_r_password.grid(row=3, column=1)
            lbl_type.grid(row=4, column=0)
            combo_type.grid(row=4, column=1)
            btn_login.grid(row=5, column=0, sticky='nsew')
            btn_signup.grid(row=5, column=1, sticky='nsew')

            # Check if blank & username is taken
            def signup():
                if ent_username.get() == '' or ent_password.get() == '' or ent_r_password.get() == '' or combo_type.get() == '':
                    window_title='Error'
                    window_msg=f'Please make sure all fields are filled in before proceeding.'
                    showerror(window_title, window_msg)
                elif ent_username.get().isspace() == True or ent_password.get().isspace() == True or ent_r_password.get().isspace() == True:
                    showerror('Error', 'Please make sure all fields are fiiled with a correct value.')
                elif ent_password.get() != ent_r_password.get():
                    window_title='Error'
                    window_msg=f'Please make sure password and re-type password are the same before proceeding.'
                    showerror(window_title, window_msg)
                else:
                    with open ('account.json', 'r') as infile:
                        all_accounts = json.load (infile)
                    infile.close()
                    for i in all_accounts:
                        if i['Username'] == ent_username.get():
                            window_title='Error'
                            window_msg=f'Username is already taken. Please try again.'
                            showerror(window_title, window_msg)
                            break
                    else:
                        username = ent_username.get()
                        password = ent_password.get()
                        user_type = combo_type.get()
                        new_acc = {"Username": username, 'Password': password, "User type": user_type, "Money": 0}
                        with open ('account.json', 'r') as infile:
                            all_accounts = json.load (infile)
                        infile.close()
                        all_accounts.append(new_acc)
                        with open ('account.json', 'w') as infile:
                            json.dump (all_accounts, infile, indent = 2)
                        infile.close()
                        login_screen()
                        showinfo('Successful','Your account has been signed up successfully.')
                        
            ##### Widget command #####
            btn_login['command'] = login_screen
            btn_signup['command'] = signup
    
        wrapper = tk.LabelFrame(root)
        wrapper.pack(expand='yes', padx=10, pady=10)
        lbl_title = ttk.Label(wrapper, text='Login', font='bold')
        lbl_username = ttk.Label(wrapper, text='Username:')
        lbl_password = ttk.Label(wrapper, text='Password:')
        ent_username = ttk.Entry(wrapper)
        ent_password = ttk.Entry(wrapper, show="*")
        btn_login = ttk.Button(wrapper, text='Login')
        btn_signup = ttk.Button(wrapper, text="Don't have an account? Sign up")
        lbl_title.grid(row=0, columnspan=2)
        lbl_username.grid(row=1, column=0)
        ent_username.grid(row=1, column=1)
        lbl_password.grid(row=2, column=0)
        ent_password.grid(row=2, column=1)
        btn_login.grid(row=4, column=1, sticky='nsew')
        btn_signup.grid(row=4, column=0, sticky='nsew')

        # Check if blank & verify existence of the account
        def login():
            if ent_username.get() == '' or ent_password.get() == '':
                window_title='Error'
                window_msg=f'Please make sure all fields are filled in before proceeding.'
                showerror(window_title, window_msg)
            elif ent_username.get().isspace() == True or ent_password.get().isspace() == True:
                showerror('Error', 'Please make sure all fields are fiiled with a correct value.')
            else:
                global current_username
                current_username = ent_username.get()
                with open ('account.json', 'r') as infile:
                    all_accounts = json.load (infile)
                infile.close()
                for i in all_accounts:
                    if i['Username'] == ent_username.get() and i['Password'] == ent_password.get():
                        ent_username.delete(0, 'end')
                        ent_password.delete(0, 'end')
                        # Send user to next frame depending on usertype
                        if i['User type'] == 'Administrator':
                            admin_panel(root, current_username)
                        elif i['User type'] == 'Buyer':
                            buyer_panel(root, current_username)
                        break
                else:
                    window_title='Error'
                    window_msg=f'Incorrect username or password.'
                    showerror(window_title, window_msg)
        
        ##### Widget command #####
        btn_login['command'] = login
        btn_signup['command'] = signup_screen
    login_screen()