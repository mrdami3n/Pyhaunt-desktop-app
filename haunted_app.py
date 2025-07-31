import sys
import random
import threading
import time
import math
import array
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QGuiApplication, QCursor, QPalette, QColor, QFont
from PyQt6.QtCore import QTimer, Qt, QPoint, QPropertyAnimation, QEasingCurve, QObject, pyqtSignal, QThread

# Pygame is used for playing generated sounds.
# It's a common library for this purpose and works well with PyQt.
try:
    import pygame
except ImportError:
    print("Pygame not found. Please install it: pip install pygame")
    sys.exit()

# --- Sound Generation ---
# We can't use external files, so we'll generate a spooky whisper sound dynamically.
def generate_whisper_sound(duration_ms=1500, frequency=44100):
    """
    Generates a byte array representing a synthesized whisper sound.
    This creates a sound from scratch to avoid needing any external audio files.
    """
    num_samples = int(duration_ms * (frequency / 1000.0))
    samples = [random.uniform(-1.0, 1.0) for _ in range(num_samples)]
    for i in range(num_samples):
        envelope = 0.5 * (1.0 - math.cos(2 * math.pi * i / num_samples))
        envelope *= (0.6 + 0.4 * math.sin(40 * math.pi * i / frequency))
        samples[i] *= envelope
    max_amplitude = 2**15 - 1
    pcm_samples = [int(sample * max_amplitude) for sample in samples]
    sound_data = array.array('h', pcm_samples)
    return sound_data.tobytes()

class SoundPlayer:
    """
    A simple class to handle initializing pygame and playing generated sounds.
    """
    def __init__(self):
        try:
            pygame.mixer.init()
            self.whisper_sound_data = generate_whisper_sound()
            self.whisper_sound = pygame.mixer.Sound(buffer=self.whisper_sound_data)
        except pygame.error as e:
            print(f"Failed to initialize pygame mixer or create sound: {e}")
            self.whisper_sound = None

    def play_whisper(self):
        """Plays the generated whisper sound if available."""
        if self.whisper_sound:
            self.whisper_sound.play()

class GhostlyTextWindow(QLabel):
    """
    A frameless, transparent window that types out text character by character.
    This simulates a ghost typing a message onto the screen.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("color: #FF6347; font-size: 24px; font-weight: bold; font-family: 'Courier New';")
        self.full_text = ""
        self.current_text = ""
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.type_next_character)

    def start_typing(self, text):
        """Initializes and starts the typing animation."""
        self.full_text = text
        self.current_text = ""
        self.setText("")
        self.adjustSize()
        self.show()
        # This timer is safe because start_typing is now only called from the main thread
        self.typing_timer.start(random.randint(100, 300))

    def type_next_character(self):
        """Adds the next character to the label and handles animation end."""
        if len(self.current_text) < len(self.full_text):
            self.current_text += self.full_text[len(self.current_text)]
            self.setText(self.current_text)
            self.adjustSize()
        else:
            self.typing_timer.stop()
            self.fade_out()

    def fade_out(self):
        """Animates the window's opacity to 0, then hides it."""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.hide)
        self.animation.start()

