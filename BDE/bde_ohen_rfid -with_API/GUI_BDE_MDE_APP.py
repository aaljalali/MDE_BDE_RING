# gui.py
# pip install pillow
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from global_settings import GlobalSettings
from activities import close_bde_app


class BDEApp:
    def __init__(self, parameter1, parameter2):
        self.parameter1 = parameter1
        self.parameter2 = parameter2
        # the old version made for montior with 480 x 900
        # and this with 600 x 1024
        # 600/480 = 1.25 , 1024/900 = 1.37
        self.screen_widthe = 600
        self.heigh_diff = 1.37
        self.width_diff = 1.25
        self.bg_color = '#C5C5C5'  # #2C3E50
        self.font = ("Helvetica", 12)
        self.root = tk.Tk()

        self.root.title('BDE System')
        self.root.configure(bg='#000')
        self.root.resizable(width=False, height=False)
        self.root.geometry("600x1024+-2+-0")  # ("480x900+-2+-30")
        # Set the protocol handler for window close event
        self.root.protocol("WM_DELETE_WINDOW", close_bde_app)

        # Create main container frame
        self.main_frame = tk.Frame(self.root, width=self.width_diff * 474, height=self.heigh_diff * 800,
                                   bg=self.bg_color)
        self.main_frame.grid(row=0, column=0, padx=self.width_diff * 4, pady=self.heigh_diff * 0)
        self.main_frame.grid_propagate(False)

        # Create image container frame
        self.img_frame = tk.Frame(self.root, width=self.width_diff * 145, height=self.heigh_diff * 150,
                                  bg=self.bg_color)
        self.img_frame.place(x=self.width_diff * self.width_diff * 30, y=self.heigh_diff * 180)

        # Create line separator frame
        self.line_separator = tk.Frame(self.main_frame, width=self.width_diff * 480, height=self.heigh_diff * 4,
                                       bg='#221F1F')
        self.line_separator.place(x=self.width_diff * self.width_diff * 0, y=self.heigh_diff * 158)

        # Create bottom frame
        self.bottom_frame = tk.Frame(self.main_frame, width=self.width_diff * 480, height=self.heigh_diff * 38,
                                     bg='#000')
        self.bottom_frame.place(x=self.width_diff * 0, y=self.heigh_diff * 762)

        # Create Bereich label
        self.bereich_lbl = tk.Label(self.main_frame, fg='WHITE', bg='Green', text=self.parameter1,
                                    font=self.font)
        self.bereich_lbl.place(x=self.width_diff * 156, y=self.heigh_diff * 54, width=self.width_diff * 216,
                               height=self.heigh_diff * 30)

        self.berich_lbl2 = tk.Label(self.main_frame, bg=self.bg_color, text='Bereich_Name', font=self.font)
        self.berich_lbl2.place(x=self.width_diff * 50, y=self.heigh_diff * 58, width=self.width_diff * 100,
                               height=self.heigh_diff * 17)

        # Create Abteilung label
        self.abteilung_lbl = tk.Label(self.main_frame, fg='white', bg='Green', text=self.parameter2,
                                      font=self.font)
        self.abteilung_lbl.place(x=self.width_diff * 156, y=self.heigh_diff * 96, width=self.width_diff * 216,
                                 height=self.heigh_diff * 30)

        self.abteilung_lbl2 = tk.Label(self.main_frame, bg=self.bg_color, text='Abteilung_Name', font=self.font)
        self.abteilung_lbl2.place(x=self.width_diff * 50, y=self.heigh_diff * 96, width=self.width_diff * 100,
                                  height=self.heigh_diff * 17)

        # Create Leistungsart label
        self.leistungsart_lbl = Label(self.main_frame, fg='WHITE', bg='#090808', font=self.font)
        self.leistungsart_lbl.place(x=self.width_diff * 0, y=self.heigh_diff * 420, width=self.width_diff * 480,
                                    height=self.heigh_diff * 45)
        # self.leistungsart_lbl['bg'] = 'ORANGE'
        self.leistungsart_lbl['text'] = "--------- Leistungsart Barcode scannen! ---------"

        # Create Leistungsart label
        self.machine_leistungsart_lbl = Label(self.main_frame, fg='WHITE', bg='ORANGE', font=self.font)
        self.machine_leistungsart_lbl.place(x=self.width_diff * 0, y=self.heigh_diff * 530, width=self.width_diff * 480,
                                            height=self.heigh_diff * 45)
        # self.leistungsart_lbl['bg'] = 'ORANGE'
        self.machine_leistungsart_lbl['text'] = " Maschine Leistungsart scannen! "

        # Create Start time label
        # self.start_lbl = Label(self.main_frame, fg='WHITE', bg='#090808', text='00 00 00 00 00 00',
        #                       font=self.font)
        # self.start_lbl.place(x=self.width_diff*97, y=self.heigh_diff*540, width=self.width_diff*278, height=self.heigh_diff*36)

        # Create operator activity duaration label
        self.operator_activity_duration_lbl = Label(self.main_frame, fg='WHITE', bg='#090808', text='00:00:00',
                                                    font=self.font)
        self.operator_activity_duration_lbl.place(x=self.width_diff * 97, y=self.heigh_diff * 480,
                                                  width=self.width_diff * 278, height=self.heigh_diff * 36)

        # Create machine activity duaration label
        self.machine_activity_duration_lbl = Label(self.main_frame, fg='WHITE', bg='#090808', text='00:00:00',
                                                   font=self.font)  # bg='#090808'

        self.machine_activity_duration_lbl.place(x=self.width_diff * 97, y=self.heigh_diff * 590,
                                                 width=self.width_diff * 278, height=self.heigh_diff * 36)

        self.system_message = Label(self.main_frame, fg='WHITE', bg=self.bg_color,
                                         text=GlobalSettings.system_message,anchor="w", wraplength=550,
                                         font=self.font)
        self.system_message.place(x=self.width_diff * 50, y=self.heigh_diff * 710,
                                  width=self.width_diff * 424, height=self.heigh_diff * 30)
        # Create a PhotoImage object from an image file
        # Open the image file
        self.image_ = Image.open("conection.png")
        # Resize the image to a width of 300 and a height of 200
        self.image_ = self.image_.resize((40,40))
        # Create a PhotoImage object
        self.photo_ = ImageTk.PhotoImage(self.image_)
        # Create a Label for image

        self.client_server_connection_lable = Label(self.main_frame, fg='WHITE', bg='#090808', image=self.photo_)
        self.client_server_connection_lable.place(x=0, y=self.heigh_diff * 710,
                                  width=self.width_diff * 50, height=self.heigh_diff * 30)




        # Create Station label
        self.Station_lbl = Label(self.main_frame, fg='WHITE', bg='Green', text=' ', font=self.font)
        self.Station_lbl.place(x=self.width_diff * 254, y=self.heigh_diff * 198, width=self.width_diff * 141,
                               height=self.heigh_diff * 36)
        self.Station_lbl2 = Label(self.main_frame, fg='#000', bg=self.bg_color, text='Station Nr.', font=self.font)
        self.Station_lbl2.place(x=self.width_diff * 183, y=self.heigh_diff * 205, width=self.width_diff * 70,
                                height=self.heigh_diff * 17)

        # Create Auftrag_nr label
        self.Auftrag_nr_lbl = Label(self.main_frame, fg='WHITE', bg='Orange', text=' ',
                                    font=self.font)
        self.Auftrag_nr_lbl.place(x=self.width_diff * 254, y=self.heigh_diff * 247, width=self.width_diff * 141,
                                  height=self.heigh_diff * 36)
        self.Auftrag_nr_lbl2 = Label(self.main_frame, fg='#000', bg=self.bg_color, text='Auftrag Nr.',
                                     font=self.font)
        self.Auftrag_nr_lbl2.place(x=self.width_diff * 183, y=self.heigh_diff * 252, width=self.width_diff * 70,
                                   height=self.heigh_diff * 17)

        # Create Bauteil label
        self.Bauteil_lbl = Label(self.main_frame, fg='WHITE', bg='ORANGE', text='Bauteil_Nr', font=self.font)
        self.Bauteil_lbl.place(x=self.width_diff * 254, y=self.heigh_diff * 296, width=self.width_diff * 141,
                               height=self.heigh_diff * 36)
        self.Bauteil_lbl2 = Label(self.main_frame, fg='#000', bg=self.bg_color, text='Bauteil Nr.', font=self.font)
        self.Bauteil_lbl2.place(x=self.width_diff * 183, y=self.heigh_diff * 302, width=self.width_diff * 70,
                                height=self.heigh_diff * 17)
        #############################
        ## Bauteil Status label
        #############################
        # self.Bauteil_Status_lbl = Label(self.main_frame, fg='BLACK', bg='ORANGE', text='Bauteil_Status',
        #       font=self.font)
        # self.Bauteil_Status_lbl.place(x=self.width_diff*254, y=self.heigh_diff*345, width=self.width_diff*141, height=self.heigh_diff*36)

        # self.Bauteil_Status_lbl2 = Label(self.main_frame, fg='#000', bg=self.bg_color, text='Status',
        #  font=self.font)
        # self.Bauteil_Status_lbl2.place(x=self.width_diff*183, y=self.heigh_diff*347, width=self.width_diff*70, height=self.heigh_diff*17)
        #############################
        ## User label
        #############################
        self.usr_lbl = Label(self.main_frame, fg='White', bg='#221F1F', text=' RFID chip scannen!', font=self.font)
        self.usr_lbl.place(x=self.width_diff * 32, y=self.heigh_diff * 330, width=self.width_diff * 145,
                           height=self.heigh_diff * 30)

        #############################
        ## time and date label
        #############################
        self.time_lbl = Label(self.main_frame, fg='WHITE', bg='BLACK',
                              font=self.font)
        self.time_lbl.place(x=self.width_diff * 390, y=self.heigh_diff * 765, width=self.width_diff * 90,
                            height=self.heigh_diff * 37)

        # Open the image file
        self.image = Image.open(GlobalSettings.default_img_path)
        # Resize the image to a width of 300 and a height of 200
        self.image = self.image.resize((int(140 * self.width_diff), int(140 * self.heigh_diff)))
        # Create a PhotoImage object
        self.photo = ImageTk.PhotoImage(self.image)
        # Create a Label for image
        self.img_label = Label(self.img_frame, image=self.photo)
        self.img_label.place(x=self.width_diff * 0, y=self.heigh_diff * 7)

    def update_image(self, filename):
        try:
            if GlobalSettings.displayed_img_path != filename:  # and GlobalSettings.registed_MAid != 0 :#and
                # sqlite.rfid_exists(GlobalSettings.registed_MAid) :
                GlobalSettings.displayed_img_path = filename
                # Open the image file
                self.image = Image.open(filename)
                # Resize the image to a width of 140 and a height of 140
                self.image = self.image.resize((int(140 * self.width_diff), int(140 * self.heigh_diff)))
                # Create a PhotoImage object
                self.photo = ImageTk.PhotoImage(self.image)
                # Create a Label for image
                self.img_label = Label(self.img_frame, image=self.photo)
                self.img_label.place(x=self.width_diff * 0, y=self.heigh_diff * 0)
        except:
            pass


if __name__ == '__main__':
    app = BDEApp('', '')
    app.root.mainloop()
