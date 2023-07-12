import cv2
import paddlex as pdx
from playsound import playsound

# 修改模型所在位置
predictor = pdx.deploy.Predictor('smoke_model')
face_detector = pdx.deploy.Predictor('face_model')
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        face_result = face_detector.predict(frame)
        sf = face_result[0]['score'] if face_result else 0
        print(sf)
        vis_img = pdx.det.visualize(frame, face_result, threshold=0.4, save_dir=None)
        cv2.imshow('cigarette', vis_img)
        if sf > 0.6:
            result = predictor.predict(frame)
            score = result[0]['score'] if result else 0
            print(score)
            if score >= 0.7:
                print("*"*100)
                # 修改音频所在位置
                # playsound('beep.mp3')
            # print(result)
            vis_img = pdx.det.visualize(frame, result, threshold=0.6, save_dir=None)
            cv2.imshow('Smoking Detector', vis_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
