# float_recognition
pytorch 下 darknet yolov3-voc 检测目标图像鱼漂float，linux训练完成后移植到win10使用，GTX1070，GTX1050Ti 实时

## 唤醒AI之路的处女作
应老友之托，写个自动化脚本，各种机缘巧合，选了某VideoGame中实时监测float的课题，并用传统图像处理方法判断其是否摇动。  
正直AI应用和新闻井喷，好奇，试下，很强，各种强！  

## 课题思路
1、ubuntu16.04 搭建 gpu 版 pytorch，选择实时性好的 yolov3 方法，由于有现成的 darknet 超强工具，直接用了里面准确率较高的 yolov3-voc 模型；  
2、取 VideoGame 截屏，yolov3 检测 float 的 roi 位置；  
3、opencv 在 float的 roi 里，定位 float 深蓝像素块重心坐标；  
4、连续帧图像，float 深蓝重心摇动超过阈值，认为 float 剧烈摇晃，并进行一次鼠标和键盘操作；  
5、实用驱使，需要在 win10 上跑起来，全工程复制至 win10 英文路径后，根据文档用准备好 opencv 和 darknet，VS2015 release下编译 yolo_cpp_dll.dll（gpu 版），opencv 版本不要太低，成功的是当时的最新版 opencv410；  
6、进行鼠标和键盘操作需要额外不常用的 api，这里 pygui 可以满足需求，不过，有顾忌的地方，用的 ctypes 里的 SendInput。应老友，这部分不放代码。  

## 注意
1、VideoGame 的原因，使用 SendInput 需要将 DirectX 中的 pthreadGC2.dll 和 pthreadVC2.dll 放到 dll 库中；  
2、实用仍然用到了 cuda 和 cudnn，目标计算机中要安装，版本看显卡。yolov3 编译环境是 cuda9 ，直接移植到安装了 cuda10 的目标电脑上运行没啥问题，需要在 VCdll 里，放入了当时编译用到的 cuda9 相关 dll 文件； 
3、关于2中目标电脑安装 cuda10 而不是 9，主要是测试电脑是 1050Ti 和 1050 的笔记本，未知原因无法安装 cuda9，所以多了3个庞大的 dll；    
4、删减代码后，最占用硬盘空间的是训练后的网络模型文件，后虽然尝试用更小的 yolov3-tiny 模型，但模型依赖文件需要翻墙下载，当时没有条件就没深入做更迷你的网络。后果就是 GTX1050 的显卡上会爆显存（2G，1050TI是4G），多300M；  
5、第一次做实用目标识别，并没有算法上的创新，但明显感觉当前深度学习对硬件的依赖过高，尝试做了一次调包侠，被夸奖了，很开心 :)  
n、pytorch 下的 darknet 好好用，没有特别麻烦的地方；  
