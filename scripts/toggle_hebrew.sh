#!/bin/sh
setxkbmap -layout "us,il" -option ""
[ "$(xkb-switch)" = "us" ] && xkb-switch -s il || xkb-switch -s us
xset r rate 400 80 >/dev/null 2>&1
setxkbmap -option caps:swapescape >/dev/null 2>&1
xmodmap ~/.Xmodmap >/dev/null 2>&1
