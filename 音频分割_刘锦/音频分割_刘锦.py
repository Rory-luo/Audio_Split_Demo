from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from loguru import logger
import socket     ## 获取IP地址的包

"""# 判断文件夹是否存在，如果不存在就创建"""
def create_dir(FileDir):
    """

    :param FileDir:
    :return:
    """
    res = os.path.exists(FileDir)
    if not res:
        os.makedirs(FileDir)
        logger.warning(f"Created {FileDir} Directory Successfully")
    else:
        logger.warning(f"{FileDir} is existed.")

def GetIP():
    """

    :return: ip
    """
    # 获取计算机名
    name = socket.gethostname()
    # 通过计算机名获取ip
    ip = socket.gethostbyname(name)
    return ip

def DealAudio(sound, audio_file):
    """

    :param sound: 音频文件的存储格式
    :param audio_file: 音频文件
    :return chunks: 音频片段的集合
    """
    # 拆分音频片段，存储在 chunks 变量中
    chunks = split_on_silence(sound,
                              # 必须保持沉默至少半秒钟,沉默半秒判定为有静音，就作为分割点
                              min_silence_len=500,
                              # 如果它比-45 dBFs更安静，则认为它是无声的。
                              silence_thresh=-45,
                              keep_silence=400
                              )
    logger.warning(f'拆分 {audio_file}，共得到 {len(chunks)} 个分段')

    # 放弃长度小于1秒的录音片段
    for i in list(range(len(chunks)))[::-1]:
        if len(chunks[i]) <= 1000 or len(chunks[i]) >= 100000:
            chunks.pop(i)
    logger.warning(f'放弃长度小于 1 秒的录音片段后，得到 {len(chunks)} 段小于1s或者大于100s的有效分段')

    return chunks

def CutFile():
    """

    :return:
    """
    global input_path, output_path
    create_dir(output_path)               # 判断并创建文件夹
    all_list = os.listdir(input_path)  # 用于返回指定的文件夹包含的文件或文件夹的名字的列表。

    # 遍历所以需要分割的音频文件长度
    for i in range(len(all_list)):
        # 开始拼接输入路径
        out_name = all_list[i][:-4]                         # 音频文件的完整名称
        each_file_dir = output_path + "/" + out_name
        create_dir(each_file_dir)                           # 为每个音频文件创建单独的文件夹
        file_name = input_path + "/" + all_list[i]          # 路径拼接
        ip = GetIP()                                        # 获取当前计算机的ip地址
        ex_name = ip + "_0_" + out_name                     # 输出路径拼接

        sound = AudioSegment.from_mp3(file_name)            # 读取输入音频

        chunks = DealAudio(sound, all_list[i])              # 获取拆分的音频组

        # 设置保存路径
        for chunk_count, chunk in enumerate(chunks):

            save_path = each_file_dir + '/' + ex_name + '_' + str(chunk_count) +".wav"   # 保存路径
            chunk.export(save_path, format="wav")
            logger.info(f"file_number={int(chunk_count) + 1}")
            logger.debug(f"Output FileName is {save_path}")

def Split_Audio_Algo():
    CutFile()
    logger.warning("Run Over")


if __name__ == "__main__":
    input_path = "./input"                  # 输入原始音频路径
    output_path = "./output"                # 分割以后需要保存的音频路径

    Split_Audio_Algo()                      # 调用分割音频算法
