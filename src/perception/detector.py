import cv2
import torch
from ultralytics import YOLO

# 1. 设备自适应
if torch.cuda.is_available():
    device = '0'
elif torch.backends.mps.is_available():
    device = 'mps'
else:
    device = 'cpu'

print(f"系统逻辑检查：正在使用 [ {device} ] 设备进行加速")

# 2. 加载模型
model = YOLO('yolov8n.pt') 

# 3. 打开摄像头
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if device == '0' else cv2.VideoCapture(0)

print("正在启动感知模块... 目标限制：仅限人体 (Person) | 按 'q' 键退出")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 4. 核心跟踪逻辑（关键修改）
    results = model.track(
        frame, 
        conf=0.5,           # 置信度阈值
        verbose=False,      # 关闭打印
        classes=[0],        # 只检测人
        device=device,      # 设备
        persist=True,       # 保持跟踪ID（重要！）
        tracker="bytetrack.yaml"  # 显式指定ByteTrack（可选，默认就是）
    )

    # 5. 渲染与显示
    annotated_frame = results[0].plot()
    
    # 获取人数和跟踪ID
    person_count = len(results[0].boxes)
    
    # 显示每个人的跟踪ID
    if results[0].boxes.id is not None:  # 检查是否有跟踪ID
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)
        cv2.putText(annotated_frame, f"People: {person_count} | IDs: {track_ids.tolist()}", 
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(annotated_frame, f"People: {person_count}", 
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Universal_Scientist_Perception_V1", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()