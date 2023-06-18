from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
from ConfigGuiBackEnd import ButtonFunctions 


   

class ConfigurationTool:
    def __init__(self, image_path):
        self.root = Tk()
        self.root.title('Configuration tool')
        self.root['bg'] ='#fff' #'#0C0C0C'
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight())) # Set window size to full screen
        self.root.resizable(width=False, height=False) 
        self.detected_mod_lbl = None
        self.img_container = None
        self.buttons_container = None
        self.buttons_2_container = None
        self.img_filters_container = None
        self.add_par_container = None
        self.img_canvas = None
        self.img_item = 0
        
        self.but_functions = ButtonFunctions()
        
        self.buttons_container_width = int(self.root.winfo_screenwidth()*0.1 )
        self.buttons_container_height = int(self.root.winfo_screenheight()*0.9)
        self.buttons_container_x = int(self.root.winfo_screenwidth() - self.buttons_container_width)
        self.buttons_container_y = 0
        
        self.img_container_width = int(self.root.winfo_screenwidth()*0.9)
        self.img_container_height = int(self.root.winfo_screenheight()*0.9)
        self.img_container_x = 0
        self.img_container_y = 0
        
        self.img_resize_width = int(self.img_container_width)
        self.img_resize_height = int(self.img_container_height)
        print('self.img_resize_width', self.img_resize_width)
        
        self.resize_percent_width =  None
        self.resize_percent_height = None
        self.img_path = None
        self.load_image(image_path )

        
        self.create_ui()

        # Add protocol handler to prevent window from closing when close button is clicked
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.root.destroy()
         
        # Add code to handle closing the window here
         
    def load_image(self, image_path=None):
            if image_path:
                self.img_path = image_path
                #load = Image.open(image_path)
                # load = load.resize((self.img_resize_width, self.img_resize_height))
                # Open image and get original size
                original_image = Image.open(image_path)
                original_width, original_height = original_image.size
                print(f"Original image size: {original_width} x {original_height}")

                # Resize image and get new size
                resized_image = original_image.resize((self.img_resize_width, self.img_resize_height))
                resized_width, resized_height = resized_image.size
                print(f"Resized image size: {resized_width} x {resized_height}")

                # Calculate resize percentage in width and height
                self.resize_percent_width =  self.img_resize_width / original_width    
                self.resize_percent_height =  self.img_resize_height / original_height
                print(f"Resize percent in width: {self.resize_percent_width:.2f}")
                print(f"Resize percent in height: {self.resize_percent_height:.2f}")

                # Convert to Tkinter PhotoImage and display in canvas
                self.img = ImageTk.PhotoImage(resized_image)
                if self.img_canvas:
                    self.img_item = self.img_canvas.create_image(0, 0, anchor=NW, image=self.img)
                    self.img_canvas.mainloop()
     
     

    def create_ui(self):
        #############################
        ## img CONTAINER
        #############################
        self.img_container = Frame(self.root, width=self.img_container_width, height=self.img_container_height, bg='#4E4E6E')
        self.img_container.place(x=self.img_container_x, y=self.img_container_y)
        self.img_canvas = Canvas(self.img_container, width=self.img_container_width, height=self.img_container_height, cursor="cross")
        self.img_canvas.place(x=00, y=0)
        self.img_item = self.img_canvas.create_image(0, 0, anchor=NW, image=self.img)

        #############################
        ## Buttons CONTAINER
        #############################
        self.buttons_container = Frame(self.root, width=self.buttons_container_width, height=self.buttons_container_height, bg='#000')
        self.buttons_container.place(x=self.buttons_container_x , y=self.buttons_container_y)

  
        show_img_but = Button(self.buttons_container, compound=LEFT, fg='WHITE', bg='#001F3F',padx=10, pady=5, text="Select Image",command =lambda: self.load_image(self.but_functions.browse_files()), font=("Helvetica", 12))
        show_img_but.place(relx=0.5, rely=0.1, anchor=CENTER, width=self.buttons_container_width, height=self.buttons_container_height*0.05)
        
        show_img_but1 = Button(self.buttons_container, compound=LEFT, fg='WHITE', bg='#001F3F',padx=10, pady=5, text="Parameters zeigen",command = lambda: self.but_functions.show_all_parametrs_but_func(self.img_canvas,self.img, self.img_item,self.resize_percent_width, self.resize_percent_height), font=("Helvetica", 12))                                                                     
        show_img_but1.place(relx=0.5, rely=0.15, anchor=CENTER, width=self.buttons_container_width, height=self.buttons_container_height*0.05)

        show_img_but2 = Button(self.buttons_container, compound=LEFT, fg='WHITE', bg='#001F3F',padx=10, pady=5, text="Parameters löschen", font=("Helvetica", 12))
        show_img_but2.place(relx=0.5, rely=0.2, anchor=CENTER, width=self.buttons_container_width, height=self.buttons_container_height*0.05)

        show_img_but3 = Button(self.buttons_container, compound=LEFT, fg='WHITE', bg='#001F3F',padx=10, pady=5,command = lambda: self.but_functions.add_par_but_func(self.img_canvas,self.img,self.resize_percent_width, self.resize_percent_height), text="Neuen Parameter", font=("Helvetica", 12))
        show_img_but3.place(relx=0.5, rely=0.25, anchor=CENTER, width=self.buttons_container_width, height=self.buttons_container_height*0.05)
        
        icon = PhotoImage(file='symbole/eye.png')
        show_img_but4 = Button(self.buttons_container, compound=LEFT, fg='WHITE', bg='#001F3F',padx=10, pady=5, text="Merkmals zeigen",command = lambda: self.but_functions.show_mwerkmal_func(self.img_canvas,self.img, self.img_item,self.resize_percent_width, self.resize_percent_height), font=("Helvetica", 12))
        show_img_but4.place(relx=0.5, rely=0.3, anchor=CENTER, width=self.buttons_container_width, height=self.buttons_container_height*0.05)

        show_img_but5 = Button(self.buttons_container, compound=LEFT, fg='WHITE', bg='#001F3F',padx=10, pady=5, text="Mode löschen", font=("Helvetica", 12))
        show_img_but5.place(relx=0.5, rely=0.35, anchor=CENTER, width=self.buttons_container_width, height=self.buttons_container_height*0.05)

        show_img_but6 = Button( self.buttons_container,text="Add Mode and Mermal",command = lambda: self.but_functions.add_mode_merkmal_but_func(self.img_canvas,self.img_path, self.img_item,self.resize_percent_width, self.resize_percent_height),font=("Helvetica", 12),fg='white',bg='#001F3F',compound=LEFT,padx=10, pady=5)
        show_img_but6.place(relx=0.5, rely=0.4, anchor=CENTER, width=self.buttons_container_width, height=self.buttons_container_height*0.05)

        
    
        
def main():
    config_tool = ConfigurationTool("default.jpg")
    config_tool.root.mainloop()

if __name__ == '__main__':
    main()





