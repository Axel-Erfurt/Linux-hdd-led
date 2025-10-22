#!/usr/bin/env python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import warnings
warnings.filterwarnings("ignore")

if len(sys.argv) < 3:
    print("Es müssen 2 Geräte angegeben werden")
    sys.exit()

hd = sys.argv[1]
hd_2 = sys.argv[2]
fn = f"/sys/block/{hd}/stat"
fn_2 = f"/sys/block/{hd_2}/stat"
UPDATE = 100    # update interval in ms
ro, wo = 0, 0
last = ""
UPDATE_2 = 100    # update interval in ms
ro_2, wo_2 = 0, 0
last_2 = ""

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
    
def update_2():
    global ro_2, wo_2, last_2

    f_2 = open(fn_2).read().split()
    r_2, w_2 = f_2[0], f_2[4]
    rr_2, ww_2 = "0", "0"
    if r_2 != ro_2:
        rr_2 = "1"
    if w_2 != wo_2:
        ww_2 = "1"
    ro_2, wo_2 = r_2, w_2
    i = f"icon{rr_2}{ww_2}.png"
    if i != last_2:
        tray.set_from_file(i)
        tray.set_visible(True)
        last_2 = i
    GLib.timeout_add(UPDATE_2, update_2)

tray.connect("activate", Gtk.main_quit)
update()
update_2()
Gtk.main()

