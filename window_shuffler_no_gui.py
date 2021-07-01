#!/usr/bin/env python3
import shuffler_tools as st
import shuffler_geo as geo
import gi
gi.require_version("Wnck", "3.0")
from gi.repository import Wnck
import sys
from shuffler_tools import app_path
import subprocess

"""
FXNS TO FETCH DATA
"""

def get_grid_dimensions():
  try:
      return [
          int(n) for n in open(st.matr_file).read().strip().split()
      ]
  except FileNotFoundError:
      return [2, 2]


def get_monitor_dimensions():
  win_geodata = geo.get_windows_oncurrent_stacked(Wnck.Screen.get_default())
  wins = win_geodata["windows"]
  monitor_dimensions = st.calc_monitor_dimensions(win_geodata)
  return monitor_dimensions


def get_grid_tile_dimensions():
  monitor_dimensions = get_monitor_dimensions()
  grid_dimensions = get_grid_dimensions()
  monitor_span_x = monitor_dimensions[1][0] - monitor_dimensions[0][0]
  monitor_span_y = monitor_dimensions[1][1] - monitor_dimensions[0][1]
  tile_span_x = monitor_span_x // grid_dimensions[0]
  tile_span_y = monitor_span_y // grid_dimensions[1]
  return (tile_span_x, tile_span_y)


def get_current_grid_position(window):
  window_geometry = window.get_geometry()
  grid_dimensions = get_grid_dimensions()
  tile_dimensions = get_grid_tile_dimensions()
  window_offset_x = window_geometry[0]
  window_offset_y = window_geometry[1]
  window_width = window_geometry[2]
  window_height = window_geometry[3]
  
  tiles_offset_x = round(window_offset_x / tile_dimensions[0])
  tiles_offset_y = round(window_offset_y / tile_dimensions[1])
  tiles_spanned_by_window_x = round(window_width / tile_dimensions[0])
  tiles_spanned_by_window_y = round(window_height / tile_dimensions[1])
  return (
    tiles_offset_x, 
    tiles_offset_y, 
    tiles_offset_x + tiles_spanned_by_window_x, 
    tiles_offset_y + tiles_spanned_by_window_y
  )


def get_active_window():
  screendata = Wnck.Screen.get_default()
  screendata.force_update()
  return screendata.get_active_window()


"""
FXNS TO MUTATE STATE
"""

def save_grid(x, y):
  open(st.matr_file, "wt").write(str(x) + " " + str(y))


def toggle_max():
  active_window = get_active_window()
  ismax = active_window.is_maximized()
  if ismax:
      active_window.unmaximize()
  else:
      active_window.maximize()


def move_window(window, starting_tile_x, starting_tile_y, ending_tile_x, ending_tile_y):
  grid_dimensions = get_grid_dimensions()
  grid_tile_dimensions = get_grid_tile_dimensions()

  start_x = (grid_tile_dimensions[0] * (starting_tile_x)) + st.MARGIN
  start_y = (grid_tile_dimensions[1] * (starting_tile_y)) + st.MARGIN + st.TITLE_BAR_OFFSET_Y
  width = (max(1, ending_tile_x - starting_tile_x) * grid_tile_dimensions[0]) - (2 * st.MARGIN)
  height = (max(1, ending_tile_y - starting_tile_y) * grid_tile_dimensions[1]) - (2 * st.MARGIN)

  st.shuffle(window, start_x, start_y, width, height)
  return


def shift_window(window, shift_x, shift_y):
  grid_dimensions = get_grid_dimensions()
  current_tile_position = get_current_grid_position(window)

  new_tile_start_x = min(grid_dimensions[0], max(0, current_tile_position[0] + shift_x))
  new_tile_start_y = min(grid_dimensions[1], max(0, current_tile_position[1] + shift_y))
  new_tile_end_x = min(grid_dimensions[0], max(0, current_tile_position[2] + shift_x))
  new_tile_end_y = min(grid_dimensions[1], max(0, current_tile_position[3] + shift_y))

  move_window(window, new_tile_start_x, new_tile_start_y, new_tile_end_x, new_tile_end_y)
  
  
def snap_window(window):
  shift_window(window, 0, 0)


def resize_window(window, resize_x, resize_y):
  grid_dimensions = get_grid_dimensions()
  current_tile_position = get_current_grid_position(window)

  new_tile_start_x = current_tile_position[0]
  new_tile_start_y = current_tile_position[1]
  new_tile_end_x = min(grid_dimensions[0], max(0, current_tile_position[2] + resize_x))
  new_tile_end_y = min(grid_dimensions[1], max(0, current_tile_position[3] + resize_y))

  move_window(window, new_tile_start_x, new_tile_start_y, new_tile_end_x, new_tile_end_y)


"""
MAIN FUNCTION
"""

if __name__ == "__main__":
  shuffler_args = sys.argv[1:]

  if shuffler_args[0] == "s": # snap
    scr = Wnck.Screen.get_default()
    scr.force_update()
    win_geodata = geo.get_windows_oncurrent_stacked(scr)
    windows = win_geodata["windows"]
    for window in windows:
      snap_window(window)
  elif shuffler_args[0] == "f": # fullscreen
    toggle_max()
  elif shuffler_args[0] == "m": # move active
    shift_x = int(shuffler_args[1])
    shift_y = int(shuffler_args[2])
    window = get_active_window()
    shift_window(window, shift_x, shift_y)
  elif shuffler_args[0] == "r": # resize
    resize_x = int(shuffler_args[1])
    resize_y = int(shuffler_args[2])
    window = get_active_window()
    resize_window(window, resize_x, resize_y)