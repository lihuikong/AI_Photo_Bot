import cv2
from perception.detector import PersonDetector

detector = PersonDetector()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # 调用封装好的接口
    annotated_frame, info, dt = detector.detect_and_track(frame)

    # 打印给成员B看的数据流：例如 ID 1 的中心点
    if info:
        print(f"追踪中: {info[0]['id']} 坐标: {info[0]['center']}")

    cv2.imshow("Scientist_Perception", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()