import cv2
import time

def show_fps():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 初始化帧率计数器和计时器
    frame_count = 0
    start_time = time.time()

    while True:
        # 读取视频流的帧
        ret, frame = cap.read()

        if ret:
            # 在帧上绘制当前的帧数
            cv2.putText(frame, f"FPS: {frame_count / (time.time() - start_time):.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 在窗口中显示帧
            cv2.imshow('Camera', frame)

            # 按下ESC键退出循环
            if cv2.waitKey(1) == 27:
                break

            # 更新帧率计数器
            frame_count += 1
        else:
            break

        # 检查窗口关闭事件
        if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
            break

    # 释放摄像头和关闭窗口
    cap.release()
    cv2.destroyAllWindows()

    # 打印帧率
    print("平均帧率: {:.2f}".format(frame_count / (time.time() - start_time)))

# 调用函数显示帧率
show_fps()
