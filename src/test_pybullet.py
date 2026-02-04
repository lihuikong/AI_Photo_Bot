import pybullet as p
import pybullet_data
import time
import numpy as np
import sys
import os
import select
class CarController:
    def __init__(self):
        """初始化小车控制器"""
        # 控制参数
        self.speed = 0.0      # 速度：正数前进，负数后退
        self.steer = 0.0      # 转向：-1左转，1右转
        self.max_speed = 30   # 最大速度
        self.max_steer = 0.5  # 最大转向角度
        
        # 小车关节
        self.drive_joints = [2, 3, 5, 7]  # 驱动轮
        self.steer_joints = [4, 6]        # 转向轮
        
        # 初始化
        self.init_simulation()
        self.setup_car()
        
        print("\n" + "="*50)
        print("小车控制说明:")
        print("="*50)
        print("W / ↑ : 前进加速")
        print("S / ↓ : 后退加速")
        print("A / ← : 左转")
        print("D / → : 右转")
        print("空格键: 刹车/停止")
        print("R     : 重置位置")
        print("Q     : 退出")
        print("="*50)
        print("\n开始控制...")
    
    def init_simulation(self):
        """初始化仿真环境"""
        self.physics_client = p.connect(p.GUI)
        
        # 设置搜索路径
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        
        # 设置重力
        p.setGravity(0, 0, -9.8)
        
        # 加载地面
        p.loadURDF("plane.urdf")
        
        # 设置相机
        p.resetDebugVisualizerCamera(
            cameraDistance=5,
            cameraYaw=0,
            cameraPitch=-30,
            cameraTargetPosition=[0, 0, 0]
        )
    
    def setup_car(self):
        """设置小车"""
        # 加载小车
        start_pos = [0, 0, 0.1]
        start_orientation = p.getQuaternionFromEuler([0, 0, 0])
        self.car_id = p.loadURDF(
            "racecar/racecar.urdf",
            start_pos,
            start_orientation
        )
        
        # 设置轮子摩擦力
        for joint in self.drive_joints:
            p.changeDynamics(self.car_id, joint, lateralFriction=2.0)
    
    def apply_controls(self):
        """应用控制命令"""
        # 1. 转向控制
        for joint in self.steer_joints:
            p.setJointMotorControl2(
                self.car_id,
                joint,
                p.POSITION_CONTROL,
                targetPosition=self.steer * self.max_steer,
                force=10.0,
                maxVelocity=10.0
            )
        
        # 2. 速度控制
        for joint in self.drive_joints:
            p.setJointMotorControl2(
                self.car_id,
                joint,
                p.VELOCITY_CONTROL,
                targetVelocity=self.speed,
                force=20.0
            )
    
    def get_keyboard_input(self):
        """获取键盘输入（跨平台）"""
        try:
            # Windows
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                return key
        except:
            try:
                # Linux/Mac
                import termios
                import tty
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                        key = sys.stdin.read(1)
                        return key.lower()
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass
        return None
    
    def print_status(self, step):
        """打印状态信息"""
        # 获取小车状态
        pos, orn = p.getBasePositionAndOrientation(self.car_id)
        lin_vel, ang_vel = p.getBaseVelocity(self.car_id)
        speed = np.sqrt(lin_vel[0]**2 + lin_vel[1]**2)
        
        # 清屏并显示
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*60)
        print("实时控制状态")
        print("="*60)
        print(f"步数: {step:6d} | 时间: {step/240:6.1f}s")
        print(f"速度: {self.speed:6.1f} rad/s | 转向: {self.steer:6.2f}")
        print(f"实际速度: {speed:6.2f} m/s")
        print(f"位置: X={pos[0]:6.2f}, Y={pos[1]:6.2f}, Z={pos[2]:6.2f}")
        print("-"*60)
        print("控制说明: W=前进 S=后退 A=左转 D=右转 空格=刹车 R=重置 Q=退出")
        print("="*60)
    
    def run(self):
        """主循环"""
        step = 0
        
        while True:
            # 处理键盘输入
            key = self.get_keyboard_input()
            
            if key:
                if key == 'q':
                    print("\n退出程序...")
                    break
                elif key == 'w' or key == '\x1b[A':  # W 或 上箭头
                    self.speed = min(self.max_speed, self.speed + 5)
                    print("↑ 前进加速")
                elif key == 's' or key == '\x1b[B':  # S 或 下箭头
                    self.speed = max(-self.max_speed, self.speed - 5)
                    print("↓ 后退加速")
                elif key == 'a' or key == '\x1b[D':  # A 或 左箭头
                    self.steer = max(-1.0, self.steer - 0.2)
                    print("← 左转")
                elif key == 'd' or key == '\x1b[C':  # D 或 右箭头
                    self.steer = min(1.0, self.steer + 0.2)
                    print("→ 右转")
                elif key == ' ':  # 空格键
                    self.speed = 0
                    self.steer = 0
                    print("⏹ 停止/刹车")
                elif key == 'r':  # 重置
                    self.reset_car()
                    print("🔄 重置位置")
            
            # 应用控制
            self.apply_controls()
            
            # 仿真步进
            p.stepSimulation()
            
            # 显示状态
            if step % 10 == 0:
                self.print_status(step)
            
            # 相机跟随
            if step % 20 == 0:
                pos, _ = p.getBasePositionAndOrientation(self.car_id)
                p.resetDebugVisualizerCamera(
                    cameraDistance=5,
                    cameraYaw=0,
                    cameraPitch=-30,
                    cameraTargetPosition=pos
                )
            
            step += 1
            time.sleep(1/240.0)
        
        # 清理
        p.disconnect()
    
    def reset_car(self):
        """重置小车"""
        # 重置位置和方向
        p.resetBasePositionAndOrientation(
            self.car_id,
            [0, 0, 0.1],
            p.getQuaternionFromEuler([0, 0, 0])
        )
        
        # 重置速度
        p.resetBaseVelocity(self.car_id, [0, 0, 0], [0, 0, 0])
        
        # 重置控制
        self.speed = 0
        self.steer = 0

# 运行控制程序
if __name__ == "__main__":
    controller = CarController()
    controller.run()