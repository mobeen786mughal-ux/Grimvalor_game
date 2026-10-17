from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
import random

Window.clearcolor = (0.1, 0.1, 0.15, 1)

class Player(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (60, 60)
        self.pos = (100, Window.height/2)

class Enemy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)
        self.pos = (Window.width + random.randint(0, 300), random.randint(0, int(Window.height - 50)))

class Game(Widget):
    score = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player()
        self.add_widget(self.player)
        self.enemies = []
        self.score_label = Label(text='Score: 0', pos=(20, Window.height - 50), font_size=24, size_hint=(None, None))
        self.add_widget(self.score_label)
        
        # Touch controls
        self.touch_y = self.player.center_y
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.spawn_enemy, 1.5)

    def on_touch_move(self, touch):
        self.touch_y = touch.y
        return True

    def on_touch_down(self, touch):
        self.touch_y = touch.y
        return True

    def spawn_enemy(self, dt):
        e = Enemy()
        self.enemies.append(e)
        self.add_widget(e)

    def update(self, dt):
        # Player movement
        if abs(self.player.center_y - self.touch_y) > 5:
            if self.player.center_y < self.touch_y:
                self.player.y += 8
            else:
                self.player.y -= 8

        # Enemy movement
        for enemy in self.enemies[:]:
            enemy.x -= 6
            if enemy.right < 0:
                self.remove_widget(enemy)
                self.enemies.remove(enemy)
                self.score += 1
                self.score_label.text = f'Score: {self.score}'
            
            # Collision
            if self.player.collide_widget(enemy):
                self.score_label.text = f'GAME OVER! Score: {self.score} - Touch to Restart'
                Clock.unschedule(self.update)
                Clock.unschedule(self.spawn_enemy)

    def on_touch_up(self, touch):
        if 'GAME OVER' in self.score_label.text:
            # Restart
            for e in self.enemies[:]:
                self.remove_widget(e)
            self.enemies.clear()
            self.score = 0
            self.player.pos = (100, Window.height/2)
            self.score_label.text = 'Score: 0'
            Clock.schedule_interval(self.update, 1/60)
            Clock.schedule_interval(self.spawn_enemy, 1.5)

class GrimApp(App):
    def build(self):
        return Game()

GrimApp().run()
