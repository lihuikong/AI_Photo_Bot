import cv2
from ultralytics import YOLO

# 1. 加载模型（第一次运行会自动下载，约 6MB）
model = YOLO('yolov8n.pt') 

# 2. 打开 Mac 摄像头 (0 通常是内置摄像头)
cap = cv2.VideoCapture(0)

print("正在启动感知模块... 按 'q' 键退出")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 3. 实时推理：识别画面中的物体
    results = model(frame, conf=0.5,verbose = False)

    # 4. 将识别结果画在画面上
    annotated_frame = results[0].plot()

    # 5. 显示窗口
    cv2.imshow("AI_Photo_Bot_Perception", annotated_frame)

    # 按 'q' 退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()