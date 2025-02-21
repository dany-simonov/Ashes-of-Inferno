import pygame

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        
        # Цвета
        self.normal_color = (100, 100, 120)
        self.hover_color = (150, 150, 170)
        self.text_color = (255, 255, 255)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.normal_color
        
        # Отрисовка кнопки
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        # Отрисовка текста
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
