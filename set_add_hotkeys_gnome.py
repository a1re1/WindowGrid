#!/usr/bin/env python3
import os

ABSOLUTE_PATH_TO_PYTHON = "/usr/bin/python3"
ABSOLUTE_PATH_TO_SHUFFLER = "/home/tyler/projects/window-shuffler/window_shuffler"
ABSOLUTE_PATH_TO_SHUFFLER_NO_GUI = "/home/tyler/projects/window-shuffler/window_shuffler_no_gui.py"
SHUFFLE_COMMAND = "%s %s" % (ABSOLUTE_PATH_TO_PYTHON, ABSOLUTE_PATH_TO_SHUFFLER)
SHUFFLE_COMMAND_NO_GUI = "%s %s" % (ABSOLUTE_PATH_TO_PYTHON, ABSOLUTE_PATH_TO_SHUFFLER_NO_GUI)

HOT_KEY_NAMES={
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/previewgrid/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/shrinkwindowhorizontal/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/snapallwindows/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/growwindowhorizontal/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/shrinkwindowhorizontal/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/growwindowvertical/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/movewindowleft/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/movewindowright/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/movewindowup/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/movewindowdown/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/shrinkgridhorizontal/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/growgridhorizontal/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/shrinkgridvertical/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/growgridvertical/'",
  "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/togglewindowfullscreen/'"
}


def set_hotkey(key, name, command, binding):
  os.system('gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/%s/ name %s' % (key, name))
  os.system('gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/%s/ command %s' % (key, command))
  os.system('gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/%s/ binding %s' % (key, binding))


def get_hotkey(key):
  os.system('gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/%s/ name' % key)
  os.system('gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/%s/ command' % key)
  os.system('gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/%s/ binding' % key)


def append_hotkeys_to_current(new_hotkeys):
  current_hotkeys = os.popen('gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings').read()
  list_of_current_hotkeys = set(current_hotkeys[1:-2].split(", ")) if current_hotkeys.strip() != "@as []" else set()
  final_set_of_hotkeys = list_of_current_hotkeys.union(new_hotkeys)
  return(final_set_of_hotkeys)


def convert_hotkey_set_to_string(hotkeys):
  separator = ", "
  result = "\"[" + separator.join(hotkeys) + "]\""
  return result


def init_hotkeys(hotkeys):
  cmd = "gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "+ convert_hotkey_set_to_string(hotkeys)
  os.system(cmd)


def build_shuffle_command(args, cmd = SHUFFLE_COMMAND_NO_GUI):
  return "'" + cmd + " " + args + "'"
  

init_hotkeys(append_hotkeys_to_current(HOT_KEY_NAMES))
set_hotkey("previewgrid", "'Preview Grid'", build_shuffle_command("", cmd = SHUFFLE_COMMAND), "'<Primary><Alt><Super>g'")
set_hotkey("shrinkwindowhorizontal", "'Snap All Windows to Grid'", build_shuffle_command("s"), "'<Primary><Alt><Super>space'")
set_hotkey("snapallwindows", "'Shrink Window Horizontal'", build_shuffle_command("r -1 0"), "'<Primary><Alt><Super>Left'")
set_hotkey("growwindowhorizontal", "'Grow Window Horizontal'", build_shuffle_command("r 1 0"), "'<Primary><Alt><Super>Right'")
set_hotkey("shrinkwindowhorizontal", "'Shrink Window Vertical'", build_shuffle_command("r 0 -1"), "'<Primary><Alt><Super>Up'")
set_hotkey("growwindowvertical", "'Grow Window Vertical'", build_shuffle_command("r 0 1"), "'<Primary><Alt><Super>Down'")
set_hotkey("movewindowleft", "'Move Window Left'", build_shuffle_command("m -1 0"), "'<Super>Left'")
set_hotkey("movewindowright", "'Move Window Right'", build_shuffle_command("m 1 0"), "'<Super>Right'")
set_hotkey("movewindowup", "'Move Window Up'", build_shuffle_command("m 0 -1"), "'<Super>Up'")
set_hotkey("movewindowdown", "'Move Window Down'", build_shuffle_command("m 0 1"), "'<Super>Down'")
set_hotkey("shrinkgridhorizontal", "'Shrink Grid Horizontal'", build_shuffle_command("rg -1 0"), "'<Primary><Alt><Super>minus'")
set_hotkey("growgridhorizontal", "'Grow Grid Horizontal'", build_shuffle_command("rg 1 0"), "'<Primary><Alt><Super>equal'")
set_hotkey("shrinkgridvertical", "'Shrink Grid Vertical'", build_shuffle_command("rg 0 -1"), "'<Primary><Shift><Alt><Super>underscore'")
set_hotkey("growgridvertical", "'Grow Grid Vertical'", build_shuffle_command("rg 0 1"), "'<Primary><Shift><Alt><Super>plus'")
set_hotkey("togglewindowfullscreen", "'Toggle Window Fullscreen'", build_shuffle_command("f"), "'<Primary><Super>Up'")
