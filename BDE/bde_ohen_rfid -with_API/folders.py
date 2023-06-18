import os
import datetime
import timer

def create_folders():
    main_folder = 'DB'
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)

    sub_folders = ['Erfasste_Maschindaten', 'Erfasste_Betriebsdaten']
    paths = []
    for sub_folder in sub_folders:
        sub_folder_path = os.path.join(main_folder, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.makedirs(sub_folder_path)

        current_year = str(datetime.datetime.now().year)
        year_folder_path = os.path.join(sub_folder_path, current_year)
        if not os.path.exists(year_folder_path):
            os.makedirs(year_folder_path)

        current_month = datetime.datetime.now().strftime('%B')
        month_folder_path = os.path.join(year_folder_path, current_month)
        if not os.path.exists(month_folder_path):
            os.makedirs(month_folder_path)

        paths.append(month_folder_path)

    return paths[0], paths[1]





