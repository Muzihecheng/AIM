import pygame

class Button:
    def __init__(self, screen, msg, x, y, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # 设置按钮的rect对象
        self.rect = pygame.Rect(x, y, width, height)
        
        # 按钮文本设置
        self.msg = msg
        self.font = pygame.font.Font(None, 48)
        self.text_color = (255, 255, 255)
        self.button_color = (0, 135, 255)
        
        # 渲染按钮文本
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw(self):
        """绘制按钮"""
        pygame.draw.rect(self.screen, self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect) 