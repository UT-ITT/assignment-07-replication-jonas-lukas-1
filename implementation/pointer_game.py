import pyglet
from pyglet import shapes, clock
import random
import numpy as np
# import sys
import os

screen = pyglet.display.get_display().get_default_screen()
WINDOW_WIDTH = screen.width
WINDOW_HEIGHT = screen.height

background_image = pyglet.resource.image('background.png')
background_image.width = WINDOW_WIDTH
background_image.height = WINDOW_HEIGHT

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, resizable=True, caption="Pointing Game")
window.set_mouse_visible(False)

TARGET_RADIUS = 30
TARGET_TIME = 5  # seconds
SPAWN_LEFT = 0.16
SPAWN_TOP = 0.3
SPAWN_RIGHT = 0.84
SPAWN_BOTTOM = 0.84

mouse_x = WINDOW_WIDTH // 2
mouse_y = WINDOW_HEIGHT // 2

def measure_distance(x1, y1, x2, y2):
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance

class Target:
    targets = []

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.rings = [
            shapes.Circle(x=self.x, y=self.y, radius=30, color=(220, 0, 0)),
            shapes.Circle(x=self.x, y=self.y, radius=22, color=(255, 255, 255)),
            shapes.Circle(x=self.x, y=self.y, radius=14, color=(220, 0, 0)),
            shapes.Circle(x=self.x, y=self.y, radius=6, color=(255, 255, 255)),
        ]
        self.lifetime = TARGET_TIME
        self.age = 0

    @staticmethod
    def update_targets(delta_time):
        for target in Target.targets:
            target.update(delta_time)

    @staticmethod
    def draw_targets():
        for target in Target.targets:
            target.draw()

    @staticmethod
    def create_target(delta_time):
        if random.randint(0, 10) == 0:
            radius = TARGET_RADIUS
            min_x = int(window.width * SPAWN_LEFT) + radius
            max_x = int(window.width * SPAWN_RIGHT) - radius
            min_y = int(window.height * SPAWN_TOP) + radius
            max_y = int(window.height * SPAWN_BOTTOM) - radius

            if min_x > max_x or min_y > max_y:
                return

            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            Target.targets.append(Target(x, y, radius))

    @staticmethod
    def propagate_click(x, y):
        for target in reversed(Target.targets):
            distance = measure_distance(x, y, target.x, target.y)
            if distance <= target.radius:
                Target.targets.remove(target)
                break

    def update(self, time_delta):
        self.age += time_delta
        if self.age > self.lifetime:
            Target.targets.remove(self)

    def draw(self):
        for ring in self.rings:
            ring.draw()

bb_wall = shapes.BorderedRectangle(
    int(window.width * SPAWN_LEFT),
    int(window.height * SPAWN_TOP),
    int(window.width * (SPAWN_RIGHT - SPAWN_LEFT)),
    int(window.height * (SPAWN_BOTTOM - SPAWN_TOP)),
    border=2,
    color=(255, 255, 255),
    border_color=(255, 0, 0)
)

@window.event
def on_resize(width, height):
    background_image.width = width
    background_image.height = height
    return pyglet.event.EVENT_HANDLED

@window.event
def on_mouse_press(x, y, button, modifiers):
    Target.propagate_click(x, y)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        os._exit(0)  # sys.exit(0) -> for mac and linux

@window.event
def on_draw():
    window.clear()
    background_image.blit(0, 0)
    Target.draw_targets()
    # bb_wall.draw() # For testing the spawn area

    glow = shapes.Circle(x=mouse_x, y=mouse_y, radius=7, color=(255, 40, 40))
    core = shapes.Circle(x=mouse_x, y=mouse_y, radius=3, color=(255, 220, 220))

    glow.draw()
    core.draw()

clock.schedule_interval(Target.update_targets, 0.1)
clock.schedule_interval(Target.create_target, 0.15)

pyglet.app.run()
