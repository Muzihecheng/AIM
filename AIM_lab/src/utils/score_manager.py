import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
import pygame

class ScoreManager:
    def __init__(self):
        self.scores_file = "data/scores.json"
        self.ensure_data_dir()
        self.load_scores()
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.scores_file):
            with open(self.scores_file, "w") as f:
                json.dump({}, f)
    
    def load_scores(self):
        """加载历史分数"""
        try:
            with open(self.scores_file, "r") as f:
                self.scores = json.load(f)
        except:
            self.scores = {}
    
    def save_score(self, mode_name, score, accuracy):
        """保存新的分数记录"""
        if mode_name not in self.scores:
            self.scores[mode_name] = []
            
        # 添加新记录
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "accuracy": accuracy
        }
        self.scores[mode_name].append(record)
        
        # 保存到文件
        with open(self.scores_file, "w") as f:
            json.dump(self.scores, f)
    
    def get_mode_history(self, mode_name):
        """获取指定模式的历史记录"""
        return self.scores.get(mode_name, [])
    
    def create_history_graph(self, mode_name, width=400, height=200):
        """创建历史记录图表"""
        records = self.get_mode_history(mode_name)
        if not records:
            return None, None
            
        # 创建分数图表
        plt.figure(figsize=(width/100, height/100), dpi=100)
        plt.style.use('dark_background')
        
        # 提取数据
        scores = [r["score"] for r in records]
        
        # 绘制得分曲线
        plt.plot(scores, color='#00ff00', marker='o')
        plt.title(f'Score History')
        plt.grid(True, alpha=0.3)
        
        # 将图表转换为pygame surface
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        plt.close()
        
        # 创建surface
        score_graph = pygame.image.load(buf)
        buf.close()
        
        # 创建准确率图表
        plt.figure(figsize=(width/100, height/100), dpi=100)
        plt.style.use('dark_background')
        
        # 提取数据
        accuracies = [r["accuracy"] for r in records]
        
        # 绘制准确率曲线
        plt.plot(accuracies, color='#ff9900', marker='o')
        plt.title(f'Accuracy History')
        plt.grid(True, alpha=0.3)
        
        # 将图表转换为pygame surface
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        plt.close()
        
        # 创建surface
        accuracy_graph = pygame.image.load(buf)
        buf.close()
        
        return score_graph, accuracy_graph 