import cv2
from tkinter import filedialog, Tk
import tkinter as tk
from tkinter import simpledialog
from collections import OrderedDict
from PIL import Image, ImageTk
from ConfigDatabase import ConfigDatabase_
import os
import shutil
import sys

# Get the current working directory
current_script_path= os.path.abspath(__file__) 
script_dir = os.path.dirname(current_script_path)
parent_dir = os.path.dirname(script_dir)

# Add the path to the PatternDetection directory to the sys.path list
pattern_detection_path = parent_dir + '/PatternDetection'
print(pattern_detection_path)
sys.path.append(pattern_detection_path)
print(pattern_detection_path)
print('Added path to PatternDetection directory:', pattern_detection_path)
 
import detect_pattern
from detect_pattern import ImageMatcher




def copy_and_rename_file(file_path, dst_dir, new_filename):
    # Get the directory and filename from the file path
    src_dir, original_filename = os.path.split(file_path)

    # Get the file extension from the original filename
    extension = os.path.splitext(original_filename)[1]

    # Create the new filename with the same extension
    new_filename_with_extension = f"{new_filename}{extension}"

    # Check if the destination directory already has a file with the new filename
    if os.path.exists(os.path.join(dst_dir, new_filename_with_extension)):
        # If so, delete the old file
        os.remove(os.path.join(dst_dir, new_filename_with_extension))

    # Copy the file from the source directory to the destination directory with the new name and extension
    shutil.copy2(os.path.join(src_dir, original_filename), os.path.join(dst_dir, new_filename_with_extension))

    # Return the new filename with its extension
    return new_filename_with_extension


