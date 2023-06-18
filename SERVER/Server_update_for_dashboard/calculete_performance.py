import json
from datetime import datetime


def calculate_duration_sec(timestamp1, timestamp2):
    dt1 = datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S")
    dt2 = datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S")
    duration_sec = (dt2 - dt1).total_seconds()
   ## print(timestamp1, ' ', timestamp2, '         duration_sec: ', duration_sec)
    return duration_sec


def calculate_percentage(data):
    total_seconds = sum(data.values())
    percentage_data = {}

    for key, value in data.items():
        percentage = (value / total_seconds) * 100
        percentage_data[key] = round(percentage, 2)

    return percentage_data


def load_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    flattened_data = [entry for sublist in data for entry in sublist]
    return flattened_data


def process_data(data_array):
    data_dict = {}

    current_perf_id = data_array[0][2]
    ts = data_array[0][0]

    for arr in data_array:
        if current_perf_id != arr[2]:
            try:
                data_dict[current_perf_id]["duration_sec"] = data_dict[current_perf_id].get("duration_sec", 0) + calculate_duration_sec(ts, arr[0])
            except KeyError:
                data_dict[current_perf_id] = {"duration_sec": calculate_duration_sec(ts, arr[0])}

            current_perf_id = arr[2]
            ts = arr[0]

    total_duration_sec = sum(data_dict[key]["duration_sec"] for key in data_dict)
    for key in data_dict:
        duration_sec = data_dict[key]["duration_sec"]
        percentage = (duration_sec / total_duration_sec) * 100
        data_dict[key]["percentage"] = round(percentage, 2)

    return data_dict


if __name__ == "__main__":
    file_path = "response_mde_update.json"
    data_array = load_data_from_file(file_path)
    print(process_data(data_array))
    
# [[['2023-03-27 12:09:31', 12, 2, '11890', '1100'], ['2023-03-27 12:37:00', 12, 3, '11890', '1100'], ['2023-03-27 12:51:32', 12, 4, '11890', '1100'], ['2023-03-27 12:52:43', 12, 5, '11890', '1100'], ['2023-03-27 13:30:11', 12, 1, '11890', '1100'], ['2023-03-27 13:37:29', 12, 2, '11890', '1100'], ['2023-03-27 13:38:27', 12, 3, '11890', '1100'], ['2023-03-27 13:44:39', 12, 4, '11890', '1100'], ['2023-03-27 13:45:37', 12, 5, '11890', '1100'], ['2023-03-27 13:46:57', 12, 1, '11890', '1100'], ['2023-03-27 13:49:35', 12, 2, '11890', '1100'], ['2023-03-27 13:50:10', 12, 3, '11890', '1100'], ['2023-03-27 13:51:09', 12, 4, '11890', '1100'], ['2023-03-27 13:51:22', 12, 5, '11890', '1100'], ['2023-03-27 14:02:53', 12, 2, '11890', '1100'], ['2023-03-27 14:03:46', 12, 2, '11890', '1100'], ['2023-03-27 14:23:51', 12, 3, '11890', '1100'], ['2023-03-27 14:24:08', 12, 4, '11890', '1100'], ['2023-03-27 14:30:15', 12, 1, '11890', '1100'], ['2023-03-27 14:31:02', 12, 1, '11890', '1100'], ['2023-03-27 14:45:49', 12, 5, '11890', '1100'], ['2023-03-27 14:48:11', 12, 3, '11890', '1100'], ['2023-03-27 14:49:27', 12, 2, '11890', '1100'], ['2023-03-27 15:07:17', 12, 4, '11890', '1100'], ['2023-03-27 15:09:22', 12, 1, '11890', '1100'], ['2023-03-27 15:10:55', 12, 5, '11890', '1100'], ['2023-03-27 15:12:01', 12, 2, '11890', '1100'], ['2023-03-27 15:14:18', 12, 3, '11890', '1100'], ['2023-03-27 15:15:49', 12, 4, '11890', '1100'], ['2023-03-27 15:17:02', 12, 1, '11890', '1100'], ['2023-03-27 15:18:19', 12, 5, '11890', '1100'], ['2023-03-27 15:20:07', 12, 2, '11890', '1100'], ['2023-03-27 15:22:45', 12, 3, '11890', '1100'], ['2023-03-27 15:23:19', 12, 4, '11890', '1100'], ['2023-03-27 15:24:57', 12, 5, '11890', '1100'], ['2023-03-27 15:26:43', 12, 1, '11890', '1100'], ['2023-03-27 15:28:01', 12, 2, '11890', '1100'], ['2023-03-27 15:29:17', 12, 3, '11890', '1100'], ['2023-03-27 15:30:49', 12, 4, '11890', '1100'], ['2023-03-27 15:32:15', 12, 5, '11890', '1100'], ['2023-03-27 15:34:37', 12, 1, '11890', '1100'], ['2023-03-27 15:36:09', 12, 2, '11890', '1100'], ['2023-03-27 15:37:39', 12, 3, '11890', '1100'], ['2023-03-27 15:39:00', 12, 4, '11890', '1100'], ['2023-03-27 15:40:31', 12, 5, '11890', '1100'], ['2023-03-27 15:42:52', 12, 1, '11890', '1100'], ['2023-03-27 15:44:12', 12, 2, '11890', '1100'], ['2023-03-27 15:45:28', 12, 3, '11890', '1100'], ['2023-03-27 15:47:11', 12, 4, '11890', '1100'], ['2023-03-27 15:48:57', 12, 5, '11890', '1100']]]
#