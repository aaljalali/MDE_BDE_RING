import os
import sys
import re

# Get the current working directory
current_script_path= os.path.abspath(__file__) 
script_dir = os.path.dirname(current_script_path)
root_dir = os.path.dirname(script_dir)
print('root_dir:', root_dir)

# Add the path to the CaptureDevice directory to the sys.path list
API_path = root_dir + '/API'
sys.path.append(API_path)
print('Added path to CaptureDevice directory:', API_path)

import api_client



def get_digits(text,with_comma):
    if with_comma:
        filtered_text = re.sub(r'[^0-9.,]', '', text)
        filtered_text = filtered_text.replace(',', '.')
    else:
        filtered_text = re.sub(r'[^0-9]', '', text)
    return filtered_text



last_machine_status = 'Unknown'
last_Program_name = 'Unknown'
last_tool = 'Unknown'
def get_machine_status(data): # hier i need to change the name of the function
    global last_machine_status
   
    ts = data['TS']
    mode_id = data['ModeId']
    
   
    if mode_id in [5,6]:
        machine_status = 'MB'
        last_machine_status = machine_status
        mde_data = {'TS': ts,'Machine_performance': machine_status,'Tool_number': '','Program_name':''}
        
    elif mode_id in [1,2,3,4,9] :
        machine_status = 'LUN'
        last_machine_status = machine_status
        mde_data = {'TS': ts,'Machine_performance': machine_status, 'Program_name':  '' , 'Tool_number': '' }
    
    
    elif mode_id == 7  :
        
        tool = data['T']
        Run = data['run']
        Program_name = data['pgm1']
        if 'Kanal'not in Program_name:
             Program_name =''
        if Run !='oO':
           machine_status = 'An'
        else:
            machine_status ='LUN'
        mde_data = {'TS': ts,'Machine_performance': machine_status, 'Program_name':  Program_name , 'Tool_number':  tool }
         
    elif mode_id in [10] :
        machine_status = 'Aus'
        last_machine_status = machine_status
        mde_data = {'TS': ts,'Machine_performance': machine_status,'Tool_number': '','Program_name':''}
   
    else:
        machine_status = 'Unknown'
        mde_data = {'TS': ts,'Machine_performance': machine_status,'Tool_number': '','Program_name':''}
        

     
    return mde_data

    