class ButtonFunctions:
    show_patametes_active = False
    show_merkaml_active = False
     
    def __init__(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ButtonFunctions')
        self.matcher = ImageMatcher()
        #self.config_db = ConfigDatabase_("MDE_Configuration.db")
        if os.path.exists('ConfigFiles'):#check if the ConfigFiles is in the same dir (that is for exe. )
            self.config_db = ConfigDatabase_("ConfigFiles/MDE_Configuration.db")
        else:
            self.config_db = ConfigDatabase_(f"{parent_dir}/ConfigFiles/MDE_Configuration.db")
        self.current_mode_id = None
        
        
    def browse_files(self):
        root = Tk()
        root.withdraw()
        # browse for image file and return its path
        filename = filedialog.askopenfilename(filetypes=[("Image File",('*.bmp', '*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff')),("all files","*.*")])
        # get the toplevel window and destroy it
        if filename:
            toplevel = root.winfo_toplevel()
            toplevel.destroy()

        img = cv2.imread(filename)
        try:
            self.current_mode_id =  self.matcher.match_images(img)
        except:
            self.current_mode_id = -1 
        print('current_mode_id >>>>>>>>>>>>>>>>>',  self.current_mode_id)
        return filename
   
    
    def add_par_but_func(self, img_canvas, img, resize_percent_width , resize_percent_height ):
       # print( resize_percent_width , resize_percent_height )

        painter = Painter(img_canvas,None, resize_percent_width , resize_percent_height, self.current_mode_id)
        painter.draw_parameter = True
        painter.draw_merkmal = False
        painter.run()
       # print(painter.rectangles)
    
    
    def add_mode_merkmal_but_func(self, img_canvas, img_path, img_item, resize_percent_width, resize_percent_height ):
        print('img_path >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', img_path)
        if self.current_mode_id >0:
            current_mode_name = self.config_db.get_mod_name(self.current_mode_id)
            print (f"mode exist , mode name = {current_mode_name}, mode id = {self.current_mode_id }")
            img = Image.open(img_path)
            self.show_mwerkmal_func(img_canvas, img, img_item, resize_percent_width , resize_percent_height)
        
        #print( resize_percent_width , resize_percent_height )
        painter = Painter(img_canvas, img_path, resize_percent_width , resize_percent_height)
        painter.draw_merkmal = True
        painter.draw_parameter = False
        painter.run()
       # print(painter.rectangles)
       
    def clear_canvas(self, img_canvas, img_item): # clear cavas exept img_item
        for item in img_canvas.find_all():
            if item != img_item:
                img_canvas.delete(item)
                
    def show_all_parametrs_but_func(self, img_canvas, img, img_item, resize_percent_width , resize_percent_height):
        ButtonFunctions.show_patametes_active = not ButtonFunctions.show_patametes_active
        
       
        if  ButtonFunctions.show_patametes_active :
            
            painter = Painter(img_canvas,None, resize_percent_width , resize_percent_height)

            painter.rectangles =painter.config_db.get_parametrs(self.current_mode_id)
            for par_name, pos in painter.rectangles.items():
                print(par_name, pos)
                painter.create_rectangle_with_text(pos[0], pos[1], pos[2], pos[3], painter.canvas, par_name, painter.brush_thickness, painter.font )
        else:
             self.clear_canvas(img_canvas, img_item)
             
    
    
    
    def show_mwerkmal_func(self, img_canvas, img, img_item, resize_percent_width , resize_percent_height):
        painter = Painter(img_canvas,None, resize_percent_width , resize_percent_height)
        pos = painter.config_db.get_mermal_pos(self.current_mode_id)
            
         
        ButtonFunctions.show_merkaml_active = not ButtonFunctions.show_merkaml_active
 

        if  ButtonFunctions.show_merkaml_active :
            
            
            #####
           #
            #matcher = ImageMatcher()
           # matcher.match_images(img)
            #####
             current_mode_name = self.config_db.get_mod_name(self.current_mode_id)
             painter.create_rectangle_with_text(pos[0], pos[1], pos[2], pos[3], painter.canvas, f"MERKMAL, {current_mode_name}", painter.brush_thickness, painter.font )
        else:
            self.clear_canvas(img_canvas, img_item)
        


class Painter:
    def __init__(self, canvas, img_path, resize_percent_width=1, resize_percent_height=1 , mode_id= None):
        self.current_mode_id = mode_id
        self.img_path = img_path
        self.resize_percent_width = resize_percent_width
        self.resize_percent_height = resize_percent_height
        
        self.canvas = canvas
        # set the thickness of the brush
        self.brush_thickness = 1
        # set a flag to indicate whether the user is currently drawing
        self.drawing = False
        # set up a font for displaying text
        self.font = ("Arial", 20)
        # set a flag to indicate whether the user has finished drawing the rectangle
        self.drawing_started = False
        if os.path.exists('ConfigFiles'):#check if the ConfigFiles is in the same dir (that is for exe. )
            self.config_db = ConfigDatabase_("ConfigFiles/MDE_Configuration.db")
        else:
            self.config_db = ConfigDatabase_(f"{parent_dir}/ConfigFiles/MDE_Configuration.db")
        #self.config_db = ConfigDatabase_("MDE_Configuration.db")
        # set up a dictionary to store the rectangles and their names
        self.rectangles ={}
        self.draw_merkmal = False
        self.draw_parameter = False
        
    def create_rectangle_with_text(self, x1, y1, x2, y2, canvas, name, brush_thickness=1, font=None):
        x1 *= self.resize_percent_width
        x2 *= self.resize_percent_width
        y1 *= self.resize_percent_height
        y2 *= self.resize_percent_height
        rect = canvas.create_rectangle(x1, y1, x2, y2, outline='#00ff00', width=brush_thickness)
        text = canvas.create_text(x2 + 5, y1, text=name, anchor='w', font=font, fill='#00ff00')
        return rect, text


    def run(self):
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.update_rectangle)
        self.canvas.bind('<ButtonRelease-1>', self.finish_drawing)
     #   self.canvas.mainloop()

    def start_drawing(self, event):
       # print(f"start_drawing")
        self.drawing = True
        self.start_pos = (event.x, event.y)
        self.end_pos = (event.x, event.y)
        self.drawing_started = True

    def finish_drawing(self, event):
        #print('finish_drawing ', self.resize_percent_width)
        self.drawing = False
    
        if self.draw_parameter :
            # prompt the user to enter the name of the rectangle
            name = simpledialog.askstring(title="Variable Name", prompt="Enter the name of the Variable:")
            if name is None:
                return
            elif name:
                x1,y1,x2,y2 =  self.start_pos[0], self.start_pos[1],  self.end_pos[0], self.end_pos[1]
                x1 /= self.resize_percent_width
                x2 /= self.resize_percent_width
                y1 /= self.resize_percent_height
                y2 /= self.resize_percent_height
                last_rectangle = {}
                last_rectangle[name] = int(x1),int(y1),int(x2),int(y2)
                #print('last_rectangle', last_rectangle)
               
                self.create_rectangle_with_text(x1,y1,x2,y2 , self.canvas, name, self.brush_thickness, self.font )
                self.config_db.creat_config_db()
                self.config_db.insert_data("Parameters", (name, self.current_mode_id, str(last_rectangle[name])))
                
        elif self.draw_merkmal:
             mode_name = simpledialog.askstring(title="Mode Name", prompt="Enter the name of the Mode:")
             if mode_name is None:
                return
             elif mode_name:
                x1,y1,x2,y2 =  self.start_pos[0], self.start_pos[1],  self.end_pos[0], self.end_pos[1]
                x1 /= self.resize_percent_width
                x2 /= self.resize_percent_width
                y1 /= self.resize_percent_height
                y2 /= self.resize_percent_height
                last_rectangle = {}
                last_rectangle[mode_name] = int(x1),int(y1),int(x2),int(y2)
               # print('last_rectangle', last_rectangle)
                new_img_path = copy_and_rename_file(self.img_path,f"{parent_dir}/ConfigFiles/templates", mode_name)

                self.config_db.add_mode(mode_name, str(last_rectangle[mode_name]), new_img_path)
                self.create_rectangle_with_text(x1,y1,x2,y2 , self.canvas, 'Merkmal, '+mode_name, self.brush_thickness, self.font )
                self.draw_merkmal = False
                
           

    
    def update_rectangle(self, event):
        if self.drawing:
            self.end_pos = (event.x, event.y)
            if self.drawing_started :
                x1, y1 = self.start_pos
                x2, y2 = self.end_pos
                self.canvas.delete('tmp_rect')
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='#00ff00', width=self.brush_thickness, tags='tmp_rect')

 

if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)
    canvas.config(width= 1080, height= 720)
    
   # painter = Painter(canvas)
   # painter.run()



        