import pandas as pd

# 读取csv文件
data = []
with open('raw data/DefaultTrial_Session35_Shimmer_FC32_Calibrated_PC.txt', 'r') as file:
    for line in file:
        data.append(line.strip().split('\t'))

# 将数据创建为DataFrame
df = pd.DataFrame(data[2:], columns=data[1])

# 选择特定列
columns_to_keep = [
    'Shimmer_FC32_TimestampSync_FormattedUnix_CAL',
    'Shimmer_FC32_GSR_Skin_Resistance_CAL',
    'Shimmer_FC32_PPG_A13_CAL'
]
df = df[columns_to_keep]

# 保存DataFrame为txt文件
df.to_csv('time_gsr_ppg.txt', index=False)
