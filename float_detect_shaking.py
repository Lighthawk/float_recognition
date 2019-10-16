import random
import time
from PIL import ImageGrab
import float_common
import float_yolov3

RANDOM_FILEID = random.randint(1, 10000)


def grab_screen(box=[]):
    img_grab = []
    if len(box) == 0:
        img_grab = ImageGrab.grab()
    else:
        img_grab = ImageGrab.grab(bbox=box)
    # img_grab.show()
    return img_grab


def float_gotfrom_grab_screen(net, meta, grab_box, remain_times):
    found_float = False
    img_float = []
    fbox = []

    while remain_times > 0:
        remain_times -= 1
        # img_grab = Image.open('tmp.jpg')  # test line
        img_grab = grab_screen(grab_box)
        filepath = './temps/tmp' + str(RANDOM_FILEID) + '.jpg'
        img_grab.save(filepath)
        fres, fimg, fbox = float_yolov3.detect_float(net, meta, img_grab, filepath)
        # fres, fimg, fbox = float_yolov3.detect_float(net, meta, img_grab)
        if len(fres) > 0:
            found_float = True
            img_float = img_grab.crop(fbox)
            break
        else:
            time.sleep(float_common.WAIT_TIME_NONE)
            continue
    return found_float, img_float, fbox, remain_times

#
# def float_shake(img_pre, img_cur, box_pre, box_cur):
#     diff = abs(box_cur[0] - box_pre[0]) + abs(box_cur[1] - box_pre[1]) + abs(img_cur.size[0] - img_pre.size[0])
#     print("diff = ", diff, ", box_pre = ", box_pre, ", box_cur = ", box_cur, ", wdf = ", img_cur.size[0] - img_pre.size[0])
#     if diff >= SHAKE_CRITICAL:
#         return True
#     else:
#         return False

def float_shake(img_pre, img_cur, box_pre, box_cur):
    pre_core = float_blue_leaf_core(img_pre, box_pre)
    cur_core = float_blue_leaf_core(img_cur, box_cur)

    diff = abs(cur_core[0] - pre_core[0]) + abs(cur_core[1] - pre_core[1])
    print("diff_float = ", diff)
    if abs(cur_core[0] - pre_core[0]) + abs(cur_core[1] - pre_core[1]) >= float_common.SHAKE_CRITICAL:
        return True
    else:
        return False


def float_blue_leaf_core(img, box):
    r_channel, g_channel, b_channel = img.split()
    color_hash = []
    for i in range(256):
        if i > float_common.BINARYZATION_THRESHOLD:
            color_hash.append(1)
        else:
            color_hash.append(0)
    img_bin = r_channel.point(color_hash, '1')
    # img_bin.show()
    sum_w = 0
    sum_h = 0
    cnt = 1
    # print("box = ", box, " ww = %d " % (box[2]-box[0]), "  hh = %d " % (box[3]-box[1]), " imgsize = ", img_bin.size, "\n")
    for wi in range(box[2] - box[0]):
        for hi in range(box[3] - box[1]):
            # 5("wi = %d " % wi, " hi = %d \n" % hi)
            if img_bin.getpixel((wi, hi)) >= 1:
                sum_w += wi + box[0]
                sum_h += hi + box[1]
                cnt += 1
    core_x = int(1.0 * sum_w / (1.0*cnt))
    core_y = int(1.0 * sum_h / (1.0*cnt))
    return [core_x, core_y]


def float_position(img, box):
    [tarx, tary] = float_blue_leaf_core(img, box)
    # [tarx, tary] = [int((box[0] + box[2])/2.0), int((box[1] + box[3])/2.0)]
    return tarx, tary


def test_func():
    picpath = "output/test/WoWScrnShot_060119_033015.jpg"
    net, meta = float_yolov3.init_yolov3()
    found_float, img_float, box, remain_times = float_gotfrom_grab_screen(net, meta, [], 18)

    x, y, w, h = box[0], box[1], box[2], box[3]
    floatx = img_float
    floatx.show()
    r, g, b = floatx.split()
    gray = floatx.convert("L")
    gray.show()
    r.show()
    g.show()
    b.show()

    hash2 = []
    for i in range(256):
        if i < float_common.BINARYZATION_THRESHOLD:
            hash2.append(0)
        else:
            hash2.append(1)
    imgBina = r.point(hash2, '1')
    imgBina.show()
    sumX = 0
    sumY = 0
    cnt = 0
    for xi in range(w):
        for yi in range(h):
            if imgBina[xi][yi] >= 1:
                sumX += xi + x
                sumY += yi + y
                cnt += 1
    [sumX, sumY] # 可以用来判定两张图蓝色叶子的总坐标绝对距离是否变化了，最终变成了重心的绝对位置是否变化了


