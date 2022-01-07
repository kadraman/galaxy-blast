import pygame as pg

import constants


class Game(object):
    """
    A single instance of this class is responsible for
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event
    queue, framerate, updating the display, etc.).
    and its run method serves as the "game loop".
    """

    def __init__(self, screen, joystick, states, start_state):
        """
        Initialize the Game object.

        screen: the pygame display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state
        """
        self.done = False
        self.screen = screen
        self.joystick = joystick
        self.clock = pg.time.Clock()
        self.fps = constants.FPS
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        """
        Events are passed for handling to the current state.
        """
        for event in pg.event.get():
            self.state.get_event(event, self.joystick)

    def flip_state(self):
        """
        Switch to the next game state.
        """
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        """
        Check for state flip and update active state.

        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        """
        Pass display surface to active state for drawing.
        """
        self.state.draw(self.screen)

    def run(self):
        """
        Main game loop
        """

        # run startup on first state
        persistent = self.state.persist
        self.state.startup(persistent)

        if constants.MUTE_SOUND:
            pg.mixer.pause()
        else:
            pg.mixer.music.load('./assets/sounds/251461__joshuaempyre__arcade-music-loop.wav')
            pg.mixer.music.play(-1)

        dt = 0
        while not self.done:
            # dt = self.clock.tick(self.fps)
            dt = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.flip()

        pg.mixer.music.stop()
