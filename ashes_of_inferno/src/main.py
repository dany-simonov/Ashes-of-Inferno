import pygame
import os
import sys
from button import Button
from music_player import MusicPlayer
from settings import Settings
from settings_window import SettingsWindow
from achievements_window import AchievementsWindow
from game_screen import GameScreen

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Ashes of Inferno")
        
        # Загрузка фонового изображения
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bg_path = os.path.join(self.base_path, "assets", "places", "main_screen.jpg")
        self.background = pygame.image.load(bg_path)
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        
        self.title_font = pygame.font.SysFont('arial', 72, bold=True)
        self.button_font = pygame.font.SysFont('arial', 36, bold=True)
        
        # Создание окон
        self.settings_window = SettingsWindow(self.screen)
        self.achievements_window = AchievementsWindow(self.screen)
        
        self.buttons = self.create_buttons()
        self.music_player = MusicPlayer()
        
        self.current_window = 'main'
        self.game_screen = GameScreen(self.screen)
        self.show_exit_prompt = False
        
    def create_buttons(self):
        buttons = []
        button_texts = ["Новая игра", "Продолжить игру", "Настройки", "Достижения", "Выход"]
        
        screen_center_x = self.screen.get_width() // 2
        start_y = self.screen.get_height() // 2 - 100
        
        for i, text in enumerate(button_texts):
            button = Button(
                screen_center_x - 150,  # Увеличили ширину кнопок
                start_y + i * 70,
                300, 50,  # Увеличили ширину кнопок
                text,
                self.button_font
            )
            buttons.append(button)
        return buttons

# В методе handle_events добавим обработку ESC
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.show_exit_prompt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_window != 'main':
                        self.current_window = 'main'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_exit_prompt:
                    self.handle_exit_prompt(mouse_pos)
                elif self.current_window == 'main':
                    self.handle_main_buttons(mouse_pos)
                elif self.current_window == 'settings':
                    if self.settings_window.handle_click(mouse_pos):
                        self.current_window = 'main'
                    self.music_player.set_volume(self.settings_window.volume / 100)
                elif self.current_window == 'achievements':
                    if self.achievements_window.handle_click(mouse_pos):
                        self.current_window = 'main'
                elif self.current_window == 'game':
                    self.game_screen.handle_events(event)

    def handle_main_buttons(self, mouse_pos):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                if button.text == "Выход":
                    self.show_exit_prompt = True
                elif button.text == "Настройки":
                    self.current_window = 'settings'
                elif button.text == "Достижения":
                    self.current_window = 'achievements'
                elif button.text == "Новая игра":
                    self.current_window = 'game'

    def handle_exit_prompt(self, mouse_pos):
        yes_rect = pygame.Rect(self.screen.get_width()//2 - 160, self.screen.get_height()//2, 150, 50)
        no_rect = pygame.Rect(self.screen.get_width()//2 + 10, self.screen.get_height()//2, 150, 50)
        
        if yes_rect.collidepoint(mouse_pos):
            self.quit_game()
        elif no_rect.collidepoint(mouse_pos):
            self.show_exit_prompt = False

    def draw(self):
        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))
        
        if self.current_window == 'main':
            self.draw_main_menu()
        elif self.current_window == 'settings':
            self.settings_window.draw()
        elif self.current_window == 'achievements':
            self.achievements_window.draw()
        elif self.current_window == 'game':
            self.game_screen.draw()
            
        if self.show_exit_prompt:
            self.draw_exit_prompt()
            
        pygame.display.flip()

    def draw_main_menu(self):
        # Отрисовка заголовка
        title_surface = self.title_font.render("Ashes of Inferno", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Отрисовка кнопок
        for button in self.buttons:
            button.draw(self.screen)

    def draw_exit_prompt(self):
        # Затемнение фона
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        # Отрисовка окна подтверждения
        prompt_rect = pygame.Rect(self.screen.get_width()//2 - 200, self.screen.get_height()//2 - 100, 400, 200)
        pygame.draw.rect(self.screen, (50, 50, 50), prompt_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), prompt_rect, 2)
        
        # Текст
        text = self.button_font.render("Вы точно хотите выйти?", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
        self.screen.blit(text, text_rect)
        
        # Кнопки
        yes_button = Button(self.screen.get_width()//2 - 160, self.screen.get_height()//2, 150, 50, "Да", self.button_font)
        no_button = Button(self.screen.get_width()//2 + 10, self.screen.get_height()//2, 150, 50, "Нет", self.button_font)
        
        yes_button.draw(self.screen)
        no_button.draw(self.screen)
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

        
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            
    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()


