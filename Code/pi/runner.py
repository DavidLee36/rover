# This script auto runs on the raspberry pi and is responsible for remotely starting/stopping main.py and shutting down the pi

import os
import subprocess
import sys
import time

import pygame
from pygame._sdl2 import controller as sdl_controller

import controller_mapping as cmap

SHUTDOWN_HOLD_SECS = 3
SHUTDOWN_BTNS = {cmap.A_BTN, cmap.B_BTN, cmap.X_BTN, cmap.Y_BTN}
MAIN_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

def get_child_env():
    env = os.environ.copy()
    env.pop("SDL_VIDEODRIVER", None)
    env.pop("SDL_AUDIODRIVER", None)
    # The runner runs under systemd with no desktop session, so main.py needs
    # the graphical session's variables handed to it to open its pygame window.
    # The Pi desktop is Wayland; SDL2 reaches it through XWayland at DISPLAY=:0.
    env.setdefault("DISPLAY", ":0")
    env.setdefault("WAYLAND_DISPLAY", "wayland-1")
    env.setdefault("XAUTHORITY", "/home/david/.Xauthority")
    env.setdefault("XDG_RUNTIME_DIR", "/run/user/1000")
    return env

def main():
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.display.init()
    sdl_controller.init()
    try:
        sdl_controller.set_eventstate(True)  # ensure CONTROLLER* events are emitted
    except Exception:
        pass  # not present on this pygame build

    controllers = {}
    main_proc = None
    shutdown_hold_start = None
    clock = pygame.time.Clock()

    print("Runner started, waiting for controller...")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.CONTROLLERDEVICEADDED:
                ctrl = sdl_controller.Controller(event.device_index)
                controllers[ctrl.as_joystick().get_instance_id()] = ctrl
                print(f"Controller connected: {sdl_controller.name_forindex(event.device_index)}")

            elif event.type == pygame.CONTROLLERDEVICEREMOVED:
                controllers.pop(event.instance_id, None)
                print("Controller disconnected")

            elif event.type == pygame.CONTROLLERBUTTONDOWN:
                if event.button == cmap.START_BTN:
                    if main_proc is None or main_proc.poll() is not None:
                        print("Launching main.py...")
                        main_proc = subprocess.Popen(
                            [sys.executable, MAIN_SCRIPT],
                            env=get_child_env()
                        )

        # Check shutdown combo across all connected controllers
        for ctrl in controllers.values():
            if all(ctrl.get_button(btn) for btn in SHUTDOWN_BTNS):
                if shutdown_hold_start is None:
                    shutdown_hold_start = time.monotonic()
                elif time.monotonic() - shutdown_hold_start >= SHUTDOWN_HOLD_SECS:
                    print("Shutting down Pi...")
                    subprocess.run(["sudo", "shutdown", "-h", "now"])
                break
        else:
            shutdown_hold_start = None

        clock.tick(30)

if __name__ == "__main__":
    main()
