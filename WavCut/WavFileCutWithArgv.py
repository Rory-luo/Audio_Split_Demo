#encoding=utf-8
import sys
import NEWCutWavFile
from loguru import logger

def Split_Audio_Algo():
    First_Argv  = str(sys.argv[1])

    NEWCutWavFile.SetFileName(First_Argv)

    NEWCutWavFile.CutFile()

    logger.warning("Run Over")

if __name__ == "__main__":
    logger.add("log_{time}.log", rotation="500 MB", retention="7 days")   # 将所有的记录全都写入日志文件中查看
    """
    log_{ time }.log 表示按照执行代码的时间生成日志文件
    rotation  表示文件过大就会重新生成一个文件;
    retention 表示一段时间后会清空该文件
    """

    Split_Audio_Algo()
