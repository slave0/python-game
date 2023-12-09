from map import Map
from utils import cls
from helicopter import Helicopter as Helico
from pynput import keyboard
import time
import json

TICK_SLEEP = 0.05
TREE_UPDATE = 50
FIRE_UPDATE = 120
CLOUDS_UPDATE = 100
MAP_WIDTH, MAP_HEIGHT = 20, 10
MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
# f - save, g - locad

helico = Helico(MAP_WIDTH, MAP_HEIGHT)
map = Map(MAP_WIDTH, MAP_HEIGHT)

print(helico.x, helico.y)
tick = 1
def process_key(key):
    global helico, map, tick
    key = key.char
    # Обработка движений вертолета
    if key in MOVES.keys():
        y, x = MOVES[key][0], MOVES[key][1]
        helico.move(x, y)
    # Сохранение игры
    elif key == 'f':
        data = {"helicopter": helico.export_data(), 
                "clouds": map.clouds.export_data(), 
                "map": map.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    # Загрузка игры
    elif key == 'g':
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            helico.import_data(data["helicopter"])
            map.import_data(data["map"])
            map.clouds.import_data(data["clouds"])
            tick = data["tick"]

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key, )
listener.start()


while True:
    cls()
    map.process_helicopter(helico)
    helico.print_stats()
    map.print_map(helico)
    print("TICK", tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        map.set_with_condition(map.rand_cell(), 0, 1)
    if (tick % FIRE_UPDATE == 0):
        map.update_fires(helico)
    if (tick % CLOUDS_UPDATE == 0):
        map.update_clouds()