import os
import sys

try:
    import libximc.highlevel as ximc
except ImportError:
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    ximc_dir = os.path.join(cur_dir, "..", "ximc")
    ximc_package_dir = os.path.join(ximc_dir, "crossplatform", "wrappers", "python")
    sys.path.append(ximc_package_dir)
    import libximc.highlevel as ximc

    print("Success!")


def axis_status(axis: ximc.Axis) -> None:
    print("\nGet status")
    status = axis.get_status()
    print("Status.Ipwr: {}".format(status.Ipwr))
    print("Status.Upwr: {}".format(status.Upwr))
    print("Status.Iusb: {}".format(status.Iusb))
    print("Status.Flags: {}".format(status.Flags))


def axis_position(axis: ximc.Axis) -> 'tuple':

    pos = axis.get_position()
    print("Position: {0} steps, {1} Micro-steps".format(pos.Position, pos.uPosition))
    return pos.Position, pos.uPosition


def get_speed(axis: ximc.Axis) -> int:
    print("\nGet speed")
    move_settings = axis.get_move_settings()
    return move_settings.Speed


def set_speed(axis: ximc.Axis, speed: int) -> None:
    print("\nSet speed ")
    move_settings = axis.get_move_settings()
    print("The speed was equal to {0}. We will change it to {1}".format(move_settings.Speed, speed))
    move_settings.Speed = speed
    axis.set_move_settings(move_settings)


enum_flags = ximc.EnumerateFlags.ENUMERATE_PROBE | ximc.EnumerateFlags.ENUMERATE_NETWORK

enum_hints = "addr="

devices_unsorted = ximc.enumerate_devices(enum_flags, enum_hints)
devices = sorted(devices_unsorted, key=lambda d: d["ControllerName"])

if len(devices) == 0:
    print("The devices were not found.")
else:
    # Print devices list
    print("Found {} device(s):".format(len(devices)))

open_names = []

if len(sys.argv) > 1:
    open_names.append(sys.argv[1])
elif len(devices) > 0:
    for device in devices:
        open_names.append(device["uri"])
# print(open_names)

# ******************************************** #
#              Create axis object              #
# ******************************************** #
# Axis is the main libximc.highlevel class. It allows you to interact with the device.
# Axis takes one argument - URI of the device
axes = []  # List to store all Axis objects

for open_name in open_names:
    ax = ximc.Axis(open_name)
    print("\nOpening device " + ax.uri)
    axes.append(ax)

axis1, axis2, axis3 = axes[:3] if len(axes) > 2 else None


def initialize_axes():
    return axis1, axis2, axis3
