
![kadramans Galaxy Blast](media/screenshot-1.png)

This is a simple but functional retro space shooter written in [Python](https://www.python.org/)
using the [Pygame](https://www.pygame.org/) library. It makes use of some interesting practices 
that you could potentially use in your own game, including:

    - State machine for navigating between games states and passing/persisting data between them
    - Use of "spritesheets" to quickly load sprite data from a single file
    - Simple menu system for selecting/navigating the game
    - Game control using keyboard or joystick/gamepad
    - Frame independence using "delta time" in animations

The game's graphics are bespoke (with [Galaga](https://en.wikipedia.org/wiki/Galaga) style enemies) but 
sounds and music are download from [Freesound](https://freesound.org/).
The individual files have retained original filenames with id and user for reference and attribution.

## Running the game

The game is designed to work with Python 3 and can be downloaded and configured using the following from 
a command prompt:

```aidl
pip install virtualenv
git clone https://github.com/kadraman/galaxy-blast.git
cd galaxy-blast
python -m venv dev
source dev/bin/activate
pip install -r requirements.txt
python main.py
```

## Playing the game

The game play should be recognisable - simply kill as many enemies as possible (as many times as 
possible) before you loose all of your lives! There are a number of enemies which move and attack in
different ways and are worth different points:

![Minion 1](assets/images/enemy_1_ship-1.png?raw=true) - 1 point 
![Minion 2](assets/images/enemy_2_ship-1.png?raw=true) - 2 points
![Minion 3](assets/images/enemy_3_ship-1.png?raw=true) - 5 points
![Master Enemy](assets/images/master_enemy_1_ship-1.png?raw=true) - 10 points (watch those mines)
![Boss Enemy](assets/images/boss_enemy_ship-1.png?raw=true) - 25 points (takes a few hits)

There's also an extra 50 points for completing a wave!

![Game Play](media/screenshot-2.png)

Enjoy!!

"kadraman"
