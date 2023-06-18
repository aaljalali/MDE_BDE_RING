import json
import datetime
from datetime import datetime
import datetime as dt

import os
import sys
# Get the current working directory
current_script_path= os.path.abspath(__file__) 
script_dir = os.path.dirname(current_script_path)
root_dir = os.path.dirname(script_dir)

print('root_dir:', root_dir)

# Add the path to the CaptureDevice directory to the sys.path list
DataGeneration_path = root_dir + '/DataGeneration'
sys.path.append(DataGeneration_path)
print('Added path to DataGeneration directory:', DataGeneration_path)

import mde_global_settings

class MyTime():
    def __init__(self ):
        self.ts_format = "%Y-%m-%d %H:%M:%S"
    
    def get_ts(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_current_month(self):
        return datetime.now().strftime("%B")

    def get_current_year(self):
        return datetime.now().strftime("%Y")

    def get_current_day(self):
        return datetime.now().strftime("%d")

    def get_current_hour(self):
        return datetime.now().strftime("%H")


    def extract_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H_%M_%S')
        year = date_obj.strftime("%Y")
        month = date_obj.strftime('%B')
        day = date_obj.strftime("%d")
        hour = date_obj.strftime("%H")
        return year, month, day, hour

    
class MyFolders:
    def __init__(self, config_path=None):
        if not config_path:
         
            if os.path.exists('ConfigFiles'):#check if the ConfigFiles is in the same dir (that is for exe. ) 
                config_path = 'ConfigFiles/mde_config.json'
            else:    
                script_dir = os.path.dirname(os.path.abspath(__file__))#/home/pi/Desktop/venv_MDE/Zoller/CaptureDevice
                parent_dir = os.path.dirname(script_dir) #/home/pi/Desktop/venv_MDE/Zoller
                config_path = os.path.join(parent_dir, 'ConfigFiles/mde_config.json')#/home/pi/Desktop/venv_MDE/Zoller/ConfigFiles/mde_config.json
        self.my_time = MyTime()
        with open(config_path, 'r') as f:
            self.config = json.load(f)
            self.image_folder = self.config['image_folder']

    def get_current_img_folder(self):
        current_folder = os.path.join(self. image_folder, self.my_time.get_current_year(), self.my_time.get_current_month(),
                                      self.my_time.get_current_day(), f"{self.my_time.get_current_hour()}Uhr")
        if not os.path.exists(current_folder):
            os.makedirs(current_folder)
        return current_folder
       
    
    def get_image_path(self,capture, img_ts):
        """
        Diese Funktion generiert den Pfad zum Bild mit dem angegebenen Zeitstempel.
        """
        img_folder = f"/home/pi/Images/{img_ts.strftime('%Y')}/{img_ts.strftime('%B')}/{img_ts.strftime('%d')}/{img_ts.strftime('%H')}Uhr"
        img_path = os.path.join(img_folder, f"{capture.customer_id}_{capture.machine_id}_{img_ts}.{capture.image_format}")
        return img_path

    def create_db_folders(self, img_ts=None):
        main_folder = '/home/pi/_DB_'
        if img_ts is None:
            current_year = str(dt.datetime.now().year)
            current_month = dt.datetime.now().strftime('%B')
        else:
            current_year, current_month,_,_ = self.my_time.extract_date(img_ts)
             
             
        
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        sub_folders = ['Roh_Maschindaten']
        paths = []
        for sub_folder in sub_folders:
            sub_folder_path = os.path.join(main_folder, sub_folder)
            if not os.path.exists(sub_folder_path):
                os.makedirs(sub_folder_path)

           
            year_folder_path = os.path.join(sub_folder_path, current_year)
            if not os.path.exists(year_folder_path):
                os.makedirs(year_folder_path)

            
            month_folder_path = os.path.join(year_folder_path, current_month)
            if not os.path.exists(month_folder_path):
                os.makedirs(month_folder_path)

            paths.append(month_folder_path)

        return paths[0]
    

    def get_db_and_table_names(self, img_ts, my_time):
        # If there is no image timestamp, use the current date and hour to create the database and table names
        if img_ts is None:
            db_name = f"{self.my_time.get_current_day()}_{self.my_time.get_current_month()}_{self.my_time.get_current_year()}"
            tbl_name = f"Roh_{self.my_time.get_current_hour()}00"
        # If there is an image timestamp, use it to create the database and table names
        else:
            yera, month, day, hour = self.my_time.extract_date(img_ts)  # extract date and hour from image timestamp
            db_name = f"{day}_{month}_{yera}"  # format date in "dd_mm_yyyy" format
            tbl_name = f"Roh_{hour}00"  # format hour  

        # Return the database and table names
        return db_name, tbl_name
           
# Nur ausführen, wenn die Datei direkt ausgeführt wird
#if __name__ == "__main__":
 #   pass

 





 





        
