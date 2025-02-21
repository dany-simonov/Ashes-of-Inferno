import pygame
import os

class MusicPlayer:
    def __init__(self):
        self.current_track = 0
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.music_dir = os.path.join(self.base_path, "assets", "muz")
        
        # Явно задаем треки
        self.tracks = [
            os.path.join(self.music_dir, "au1.mp3"),
            os.path.join(self.music_dir, "au2.mp3")
        ]
        
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        self.start_playback()
        self.is_playing = True

    def start_playback(self):
        if self.tracks and os.path.exists(self.tracks[self.current_track]):
            pygame.mixer.music.load(self.tracks[self.current_track])
            pygame.mixer.music.play()
    
    def handle_music_end(self):
        self.current_track = (self.current_track + 1) % len(self.tracks)
        self.start_playback()
        
    def toggle_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.is_playing = not self.is_playing
        
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
