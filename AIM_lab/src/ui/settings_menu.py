import pygame
from src.ui.button import Button

class SettingsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        # 使用当前设置中的灵敏度值
        self.sensitivity = settings.sensitivity
        
        # 根据当前灵敏度值设置滑块位置
        slider_width = 400
        slider_x = 300 + (self.sensitivity - 0.1) / 1.9 * slider_width
        
        # 创建滑动条和按钮
        self.slider_rect = pygame.Rect(300, 200, slider_width, 10)
        self.slider_handle_rect = pygame.Rect(slider_x - 10, 195, 20, 20)
        
        # 保存按钮
        self.save_button = Button(
            self.screen,
            "Save",
            self.settings.screen_width // 2 - 100,
            400,
            200,
            50
        )
    
    def run(self):
        running = True
        dragging = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.slider_handle_rect.collidepoint(mouse_pos):
                        dragging = True
                    elif self.save_button.rect.collidepoint(mouse_pos):
                        self._save_settings()
                        return True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                
                if event.type == pygame.MOUSEMOTION and dragging:
                    mouse_x = pygame.mouse.get_pos()[0]
                    # 限制滑块在滑动条范围内
                    x = max(self.slider_rect.left, min(mouse_x, self.slider_rect.right))
                    self.slider_handle_rect.centerx = x
                    # 计算灵敏度值 (0.1 到 2.0)
                    self.sensitivity = 0.1 + (x - self.slider_rect.left) / self.slider_rect.width * 1.9
            
            self._draw()
        
        return True
    
    def _draw(self):
        self.screen.fill(self.settings.bg_color)
        
        # 绘制标题
        try:
            font = pygame.font.Font("assets/fonts/simsunb.ttf", 48)
            small_font = pygame.font.Font("assets/fonts/simsunb.ttf", 24)
        except FileNotFoundError:
            font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 24)
        
        # 绘制标题
        title = font.render("Settings", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.settings.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # 绘制灵敏度值
        sens_text = small_font.render(f"Sensitivity: {self.sensitivity:.2f}", True, (255, 255, 255))
        self.screen.blit(sens_text, (300, 150))
        
        # 绘制滑动条
        pygame.draw.rect(self.screen, (100, 100, 100), self.slider_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.slider_handle_rect)
        
        # 绘制保存按钮
        self.save_button.draw()
        
        pygame.display.flip()
    
    def _save_settings(self):
        """保存设置到配置文件"""
        self.settings.sensitivity = self.sensitivity
        # 这里可以添加保存到文件的代码 