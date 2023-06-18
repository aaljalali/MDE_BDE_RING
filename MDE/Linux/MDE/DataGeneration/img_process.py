import os
import sys
import time
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import traceback

# Add parent directory to sys.path so that we can import modules from there
# Get the current working directory
current_script_path= os.path.abspath(__file__) 
script_dir = os.path.dirname(current_script_path)#/home/pi/Desktop/venv_MDE/Zoller/DataGeneration
parent_dir = os.path.dirname(script_dir)#/home/pi/Desktop/venv_MDE/Zoller 
sys.path.append(script_dir)

# Import modules from parent directory
from mde_global_settings import *
from detect_pattern import ImageMatcher
from ConfigDatabase import *
from time_folders import *
# Get the current working directory
current_script_path= os.path.abspath(__file__) 
script_dir = os.path.dirname(current_script_path)
root_dir = os.path.dirname(script_dir)
# Add the path to the Configuration directory to the sys.path list
ConfigFiles_path = root_dir + '/ConfigFiles'
sys.path.append(ConfigFiles_path)
print('Added path to ConfigFiles directory:', ConfigFiles_path)

DataGeneration_path = root_dir + '/DataGeneration'
sys.path.append(DataGeneration_path)
print('Added path to DataGeneration directory:', DataGeneration_path)


templates_path = root_dir+'/ConfigFiles/templates'
# Add the path to the CaptureDevice directory to the sys.path list
API_path = root_dir + '/API'
sys.path.append(API_path)
print('Added path to CaptureDevice directory:', API_path)
config_path =ConfigFiles_path +'/mde_config.json'

import api_client
from MD_filter import *





class ImageFiler():
    def image_filter(self,img):
       
        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Threshold image to binary
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Invert image
        thresh = cv2.bitwise_not(thresh)

        # Make sure the background is white
        bg = np.zeros((1,1), dtype=np.uint8)
        bg[0,0] = thresh[0,0]
        if bg[0,0] == 0:
            thresh = cv2.bitwise_not(thresh)

        # Return preprocessed image
        return thresh
 



class ExtractParametrs:
    def __init__(self ):
        with open(config_path, 'r') as f:
            config = json.load(f)
            self.machine_id = config['machine_id']
            self.img_filters = config['img_filters']
        self.img_filter = ImageFiler()
        self.db_folder = MyFolders()
        
        if os.path.exists('ConfigFiles'):#check if the ConfigFiles is in the same dir (that is for exe. )
            self.config_db = ConfigDatabase_("ConfigFiles/MDE_Configuration.db")
        else:
            self.config_db = ConfigDatabase_(f"{parent_dir}/ConfigFiles/MDE_Configuration.db")
        
        self.my_time=   MyTime()
        self.matcher = ImageMatcher()
         

    def load_image(self, image):
        if isinstance(image, str):
            image_path = image
            image = cv2.imread(image)
        elif isinstance(image, np.ndarray):
            image_path = None
        elif isinstance(image, Image.Image):
            image_path = None
            image = np.array(image)
        else:
            raise ValueError("Unsupported image type")
        
        return image

        
    def extract_parameters_from_img(self, ts, image_):
        # to be sure that the image is cv2 image
        image = self.load_image(image_)
        
        
        #print('extract_parameters_from_img...')
        if image is not None:
                ##############
                self.current_mode_id =  self.matcher.match_images(image)
                print('current_mode_id = ', self.current_mode_id)
                parameters_positions= self.config_db.get_parametrs(self.current_mode_id)
               # print(' parameters_positions = ', parameters_positions)
                ##############
                extract_duration = n = 0
                # Extract parameters from each position
                parameters_names_values = {}
                parameters_names_values['TS'] = ts
                parameters_names_values['ModeId'] = self.current_mode_id
                for name, pos in parameters_positions.items():
                    #print('>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<< pos = ', pos)
                    # Get the coordinates of the position
                    x1, y1, x2, y2 = pos
                    img = image[y1:y2, x1:x2]
                    # Extract the parameter from the image using Tesseract OCR
                    start_time = time.time()
                    if self.img_filters:
                        img=self.img_filter.image_filter(img)
                    #cv2.imshow("Image", img)
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()
                    parameter = pytesseract.image_to_string(img, config="-l eng --oem 3 --psm 6")
                    
                    
                    end_time = time.time()

                    # Add the parameter to the dictionary
                    parameters_names_values[name] = parameter.strip()

                    # #print the time it took to extract the parameter
                    ##print(f"Extracted {name} in {end_time-start_time:.2f} seconds")
                    extract_duration += end_time - start_time
                    n += 1
                
                # #print the total time taken to extract all parameters
              #  print(f"{n} parameters extracted in {extract_duration:.2f} seconds")
                #print(parameters_names_values)
                self.save_extracted_parameters(parameters_names_values, ts)
                return parameters_names_values
   
   
   


           

    def save_extracted_parameters(self, parameters_names_values, img_ts=None):# img_ts falls erfassung von alten Bildern
        curent_db_path = self.db_folder.create_db_folders(img_ts)
        db_name, tbl_name = self.db_folder.get_db_and_table_names(img_ts, self.my_time)
        self.config_db.creat_roh_data_db_table( curent_db_path, db_name, tbl_name)
        ## creat table for filterd data
        self.config_db.creat_roh_data_db_table( curent_db_path, db_name, tbl_name+'_filtered')
        self.config_db.creat_filterd_roh_data_db_table( curent_db_path, db_name, tbl_name+'_filtered_2')
        
        db_file = f"{curent_db_path}/{db_name}"
        db_file_filterde = f"{curent_db_path}/{db_name}"
        db_file_filterde_2 = f"{curent_db_path}/{db_name}"
         
        try:
            self.config_db.insert_roh_data(db_file,  tbl_name ,parameters_names_values)
            ## filterd data
            self.config_db.insert_unique_roh_data(db_file_filterde,  tbl_name+'_filtered' ,parameters_names_values) 
             ## filter to have just ts and machine status
            data_inserted = self.config_db.insert_unique_roh_data(db_file_filterde,  tbl_name+'_filtered_2' ,get_machine_status(parameters_names_values))
            if data_inserted:
                    mde_data_with_station_id = dict(get_machine_status(parameters_names_values))
                    mde_data_with_station_id['Station_ID'] = self.machine_id
                    api_client.post_mde_data(mde_data_with_station_id)
        
            
        except Exception as e:
             
             print('sqlite3.IntegrityError', e)
             traceback.print_exc()
 






if __name__ == '__main__':

    # Create an instance of the ExtractParametrs class with an image path
    extract_parameters_obj = ExtractParametrs()

    # Extract the parameters from the image
    my_time =  MyTime()
    ts= my_time.get_ts()
    parameters_names_values = extract_parameters_obj.extract_parameters_from_img(ts,  '/home/pi/Desktop/DMU70v/PatternDetection/templates/1.tiff')
    ##print(parameters_names_values)
    # save the extracted parameters
   # extract_parameters_obj.save_extracted_parameters(parameters_names_values )
    #print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<',get_machine_status(['2023-04-16 21:00:01', 4, 'STOPP']))
