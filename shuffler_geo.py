#!/usr/bin/env python3
import subprocess
import gi
gi.require_version("Wnck", "3.0")
from gi.repository import Wnck, Gdk


"""
WindowShuffler
Author: Jacob Vlijm
Co Author: Tyler Whitehurst
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


def get_currmonitor_atpos(x, y, display=None):
    if not display:
        display = Gdk.Display.get_default()
    display = Gdk.Display.get_default()
    return display.get_monitor_at_point(x, y)


def get_winlist(scr):
    return scr.get_windows_stacked()


def get_strut(xid):
    s = "_NET_WM_STRUT(CARDINAL) = "
    strut_data = subprocess.check_output(
        ["xprop", "-id", xid]
    ).decode("utf-8")
    match = [int(n) for n in [
        l for l in strut_data.splitlines() if s in l
    ][0].split("=")[1].strip().split(",")
    ]
    plank = True if 'WM_NAME(STRING) = "plank"' in strut_data else False
    return match


def get_plankstrutvals(span, strutvals, mpos):
    # get left_strutval - ok
    left = strutvals[0]
    left = left if left == 0 else left - mpos[0]
    # get right strutval
    right = strutvals[1]
    right = right if right == 0 else right - (span[0] - (mpos[0] + mpos[2]))
    # get top strutval
    top = strutvals[2]
    top = top if top == 0 else top - mpos[1]
    # get bottom strutval
    bottom = strutvals[3]
    # print("research", bottom, mpos[1], mpos[3])
    bottom = bottom if bottom == 0 else \
        bottom - (span[1] - (mpos[1] + mpos[3]))
    return left, right, top, bottom


def get_windows_oncurrent_stacked(scr=None):
    # get screen / span size for if plank is on the right
    if not scr:
        scr = Wnck.Screen.get_default()
        scr.force_update()
    screensize = scr.get_width(), scr.get_height()
    # get all windows
    relevants = get_winlist(scr)
    mouse_position = Gdk.get_default_root_window().get_pointer()[1:3]
    currmonitor = get_currmonitor_atpos(mouse_position[0], mouse_position[1])
    planks = []
    otherdocks = []
    normal = []
    # split them up
    for w in relevants:
        loc = w.get_geometry()[:2]
        monitor = get_currmonitor_atpos(loc[0], loc[1])
        if monitor == currmonitor:
            typedata = str(w.get_window_type())
            if "NORMAL" in typedata:
                normal.append(w)
            elif "DOCK" in typedata:
                if w.get_name() == "plank":
                    planks.append(w)
                else:
                    otherdocks.append(w)
    # current monitor position and -size
    mgeo = currmonitor.get_geometry()
    mpos = [mgeo.x, mgeo.y, mgeo.width, mgeo.height]
    # get data on docks on current screen
    dockgeo = [get_strut(str(d.get_xid())) for d in otherdocks]
    plankgeo = [
        get_plankstrutvals(
            screensize, get_strut(str(p.get_xid())), mpos,
        ) for p in planks
    ]
    allpanels = dockgeo + plankgeo
    strut = [sum([strut[i] for strut in allpanels]) for i in range(4)]
    # summarize
    # working area
    wa = [
        strut[0], strut[2], mpos[2] - (strut[0] + strut[1]),
        mpos[3] - (strut[2] + strut[3]),
    ]
    # normal, visible windows on current monitor on current workspace
    currws = scr.get_active_workspace()
    windows = [
        w for w in normal if all([
            w.get_workspace() == currws,
            not w.is_minimized(),
        ])
    ]
    # offset due to monitor position
    offset = mpos[0], mpos[1]
    return {"wa": wa, "windows": windows, "offset": offset}
