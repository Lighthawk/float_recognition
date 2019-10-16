#########################
#  每改完这个文件       #
#  需要重新运行bat文件  #
#########################

# 每隔多少秒截图一次，取值 0.2 到 1 之间任意小数，推荐 0.5
WAIT_TIME_GOT = 0.2        
WAIT_TIME_NONE = 1.0

# 每次钓鱼截图次数，WAIT_TIME 分别为 0.2, 0.5, 1 的时候，该参数分别为 70, 65, 50，其它时候就近取值
FLOAT_INTERVALS = 65    


# 二值化浮漂图像阈值，一般不用动的，要设置是 40 ~ 60之间的整数
# 40 对鱼漂晃动感知灵敏些，容易导致接下来 SHAKE_CRITICAL 数值容易偏大或偏小，提竿不一定准
BINARYZATION_THRESHOLD = 60  


# 浮漂晃动范围阈值，大于这个值就右键提竿
# 实际用的时候，如果鱼漂晃动，没有提竿，说明这个值太大了，需要改小
# 反之，如果鱼漂还没晃动，就提竿了，说明这个值太小了，需要该大
# 视角拉最近的话，这个数值基本是 15 到 20 之间的整数
# 视角拉远要改小，改多少要反复运行bat来尝试了
# 如果没有挂大鱼漂，小鱼漂应该也可以识别并提竿，这个数值可能是 5 左右
SHAKE_CRITICAL = 15          


# 暗月岛常用参数：WAIT_TIME 0.5, INTERVAL 65, THRESHOLD 60, SHAKE 15


# 按键表：
# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
FLOAT_KEY = 0x4C       # 'number5', 钓鱼技能快捷键
FLOAT_REFRESH = 0x4D   # 'number6', 挂大鱼漂快捷键


# 程序运行总时间，具体说是丢鱼漂的次数
# 20000次时间蛮久的，之前目测，半小时大概丢150次鱼漂，所以这个可以看情况随意改小
FLOAT_TIMES = 20000      


 # 换大鱼漂的时间间隔，按秒来算，1800秒为半小时。
 # 注意！这脚本起手不挂鱼漂       
FLOAT_CHANGE_BIG_TIME = 1800   


# float_control.py 第21行将行首井号删掉，代码上下对其，表示脚本起手挂大鱼漂
# 不太重要的选做功能就没太上心封装... 

