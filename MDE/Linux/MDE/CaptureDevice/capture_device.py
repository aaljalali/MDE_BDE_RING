import json
from threading import Thread
from time import sleep
import cv2
from time_folders import MyFolders, MyTime
import os
import sys
# Get the current working directory
current_script_path= os.path.abspath(__file__) 
script_dir = os.path.dirname(current_script_path)



class Capture:
    def __init__(self, config_path=None):
        if not config_path:
            # If config_path is not provided, assume the config file
            # is located in the same directory as this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, 'mde_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
            self.image_width = config['image_width']
            self.image_height = config['image_height']
            self.capture_interval = config['capture_interval']
            self.machine_id = config['machine_id']
            self.customer_id = config['customer_id']
            self.image_format = config['image_format']
            self.machine_off_sleep_n_sec = config['machine_off_sleep_n_sec']
            self.should_save_img = config['should_save_img']
            print('should_save_img', self.should_save_img)
            
        self.camera = None
        self.my_folders = MyFolders(config_path)
        self.my_time = MyTime()
        self.first_img_ts = None
        self.is_first_img = True
        self.current_img_ts = None
        self.current_image = None
        self.is_machine_off =  False
#


    def capture_device_init(self):
        cam_port = 0
        self.camera = cv2.VideoCapture(cam_port, cv2.CAP_V4L2)
        #self.camera.set(cv2.CAP_PROP_FORMAT, cv2.VideoWriter_fourcc(*self.image_format))
        self.camera.set(3, self.image_width)
        self.camera.set(4, self.image_height)

    def get_img(self):
        result, image = self.camera.read()
        ts = self.my_time.get_ts()
        if result:
            return ts, image
        else:
            print("No image detected.")


    def save_img(self, image, path):
        cv2.imwrite(path, image)


    def show_img(self, image, win_name):
        cv2.imshow(win_name, image)
        cv2.waitKey(0)
        cv2.destroyWindow(win_name)

    def test_capture(self):
        print('capture test 15 sec ...')
        i = 0
        while(i<27):
            try:
                img = self.get_img()
                img_actuell = img
                sleep(0.1)
                i = i + 1
            except:
                print('check your capture device')
                sleep(10)
        print('capture test done!')
  
  
    def is_no_signal_image(self, image):    
        template = cv2.imread(script_dir+'/no_signal.tiff' , cv2.IMREAD_GRAYSCALE)
       # Convert the image to grayscale if necessary
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply template matching
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # Find the maximum match value
        _, match_val, _, _ = cv2.minMaxLoc(result)
        return match_val>0.95
    
    def capture_and_save(self): 
        self.current_img_ts, self.current_image = self.get_img()
        if self.is_first_img:
            self.first_img_ts = self.current_img_ts
            self.is_first_img = False
            

        if self.should_save_img and not self.is_machine_off:
            self.current_image_path = self.my_folders.get_current_img_folder()
            image_path = f"{self.current_image_path}/{self.customer_id}_{self.machine_id}_{self.current_img_ts}.{self.image_format}"
            self.save_img(self.current_image, image_path)
        else:
            pass
        try:
            if self.is_no_signal_image(self.current_image):
                self.is_machine_off = True
                print(f'Maschiene Aus! sleep {self.machine_off_sleep_n_sec} sec.')
                sleep(self.machine_off_sleep_n_sec)
            else:
                self.is_machine_off = False
        except:
            print('check img_process.no_signal_image()')

    def capture(self):
        while True:
            
            try:
                self.capture_and_save()
                sleep(self.capture_interval)
                print('capture!')
            except:
                print('some thing went wrong in capture_and_save()')
                
    
    def start(self):
        self.capture_device_init()
        self.test_capture()
        
        t = Thread(target=self.capture)
        t.start()
        
        
        
if __name__ == '__main__':

    capture = Capture( )
    capture.start()
     











