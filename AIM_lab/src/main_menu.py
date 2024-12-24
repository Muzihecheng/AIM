import pygame
import sys
from src.settings import Settings
from src.ui.button import Button

class MainMenu:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        
        # 设置窗口
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("AimLab")
        
        # 创建按钮
        button_width = 200
        button_height = 50
        
        # 开始按钮 - 右下角
        self.play_button = Button(
            self.screen,
            "Start",
            self.settings.screen_width - button_width - 50,  # 右边距50像素
            self.settings.screen_height - button_height - 50,  # 下边距50像素
            button_width,
            button_height
        )
        
        # 设置按钮 - 右上角
        settings_size = 40  # 设置按钮为方形
        self.settings_button = Button(
            self.screen,
            "Set",  # 使用齿轮符号
            self.settings.screen_width - settings_size - 20,  # 右边距20像素
            20,  # 上边距20像素
            settings_size,
            settings_size
        )
        
        # 游戏模式列表
        self.game_modes = [
            "SixShot",
            "QuickShot",
            "HeadShot",
        ]
        
        # 添加选中的游戏模式
        self.selected_mode = None
        
        # 添加记分管理器
        from src.utils.score_manager import ScoreManager
        self.score_manager = ScoreManager()
    
    def run(self):
        """主游戏循环"""
        while True:
            self._check_events()
            self._update_screen()
    
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_clicks(mouse_pos)
                self._check_mode_selection(mouse_pos)
    
    def _check_button_clicks(self, mouse_pos):
        """检查按钮点击"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()
        elif self.settings_button.rect.collidepoint(mouse_pos):
            self._open_settings()
    
    def _check_mode_selection(self, mouse_pos):
        """检查是否点击了游戏模式"""
        for i, mode in enumerate(self.game_modes):
            mode_rect = pygame.Rect(50, 200 + i * 60, 200, 40)
            if mode_rect.collidepoint(mouse_pos):
                self.selected_mode = mode
                break
    
    def _update_screen(self):
        """更新屏幕内容"""
        self.screen.fill(self.settings.bg_color)
        
        # 绘制标题
        try:
            font = pygame.font.Font("assets/fonts/simsunb.ttf", 74)
            mode_font = pygame.font.Font("assets/fonts/simsunb.ttf", 32)
        except FileNotFoundError:
            print("警告：找不到字体文件 assets/fonts/simsunb.ttf")
            font = pygame.font.Font(None, 74)
            mode_font = pygame.font.Font(None, 32)
        
        # 绘制游戏标题    
        title = font.render("AimLab", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.settings.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # 绘制左侧游戏模式列表
        for i, mode in enumerate(self.game_modes):
            # 如果是选中的模式，使用不同的颜色
            color = (255, 255, 255)
            if mode == self.selected_mode:
                color = (255, 200, 0)  # 选中的模式示为金色
                
            mode_text = mode_font.render(mode, True, color)
            mode_rect = mode_text.get_rect(
                left=50,
                top=200 + i * 60
            )
            self.screen.blit(mode_text, mode_rect)
        
        # 绘制按钮
        self.play_button.draw()
        self.settings_button.draw()
        
        # 如果选择了模式，显示历史记录图表
        if self.selected_mode:
            score_graph, accuracy_graph = self.score_manager.create_history_graph(self.selected_mode)
            if score_graph and accuracy_graph:
                # 在右侧显示分数图表
                score_rect = score_graph.get_rect()
                score_rect.right = self.settings.screen_width - 50
                score_rect.top = 200
                self.screen.blit(score_graph, score_rect)
                
                # 在分数图表下方显示准确率图表
                acc_rect = accuracy_graph.get_rect()
                acc_rect.right = self.settings.screen_width - 50
                acc_rect.top = score_rect.bottom + 20
                self.screen.blit(accuracy_graph, acc_rect)
        
        pygame.display.flip()
    
    def _start_game(self):
        """开始游戏"""
        if not self.selected_mode:
            return
            
        # 根据选择的模式启动相应的游戏
        from src.modes.six_shot import SixShot
        from src.modes.quick_shot import QuickShot
        from src.modes.head_shot import HeadShot
        
        game_mode = None
        if self.selected_mode == "SixShot":
            game_mode = SixShot(self.screen, self.settings)
        elif self.selected_mode == "QuickShot":
            game_mode = QuickShot(self.screen, self.settings)
        elif self.selected_mode == "HeadShot":
            game_mode = HeadShot(self.screen, self.settings)
            
        if game_mode:
            # 运行游戏，如果返回False则退出程序
            result = game_mode.run()
            # 重新加载分数管理器
            self.score_manager.load_scores()
            if not result:
                sys.exit()
    
    def _open_settings(self):
        """打开设置界面"""
        from src.ui.settings_menu import SettingsMenu
        settings_menu = SettingsMenu(self.screen, self.settings)
        settings_menu.run() 