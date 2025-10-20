#!/usr/bin/env python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import warnings
warnings.filterwarnings("ignore")

hd = sys.argv[1]
fn = f"/sys/block/{hd}/stat"
UPDATE = 100    # update interval in ms
ro, wo = 0, 0
last = ""

tray = Gtk.StatusIcon()
tray.set_visible(True)
menu = Gtk.Menu()


def update():
    global ro, wo, last

    f = open(fn).read().split()
    r, w = f[0], f[4]
    rr, ww = "0", "0"
    if r != ro:
        rr = "1"
    if w != wo:
        ww = "1"
    ro, wo = r, w
    i = f"icon{rr}{ww}.png"
    if i != last:
        tray.set_from_file(i)
        tray.set_visible(True)
        last = i
    GLib.timeout_add(UPDATE, update)

tray.connect("activate", Gtk.main_quit)
update()
Gtk.main()

