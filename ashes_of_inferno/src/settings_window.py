import pygame

class SettingsWindow:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 36)
        self.volume = 100  # Начальная громкость 100%
        self.graphics_quality = 1
        self.qualities = ["Низкое", "Среднее", "Высокое"]
        
    def handle_click(self, pos):
        # Кнопка "Назад"
        back_button = pygame.Rect(50, 50, 100, 40)
        if back_button.collidepoint(pos):
            return True

        # Ползунок громкости
        slider_rect = pygame.Rect(self.screen.get_width()//2 - 100, 200, 200, 20)
        if slider_rect.collidepoint(pos):
            self.volume = (pos[0] - slider_rect.x) / slider_rect.width * 100
            self.volume = max(0, min(100, self.volume))
            
        # Качество графики
        for i, quality in enumerate(self.qualities):
            button_rect = pygame.Rect(self.screen.get_width()//2 - 100, 300 + i*60, 200, 50)
            if button_rect.collidepoint(pos):
                self.graphics_quality = i
        
        return False
                
    def draw(self):
        # Фон
        self.screen.fill((20, 20, 30))
        
        # Кнопка "Назад"
        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(self.screen, (100, 100, 100), back_button)
        back_text = self.font.render("Назад", True, (255, 255, 255))
        self.screen.blit(back_text, (60, 55))
        
        # Заголовок
        title = self.font.render("Настройки", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 50))
        
        # Громкость
        volume_text = self.font.render(f"Громкость: {int(self.volume)}%", True, (255, 255, 255))
        self.screen.blit(volume_text, (self.screen.get_width()//2 - volume_text.get_width()//2, 150))
        
        # Ползунок громкости
        slider_rect = pygame.Rect(self.screen.get_width()//2 - 100, 200, 200, 20)
        pygame.draw.rect(self.screen, (100, 100, 100), slider_rect)
        pygame.draw.rect(self.screen, (200, 50, 50), 
                        (slider_rect.x, slider_rect.y, slider_rect.width * (self.volume/100), slider_rect.height))
        
        # Качество графики
        graphics_text = self.font.render("Качество графики:", True, (255, 255, 255))
        self.screen.blit(graphics_text, (self.screen.get_width()//2 - graphics_text.get_width()//2, 250))
        
        for i, quality in enumerate(self.qualities):
            color = (200, 50, 50) if i == self.graphics_quality else (100, 100, 100)
            button_rect = pygame.Rect(self.screen.get_width()//2 - 100, 300 + i*60, 200, 50)
            pygame.draw.rect(self.screen, color, button_rect)
            quality_text = self.font.render(quality, True, (255, 255, 255))
            self.screen.blit(quality_text, (button_rect.centerx - quality_text.get_width()//2, 
                                          button_rect.centery - quality_text.get_height()//2))
