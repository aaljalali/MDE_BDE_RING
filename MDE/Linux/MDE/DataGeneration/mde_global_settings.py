import os
import sys

# Get the current working directory
current_script_path= os.path.abspath(__file__) 
script_dir = os.path.dirname(current_script_path)
root_dir = os.path.dirname(script_dir)

print('root_dir:', root_dir)

# Add the path to the CaptureDevice directory to the sys.path list
capture_device_path = root_dir + '/CaptureDevice'
sys.path.append(capture_device_path)
print('Added path to CaptureDevice directory:', capture_device_path)

# Add the path to the Configuration directory to the sys.path list
configuration_path = root_dir + '/Configuration'
sys.path.append(configuration_path)
print('Added path to Configuration directory:', configuration_path)

# Add the path to the PatternDetection directory to the sys.path list
pattern_detection_path = root_dir + '/PatternDetection'
sys.path.append(pattern_detection_path)
print('Added path to PatternDetection directory:', pattern_detection_path)



if os.path.exists('ConfigFiles'):#check if the ConfigFiles is in the same dir (that is for exe. ) 
        mde_json_config_path = 'ConfigFiles/mde_config.json'
else:    
       
        mde_json_config_path = os.path.join(root_dir, 'ConfigFiles/mde_config.json')#/home/pi/Desktop/venv_MDE/Zoller/ConfigFiles/mde_config.json



# Print a message to indicate that the process is complete
print('Done')
