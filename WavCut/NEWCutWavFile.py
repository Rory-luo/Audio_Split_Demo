#encoding=utf-8
import os
import wave
import numpy as np
import sys

from loguru import logger

CutTimeDef = 240       # 以240ms截断文件
CutFrameNum = 0
musicPrimaryName = sys.argv[1]
FileDir = sys.argv[2]

FileName = musicPrimaryName

def create_dir(FileDir):
    res = os.path.exists(FileDir)
    if not res:
        os.makedirs(FileDir)
        logger.warning(f"Created {FileDir} Directory Successfully")
    else:
        logger.warning(f"{FileDir} is existed.")


def SetFileName(WavFileName):
    global  FileName
    logger.info(F"SetFileName File Name is {FileName}")
    FileName = WavFileName

def CutFile():
    global  FileName
    logger.info(F"CutFile File Name is {FileName}")

    # 打开wav文件 ，open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据。
    f = wave.open(r"" + FileName, "rb")

    # 读取格式信息
    # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
    # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    CutFrameNum = framerate * CutTimeDef / 1000
    logger.info(F"CutFrameNum={CutFrameNum}")
    logger.info(F"nchannels={nchannels}")
    logger.info(f"sampwidth={sampwidth}")
    logger.info(f"framerate={framerate}")
    logger.info(f"nframes={nframes}")
    str_data = f.readframes(nframes)
    f.close()                                   # 将波形数据转换成数组

    # 需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    temp_data = wave_data.T
    # StepNum = int(nframes/200)
    StepNum = int(CutFrameNum)
    StepTotalNum = 0
    haha = 0
    create_dir(FileDir)
    file_name_ = FileName.split(".wav")[0]
    FileDir_ = FileDir + '/' + file_name_
    create_dir(FileDir_)

    while StepTotalNum < nframes:
        logger.info(f"file_step={int(haha)}")
        FileName = FileDir_ + '/' + "0_" + "SampleVoice_" + str(haha) + ".wav"
        logger.debug(f"Output FileName is {FileName}")
        temp_dataTemp = temp_data[StepNum * (haha):StepNum * (haha + 1)]
        haha = haha + 1
        StepTotalNum = haha * StepNum

        temp_dataTemp.shape = 1, -1
        temp_dataTemp = temp_dataTemp.astype(np.short)  # 打开WAV文档
        f = wave.open(r"" + FileName, "wb")  #
        # 配置声道数、量化位数和取样频率
        f.setnchannels(nchannels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        # 将wav_data转换为二进制数据写入文件
        f.writeframes(temp_dataTemp.tostring())
        f.close()
