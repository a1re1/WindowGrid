# Window Grid

![grid](https://user-images.githubusercontent.com/26413204/124216071-5b4a3580-dac3-11eb-9a23-d9126cbf192f.gif)


(This repo originally is a for of Window Shuffler for Budgie, but I ended up rewriting almost everything for my own preferences.)

This app functions similar to AppGrid for MacOS or PowerToys window managing for Windows.

It's a pretty powerful grid based window mangement system without needing to run a fullon tiling window manager. For your desktop.

This app utilizes a python program that quickly calculate the position of your current window with respect to a predetermined grid then allows you to use various hotkeys to move / resize your active window to span multiple grid elements.

I utilize an ultrawide monitor and being able to snap all windows to arbitrary grids makes multitasking a breeze.

# Setup

1) Clone this repo
2) Modify config.py; Make sure to update the paths `ABSOLUTE_PATH_TO_PYTHON`, `ABSOLUTE_PATH_TO_SHUFFLER`, `ABSOLUTE_PATH_TO_SHUFFLER_NO_GUI`
3) Modify other configs if preferred. `MARGIN` controls the margin between window tiles in the grid. Personally I think a small margin between windows looks nice, but I won't hate you if you turn it to 0. `TITLE_BAR_OFFSET` can be used to position your windows where the top bar would be if you have a hidden topbar. I find that `-32` works as a decent offset. If you do not hide your top bar this likely should be 0.
4) Run `$python3 set_add_hotkeys_gnome.py` to set your keybindings. (You can modify this file to change keybindings from default. They are currently set to my preference.)


# Usage

## Window Management

Move windows: `Alt + Arrow Keys` -- Windows will retain size when moved unless they reach the edge of the screen at which they will shrink to whatever space is available.

Grow window: `Ctrl + Alt + Super + <Arrow Down / Right>` -- You can expand a window to fill the next grid positions with the down and right arrow keys. You can expand windows to available space in the grid.

Shrink window: `Ctrl + Alt + Super + <Arrow Up / Left>` -- You can shrink a window by a single grid tile from the down / right positions. The final span of a window can shrink to either a single row / column.

Toggle fullscreen: `Ctrl + Super + Arrow Up` -- Toggles fullscreen windows.

Snap all non minimized windows to grid: `Ctrl + Alt + Super + Space` -- All non minimized windows will snap to their closest grid positions.


## Grid Management

The system works by tiling each window to a grid. To accomplish this there are some tools to manage your grid layout.

Grow / Shrink number of columns: `Ctrl + Alt + Super + <minus / plus>` respectively -- This will add or remove columns from your grid.

Grow / Shrink number of rows: `Ctrl + Alt + Super + Shift + <minus / plus>` respectively -- This will add or remove rows from your grid.

Visualize current grid layout: `Ctrl + Alt + Super + g` (`Esc` will close the preview) -- This will open an overlay that will show your current layout (there's a bug currently where updating your grid layout will not update the overlay in real time. You can trigger a recalculation of the view with any key input though so it will update eventually.)


# Known Bugs
- Grid preview does not always update in real time.
- Some windows do not always respect top bar offsets. I can't actually figure out how to determine when windows do / don't respect this offset, but it's kind of annoying sometimes. Notably, this happens in Steam.