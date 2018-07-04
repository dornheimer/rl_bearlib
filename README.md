# roguelike

a rewrite of the libtcod/python3 roguelike, using bearlibterminal for
rendering and an engine driven by an entity-component-system.

basic prototype with dungeon generation, player movement and FOV.

## setup

requires Python 3.6

    git clone https://github.com/dornheimer/rl_bearlib
    cd rl_bearlib
    pip install -r requirements.txt

    # start game
    ./main

## [credits]

ecs implementation inspired by
[this project](https://gitlab.com/NoahTheDuke/roguelikedev-tutorial-ecs) (NoahTheDuke) and [ruby rogue](https://github.com/alexkurowski/ruby-rogue) (alexkurowski)
</br>
[tileset](https://gitlab.com/spiral-king/taffer) (Taffer)
