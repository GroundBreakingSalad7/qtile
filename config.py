# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.notify import notifier
#from libqtile.utils import guess_terminal
import os # To run shell commands
import weakref # To control volume

mod = "mod4"
alt = "mod1"

# debugging
logger.warning("Error")

terminal = 'st'
terminal_session = f'{terminal} -e tmux'
file = f'{terminal} -e vifm'
otherfilemanager = 'nautilus -w'
browser = 'firefox'
incognitobrowser = 'firefox --private-window'
notes = f'{terminal} -e joplin'
dmenu = 'dmenu_run -i -fn "Ploni ML V2 AAA:bold:pixelsize=18"'
torrent = 'dmenu-torrent'
create_doc = '/home/yoavkonak/.scripts/create-latex-document.sh'
password = 'dmenu_pass 18'
screenshot = 'flameshot gui -p /home/yoavkonak/'
social = 'signal-desktop'
music = f'{terminal} -e ncmpcpp'
top = f'{terminal} -e gotop'
lock = '/home/yoavkonak/.scripts/lock.sh'
fancylock = 'i3lock-fancy-dualmonitor -f Ploni-ML-v2-AAA-Light'
toggle_hebrew = '~/.config/qtile/scripts/toggle_hebrew.sh'
# Music
music_play_pause = 'bash -c "if mpc status | grep paused; then mpc play; else mpc pause; fi"'
#music_seekthroughforward = 'bash -c "mpc seekthrough +1"'
#music_seekthroughback = 'bash -c "mpc seekthrough -2"'

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod], "space", lazy.spawn(toggle_hebrew),
        desc="Toggle hebrew"),
    
    # Add alt+tab functionality
    Key([alt], "Tab", lazy.layout.next(), 
        desc="Move window focus to other window"),
    Key([alt, "shift"], "Tab", lazy.layout.previous(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal_session), desc=f'Launch terminal: {terminal}'),
    Key([mod], "t", lazy.spawn(terminal_session), desc=f'Launch terminal: {terminal}'),
    Key([mod, "shift"], "t", lazy.spawn(f'bash -c \"{terminal} -e $SHELL\"')),
    Key([mod, "control", "shift"], "t", lazy.spawn(f'bash -c \"CMD=$(dmenu_path | dmenu -i -fn \'Ploni ML V2 AAA:bold:pixelsize=18\' -p \'What command do you want to run? \'); [ -z $CMD ] || {terminal} -e $CMD\"'), desc=f'Launch terminal: {terminal}'),
    # Key([mod, "control", "shift"], "t", lazy.spawn(f'bash -c \"CMD=$(dmenu_path | dmenu -i -fn \'Ploni ML V2 AAA:bold:pixelsize=18\' -p \'What command do you want to run? \'); {terminal} -e $CMD\"'), desc=f'Launch terminal: {terminal}'),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, alt, "shift", "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(dmenu),
        desc="Spawn a command using dmenu"),
    Key([mod, "shift"], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Make the focused window fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),

    # Volume control
    Key([mod, alt, 'control'], "k", lazy.spawn('amixer -D pulse sset Master 5%+'), desc="Volume up"),
    Key([mod, alt, 'control'], "j", lazy.spawn('amixer -D pulse sset Master 5%-'), desc="Volume down"),
    Key([mod, alt, 'control'], "m", lazy.spawn('amixer -D pulse sset Master toggle'), desc="Mute volume"),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer -D pulse sset Master 10%+"),
        desc="Increase volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer -D pulse sset Master 5%-"),
        desc="Decrease volume",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer -D pulse sset Master toggle"),
        desc="Toggle mute",
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause"),

    # Music control (MPD)
    Key([mod, alt, 'control'], "p", lazy.spawn(music_play_pause), desc="Toggle pause (mpc)"),
    #Key([mod, alt, 'control'], ".", lazy.spawn(music_seekthroughforward), desc="test"),
    #Key([mod, alt, 'control'], ",", lazy.spawn(music_seekthroughback), desc="test"),

    Key([mod], "v", lazy.spawn('pavucontrol'), desc="Volume control"),

    # Lock the screen
    Key([mod, alt, 'control'], "l", lazy.spawn(lock), desc="Lock the screen"),
    Key([mod, alt, 'control', 'shift'], "l", lazy.spawn(fancylock),
            desc="Lock the screen with blur effect"),
    
    # Launch a web browser
    Key([mod], "b", lazy.spawn(browser), desc="Launch a web browser"),
    Key([mod, 'shift'], "b", lazy.spawn(incognitobrowser), desc="Launch a web browser"),
    
    # Launch a file manager
    Key([mod], "e", lazy.spawn(file), desc="Launch a file manager"),
    Key([mod, 'shift'], "e", lazy.spawn(otherfilemanager), desc="Launch a GUI file manager"),

    # Launch ytop
    Key([mod], "m", lazy.spawn(top), desc="Launch ytop"),
    
    # Launch ytop
    Key([mod], "c", lazy.spawn(f'{terminal} -e joplin'), desc="Launch Joplin"),
    
    # Launch ncmpcpp
    Key([mod, 'shift'], "m", lazy.spawn(music), desc="Launch ncmpcpp"),
    
    # Take a screenshot
    Key([mod], "p", lazy.spawn(screenshot), desc="Take a screenshot"),
    
    # Password manager
    Key([mod, 'shift'], "p", lazy.spawn(password), desc="Password manager"),
    
    # Torrent
    Key([mod], "g", lazy.spawn(torrent), desc="Torrent"),
    
    # Create LaTeX documents
    Key([mod], "d", lazy.spawn(create_doc), desc="Create LaTeX documents"),

]

