import pygame as pg
try:
    import queue
except ImportError:
    import Queue as queue

from .base_state import BaseState

from modules.display_utils import BackGround
from modules.display_utils import TextPrint

import constants


class ControllerTest(BaseState):
    def __init__(self):
        super(ControllerTest, self).__init__()
        self.interval = 0
        self.last_press = None
        self.messages = queue.Queue()
        # self.options = ["Display", "Controller", "Main Menu"]
        self.next_state = "SETTINGS"

    def startup(self, persistent):
        self.messages = queue.Queue()
        self.interval = 0
        self.last_press = None
        self.persist = persistent
        color = self.persist["screen_color"]
        try:
            color
        except NameError:
            color = self.default_screen_color
        self.screen_color = color
        background = self.persist["background"]
        try:
            background
        except NameError:
            background = self.default_background
        self.background = background

    def render_text(self, index):
        color = pg.Color("red") if index == self.active_index else pg.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0],
                  self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def get_event(self, event, controller):
        if event.type < pg.USEREVENT:
            etype = event.type
            if hasattr(event, "key"):
                ekey = event.key
                ename = pg.key.name(event.key)
            else:
                ekey = None
                ename = None
            self.messages.put('event type: %s: key: %s name: %s' % (str(etype), str(ekey), ename))
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.next_state = "SETTINGS"
                self.done = True
        elif event.type == pg.JOYBUTTONDOWN:
            self.messages.put('Joystick %d, button: %d pressed' % (event.joy, event.button))
        elif event.type == pg.JOYBUTTONUP:
            self.messages.put('Joystick %d, button: %d released' % (event.joy, event.button))

    def draw(self, surface):
        # background = BackGround(constants.DEFAULT_BACKGROUND, [0, 0])
        # surface.fill([255, 255, 255])
        # surface.blit(background.image, background.rect)
        surface.fill(self.screen_color)

        tp = TextPrint()

        tp.draw(surface, "[Press ESC to stop test]")

        # Get count of joysticks
        joystick_count = pg.joystick.get_count()

        tp.draw(surface, "Number of joysticks: {}".format(joystick_count))
        tp.indent()

        # For each joystick:
        for i in range(joystick_count):
            joystick = pg.joystick.Joystick(i)
            # joystick.init()

            tp.draw(surface, "Joystick {}".format(i))
            tp.indent()

            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            tp.draw(surface, "Joystick name: {}".format(name))

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            tp.draw(surface, "Number of axes: {}".format(axes))
            tp.indent()

            for j in range(axes):
                axis = joystick.get_axis(i)
                tp.draw(surface, "Axis {} value: {:>6.3f}".format(j, axis))
            tp.unindent()

            buttons = joystick.get_numbuttons()
            tp.draw(surface, "Number of buttons: {}".format(buttons))
            tp.indent()

            for k in range(buttons):
                button = joystick.get_button(i)
                tp.draw(surface, "Button {:>2} value: {}".format(k, button))
            tp.unindent()

            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            tp.draw(surface, "Number of hats: {}".format(hats))
            tp.indent()

            for l in range(hats):
                hat = joystick.get_hat(i)
                tp.draw(surface, "Hat {} value: {}".format(l, str(hat)))
            tp.unindent()

            tp.unindent()

        # Print any button messages from the queue
        self.interval += 1
        if not self.messages.empty():
            self.last_press = self.messages.get()
        else:
            tp.indent()
            tp.draw(surface, self.last_press)
            tp.unindent()
