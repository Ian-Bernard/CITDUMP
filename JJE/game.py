#!/usr/bin/env python3
# Game file for JJE
# This is how the game functions

from player import Player
from collections import OrderedDict
import world
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import gtk

class handler:
    def on_window1_destroy(self, object, data=None):
        print("quit with cancel")
        gtk.main_quit()

    def on_gtk_quit_activate(self, menuitem, data=None):
        print("quit from menu")
        gtk.main_quit()

    def __init__(self):
        self.gladefile = "MansionGUI.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.show()

main = handler()
gtk.main()

def play():
    print("Escape from the abandoned mansion!")
    world.parse_world_dsl()
    player = Player()
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print("Your journey has been cut short!")

def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action!")

def get_available_actions(room, player):
    actions = OrderedDict()
    print("Choose an action: ")
    if player.inventory:
        action_adder(actions, 'i', player.print_inventory, "Print Inventory")
    if isinstance(room, world.TraderTile):
        action_adder(actions, 't', player.trade, "Trade")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'n', player.move_north, "Go North")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_south, "Go South")
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'e', player.move_east, "Go East")
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'w', player.move_west, "Go West")
        if player.hp < 100:
            action_adder(actions, 'h', player.heal, "Heal")
    return actions

def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))

def get_player_command():
    return input('Action: (N, S, E, W, I, A, H: ')

play()

