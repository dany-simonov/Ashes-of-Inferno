import pygame


class AchievementsWindow:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 36)
        
    def handle_click(self, pos):
        # Кнопка "Назад"
        back_button = pygame.Rect(50, 50, 100, 40)
        if back_button.collidepoint(pos):
            return True
        return False
        
    def draw(self):
        self.screen.fill((20, 20, 30))
        
        # Кнопка "Назад"
        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(self.screen, (100, 100, 100), back_button)
        back_text = self.font.render("Назад", True, (255, 255, 255))
        self.screen.blit(back_text, (60, 55))
        
        # Заголовок черным цветом
        title = self.font.render("Ваши достижения", True, (0, 0, 0))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 50))
        
        # Текст о достижениях
        text = self.font.render("Достижения будут доступны в полной версии игры", True, (150, 150, 150))
        self.screen.blit(text, (self.screen.get_width()//2 - text.get_width()//2, 
                               self.screen.get_height()//2 - text.get_height()//2))