def show_keys():
    key_help = ""
    for k in keys:
        mods = ""

        for m in k.modifiers:
            if m == "mod4":
                mods += "Super + "
            else:
                mods += m.capitalize() + " + "

        if len(k.key) > 1:
            mods += k.key.capitalize()
        else:
            mods += k.key

        key_help += "{:<30} {}".format(mods, k.desc + "\n")

    return key_help

keys.extend(
    [
        Key(
            [mod],
            "a",
            lazy.spawn(
                "sh -c 'echo \""
                + show_keys()
                + '" | rofi -dmenu -theme ~/.config/rofi/configTall.rasi -i -p "?"\''
            ),
            desc="Print keyboard bindings",
        ),
    ]
)

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False),
            desc="Switch to & move focused window to group {}".format(i.name)),
        Key([mod, "control", "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

border_color = '#5b5f7a'
border_color_inactive = '#282a38'
default_margin=0

layouts = [
    layout.Columns(margin=default_margin,
        border_focus=border_color,
        border_focus_stack='#9fa5ce',
        border_normal=border_color_inactive,
        border_normal_stack=border_color_inactive),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Floating(border_focus=border_color,
        border_normal=border_color_inactive,
        border_width=2),
    # layout.Matrix(),
    #layout.MonadTall(),
    layout.Bsp(margin=default_margin,
        border_focus=border_color,
        border_normal=border_color_inactive),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(border_focus=border_color,
        border_normal=border_color_inactive,
        border_width=2),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Ploni ML V2 AAA',
    fontsize=14,
    padding=8,
)
extension_defaults = widget_defaults.copy()

# widget.GroupBox colors
other_fg_color = '#5b5f7a'
grey_fg_color = '#404040'

#fg_color = '#ae9ff2'
fg_color = '#8A8EA8'
bg_color = '#252735'

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.Image(
                    #filename = "~/.config/qtile/logo.png",
                    #scale = "False",
                    #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal_session)}),
                
                widget.TextBox("Qtile", foreground=fg_color,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal_session)}),

                #widget.Sep(
                    #linewidth = 0,
                    #padding = 6,
                    #foreground = fg_color,
                    #background = bg_color
                    #),

                widget.GroupBox(other_current_screen_border=other_fg_color,
                    current_screen_border=other_fg_color,
                    this_current_screen_border=other_fg_color,
                    this_screen_border=grey_fg_color,
                    inactive=other_fg_color,
                    #highlight_method="block",
                    disable_drag=True,
                    rounded=True),
                widget.Prompt(),

                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),

                # Clock
                widget.TextBox("Current time:", foreground=fg_color),
                widget.Clock(format='%I:%M:%S %p %a %d/%m/%Y'),

                # Layout
                widget.Sep(),
                widget.TextBox("Current layout:", foreground=fg_color),
                widget.CurrentLayout(),

                ## Keyboard layout
                #widget.Sep(),
                #widget.KeyboardLayout(configured_keyboards=['us', 'il']),
                #widget.TextBox("Keyboard layout:", foreground=fg_color),
                #widget.TextBox(os.system('xkb-switch')),
                #widget.KeyboardLayout(configured_keyboards=['us', 'il']),

                # Volume
                widget.Sep(),
                widget.TextBox("Volume:", foreground=fg_color),
                widget.Volume(),

                # System tray
                widget.Sep(),
                widget.TextBox("System tray:", foreground=fg_color),
                widget.Systray(),

                #widget.QuickExit(),
            ],
            24,
            background=bg_color,
            opacity=0.925,
            #opacity=0.85,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# Set wallpaper
