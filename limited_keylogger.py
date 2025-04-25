from pynput import keyboard
import json
from datetime import datetime
import os
import time
import sys
import platform
import re

class LimitedKeylogger:
    def __init__(self):
        self.log_file = "limited_keylog.json"
        self.keys_pressed = []
        self.start_time = datetime.now()
        self.last_key_time = None
        self.key_press_times = {}  
        self.special_commands = {
            keyboard.Key.ctrl_l: False,
            keyboard.Key.ctrl_r: False,
            keyboard.Key.cmd: False,
            keyboard.Key.cmd_r: False,
            keyboard.Key.alt_l: False,
            keyboard.Key.alt_r: False,
            keyboard.Key.shift: False,
            keyboard.Key.shift_r: False,
        }
        self.running = True
        self.system = platform.system()

    def is_alphanumeric(self, key_char):
        if not key_char:
            return False
        return bool(re.match(r'^[a-zA-Z0-9]$', key_char))

    def on_key_press(self, key):
        if key == keyboard.Key.f12:
            print("\nFinalizando o keylogger...")
            self.running = False
            return False

        current_time = time.time()
        
        self.key_press_times[key] = current_time
        
        flight_time = None
        if self.last_key_time is not None:
            flight_time = current_time - self.last_key_time
        
        if key in self.special_commands:
            self.special_commands[key] = True
        
        command_type = None
        if (self.special_commands[keyboard.Key.ctrl_l] or self.special_commands[keyboard.Key.ctrl_r] or
            self.special_commands[keyboard.Key.cmd] or self.special_commands[keyboard.Key.cmd_r]):
            if hasattr(key, 'char') and key.char == 'v':
                command_type = "paste"
            elif hasattr(key, 'char') and key.char == 'c':
                command_type = "copy"
            elif hasattr(key, 'char') and key.char == 'x':
                command_type = "cut"
        
        if key == keyboard.Key.backspace:
            command_type = "backspace"
        elif key in [keyboard.Key.left, keyboard.Key.right, keyboard.Key.up, keyboard.Key.down]:
            command_type = "cursor_movement"

        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        key_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "application": self.get_active_window(),
            "flight_time": round(flight_time, 3) if flight_time is not None else None,
            "command_type": command_type
        }

        if not self.is_alphanumeric(key_char) or command_type is not None:
            key_data["key"] = key_char
        
        self.keys_pressed.append(key_data)
        self.last_key_time = current_time
        self.save_to_json()

    def on_key_release(self, key):
        current_time = time.time()
        
        if key in self.key_press_times:
            hold_time = current_time - self.key_press_times[key]
            
            if self.keys_pressed:
                self.keys_pressed[-1]["hold_time"] = round(hold_time, 3)
                self.save_to_json()
            
            del self.key_press_times[key]
        
        if key in self.special_commands:
            self.special_commands[key] = False

    def get_active_window(self):
        try:
            if self.system == "Darwin":
                from AppKit import NSWorkspace
                active_app = NSWorkspace.sharedWorkspace().activeApplication()
                return active_app['NSApplicationName']
            elif self.system == "Windows":
                import win32gui
                window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                return window
            elif self.system == "Linux":
                try:
                    import subprocess
                    cmd = 'xdotool getwindowfocus getwindowname'
                    window = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
                    return window
                except:
                    return "Unknown"
            else:
                return "Unknown"
        except:
            return "Unknown"

    def save_to_json(self):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.keys_pressed, f, indent=4)

    def start(self):
        print("Limited Keylogger iniciado. Pressione F12 para finalizar.")
        with keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        ) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = LimitedKeylogger()
    keylogger.start() 