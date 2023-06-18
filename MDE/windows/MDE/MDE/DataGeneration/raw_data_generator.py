import mde_global_settings
from mde_global_settings import *
from time_folders import *
from capture_device import Capture
import datetime as dt
from time import sleep
from img_process import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\aaljalali\Downloads\MDE\tessarct'

def wait_for_first_image(capture):
    """
    Diese Funktion wartet auf das erste erfasste Bild, indem sie so lange in einer Schleife verbleibt, bis der Zeitstempel des ersten Bildes verfügbar ist.
    """
    while capture.first_img_ts is None:
        pass
    #print('first_img_ts:   ', capture.first_img_ts)
    return capture.first_img_ts


def find_next_image(capture, first_img_ts,extract_parameters_from_img):
    """
    This function finds the next image captured by the camera after the given timestamp, and sends it to the
    specified function for processing.
    """
    my_folders = MyFolders()
    img_ts = dt.datetime.strptime(first_img_ts, '%Y-%m-%d %H:%M:%S')
    
    while True:
        current_img_ts = dt.datetime.strptime(capture.current_img_ts, '%Y-%m-%d %H:%M:%S')
        
        if img_ts <= current_img_ts:
            img_path = my_folders.get_image_path(capture, img_ts)
            
            if os.path.exists(img_path):
                #print(img_path, '>>>>>>>>>i found one image>>>>>>>>>> ')
                extract_parameters_from_img(current_img_ts, img_path)  # process the found image
                
            img_ts += dt.timedelta(seconds=1)
            sleep(0.1)



def process_image_and_save_text():
    """
    Diese Funktion startet die Erfassung von Bildern und ruft die anderen Funktionen auf, um sie zu verarbeiten.
    """
    my_time = MyTime()
    capture = Capture()
    capture.start()
    extract_parameters_obj = ExtractParametrs()
  
    #first_img_ts = wait_for_first_image(capture)
    ### finde the next image , extact the texts and save them in db
    #find_next_image(capture, first_img_ts, extract_parameters_obj.)
    ###############
    while(True):
        extract_parameters_obj.extract_parameters_from_img(capture.current_img_ts, capture.current_image)
        sleep(0.1)
        if capture.is_machine_off:
            sleep(capture.machine_off_sleep_n_sec)
    ############



def process_old_image_and_save_text(folder_path):
    extract_parameters_obj = ExtractParametrs()
    #sort the files in the fplder from old to new 
    sorted_files = sorted(os.listdir(folder_path), key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))

    for filename in sorted_files:
        # check if the file is an image and extract parameters from it
        if filename.endswith(('.tiff', '.jpg')):
            ts = filename[4:-5] if filename.endswith('.tiff') else filename[4:-4]
            img = cv2.imread(os.path.join(folder_path, filename))
            extract_parameters_obj.extract_parameters_from_img(ts, img)

            
            
   
    
if __name__ == "__main__":
    ## live
  #  process_image_and_save_text()
   #
    ## folder
    process_old_image_and_save_text(f"C:\\Users\\aaljalali\\Downloads\\01")

  
 
 