#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/arthur-rachbauer.jpg'
#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/boris-baldinger-VEkIsvDviSs-unsplash.jpg'

############################################### BLUE ##########################################
#  wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/david-clode-EknN2SI7X80-unsplash.jpg'
#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/matt-hardy-6ArTTluciuA-unsplash.jpg'
#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/rene-padillo-GyUoN-opIMM-unsplash.jpg'
############################################### BLUE ##########################################
# FAVORITE
#####    wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/vincentiu-solomon-Z4wF0h47fy8-unsplash.jpg'
wallpaper_choice = '~/.config/qtile/Wallpapers/Purple/andrew-clifton.jpg' # Yellow
#wallpaper_choice = '~/.config/qtile/Wallpapers/elena-prokofyeva-NDuPLKYRXQU-unsplash.jpg' # blue

#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/leon-overweel-GZd3l4Yxdxs-unsplash.jpg'
##wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/ian-dooley-DuBNA1QMpPA-unsplash.jpg'
#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/jeremy-bishop-9pRjY4d7nJE-unsplash.jpg'
#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/krisztian-tabori-nZGNVOvEYio-unsplash.jpg'
#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/mar-bustos-ARVFsI-32Uk-unsplash.jpg'
wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/quino-al-JFeOy62yjXk-unsplash.jpg'
## Purple
# wallpaper_choice = '~/.config/qtile/Wallpapers/Purple/kai-oberhauser-BKAaLmT0tIs-unsplash.jpg'
# wallpaper_choice = '~/.config/qtile/Wallpapers/Purple/arch.png'
# wallpaper_choice = '~/.config/qtile/Wallpapers/arch_dracula.png'
# wallpaper_choice = '~/.config/qtile/Wallpapers/Purple/arunas-naujokas-wWeu12lTDbU-unsplash.jpg'
#wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/oleg-chursin-vaPoJZB9Mzg-unsplash.jpg'
# wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/james-donovan-kFHz9Xh3PPU-unsplash.jpg'
wallpaper_choice = '~/.config/qtile/Wallpapers/Unsplash/waranont-joe-T7qyLNPwgKA-unsplash.jpg'

os.system('feh --bg-fill ' + wallpaper_choice)

# Run on startup
os.system('~/.config/qtile/autorun.sh')

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False # Follow cursor focus
floating_layout = layout.Floating(border_focus=border_color,
        border_normal=border_color_inactive,
        border_width=3,
        float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_type="utility"),
        Match(wm_type="notification"),
        Match(wm_class='confirmreset'),       # gitk
        Match(wm_class='makebranch'),         # gitk
        Match(wm_class='maketag'),            # gitk
        Match(wm_class='ssh-askpass'),        # ssh-askpass
        Match(wm_class='Pinentry-gtk-2'),     # GPG key password entry
        Match(wm_class='gnome-calculator'),   # Gnome calculator
        #Match(wm_class='pavucontrol'),        # Pavucontrol
        Match(title='branchdialog'),          # gitk
        Match(title='pinentry'),              # GPG key password entry
        Match(title='pinentry-gtk-2'),        # GPG key password entry
        ])
auto_fullscreen = True # Allow windows to request fullscreen
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"
wmname = "qtile"
