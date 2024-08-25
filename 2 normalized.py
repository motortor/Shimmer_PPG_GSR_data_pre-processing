import pandas as pd

# 读取数据文件并跳过第二行
file_path = 'time_gsr_ppg.txt'
data = pd.read_csv(file_path, skiprows=[1])

# 确保指定列的数据类型为浮点型
data['Shimmer_FC32_GSR_Skin_Resistance_CAL'] = pd.to_numeric(data['Shimmer_FC32_GSR_Skin_Resistance_CAL'])
data['Shimmer_FC32_PPG_A13_CAL'] = pd.to_numeric(data['Shimmer_FC32_PPG_A13_CAL'])

# 获取指定列的数据
gsr_data = data['Shimmer_FC32_GSR_Skin_Resistance_CAL']
ppg_data = data['Shimmer_FC32_PPG_A13_CAL']

# 计算最大值和最小值
gsr_max = gsr_data.max()
gsr_min = gsr_data.min()
ppg_max = ppg_data.max()
ppg_min = ppg_data.min()

print(f"GSR最大值: {gsr_max}, GSR最小值: {gsr_min}")
print(f"PPG最大值: {ppg_max}, PPG最小值: {ppg_min}")

# 归一化处理
gsr_normalized = (gsr_data - gsr_min) / (gsr_max - gsr_min)
ppg_normalized = (ppg_data - ppg_min) / (ppg_max - ppg_min)

# 创建新的DataFrame，只保留需要的列
normalized_data = pd.DataFrame({
    'Shimmer_FC32_TimestampSync_FormattedUnix_CAL': data['Shimmer_FC32_TimestampSync_FormattedUnix_CAL'],
    'Shimmer_FC32_GSR_Skin_Resistance_CAL_Normalized': gsr_normalized,
    'Shimmer_FC32_PPG_A13_CAL_Normalized': ppg_normalized
})

# 保存归一化后的数据到新的文件
output_file_path = 'normalized_time_gsr_ppg.txt'
normalized_data.to_csv(output_file_path, index=False)

print(f"归一化后的数据已保存到 {output_file_path}")
