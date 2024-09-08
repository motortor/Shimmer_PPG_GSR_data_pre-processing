# Shimmer_PPG_GSR_data_pre-processing
这是一个针对Shimmer3 GSR+ Unit传感器收集到的GSR和PPG信号进行预处理的脚本，步骤可分为4步：

Here is a script for preprocessing GSR and PPG signals collected by the Shimmer3 GSR+ Unit sensor, which can be divided into 4 steps:

# 1. 删除无用的数据，选取特定列（Remove unnecessary data and select specific columns）
通过Consensys软件从Shimmer3 GSR+ Unit传感器收集到的原始数据包含如下内容：

The raw data collected from the Shimmer3 GSR+ Unit sensor through the Consensys software contains the following:
```
Shimmer_FC32_TimestampSync_FormattedUnix_CAL
Shimmer_FC32_Accel_LN_X_CAL
Shimmer_FC32_Accel_LN_Y_CAL
Shimmer_FC32_Accel_LN_Z_CAL
Shimmer_FC32_Battery_CAL
Shimmer_FC32_GSR_Range_CAL
Shimmer_FC32_GSR_Skin_Conductance_CAL
Shimmer_FC32_GSR_Skin_Resistance_CAL
Shimmer_FC32_Gyro_X_CAL
Shimmer_FC32_Gyro_Y_CAL
Shimmer_FC32_Gyro_Z_CAL
Shimmer_FC32_Mag_X_CAL
Shimmer_FC32_Mag_Y_CAL
Shimmer_FC32_Mag_Z_CAL
Shimmer_FC32_PPG_A13_CAL	
```
乍一看感觉很多，但如果只对GSR和PPG生理信号进行分析的话，只需要提取：

At first glance, it may seem like a lot, but if we are only analyzing the GSR and PPG physiological signals, we only need to extract:
```
Shimmer_FC32_TimestampSync_FormattedUnix_CAL （Unix时间戳）
Shimmer_FC32_GSR_Skin_Resistance_CAL （皮肤电阻数据）
Shimmer_FC32_PPG_A13_CAL （光体积描记法数据）
```
这3行就足够了。
运行第一个"1 delete useless.py"代码，就可以将需要的数据从原始数据"DefaultTrial_Session35_Shimmer_FC32_Calibrated_PC.txt"提取并保存到"time_gsr_ppg.txt"文件中。

These three lines are enough.
By running the first script, "1 delete useless.py", the necessary data will be extracted from the raw data file "DefaultTrial_Session35_Shimmer_FC32_Calibrated_PC.txt" and saved to the "time_gsr_ppg.txt" file.

# 2. 对数据进行归一化（Perform data normalization）
运行第二个"2 normalized.py"代码，将会对从文件"time_gsr_ppg.txt"中读取的 GSR(皮肤电反应) 和PPG (脉搏波) 数据进行预处理，包括读取数据、数据类型转换为浮点型 (float)、计算最大最小值、归一化处理等操作。

Running the second script, "2 normalized.py", will preprocess the GSR (Galvanic Skin Response) and PPG (Photoplethysmogram) data read from the "time_gsr_ppg.txt" file. This includes reading the data, converting the data types to float, calculating the maximum and minimum values, and performing normalization operations.
```
gsr_normalized = (gsr_data - gsr_min) / (gsr_max - gsr_min)
ppg_normalized = (ppg_data - ppg_min) / (ppg_max - ppg_min)
```
使用最小-最大归一化方法将GSR和PPG数据转换到[0,1]区间。这个过程是通过减去最小值再除以最大值与最小值的差值来实现的。
最后将归一化后的数据保存到"normalized_time_gsr_ppg.txt"文件中。

Using the min-max normalization method, the GSR and PPG data are scaled into the [0,1] range. This is achieved by subtracting the minimum value and then dividing by the difference between the maximum and minimum values.
Finally, the normalized data is saved to the "normalized_time_gsr_ppg.txt" file.

# 3.按照时间戳切割数据
在上一个[音乐播放器](https://github.com/motortor/Music-Player-with-Rating-Functionality)的项目中，我们已经可以记录实验者收听音乐时，对应的开始和结束的时间戳。
第三个代码针对上一个项目结果的输出格式，读取其中的歌曲播放记录，包括歌曲ID、开始和结束时间，以及满意度fitness。
然后对照播放记录，从"normalized_time_gsr_ppg.txt"文件中提取出每首歌在特定时间范围内的GSR和PPG数据，并将这些数据分别保存到GSR和PPG文件夹中，并以对应歌曲的名称命名txt文件。
值得一提的是，由于在我设计的音乐播放器中，所有音乐切片的时长均为30秒，所以提取出的所有数据文件的大小应该几乎一致。

In the previous [Music Player](https://github.com/motortor/Music-Player-with-Rating-Functionality) project, we were already able to record the timestamps corresponding to the start and end times when participants listened to music.
The third script, based on the output format of the previous project, reads the music playback records, including the song ID, start and end times, and the satisfaction level (fitness). 
Then, according to the playback records, the script extracts the GSR and PPG data within the specific time range for each song from the "normalized_time_gsr_ppg.txt" file and saves this data into the GSR and PPG folders, naming the txt files according to the corresponding song names.
It is worth mentioning that, since all music clips in the music player I designed are 30 seconds long, the size of all extracted data files should be nearly identical.
