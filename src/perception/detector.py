import torch
import time
from ultralytics import YOLO  # type: ignore

class PersonDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # 1. 第一性原理：硬件自适应。优先使用 MPS 加速
        if torch.backends.mps.is_available():
            self.device = 'mps'
        elif torch.cuda.is_available():
            self.device = '0'
        else:
            self.device = 'cpu'
            
        # 2. 加载模型
        self.model = YOLO(model_path)
        print(f"感知模块初始化成功 | 运行设备: {self.device}")

    def detect_and_track(self, frame):
        """
        核心逻辑：执行检测并返回归一化后的数据。
        解决 Pylance 的 None 类型报错及 ndarray 属性报错。
        """
        t_start = time.time()
        
        # 3. 运行追踪 (ByteTrack)
        # classes=[0] 确保仅检测人 (Person)
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
        
        # 4. 数据解析与归一化
        tracked_objects = []
        result = results[0]
        img_h, img_w = frame.shape[:2]
        
        # 显式判定：只有当检测结果存在且包含 ID 时才执行解析逻辑
        if result.boxes is not None and result.boxes.id is not None:
            # 这里的顺序极其重要：先将 Tensor 移至 cpu，再转为 numpy 或 list
            # 避免出现 "ndarray has no attribute cpu" 的错误
            ids = result.boxes.id.int().cpu().tolist()
            boxes = result.boxes.xywh.cpu().numpy() # 矩形框数据：[x_center, y_center, width, height]
            
            for obj_id, box in zip(ids, boxes):
                # 归一化坐标计算 (0.0 - 1.0)
                # 这为成员 B 的 PID 控制提供了与分辨率无关的确定性输入
                norm_x = round(box[0] / img_w, 3)
                norm_y = round(box[1] / img_h, 3)
                norm_w = round(box[2] / img_w, 3)
                norm_h = round(box[3] / img_h, 3)
                
                tracked_objects.append({
                    "id": int(obj_id),
                    "rel_center": (norm_x, norm_y), # 归一化中心点坐标
                    "abs_center": (int(box[0]), int(box[1])), # 像素级中心点坐标
                    "rel_size": (norm_w, norm_h) # 归一化尺寸
                })
                
        # 返回渲染后的画面、结构化数据列表、以及推理延迟
        return result.plot(), tracked_objects, latency