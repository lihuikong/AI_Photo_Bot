# AI_Photo_Bot

## 📖 项目简介

基于深度学习的智能摄影机器人，能够自动识别、跟随目标并完成拍摄任务。

**核心功能**：
- 实时人体检测与跟踪
- 自主运动控制与跟随
- 智能拍照时机判断

**技术栈**：
- 目标检测：YOLOv8
- 硬件平台：Jetson Orin Nano + 树莓派4B
- 通信框架：ROS2 Humble
- 开发语言：Python 3.10

---

## 🎯 项目目标

**短期（MVP）**：
- ✅ 实时目标检测（已完成）
- 🔄 目标跟踪算法（进行中）
- ⏳ 运动控制（待开发）

**长期**：
- 全地形跟随能力
- 智能构图优化
- 多模态交互

---

## 🚀 快速开始

### 环境要求
- Ubuntu 22.04
- Python 3.10+
- CUDA 11.8+（Jetson平台）

### 安装依赖
```bash
# 克隆仓库
git clone https://github.com/你的用户名/ai-photo-robot.git
cd ai-photo-robot

# 安装Python依赖
pip install -r requirements.txt

# 下载YOLOv8模型
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

### 运行示例
```bash
# 测试目标检测
python src/detection.py

# 运行完整系统（需要硬件）
python src/main.py
```

---

## 📁 项目结构
```
ai-photo-robot/
├── src/                    # 源代码
│   ├── detection.py        # 目标检测模块
│   ├── tracker.py          # 目标跟踪模块
│   ├── controller.py       # 运动控制模块
│   ├── communication.py    # 通信模块
│   └── main.py            # 主程序入口
├── tests/                  # 测试代码
├── docs/                   # 文档
├── requirements.txt        # 依赖清单
└── README.md              # 项目说明
```

---

## 👥 团队分工

| 成员 | 负责模块 | 进度 |
| 李思成 | 目标检测与跟踪 ||
| 程威 | 运动控制 ||
| 张雨豪 | 系统架构与通信 ||

---

## 🔧 开发指南

### 代码规范
- 使用PEP 8编码风格
- 函数必须写docstring
- 提交代码前运行测试

### Git工作流
```bash
# 1. 更新代码
git pull

# 2. 创建分支开发
git checkout -b feature-xxx

# 3. 提交代码
git add .
git commit -m "feat: 添加XX功能"
git push origin feature-xxx

# 4. 在GitHub上发起Pull Request
```

### 提交信息规范
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `test:` 测试相关

---

## 📊 系统架构
```
[相机] → [目标检测] → [目标跟踪] → [运动控制] → [底盘驱动]
                ↓
            [拍照决策]
```

---

## 🎬 演示视频

[点击查看演示视频](链接待补充)

---

## 📝 开发日志

### 2025-01-27
- ✅ 初始化项目结构
- ✅ 完成YOLOv8检测模块
- 🔄 调试跟踪算法

### 2025-01-20
- ✅ 项目立项
- ✅ 硬件选型完成

---

## 🐛 已知问题

- [ ] 低光照环境检测精度下降
- [ ] 快速运动时跟踪偶尔丢失
- [ ] 树莓派与Jetson通信延迟较高

---

## 🔮 未来计划

- [ ] 添加深度估计功能
- [ ] 实现多目标优先级选择
- [ ] 开发Web控制界面
- [ ] 支持语音指令控制

---

## 📚 参考资料

- [YOLOv8官方文档](https://docs.ultralytics.com)
- [ROS2教程](https://docs.ros.org)
- [Jetson开发指南](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit)

---

## 📄 许可证

MIT License

---

## 📧 联系方式

- 项目负责人：李思成
- 成员：程威、张雨豪
- 邮箱：3324567099@qq.com
- GitHub：[@lihuikong](https://github.com/lihuikong)