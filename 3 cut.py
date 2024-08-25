import datetime
import os

# 读取歌曲记录文件
def read_song_records(file_path):
    with open(file_path, 'r') as file:
        song_records = file.readlines()
    songs = []
    for line in song_records:
        if line.strip():
            parts = line.split()
            song_name = parts[0][:-1]
            start_time = parts[1] + " " + parts[2]
            end_time = parts[4] + " " + parts[5]
            fitness = parts[7]
            songs.append((song_name, start_time, end_time, fitness))
    return songs

# 读取 GSR 和 PPG 数据文件
def read_gsr_ppg_data(file_path):
    with open(file_path, 'r') as file:
        gsr_ppg_data = file.readlines()
    header = gsr_ppg_data[0].strip().split(',')
    data = []
    for line in gsr_ppg_data[2:]:
        if line.strip():
            parts = line.strip().split(',')
            timestamp = parts[0]
            gsr_value = parts[1]
            ppg_value = parts[2]
            data.append((timestamp, gsr_value, ppg_value))
    return data

# 将字符串时间转换为 datetime 对象
def str_to_datetime(time_str):
    return datetime.datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S.%f")

# 提取特定时间范围内的 GSR 和 PPG 数据
def extract_gsr_ppg_data_for_song(song, gsr_ppg_data):
    song_name, start_time, end_time, fitness = song
    start_time = str_to_datetime(start_time)
    end_time = str_to_datetime(end_time)
    gsr_values = []
    ppg_values = []
    for record in gsr_ppg_data:
        timestamp = str_to_datetime(record[0])
        if start_time <= timestamp <= end_time:
            gsr_values.append(record[1])
            ppg_values.append(record[2])
    return gsr_values, ppg_values

# 保存数据到文件
def save_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

# 创建文件夹
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 主函数
def main():
    # 创建文件夹
    create_directory('GSR')
    create_directory('PPG')

    # 读取歌曲记录
    song_records_file = 'raw data/timestamps.txt'
    songs = read_song_records(song_records_file)

    # 读取 GSR 和 PPG 数据
    gsr_ppg_file = 'normalized_time_gsr_ppg.txt'
    gsr_ppg_data = read_gsr_ppg_data(gsr_ppg_file)

    # 对每首歌提取并保存 GSR 和 PPG 数据
    for song in songs:
        song_name = song[0]
        gsr_values, ppg_values = extract_gsr_ppg_data_for_song(song, gsr_ppg_data)
        save_data_to_file(gsr_values, f"GSR/{song_name}.txt")
        save_data_to_file(ppg_values, f"PPG/{song_name}.txt")

if __name__ == "__main__":
    main()
