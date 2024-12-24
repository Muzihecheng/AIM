import pygame
import random
import math
from src.ui.button import Button

class SixShot:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.name = "SixShot"
        
        # 设置背景网格
        self.grid_size = 50
        self.grid_color = (40, 40, 40)
        self.bg_color = (70, 70, 70)
        
        # 目标小球设置
        self.targets = []
        self.target_radius = 7
        self.target_color = (255, 50, 50)
        self.max_targets = 6
        
        # 计分
        self.score = 0
        self.shots_fired = 0  # 总点击次数
        self.hits = 0        # 击中次数
        self.hit_score = 1000
        self.miss_penalty = 800
        
        # 计时器
        self.game_duration = 60  # 游戏持续60秒
        self.time_left = self.game_duration
        self.start_time = None
        self.game_over = False
        
        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)
        
        # 准心设置
        from src.ui.crosshair import Crosshair
        self.crosshair = Crosshair(screen)
        
        # 准心位置
        self.crosshair_x = self.settings.screen_width // 2
        self.crosshair_y = self.settings.screen_height // 2
        
        # 添加灵敏度管理器
        from src.utils.sensitivity import SensitivityManager
        self.sensitivity = SensitivityManager()
        self.sensitivity.set_sensitivity(settings.sensitivity)  # 使用设置中的灵敏度
        
        # 添加记分管理器
        from src.utils.score_manager import ScoreManager
        self.score_manager = ScoreManager()
        
        # 添加结束界面按钮
        button_width = 200
        button_height = 50
        center_x = self.settings.screen_width // 2
        
        self.restart_button = Button(
            self.screen,
            "Restart",
            center_x - button_width - 20,  # 左边的按钮
            self.settings.screen_height - 100,
            button_width,
            button_height
        )
        
        self.menu_button = Button(
            self.screen,
            "Menu",
            center_x + 20,  # 右边的按钮
            self.settings.screen_height - 100,
            button_width,
            button_height
        )
        
        self.spawn_targets()
        
    def spawn_targets(self):
        """生成目标小球"""
        self.targets.clear()
        margin = 100  # 边距，避免小球生成在屏幕边缘
        
        for _ in range(self.max_targets):
            while True:
                x = random.randint(margin, self.settings.screen_width - margin)
                y = random.randint(margin, self.settings.screen_height - margin)
                
                # 检查是否与其他目标重叠
                overlap = False
                for target in self.targets:
                    distance = math.sqrt((x - target[0])**2 + (y - target[1])**2)
                    if distance < self.target_radius * 4:  # 确保目标之间有足够空间
                        overlap = True
                        break
                
                if not overlap:
                    self.targets.append([x, y])
                    break
    
    def run(self):
        running = True
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        
        try:
            while running:
                result = self._handle_events()
                if result is not None:
                    return result
                
                self._update()
                self._draw()
                clock.tick(60)
        finally:
            self.sensitivity.cleanup()
            
        return True
    
    def _handle_events(self):
        """处理输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.game_over:
                    if self.restart_button.rect.collidepoint(mouse_pos):
                        self._reset_game()
                    elif self.menu_button.rect.collidepoint(mouse_pos):
                        pygame.mouse.set_visible(True)  # 确保返回菜单时显示鼠标
                        return True
                else:
                    self._handle_click((self.crosshair_x, self.crosshair_y))
            if event.type == pygame.MOUSEWHEEL:
                sens = self.sensitivity.adjust_sensitivity(event.y)
                print(f"Sensitivity: {sens:.1f}")
        return None
    
    def _reset_game(self):
        """重置游戏"""
        self.score = 0
        self.shots_fired = 0
        self.time_left = self.game_duration
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.spawn_targets()
    
    def _handle_click(self, pos):
        """处理鼠标点击"""
        self.shots_fired += 1
        mouse_x, mouse_y = pos
        hit = False
        
        for i, (x, y) in enumerate(self.targets):
            distance = math.sqrt((mouse_x - x)**2 + (mouse_y - y)**2)
            if distance <= self.target_radius:
                self.score += self.hit_score
                self.hits += 1  # 记录击中
                hit = True
                self._respawn_target(i)
                break
        
        if not hit:
            self.score = max(0, self.score - self.miss_penalty)
    
    def _respawn_target(self, index):
        """重新生成单个目标的位置"""
        margin = 100
        while True:
            x = random.randint(margin, self.settings.screen_width - margin)
            y = random.randint(margin, self.settings.screen_height - margin)
            
            # 检查是否与其他目标重叠
            overlap = False
            for i, target in enumerate(self.targets):
                if i != index:  # 不与自己比较
                    distance = math.sqrt((x - target[0])**2 + (y - target[1])**2)
                    if distance < self.target_radius * 4:
                        overlap = True
                        break
            
            if not overlap:
                self.targets[index] = [x, y]
                break
    
    def _update(self):
        """更新游戏状态"""
        if not self.game_over:
            # 更新准心位置
            self.crosshair_x, self.crosshair_y = self.sensitivity.update()
            
            # 更新时间
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) // 1000
            self.time_left = max(0, self.game_duration - elapsed_time)
            
            if self.time_left <= 0:
                self.game_over = True
                # 保存分数
                accuracy = (self.hits / self.shots_fired * 100) if self.shots_fired > 0 else 0
                self.score_manager.save_score(self.name, self.score, accuracy)
    
    def _draw(self):
        """绘制游戏画面"""
        self.screen.fill(self.bg_color)
        
        # 绘制网格
        for x in range(0, self.settings.screen_width, self.grid_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), 
                           (x, self.settings.screen_height))
        for y in range(0, self.settings.screen_height, self.grid_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), 
                           (self.settings.screen_width, y))
        
        # 绘制目标
        if not self.game_over:
            for x, y in self.targets:
                pygame.draw.circle(self.screen, self.target_color, (x, y), 
                                 self.target_radius)
        
        # 绘制UI
        try:
            font = pygame.font.Font("assets/fonts/simsunb.ttf", 32)
        except FileNotFoundError:
            font = pygame.font.Font(None, 32)
        
        # 绘制分数和时间
        accuracy = (self.hits / self.shots_fired * 100) if self.shots_fired > 0 else 0
        score_text = f"Score: {self.score} | Accuracy: {accuracy:.1f}%"
        time_text = f"Time: {self.time_left}s"
        
        score_surface = font.render(score_text, True, (255, 255, 255))
        time_surface = font.render(time_text, True, (255, 255, 255))
        
        self.screen.blit(score_surface, (20, 20))
        self.screen.blit(time_surface, (20, 60))
        
        # 如果游戏结束，显示结束界面
        if self.game_over:
            # 显示鼠标光标，隐藏准心
            pygame.mouse.set_visible(True)
            
            # 绘制半透明背景
            overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            # 绘制结束文本
            game_over_text = font.render("Game Over!", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(self.settings.screen_width // 2, 80))
            self.screen.blit(game_over_text, text_rect)
            
            # 绘制最终分数
            final_score = font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            score_rect = final_score.get_rect(center=(self.settings.screen_width // 2, 130))
            self.screen.blit(final_score, score_rect)
            
            accuracy = (self.hits / self.shots_fired * 100) if self.shots_fired > 0 else 0
            accuracy_text = font.render(f"Accuracy: {accuracy:.1f}%", True, (255, 255, 255))
            accuracy_rect = accuracy_text.get_rect(center=(self.settings.screen_width // 2, 180))
            self.screen.blit(accuracy_text, accuracy_rect)
            
            # 绘制历史记录图表
            score_graph, accuracy_graph = self.score_manager.create_history_graph(self.name)
            if score_graph and accuracy_graph:
                # 绘制分数图表
                graph_rect = score_graph.get_rect()
                graph_rect.centerx = self.settings.screen_width // 2
                graph_rect.top = 230
                self.screen.blit(score_graph, graph_rect)
                
                # 绘制准确率图表
                acc_rect = accuracy_graph.get_rect()
                acc_rect.centerx = self.settings.screen_width // 2
                acc_rect.top = graph_rect.bottom + 20
                self.screen.blit(accuracy_graph, acc_rect)
            
            # 绘制按钮
            self.restart_button.draw()
            self.menu_button.draw()
        else:
            # 游戏进行中，绘制准心
            self.crosshair.draw((int(self.crosshair_x), int(self.crosshair_y)))
        
        pygame.display.flip() 