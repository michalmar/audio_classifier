# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 10:07:11 2020

@author: kinga
"""

import os
import wave
import numpy as np
import pylab as plt
 
CutTimeDef = 5 #以5s截断文件
# CutFrameNum =0
 
cat = '1' 
folder_path = r".\data\headcold\Fault"
files = os.listdir(folder_path)
files = [folder_path + "\\" + f for f in files if f.endswith('.wav')]

 
def CutFile():
    for i in range(len(files)):
        FileName = files[i]
        print("CutFile File Name is ",FileName)
        f = wave.open(r"" + FileName, "rb")
        params = f.getparams()
        print(params)
        nchannels, sampwidth, framerate, nframes = params[:4]
        CutFrameNum = framerate * CutTimeDef
         # 读取格式信息
         # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte    单位）, 采
         # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
 
        print("CutFrameNum=%d" % (CutFrameNum))
        print("nchannels=%d" % (nchannels))
        print("sampwidth=%d" % (sampwidth))
        print("framerate=%d" % (framerate))
        print("nframes=%d" % (nframes))
        str_data = f.readframes(nframes)
        f.close()# 将波形数据转换成数组
        # Cutnum =nframes/framerate/CutTimeDef
        # 需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data.shape = -1, 2
        wave_data = wave_data.T
        temp_data = wave_data.T
        # StepNum = int(nframes/200)
        cut_len = CutFrameNum
        cut_num = 0;
        i_cut = 0
        while cut_num < nframes:
        # for j in range(int(Cutnum)):
            print("Stemp=%d" % (i_cut))
            FileName = os.path.join(folder_path, files[i][:-4] +"-"+ str(i_cut+1) + "-1.wav")
            print(FileName)
            temp_dataTemp = temp_data[cut_len * (i_cut):cut_len * (i_cut + 1)]
            i_cut = i_cut + 1;
            cut_num = i_cut * cut_len;
            temp_dataTemp.shape = 1, -1
            temp_dataTemp = temp_dataTemp.astype(np.short)# 打开WAV文档
            f = wave.open(FileName, "wb")#
            # 配置声道数、量化位数和取样频率
            f.setnchannels(nchannels)
            f.setsampwidth(sampwidth)
            f.setframerate(framerate)
             # 将wav_data转换为二进制数据写入文件
            f.writeframes(temp_dataTemp.tostring())
            f.close()
 
if __name__ == '__main__' :
    CutFile()
 
 
    print("Run Over")