#!/usr/bin/env python3
import os
import subprocess
import gi
gi.require_version("Wnck", "3.0")
from gi.repository import Wnck
from gi.repository import Gdk


"""
WindowShuffler
Author: Jacob Vlijm
Copyright © 2017-2018 Ubuntu Budgie Developers
Website=https://ubuntubudgie.org
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version. This
program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details. You
should have received a copy of the GNU General Public License along with this
program.  If not, see <https://www.gnu.org/licenses/>.
"""


# paths
userdata = os.path.join(
    os.environ["HOME"], ".config/budgie-extras/windowshuffler",
)

try:
    os.makedirs(userdata)
except FileExistsError:
    pass


MAX_ROWS = 8
MAX_COLUMNS = 20
MARGIN = 16
TITLE_BAR_OFFSET_Y = -32

matr_file = os.path.join(userdata, "matrix")
app_path = os.path.dirname(os.path.abspath(__file__))
shortcuts = os.path.join(app_path, "shortcuts")
firstrun = os.path.join(userdata, "firstrun")
recorded_layout = os.path.join(userdata, "recorded")


def importFile(file):
  data = ""
  for line in open(file):
    data += line
  return data


def calc_monitor_dimensions(win_geodata):
  wins = win_geodata["windows"]
  offset = win_geodata["offset"]
  wa = win_geodata["wa"]
  return [
    [offset[0] + wa[0], offset[1] + wa[1]],
    [wa[2], wa[3]],
  ]


def save_grid(x, y):
  open(matr_file, "wt").write(str(x) + " " + str(y))


def get_grid():
  try:
    return [
      int(n) for n in open(matr_file).read().strip().split()
    ]
  except FileNotFoundError:
    return [2, 2]


def get_grid_modified_at():
  return os.stat(matr_file).st_mtime;


def shuffle(win, x, y, w, h):
  win.unmaximize()
  north_west_corner = Wnck.WindowGravity.NORTHWEST
  flags = Wnck.WindowMoveResizeMask.X | \
    Wnck.WindowMoveResizeMask.Y | \
    Wnck.WindowMoveResizeMask.WIDTH | \
    Wnck.WindowMoveResizeMask.HEIGHT
  win.set_geometry(north_west_corner, flags, x, y, w, h)
