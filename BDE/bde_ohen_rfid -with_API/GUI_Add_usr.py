# Add_user.py
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite
from BE_Funktions import add_user_but_fun
from global_settings import GlobalSettings
from activities import kill_process
from activities import close_bde_app

class AddUser:

    def __init__(self, parameter1):
        self.MA_ID = None
        self.MA_ID = None
        self.vorname = None
        self.nachname = None
        self.rolle = None
        self.tel_nr_1 = None
        self.tel_nr_2 = None
        self.email = None

        self.parameter1 = parameter1
        self.root = tk.Tk()
        self.root.title('BDE System')
        self.root.configure(bg='#4E4E4E')
        self.root.resizable(width=False, height=False)
        self.root.geometry("480x900+-2+-0")
        # Set the protocol handler for window close event
        self.root.protocol("WM_DELETE_WINDOW", close_bde_app)
        #############################
        ## RFID Nr. label
        #############################
        #### label
        self.rfid_nr_lbl = Label(self.root, fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.rfid_nr_lbl.place(x=10, y=120, width=100, height=45)
        self. rfid_nr_lbl['text'] = "MA-ID :"
        #### ENTRY
        self. rfid_nr_lbl2 = Label(self.root, fg='WHITE', bg='#1E4E4E',
                             font=("Helvetica", 15))
        self.rfid_nr_lbl2.place(x=130, y=125, width=200, height=30)
        self. rfid_nr_lbl2['text'] = "CHIP SCANNEN !"

        #############################
        ## Choose avatar
        #############################
        # Avatar label
        self.avatar_lbl = Label(self.root, anchor='w', fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.avatar_lbl.place(x=10, y=155, width=100, height=45)
        self.avatar_lbl['text'] = "Avatar :"

        # Set available avatar names
        avatar_names_and_ids = sqlite.get_unused_avatar_names_and_ids()
        self.avaliable_avatar_names = [item[1] for item in avatar_names_and_ids]
        self.avaliable_avatar_ids = [item[0] for item in avatar_names_and_ids]
        self.choosen_avatar_name_value= self.avaliable_avatar_names[0]
        self.choosen_avatar_id = self.avaliable_avatar_ids[0]
        # Combobox creation
        self.choosen_avatar_name_var = tk.StringVar(self.root)
        self.choosen_avatar_name_var.set(self.avaliable_avatar_names[0])  # Default value to show
        self.avatar_combobox = ttk.Combobox(self.root, width=27, textvariable=self.choosen_avatar_name_var)
        self.avatar_combobox.place(x=130, y=160, width=200, height=30)

        # Set Combobox list
        self.avatar_combobox['values'] = (self.avaliable_avatar_names)

        # Get value from Combobox
        def callback(*args):
            #global choosen_avatar_name_value
            self.choosen_avatar_name_value = self.choosen_avatar_name_var.get()
            self.choosen_avatar_id = self.avaliable_avatar_ids[self.avaliable_avatar_names.index(self.choosen_avatar_name_value)]
            print(self.choosen_avatar_name_value)
            # set_avatar_id()

        self.choosen_avatar_name_var.trace("w", callback)

        #############################
        ##  Vorname
        #############################
        #### label
        self.vorname_lbl = Label(self.root, fg='WHITE', bg='#4E4E4E',
                            font=("Helvetica", 15))
        self.vorname_lbl.place(x=10, y=195, width=100, height=45)
        self.vorname_lbl['text'] = "Vorname :"
        #### ENTRY
        self.vorname_entry = Entry(self.root, fg='WHITE', bg='#4E4E4E',
                              font=("Helvetica", 15))
        self.vorname_entry.place(x=130, y=200, width=200, height=30)
        self.vorname_entry['text'] = "Vorname :"
        #############################
        ##  Nachname  
        #############################
        #### label     
        self.nachname_lbl = Label(self.root, anchor='w', fg='WHITE', bg='#4E4E4E',
                             font=("Helvetica", 15))
        self.nachname_lbl.place(x=10, y=235, width=110, height=45)
        self.nachname_lbl['text'] = "Nachname :"

        #### ENTRY
        self.nachname_entry = Entry(self.root, fg='WHITE', bg='#4E4E4E',
                               font=("Helvetica", 15))
        self.nachname_entry.place(x=130, y=240, width=200, height=30)
        self.nachname_entry['text'] = "Nachnname :"
        self.vorname_entry['text'] = "Vorname :"

        #############################
        ## Rolle
        #############################
        #### label     
        self.rolle_lbl = Label(self.root, anchor='w', fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.rolle_lbl.place(x=10, y=275, width=110, height=45)
        self.rolle_lbl['text'] = "Rolle :"

        #### ENTRY
        self.rolle_entry = Entry(self.root, fg='WHITE', bg='#4E4E4E',
                            font=("Helvetica", 15))
        self.rolle_entry.place(x=130, y=280, width=200, height=30)
        self.rolle_entry['text'] = "Rolle :"

        # Admin label
        self.admin_lbl = Label(self.root, anchor='w', fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.admin_lbl['text'] = "Admin"
        self.admin_lbl.place(x=10,y=315,width=100,height=45)

        # Radio buttons
        # create a variable to store the selection
        self.is_admin_choice = tk.StringVar()
        self.is_admin_choice.set("Nein")  # set the default selection

        # create the radio buttons
        self.ja_rb = tk.Radiobutton(self.root, text="Ja",bg="#4E4E4E", highlightbackground="#4E4E4E", variable=self.is_admin_choice, value="Ja",
                                    command=self.save_radio_selction)
        self.nein_rb = tk.Radiobutton(self.root, text="Nein",bg="#4E4E4E", variable=self.is_admin_choice, value="Nein",
                                      command=self.save_radio_selction)

        # position the radio buttons on the window
        self.ja_rb.place(x=130, y=320)
        self.nein_rb.place(x=180, y=320)

        # Function to get the selection

        '''def sel():
            global admin
            self.admin = self.var.get()
            self.is_admin_choice = "You selected the option " + str(self.var.get())
            print(self.is_admin_choice)

        self.var = IntVar()
        self.R1 = Radiobutton(self.root, bg='#4E4E4E', activebackground="#4E4E4E", activeforeground='#ffffff', highlightbackground="#4E4E4E", text="Yes", variable=self.var, value=1, command=sel)
        self.R1.place(x=130, y=320)
        self.R2 = Radiobutton(self.root, text="No", bg='#4E4E4E', activebackground="#4E4E4E", activeforeground='#ffffff', highlightbackground="#4E4E4E", variable=self.var, value=0, command=sel)
        self.R2.place(x=180, y=320)'''
        #############################
        ##  Tel. Nr.1   
        #############################
        #### label     
        self.tel_nr_1_lbl = Label(self.root, fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.tel_nr_1_lbl.place(x=10, y=355, width=100, height=45)
        self.tel_nr_1_lbl['text'] = "Tel. Nr.1  :"

        #### ENTRY
        self.tel_nr_1_entry = Entry(self.root, fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.tel_nr_1_entry.place(x=130, y=360, width=200, height=30)
        self.tel_nr_1_entry['text'] = "0550 :"
        #############################
        ##  Tel. Nr.2   
        #############################
        #### label     
        self.tel_nr_2_lbl = Label(self.root, fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.tel_nr_2_lbl.place(x=10, y=395, width=100, height=45)
        self.tel_nr_2_lbl['text'] = "Tel. Nr.2  :"

        #### ENTRY
        self.tel_nr_2_entry = Entry(self.root, fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.tel_nr_2_entry.place(x=130, y=400, width=200, height=30)
        self.tel_nr_2_entry['text'] = "0010 :"
        #############################
        ##  E_mail   
        #############################
        #### label     
        self.e_mail_lbl = Label(self.root, anchor='w', fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.e_mail_lbl.place(x=10, y=435, width=100, height=45)
        self.e_mail_lbl['text'] = "Email  :"

        #### ENTRY
        self.email_entry = Entry(self.root, fg='WHITE', bg='#4E4E4E', font=("Helvetica", 15))
        self.email_entry.place(x=130, y=440, width=200, height=30)
        self.email_entry['text'] = "0 :"
        
        #### ADD Button frontend #################
        #############################################
        self.Is_Admin = 'Nein'
        self.add_user_but=Button(self.root,fg='WHITE', bg='#221F1F',command= lambda: add_user_but_fun(self, GlobalSettings.last_scanned_MAid, self.choosen_avatar_id, self.vorname_entry.get(),
                                                                                                      self.nachname_entry.get(), self.rolle_entry.get(), self.tel_nr_1_entry.get(), self.tel_nr_2_entry.get(), self.email_entry.get(), self.is_admin_choice.get()) , text= " registrieren " ,
            font=("Helvetica", 11))
        self.add_user_but.place(x=100,y=495,width=250,height=38)




    def reset(self):
        self.rfid_nr_lbl2['bg'] = "green"
        #reader.last_scanned_rfid = 0
        self.rfid_nr_lbl2['text'] = "Neue Chip scannen"
        self.vorname_entry.delete(0, "end")
        self.nachname_entry.delete(0, "end")
        self.rolle_entry.delete(0, "end")
        self.tel_nr_1_entry.delete(0, "end")
        self.tel_nr_2_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

        self.MA_ID = ""
        self.vorname = ""
        self.nachname = ""
        self.rolle = ""
        self.tel_nr_1 = ""
        self.tel_nr_2 = ""
        self.email = ""

    def save_radio_selction(self):
            self.Is_Admin = self.is_admin_choice.get()
            print(f"Your selection is: {self.is_admin_choice.get()}")
if __name__ == '__main__':
    app = AddUser('')
    app.root.mainloop()


