import pygame
import os
import json

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Загрузка сцен
        self.load_scenes()
        self.current_scene_id = "scene_1"
        
        # Загрузка изображений
        self.load_images()
        
        # Инициализация шрифтов
        self.story_font = pygame.font.SysFont('arial', 24)
        self.stats_font = pygame.font.SysFont('arial', 20)
        self.choice_font = pygame.font.SysFont('arial', 18)
        self.story_font = pygame.font.Font(None, 32)
        self.choice_font = pygame.font.Font(None, 42)
        self.desc_font = pygame.font.Font(None, 24)
        self.description_font = pygame.font.SysFont('arial', 16)
        
        # Параметры игрока
        self.health = 5
        self.strength = 10
        
        # Создание прямоугольников для выбора
        self.create_choice_rects()
        
    def load_scenes(self):
        try:
            scenes_path = os.path.join(self.base_path, "src", "scenes.json")
            with open(scenes_path, 'r', encoding='utf-8') as file:
                self.scenes = json.load(file)
        except Exception as e:
            print(f"Ошибка загрузки сцен: {e}")
            pygame.quit()
            exit(1)
            
    def load_split_background(self, image1_path, image2_path):
        # Ищем первое изображение в обеих папках
        img1_places = os.path.join(self.base_path, "assets", "places", image1_path)
        img1_images = os.path.join(self.base_path, "assets", "images", image1_path)
        
        if os.path.exists(img1_places):
            img1 = pygame.image.load(img1_places)
        elif os.path.exists(img1_images):
            img1 = pygame.image.load(img1_images)
        else:
            raise FileNotFoundError(f"Изображение {image1_path} не найдено")
            
        # Ищем второе изображение в обеих папках    
        img2_places = os.path.join(self.base_path, "assets", "places", image2_path)
        img2_images = os.path.join(self.base_path, "assets", "images", image2_path)
        
        if os.path.exists(img2_places):
            img2 = pygame.image.load(img2_places)
        elif os.path.exists(img2_images):
            img2 = pygame.image.load(img2_images)
        else:
            raise FileNotFoundError(f"Изображение {image2_path} не найдено")
        
        # Масштабируем и объединяем изображения
        height = self.screen.get_height()
        half_width = self.screen.get_width() // 2
        
        img1 = pygame.transform.scale(img1, (half_width, height))
        img2 = pygame.transform.scale(img2, (half_width, height))
        
        combined = pygame.Surface((self.screen.get_width(), height))
        combined.blit(img1, (0, 0))
        combined.blit(img2, (half_width, 0))
        
        return combined

    def load_images(self):
        try:
            # Загружаем иконки
            heart_path = os.path.join(self.base_path, "assets", "icons", "heart.png")
            strength_path = os.path.join(self.base_path, "assets", "icons", "strength.png")
            self.heart_icon = pygame.image.load(heart_path)
            self.strength_icon = pygame.image.load(strength_path)
            
            self.heart_icon = pygame.transform.scale(self.heart_icon, (30, 30))
            self.strength_icon = pygame.transform.scale(self.strength_icon, (30, 30))

            # Загружаем фон текущей сцены
            current_scene = self.scenes[self.current_scene_id]
            bg_filename = current_scene["background"]
            
            if isinstance(bg_filename, list):
                # Для разделенного фона
                self.background = self.load_split_background(bg_filename[0], bg_filename[1])
            else:
                # Для обычного фона проверяем все папки
                bg_places = os.path.join(self.base_path, "assets", "places", bg_filename)
                bg_images = os.path.join(self.base_path, "assets", "images", bg_filename)
                bg_background = os.path.join(self.base_path, "assets", "background", bg_filename)
                
                if os.path.exists(bg_places):
                    self.background = pygame.image.load(bg_places)
                elif os.path.exists(bg_images):
                    self.background = pygame.image.load(bg_images)
                elif os.path.exists(bg_background):
                    self.background = pygame.image.load(bg_background)
                else:
                    raise FileNotFoundError(f"Изображение {bg_filename} не найдено")
                    
                self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
                
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")
            pygame.quit()
            exit(1)


    def create_choice_rects(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        self.choice_rects = [
            pygame.Rect(screen_width * 0.1, screen_height * 0.7, 
                       screen_width * 0.35, screen_height * 0.2),
            pygame.Rect(screen_width * 0.55, screen_height * 0.7,
                       screen_width * 0.35, screen_height * 0.2)
        ]
        
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.choice_rects):
                if rect.collidepoint(mouse_pos):
                    self.make_choice(i)
                    
    def make_choice(self, choice_index):
        choice = self.scenes[self.current_scene_id]["choices"][choice_index]
        self.health += choice["health_change"]
        self.strength += choice["strength_change"]
        
        self.health = max(0, min(5, self.health))
        self.strength = max(0, min(100, self.strength))
        
        self.current_scene_id = choice["next_scene"]
        self.load_images()
        
    def make_choice(self, choice_index):
        choice = self.scenes[self.current_scene_id]["choices"][choice_index]
        self.health += choice["health_change"]
        self.strength += choice["strength_change"]
        
        self.health = max(0, min(5, self.health))
        self.strength = max(0, min(100, self.strength))
        
        self.current_scene_id = choice["next_scene"]
        self.load_images()  # Добавляем эту строку

    def draw_story_text(self):
        # Параметры текстового блока
        text_width = 960  # Ширина блока текста
        text_height = 400  # Высота блока текста
        text_x = (self.screen.get_width() - text_width) // 2  # 480 пикселей от левого края
        text_y = 150  # Отступ сверху
        
        # Создаем полупрозрачный фон
        text_bg = pygame.Surface((text_width, text_height))
        text_bg.fill((50, 50, 50))
        text_bg.set_alpha(200)
        
        # Отрисовываем фон
        self.screen.blit(text_bg, (text_x, text_y))
        
        # Получаем текст и разбиваем на строки
        current_scene = self.scenes[self.current_scene_id]
        words = current_scene["text"].split()
        lines = []
        current_line = []
        
        # Разбиваем текст на строки
        for word in words:
            current_line.append(word)
            text = " ".join(current_line)
            if self.story_font.size(text)[0] > text_width - 40:  # Отступ от краев
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        
        # Отрисовываем текст
        line_height = 30
        total_text_height = len(lines) * line_height
        start_y = text_y + (text_height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            text_surface = self.story_font.render(line, True, (255, 255, 255))
            line_x = text_x + (text_width - text_surface.get_width()) // 2
            self.screen.blit(text_surface, (line_x, start_y + i * line_height))

    def draw_choices(self):
        # Параметры текстового блока истории
        story_width = 960  # Ширина блока истории
        
        # Вычисляем размеры карточек выбора
        gap = 50  # Отступ между карточками
        card_width = (story_width - gap) // 2  # Ширина карточки
        card_height = 250  # Высота карточки
        
        # Вычисляем начальную позицию
        start_x = (self.screen.get_width() - story_width) // 2
        start_y = 600  # Увеличили отступ на 100 пикселей вниз
        
        current_scene = self.scenes[self.current_scene_id]
        choices = current_scene["choices"]
        
        for i, choice in enumerate(choices):
            # Позиция карточки
            card_x = start_x + i * (card_width + gap)
            card_y = start_y
            
            # Создаем полупрозрачную карточку
            card_surface = pygame.Surface((card_width, card_height))
            card_surface.fill((50, 50, 50))
            card_surface.set_alpha(200)  # Устанавливаем прозрачность как у истории
            self.screen.blit(card_surface, (card_x, card_y))
            
            # Сохраняем область карточки
            self.choice_rects[i] = pygame.Rect(card_x, card_y, card_width, card_height)
            
            # Отрисовываем основной текст (прижат к верху)
            words = choice["text"].split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                text = " ".join(current_line)
                if self.choice_font.size(text)[0] > card_width - 20:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
            
            text_start_y = card_y + 20
            line_height = 30
            
            for j, line in enumerate(lines):
                text_surface = self.choice_font.render(line, True, (255, 255, 255))
                text_x = card_x + (card_width - text_surface.get_width()) // 2
                self.screen.blit(text_surface, (text_x, text_start_y + j * line_height))
            
            # Отрисовываем описание если есть
            if choice["description"]:
                desc_words = choice["description"].split()
                desc_lines = []
                current_line = []
                
                for word in desc_words:
                    current_line.append(word)
                    text = " ".join(current_line)
                    if self.desc_font.size(text)[0] > card_width - 20:
                        current_line.pop()
                        desc_lines.append(" ".join(current_line))
                        current_line = [word]
                if current_line:
                    desc_lines.append(" ".join(current_line))
                
                desc_line_height = 20
                total_desc_height = len(desc_lines) * desc_line_height
                desc_start_y = card_y + (card_height - total_desc_height) // 2
                
                for j, line in enumerate(desc_lines):
                    desc_surface = self.desc_font.render(line, True, (200, 200, 200))
                    desc_x = card_x + (card_width - desc_surface.get_width()) // 2
                    self.screen.blit(desc_surface, (desc_x, desc_start_y + j * desc_line_height))

    def draw_stats(self):
        # Отрисовка здоровья
        self.screen.blit(self.heart_icon, (20, 20))
        health_text = self.stats_font.render(f"Жизни: {self.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (60, 25))
        
        # Отрисовка силы под здоровьем
        self.screen.blit(self.strength_icon, (20, 60))
        strength_text = self.stats_font.render(f"Сила: {self.strength}", True, (255, 255, 255))
        self.screen.blit(strength_text, (60, 65))
        
                
    def draw(self):
        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))
        
        # Отрисовка текста истории
        self.draw_story_text()
        
        # Отрисовка статистики
        self.draw_stats()
        
        # Отрисовка вариантов выбора
        self.draw_choices()
        
        pygame.display.flip()
