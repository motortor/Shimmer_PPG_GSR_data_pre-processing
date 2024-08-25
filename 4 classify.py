import os
import numpy as np
import shutil

def remove_lines_from_file(file_path, num_lines):
    # 读取文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 删除前 num_lines 行
    updated_lines = lines[num_lines:]

    # 写回文件
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

def process_files_in_folder_for_removal(folder_path, num_lines):
    # 遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # 仅处理 .txt 文件
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                remove_lines_from_file(file_path, num_lines)

def smooth_and_save(input_file_path, window_size=50, repeat=2):
    # 读取数据
    with open(input_file_path, 'r') as file:
        data = [float(line.strip()) for line in file]

    # 重复平滑处理
    for _ in range(repeat):
        smoothed_data = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
        data = smoothed_data

    # 保存平滑后的数据到同一个文件
    with open(input_file_path, 'w') as file:
        for value in smoothed_data:
            file.write(f'{value}\n')

def process_files_in_folder_for_smoothing(folder_path, window_size=50, repeat=2):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                input_file_path = os.path.join(root, file)
                smooth_and_save(input_file_path, window_size, repeat)

def process_files(r_file, source_folder, dest_folder):
    # 读取 r_file 的内容
    with open(r_file, 'r') as file:
        lines = file.readlines()

    # 解析每一行并分类文件
    for line in lines:
        # 拆分行内容，提取文件名和评分
        parts = line.split()
        if len(parts) < 2:
            print(f'Invalid line format: {line}')
            continue

        filename = parts[0].replace(':', '')
        fitness_score = parts[-1].split(':')[-1]

        # 创建目标文件夹
        target_folder = os.path.join(dest_folder, f'fitness_{fitness_score}')
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # 源文件路径和目标文件路径
        source_file = os.path.join(source_folder, f'{filename}.txt')
        target_file = os.path.join(target_folder, f'{filename}.txt')

        # 移动文件到目标文件夹
        if os.path.exists(source_file):
            shutil.move(source_file, target_file)
            print(f'Moved {source_file} to {target_file}')
        else:
            print(f'File {source_file} not found')

    print(f'文件分类完成 for {source_folder}')

if __name__ == "__main__":
    ppg_folder_path = "PPG"
    gsr_folder_path = "GSR"
    num_lines_to_remove = 125
    window_size = 50
    repeat_smoothing = 2
    r_file = 'raw data/timestamps.txt'

    # Step 1: Remove lines from PPG and GSR files
    process_files_in_folder_for_removal(ppg_folder_path, num_lines_to_remove)
    process_files_in_folder_for_removal(gsr_folder_path, num_lines_to_remove)

    # Step 2: Smooth data directly in PPG and GSR folders, repeating the smoothing process twice
    process_files_in_folder_for_smoothing(ppg_folder_path, window_size, repeat=repeat_smoothing)
    process_files_in_folder_for_smoothing(gsr_folder_path, window_size, repeat=repeat_smoothing)

    # Step 3: Classify smoothed files based on fitness scores
    process_files(r_file, ppg_folder_path, ppg_folder_path)
    process_files(r_file, gsr_folder_path, gsr_folder_path)
