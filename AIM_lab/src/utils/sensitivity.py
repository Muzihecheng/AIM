import pygame
import ctypes
import win32api
import win32con

class MouseControls:
    """鼠标控制类"""
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_ABSOLUTE = 0x8000
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1

    def move_relative(self, x, y):
        """相对移动鼠标"""
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)

    def get_position(self):
        """获取鼠标位置"""
        return win32api.GetCursorPos()

class SensitivityManager:
    def __init__(self):
        self.sensitivity = 1.0
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        
        # 获取窗口和屏幕信息
        self.window = pygame.display.get_surface()
        self.window_pos = self.window.get_abs_offset()
        self.center_x = self.window.get_width() // 2
        self.center_y = self.window.get_height() // 2
        
        # 设置初始鼠标位置和准心位置
        self.global_center = (self.window_pos[0] + self.center_x, 
                            self.window_pos[1] + self.center_y)
        win32api.SetCursorPos(self.global_center)
        
        # 用于跟踪准心位置
        self.crosshair_x = float(self.center_x)
        self.crosshair_y = float(self.center_y)
        
        # 存储上一次的鼠标位置
        self.last_mouse_pos = pygame.mouse.get_pos()
        
        # 获取设置
        from src.settings import Settings
        self.settings = Settings()
        self.sensitivity = self.settings.sensitivity
    
    def set_sensitivity(self, value):
        """设置灵敏度"""
        self.sensitivity = value
    
    def update(self):
        """获取鼠标移动并返回调整后的位置"""
        current_mouse_pos = pygame.mouse.get_pos()
        
        # 使用当前灵敏度设置
        dx = (current_mouse_pos[0] - self.last_mouse_pos[0]) * self.sensitivity
        dy = (current_mouse_pos[1] - self.last_mouse_pos[1]) * self.sensitivity
        
        # 更新准心位置
        self.crosshair_x = max(0, min(self.window.get_width(), self.crosshair_x + dx))
        self.crosshair_y = max(0, min(self.window.get_height(), self.crosshair_y + dy))
        
        # 将鼠标重置到窗口中心
        pygame.mouse.set_pos((self.center_x, self.center_y))
        self.last_mouse_pos = (self.center_x, self.center_y)
        
        return int(self.crosshair_x), int(self.crosshair_y)
    
    def cleanup(self):
        """清理函数"""
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True) 