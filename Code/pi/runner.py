# This script auto runs on the raspberry pi and is responsible for remotely starting/stopping main.py and shutting down the pi

import os
import subprocess
import sys
import time

import pygame

import config

SHUTDOWN_HOLD_SECS = 3
SHUTDOWN_BTNS = {config.A_BTN, config.B_BTN, config.X_BTN, config.Y_BTN}
MAIN_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

def get_child_env():
    env = os.environ.copy()
    env.pop("SDL_VIDEODRIVER", None)
    env.pop("SDL_AUDIODRIVER", None)
    return env

def main():
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.display.init()
    pygame.joystick.init()

    joysticks = {}
    main_proc = None
    shutdown_hold_start = None
    clock = pygame.time.Clock()

    print("Runner started, waiting for controller...")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Controller connected: {joy.get_name()}")

            elif event.type == pygame.JOYDEVICEREMOVED:
                joysticks.pop(event.instance_id, None)
                print("Controller disconnected")

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == config.START_BTN:
                    if main_proc is None or main_proc.poll() is not None:
                        print("Launching main.py...")
                        main_proc = subprocess.Popen(
                            [sys.executable, MAIN_SCRIPT],
                            env=get_child_env()
                        )

        # Check shutdown combo across all connected joysticks
        for joy in joysticks.values():
            if all(joy.get_button(btn) for btn in SHUTDOWN_BTNS):
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
