import time
import float_common
import float_yolov3
import float_detect_shaking
import float_keyboard
import float_mouse


# GRAB_BOX = [100, 100, 1800, 800]
GRAB_BOX = [5, 5, 1910, 1070]

time.sleep(5)


# 大概 cnt 减少 150 次，一个大鱼漂
def fish_control():
    float_refresh = time.process_time()
    cnt = float_common.FLOAT_TIMES
    net, meta = float_yolov3.init_yolov3()
    # 挂大鱼漂
    # float_keyboard.UseSkillAndWait(float_common.FLOAT_REFRESH, 3)
	
    # 第一次抛竿钓鱼
    float_keyboard.UseSkillAndWait(float_common.FLOAT_KEY, 2)
	
    while cnt > 0:
        cnt -= 1
        remain_times = float_common.FLOAT_INTERVALS
        if (time.clock() - float_refresh) > float_common.FLOAT_CHANGE_BIG_TIME:
            time.sleep(22)
            float_refresh = time.clock()
            float_keyboard.UseSkillAndWait(float_common.FLOAT_REFRESH, 3)
        # print("cnt = %d" % cnt, "  , remain_times = %d" % remain_times, " float_refresh_interval = ", time.clock() - float_refresh)
        float_keyboard.UseSkillAndWait(float_common.FLOAT_KEY, 2)
        [found_float, float_cur, box_cur, remain_times] = \
                float_detect_shaking.float_gotfrom_grab_screen(net, meta, GRAB_BOX, remain_times)

        if (found_float is False) or (remain_times <= 0):
            continue

        while remain_times > 0:
            time.sleep(float_common.WAIT_TIME_GOT)
            remain_times -= 1
            # print("remain_times = %d" % remain_times)
            float_pre = float_cur
            box_pre = box_cur

            [found_float, float_cur, box_cur, remain_times] = \
                    float_detect_shaking.float_gotfrom_grab_screen(net, meta, GRAB_BOX, remain_times)

            if (found_float is False) or (remain_times <= 0):
                break
            got_fish = float_detect_shaking.float_shake(float_pre, float_cur, box_pre, box_cur)
            if got_fish is True:
                print("got_fish = True")
                fx, fy = float_detect_shaking.float_position(float_cur, box_cur)
                # fx2, fy2 = float_recognition.float_position(float_pre, box_pre)
                float_mouse.RightClick(GRAB_BOX[0] + fx, GRAB_BOX[1] + fy)
                break
    return


if __name__ == '__main__':
    fish_control()



