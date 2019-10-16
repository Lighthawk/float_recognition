
from ctypes import *
import os
import random
import time
import cv2
from PIL import Image
import numpy as np


def sample(probs):
    s = sum(probs)
    probs = [a / s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs) - 1


def c_array(ctype, values):
    arr = (ctype * len(values))()
    arr[:] = values
    return arr


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

os.environ['path'] += ';./VCdll'
lib = CDLL("./VCdll/yolo_cpp_dll.dll", RTLD_GLOBAL)

lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


# 不传入path，直接传入 PIL 图片，但是检测内存是否连续+格式转换，导致 detect 时间翻倍了。。。
# GTX 1070 CUDA9.0 一张图0.08s左右，但是这样改一张0.15s左右
# 可能这样的转的思路不太对，可是一直读写同一张图片，不知道对硬盘有没有不好的影响
def load_image_python(imgPIL):
    # imgPIL = Image.open('tmp.jpg')
    imgCv = cv2.cvtColor(np.asarray(imgPIL), cv2.COLOR_RGB2BGR)
    im = IMAGE()
    im.w = c_int(imgCv.shape[0])
    im.h = c_int(imgCv.shape[1])
    im.c = c_int(imgCv.shape[2])
    imgCv = 1.0 * imgCv / 255.0
    # cv2.imshow('dd', imgCv)
    # cv2.waitKey(0)
    if not imgCv.flags['C_CONTIGUOUS']:
        imgCv = np.ascontiguous(imgCv, dtype=imgCv.dtype)  # 如果不是C连续的内存，必须强制转换
    im.data = cast(imgCv.ctypes.data, POINTER(c_float))    # 转换为ctypes，这里转换后的可以直接利用ctypes转换为c语言中的int*，然后在c中使用
    return im


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
# def detect(net, meta, imgPIL, thresh=.5, hier_thresh=.5, nms=.45):
    fp_img = open(image, 'r')
    im = load_image(image, 0, 0)
    # im = load_image_python(imgPIL)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum, 0)
    num = pnum[0]
    if (nms): do_nms_obj(dets, num, meta.classes, nms)

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)
    fp_img.close()
    return res


def load_yolov3darknet():
    net = load_net(b"./input/float_yolov3voc.cfg", b"./input/float_yolov3voc_1400.weight", 0)
    meta = load_meta(b"./input/yolov3_voc.data")
    return net, meta


def detect_float(net, meta, img_grab, picpath):
# def detect_float(net, meta, img_full):
#     img_grab = Image.open(picpath)
    t0 = time.clock()
    res = detect(net, meta, picpath.encode('utf-8'))
    # res = detect(net, meta, img_grab)
    t1 = time.clock()
    print(res, ' costs_time = ', t1 - t0)

    if len(res) == 0:
        return [[], [], []]

    x = res[0][2][0]
    y = res[0][2][1]
    w = res[0][2][2]
    h = res[0][2][3]
    left = int(x - w / 2.0)
    right = left + int(w)
    upper = int(y - h / 2.0)
    lower = upper + int(h)

    box = (left, upper, right, lower)
    # print('box = ', box)
    img = img_grab.crop(box)  # 截取浮漂子图像
    # img.show()

    return res, img, box


def init_yolov3():
    net, meta = load_yolov3darknet()
    return net, meta


def test_func():
    net, meta = load_yolov3darknet()
    picpath = "output/test/WoWScrnShot_060119_033015.jpg"
    res, img, box = detect_float(net, meta, picpath)

