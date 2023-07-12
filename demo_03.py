import cv2
import paddlex as pdx
import pygame
import time
import threading

class VideoThread(threading.Thread):
    def __init__(self, cap, predictor):
        threading.Thread.__init__(self)
        self.cap = cap
        self.predictor = predictor
        self.fps = 0
        self.start_time = time.time()
        self.frame_interval = 2  # 每隔2帧进行一次处理或显示

    def run(self):
        frame_count = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame_count += 1

                if frame_count % self.frame_interval == 0:
                    result = self.predictor.predict(frame)
                    score = result[0]['score'] if result else 0

                    self.fps = 1.0 / (time.time() - self.start_time)
                    self.start_time = time.time()

                    print(score)
                    if score >= 0.3:
                        print("*" * 100)
                        cv2.putText(frame, 'SMOKING WARNING!!!', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # 添加文字提示

                        # 在子线程中播放警报声音
                        sound_thread = SoundThread('beep.mp3')
                        sound_thread.start()

                    vis_img = pdx.det.visualize(frame, result, threshold=0.5, save_dir=None)

                    cv2.putText(vis_img, f'FPS: {self.fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    cv2.imshow('Smoking Detector', vis_img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

class SoundThread(threading.Thread):
    def __init__(self, sound_file):
        threading.Thread.__init__(self)
        self.sound_file = sound_file

    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound_file)
        pygame.mixer.music.play()

cap = cv2.VideoCapture(0)
predictor = pdx.deploy.Predictor('smoke_model')

video_thread = VideoThread(cap, predictor)
video_thread.start()

# 等待视频线程结束
video_thread.join()

cap.release()
cv2.destroyAllWindows()