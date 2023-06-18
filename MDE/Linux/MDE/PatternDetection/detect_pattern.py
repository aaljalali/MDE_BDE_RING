import cv2
import numpy as np
import os
import sys
import time
current_script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(current_script_path)
parent_dir = os.path.dirname(script_dir)
conf_path=f"{parent_dir}/Configuration" 
sys.path.append(conf_path)
from ConfigDatabase import ConfigDatabase_


class ImageMatcher:
    def __init__(self):#, template_dir):
        self.templates = {}
        if os.path.exists('ConfigFiles'):#check if the ConfigFiles is in the same dir (that is for exe. )
            self.config_db = ConfigDatabase_("ConfigFiles/MDE_Configuration.db")
        else:
            self.config_db = ConfigDatabase_(f"{parent_dir}/ConfigFiles/MDE_Configuration.db")
        # this dic have the template id and there paths
        self.temp_id_path ={k: v[1] for k, v in self.config_db.get_modes().items()}
        self.config_db.conn.close()
        self.load_templates()
         
 
    def read_and_crop_image(self, file_path, crop_coords):
        # Read image as grayscale
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE) 
        # Crop image using NumPy array indexing
        x1, y1, x2, y2 = crop_coords
        print('<<<<<<<file_path ', file_path)

        return img[y1:y2, x1:x2]


    def load_templates(self):
        print('>>>>load_templates() .. ')
        for key, value in  self.config_db.all_modes_info_dict.items():
            mode_id = key
            crop_coords = value[0]
            if os.path.exists('ConfigFiles'):#check if the ConfigFiles is in the same dir (that is for exe. )
                 template_path = f"ConfigFiles/templates/{value[1]}"
            else:
                 template_path = f"{parent_dir}/ConfigFiles/templates/{value[1]}"
    
            template = self.read_and_crop_image(template_path, crop_coords) #cv2.imread(template_path, cv2.IMREAD_GRAYSCALE) # add parameter for grayscale mode
            
            self.templates[mode_id] = template


    def match_images(self, img):
        start_time = time.time()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        start_time = time.time()
        max_match_val, max_template_id = self.find_best_match(img_gray)
        #max_match_val, max_template_id = self.find_best_match(img) 
        #print(f"Input image matched with template {max_template_id with a match value of {max_match_val}")
        #print("matched in --- %s seconds ---" % (time.time() - start_time))
        return   max_template_id
  
  
    def find_best_match(self, img_gray):
        max_match_val = -1
        max_template_id = -1
        for template_name, template in self.templates.items():
                match_val = self.compute_match_value(img_gray, template)
                  
                #print(match_val)
                if match_val>= 0.99:
                    print(f"match_val= {match_val} ############### mode={template_name} ")
                    return match_val, template_name
                
                elif match_val > max_match_val:
                    max_match_val = match_val
                    max_template_id = template_name
      
        if match_val>= 0.99:
            return max_match_val, max_template_id
        else:
            print('match_val = ',match_val, 'wird als nicht bekannt bertachtet')
            return max_match_val,-1
     


    def compute_match_value(self, img_gray, template):
        result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, match_val, _, _ = cv2.minMaxLoc(result)
        return match_val

 
    '''def compute_match_value(self, img, template):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, match_val, _, _ = cv2.minMaxLoc(result)
        return match_val'''




def main():  
    input_dir = '/home/pi/Downloads/70er_bilder/mix'  
    matcher = ImageMatcher() 
    # test on folder with n images 
    for input_filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, input_filename)
        img = cv2.imread(input_path)
       # #print(input_path)

        pattern_id = matcher.match_images(img)
        print(pattern_id)
 
 
 
if __name__ == '__main__':
    main()



  