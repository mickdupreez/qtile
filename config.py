import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401
from libqtile.dgroups import simple_key_binder

mod = "mod4"
terminal = "alacritty"


keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
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
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

colors = [["#f8f8f2", "#f8f8f2"], #0 WHITE
          ["#282a36", "#282a36"], #1 GREAY
          ["#6272a4", "#6272a4"], #2 PURPLE
          ["#ff5555", "#ff5555"]] #3 RED

layouts = [

    layout.Bsp(
        fair = False,
        border_focus = '#e1acff',
        margin_on_single = None,
        margin = 10,
        border_width = 4),
    layout.Columns(
        border_focus = '#e1acff',
        margin_on_single = None,
        margin = 10,
        border_width = 4),
    layout.Max(),
]

group_names = [("1", {'layout': 'monadtall'}),
               ("2", {'layout': 'monadtall'}),
               ("3", {'layout': 'monadtall'}),
               ("4", {'layout': 'monadtall'}),
               ("5", {'layout': 'monadtall'}),
               ("6", {'layout': 'monadtall'}),
               ("7", {'layout': 'monadtall'}),
               ("8", {'layout': 'monadtall'}),
               ("9", {'layout': 'monadtall'})]


groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group
# allow mod3+1 through mod3+0 to bind to groups; if you bind your groups
# by hand in your config, you don't need to do this.
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder([mod])

widget_defaults = dict(
    font='MesloLGS NF BOLD',
    fontsize=15,
    padding=0,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
#### LEFT SIDE OF THE BAR ####


                ##workspaces##
                widget.GroupBox(
                    highlight_method = "rounded",
                    active = colors[3],
                    inactive = colors[1],
                    this_current_screen_border = colors[3],
                    this_screen_border = colors[3],
                    background = colors[2]
                ),


                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    foreground = colors[2],
                    background = colors[3]
                ),

                widget.Image(
                    filename = '~/Pictures/icons/firefox-icon.png',
                    margin = 2,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('firefox')},
                    background = colors[3]
                ),

                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    foreground = colors[3],
                    background = colors[2]
                ),

                widget.Image(
                    filename = '~/Pictures/icons/emacs-icon.png',
                    margin = 0,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('emacs')},
                    background = colors[2]
                ),

                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    foreground = colors[2],
                    background = colors[1]
                ),

                ##separator##
                widget.Sep(
                    linewidth = 0,
                    padding = 16,
                    background = colors[1]
                ),

                ###window name##
                widget.WindowName(
                    empty_group_string = 'No Windows open',
                ),







#### RIGHT SIDE OF THE BAR ####


                ##systray##
                widget.Systray(),
               ### CPU WIDGET ###
                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    foreground = colors[2],
                    background = colors[1]
                ),

                widget.TextBox(
                    text = ' ',
                    fontsize = 20,
                    padding = 0,
                    foreground  = colors[1],
                    background = colors[2]
                ),


                widget.CPUGraph(
                    background = colors[2]
                ),

                widget.CPU(
                    foreground = colors[1],
                    background = colors[2],
                ),

                ### RAM WIDGET ###
                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    foreground = colors[3],
                    background = colors[2],
                ),

                widget.TextBox(
                    text = ' ',
                    fontsize = 20,
                    padding = 0,
                    foreground = colors[1],
                    background = colors[3],
                ),

                widget.MemoryGraph(
                    background = colors[3],
                ),

                widget.Memory(
                    background = colors[3],
                    foreground = colors[1],
                ),

                ### NETWORK WIDGET ###
                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    foreground = colors[2],
                    background = colors[3],
                ),

                widget.TextBox(
                    text = ' ',
                    fontsize = 20,
                    padding = 0,
                    foreground = colors[1],
                    background = colors[2],
                ),


                widget.NetGraph(
                    background = colors[2],
                ),


                widget.Net(
                    interface = 'wlp5s0',
                    format = '{down} ↓↑{up}',
                    foreground = colors[1],
                    background = colors[2],
                ),

                ### CLOCK WIDGET ###
                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    background = colors[2],
                    foreground = colors[3],
                ),

                widget.TextBox(
                    text = ' ',
                    fontsize = 20,
                    padding = 0,
                    background = colors[3],
                    foreground = colors[1],

                ),


                widget.Clock(
                    format='%d-%m %a %I:%M %p',
                    background = colors[3],
                    foreground = colors[1],
                ),

                ### VOLUME WIDGET ###
                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    background = colors[3],
                    foreground = colors[2],
                ),

                widget.TextBox(
                    text = ' ',
                    fontsize = 25,
                    padding = 1,
                    background = colors[2],
                    foreground = colors[1],
                ),

                widget.Volume(
                    padding = 5,
                    format = '{}',
                    background = colors[2],
                    foreground = colors[1],

                ),

                ### LOGOUT WIDGET ###
                widget.TextBox(
                    text = '',
                    fontsize = 18,
                    padding = 0,
                    foreground = colors[3],
                    background = colors[2],
                ),

                widget.QuickExit(
                    fontsize = 20,
                    default_text = '  ',
                    countdown_format = ' {}  ',
                    background = colors[3],
                    foreground = colors[1],
                ),
            ],
            24,
            background=colors[1],
            opacity = 1,
            margin = 5,
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

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
