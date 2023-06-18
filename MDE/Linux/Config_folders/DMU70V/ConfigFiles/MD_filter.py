import os
import sys
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



last_machine_status = 'Unknown'
last_Program_name = 'Unknown'
last_tool = 'Unknown'
def get_machine_status(data): # hier i need to change the name of the function
    global last_machine_status
   
    ts = data['TS']
    mode_id = data['ModeId']
    
   
    if mode_id == 2:
        machine_status = 'MB'
        last_machine_status = machine_status
        mde_data = {'TS': ts,'Machine_performance': machine_status,'Tool_number': '','Program_name':''}
        
    elif mode_id in [3] :
        run = data['run']
        Program_name = ['Program_name']
        last_Program_name =Program_name
        tool =['Tool']
        last_tool=tool
        if run=='RUN':
            machine_status = 'An'
            
        else:
            machine_status = 'LUN'
        last_machine_status = machine_status
        mde_data = {'TS': ts,'Machine_performance': machine_status, 'Program_name': Program_name, 'Tool_number': tool}
    
    
    elif mode_id in [6] :
        run = data['run']
        Program_name = last_Program_name
        tool = last_tool
        mde_data = {'TS': ts,'Machine_performance': machine_status, 'Program_name': Program_name, 'Tool_number': tool}
         
    elif mode_id in [4] :
        machine_status = 'LUN'
        last_machine_status = machine_status
        mde_data = {'TS': ts,'Machine_performance': machine_status,'Tool_number': '','Program_name':''}
        

    elif mode_id in [9]:############################## to edit
        machine_status = 'StW'
        last_machine_status = machine_status
        mde_data = {'TS': ts,'Machine_performance': machine_status,'Tool_number': '','Program_name':''}
    
    elif mode_id in [1,5]:#Bildschirmschoner
        machine_status = last_machine_status
        mde_data = {'TS': ts,'Machine_performance': machine_status,'Tool_number': '','Program_name':''}
    else:
        machine_status = 'Unknown'
        mde_data = {'TS': ts,'Machine_performance': machine_status,'Tool_number': '','Program_name':''}
        
   
   
    
    return mde_data#{'TS': ts, 'Machine_status': machine_status,'Tool_number': '','Program_name':''}

    