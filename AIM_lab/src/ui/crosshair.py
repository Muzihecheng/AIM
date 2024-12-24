import pygame

class Crosshair:
    def __init__(self, screen, size=6, color=(255, 255, 255), thickness=2):
        self.screen = screen
        self.size = size
        self.color = color
        self.thickness = thickness
    
    def draw(self, pos):
        """绘制准心
        pos: (x, y) 准心位置
        """
        x, y = int(pos[0]), int(pos[1])  # 确保坐标是整数
        
        # 绘制十字准心
        pygame.draw.line(self.screen, self.color, 
                        (x - self.size, y), 
                        (x + self.size, y), self.thickness)
        pygame.draw.line(self.screen, self.color, 
                        (x, y - self.size), 
                        (x, y + self.size), self.thickness)
    
    def show(self):
        """显示鼠标光标"""
        pygame.mouse.set_visible(True)
    
    def hide(self):
        """隐藏鼠标光标"""
        pygame.mouse.set_visible(False) 