# --- Threading Fix: Worker and Signals ---
class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    This is the safe way to communicate from a background thread to the main GUI thread.
    """
    trigger_event = pyqtSignal(str) # Signal to trigger an event by name
    ghostly_typing_signal = pyqtSignal(str, QPoint) # Special signal for typing with data

class HauntingWorker(QObject):
    """
    A worker that runs in a separate thread to orchestrate hauntings
    without freezing the main application.
    """
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.running = True
        self.appeased = False

    def run(self):
        """The main loop for the worker thread."""
        events = [
            "flicker", "jump_mouse", "spooky_message", "ghostly_typing", "spooky_sound"
        ]
        while self.running:
            if not self.appeased:
                event_name = random.choice(events)
                
                if event_name == "ghostly_typing":
                    # For events that need data, prepare it here and emit the specific signal
                    phrases = [
                        "GET OUT", "ALWAYS WATCHING", "HEAR THE SCRATCHING?",
                        "IT'S COLD IN HERE", "BEHIND THE DOOR"
                    ]
                    screen_size = QGuiApplication.primaryScreen().size()
                    x = random.randint(0, screen_size.width() - 300)
                    y = random.randint(0, screen_size.height() - 100)
                    self.signals.ghostly_typing_signal.emit(random.choice(phrases), QPoint(x, y))
                else:
                    # For simple events, just emit the name
                    self.signals.trigger_event.emit(event_name)

            # Wait for the next event.
            time.sleep(15) 

class HauntedApp(QMainWindow):
    """
    The main application window that orchestrates all the haunted events.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Haunting")
        self.setGeometry(100, 100, 400, 200)
        self.setPalette(self.create_dark_palette())
        self.setStyleSheet("background-color: #1E1E1E;")

        self.central_widget = QLabel("The spirits are restless...", self)
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget.setFont(QFont("Garamond", 16))
        self.central_widget.setStyleSheet("color: #AAAAAA;")
        self.setCentralWidget(self.central_widget)

        self.appease_button = QPushButton("Appease the Spirits", self)
        self.appease_button.setGeometry(125, 140, 150, 40)
        self.appease_button.setStyleSheet("""
            QPushButton { background-color: #550000; color: #FFFFFF; border: 1px solid #FF0000; border-radius: 5px; font-size: 14px; }
            QPushButton:hover { background-color: #770000; }
            QPushButton:pressed { background-color: #440000; }
        """)
        self.appease_button.clicked.connect(self.appease_spirits)

        self.sound_player = SoundPlayer()
        self.ghost_window = GhostlyTextWindow()
        self.flicker_count = 0

        # Setup the worker thread
        self.thread = QThread()
        self.worker = HauntingWorker()
        self.worker.moveToThread(self.thread)

        # Connect signals from the worker to slots in the main thread
        self.worker.signals.trigger_event.connect(self.handle_event)
        self.worker.signals.ghostly_typing_signal.connect(self.ghostly_typing)
        
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def handle_event(self, event_name):
        """Routes event names from the worker signal to the correct method."""
        if event_name == "flicker":
            self.flicker_window()
        elif event_name == "jump_mouse":
            self.jump_mouse()
        elif event_name == "spooky_message":
            self.show_spooky_message()
        elif event_name == "spooky_sound":
            self.play_spooky_sound()

    def closeEvent(self, event):
        """Ensures the background thread is stopped when the window closes."""
        self.worker.running = False
        self.thread.quit()
        self.thread.wait()
        event.accept()

    def create_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        return palette

    def appease_spirits(self):
        if not self.worker.appeased:
            self.worker.appeased = True
            self.central_widget.setText("The spirits are calm... for now.")
            QTimer.singleShot(30000, self.spirits_return)

    def spirits_return(self):
        self.worker.appeased = False
        self.central_widget.setText("The spirits are restless again!")

    # --- Event Slots (Safe to call from main thread) ---

    def flicker_window(self):
        """Causes the main window to flicker rapidly using timers."""
        print("Event: Flicker")
        self.flicker_count = 10  # Number of flickers (on/off pairs)
        self.flicker_tick()

    def flicker_tick(self):
        if self.flicker_count > 0:
            current_opacity = self.windowOpacity()
            self.setWindowOpacity(1.0 if current_opacity < 1.0 else 0.3)
            self.flicker_count -= 1
            QTimer.singleShot(50, self.flicker_tick)
        else:
            self.setWindowOpacity(1.0) # Ensure it ends visible

    def jump_mouse(self):
        print("Event: Mouse Jump")
        screen_size = QGuiApplication.primaryScreen().size()
        random_x = random.randint(0, screen_size.width())
        random_y = random.randint(0, screen_size.height())
        QCursor.setPos(QPoint(random_x, random_y))

    def show_spooky_message(self):
        print("Event: Spooky Message")
        messages = ["I'm watching you.", "You are not alone.", "Look behind you."]
        msg = QMessageBox(self) # Set parent to self
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(random.choice(messages))
        msg.setWindowTitle("...")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet("QMessageBox { background-color: #1E1E1E; color: #AAAAAA; } QPushButton { background-color: #550000; color: #FFFFFF; border: 1px solid #FF0000; min-width: 80px; padding: 5px; }")
        msg.show() # Use show() instead of exec() to not block

    def ghostly_typing(self, text, position):
        print("Event: Ghostly Typing")
        self.ghost_window.move(position)
        self.ghost_window.start_typing(text)

    def play_spooky_sound(self):
        print("Event: Spooky Sound")
        self.sound_player.play_whisper()

def main():
    app = QApplication(sys.argv)
    window = HauntedApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
