import torch
import time
from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # 1. 硬件自适应 (针对你的 MacBook M3 优化)
        if torch.backends.mps.is_available():
            self.device = 'mps'
        elif torch.cuda.is_available():
            self.device = '0'
        else:
            self.device = 'cpu'
            
        # 2. 加载模型
        self.model = YOLO(model_path)
        print(f"感知模块已就绪 | 设备: {self.device}")

    def detect_and_track(self, frame):
        """
        核心逻辑：执行感知并输出标准化数据
        """
        t_start = time.time()
        
        # 3. 运行追踪 (ByteTrack)
        results = self.model.track(
            frame, 
            conf=0.5, 
            persist=True, 
            classes=[0], 
            device=self.device,
            verbose=False,
            tracker="bytetrack.yaml"
        )
        
        t_end = time.time()
        latency = (t_end - t_start) * 1000  # 毫秒
        
        # 4. 数据解析：提取成员B需要的坐标
        tracked_objects = []
        result = results[0]
        
        if result.boxes.id is not None:
            # 获取 ID, 坐标(xywh)
            ids = result.boxes.id.cpu().numpy().astype(int)
            boxes = result.boxes.xywh.cpu().numpy() # 中心点x, y, 宽, 高
            
            for obj_id, box in zip(ids, boxes):
                x_center, y_center, w, h = box
                tracked_objects.append({
                    "id": int(obj_id),
                    "center": (int(x_center), int(y_center)),
                    "size": (int(w), int(h))
                })
                
        return result.plot(), tracked_objects, latency