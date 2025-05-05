import tkinter as tk
import random
import threading
import time
import math
from color_utils import Color


class LyricsWindow:
    def __init__(self, spotify_handler, lyrics_parser):
        """
        Initialize the floating lyrics window

        Args:
            spotify_handler: Instance of SpotifyHandler
            lyrics_parser: Function to get and parse lyrics
        """
        self.spotify_handler = spotify_handler
        self.lyrics_parser = lyrics_parser

        # Initialize window
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85)
        self.root.configure(bg="black")

        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(
            f"600x60+{self.screen_width - 1300}+{self.screen_height - 100}"
        )

        # Create label for lyrics
        self.label = tk.Label(
            self.root,
            text="Loading...",
            font=("Impact", 18),
            fg="white",
            bg="black",
            wraplength=1000,
        )
        self.label.pack(pady=10)
        self.root.wm_attributes("-transparentcolor", "black")

        # Animation state variables
        self.lyrics_lines = []
        self.last_position = 0
        self.shaking = False
        self.original_x = 0
        self.original_y = 0
        self.shake_type = "random"
        self.shake_intensity = 0
        self.shake_count = 0
        self.current_corner = "bottom_center"
        self.current_typing_animation = None
        self.typing_text = ""
        self.full_text = ""
        self.char_index = 0
        self.typing_speed = 0
        self.typing_timer = None

        # Corner positions mapping
        self.CORNERS = {
            "top_left": lambda w, h: (20, 20),
            "top_right": lambda w, h: (self.screen_width - w - 20, 40),
            "bottom_left": lambda w, h: (20, self.screen_height - h - 60),
            "bottom_right": lambda w, h: (
                self.screen_width - w - 25,
                self.screen_height - h - 60,
            ),
            "top_center": lambda w, h: ((self.screen_width - w) // 2, 20),
            "bottom_center": lambda w, h: (
                (self.screen_width - w) // 2,
                self.screen_height - h - 60,
            ),
            "center_left": lambda w, h: (20, (self.screen_height - h) // 2),
            "center_right": lambda w, h: (
                self.screen_width - w - 20,
                (self.screen_height - h) // 2,
            ),
            "center": lambda w, h: (
                (self.screen_width - w) // 2,
                (self.screen_height - h) // 2,
            ),
        }

        # Set up escape key binding
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Current song tracking
        self.current_song = None
        self.current_artist = None

    def start(self):
        """Start the threads and mainloop"""
        # Start background threads
        threading.Thread(target=self.update_label, daemon=True).start()
        threading.Thread(target=self.update_song, daemon=True).start()

        # Start main loop
        self.root.mainloop()

    def shake_window(self):
        """Create shake animation effect on the window"""
        if not self.shaking:
            return

        geometry = self.root.geometry()
        width_height, x_y = geometry.split("+", 1)
        x, y = map(int, x_y.split("+"))

        new_x, new_y = self.original_x, self.original_y

        # Different shake patterns
        if self.shake_type == "random":
            # Random movement in any direction
            new_x = self.original_x + random.randint(
                -self.shake_intensity, self.shake_intensity
            )
            new_y = self.original_y + random.randint(
                -self.shake_intensity, self.shake_intensity
            )

        elif self.shake_type == "horizontal":
            # Only shake horizontally
            new_x = self.original_x + random.randint(
                -self.shake_intensity, self.shake_intensity
            )

        elif self.shake_type == "vertical":
            # Only shake vertically
            new_y = self.original_y + random.randint(
                -self.shake_intensity, self.shake_intensity
            )

        elif self.shake_type == "pulse":
            # Pulse effect - expand and contract
            modifier = 1 if self.shake_count % 2 == 0 else -1
            new_x = self.original_x - modifier * self.shake_intensity // 2
            new_y = self.original_y - modifier * self.shake_intensity // 2
            width, height = map(int, width_height.split("x"))
            width_height = f"{width + modifier * self.shake_intensity}x{height + modifier * self.shake_intensity}"

        elif self.shake_type == "circular":
            angle = self.shake_count * 0.5
            new_x = self.original_x + int(self.shake_intensity * 0.8 * math.cos(angle))
            new_y = self.original_y + int(self.shake_intensity * 0.8 * math.sin(angle))

        elif self.shake_type == "wave":
            new_x = self.original_x + int(
                self.shake_intensity * math.sin(self.shake_count * 0.5)
            )

        elif self.shake_type == "bounce":
            bounce_height = self.shake_intensity * (1 - (self.shake_count / 10) ** 2)
            new_y = self.original_y - int(max(0, bounce_height))

        self.root.geometry(f"{width_height}+{new_x}+{new_y}")

        self.shake_count += 1

        if self.shaking:
            self.root.after(30, self.shake_window)
        else:
            self.root.geometry(f"{width_height}+{self.original_x}+{self.original_y}")

    def start_shake(self):
        """Initialize and start the shake animation"""
        geometry = self.root.geometry()
        width_height, x_y = geometry.split("+", 1)
        self.original_x, self.original_y = map(int, x_y.split("+"))

        self.shake_type = random.choice(
            ["random", "horizontal", "vertical", "pulse", "circular", "wave", "bounce"]
        )

        base_intensity = random.randint(3, 7)
        if self.shake_type in ["pulse", "bounce"]:
            self.shake_intensity = base_intensity * 2
        else:
            self.shake_intensity = base_intensity

        self.shake_count = 0
        self.shaking = True
        self.shake_window()

        self.root.after(random.randint(200, 400), self.stop_shake)

    def stop_shake(self):
        """Stop the shake animation"""
        self.shaking = False

    def change_corner(self):
        """Change the window position to a different corner"""
        available_corners = list(self.CORNERS.keys())
        available_corners.remove(self.current_corner)
        self.current_corner = random.choice(available_corners)

        return self.current_corner

    def type_next_char(self):
        """Animate typing effect one character at a time"""
        if self.char_index < len(self.full_text):
            self.typing_text = self.full_text[: self.char_index + 1]
            self.label.config(text=self.typing_text)

            self.label.update_idletasks()
            width = max(self.label.winfo_reqwidth() + 40, 400)
            height = self.label.winfo_reqheight() + 20
            x, y = self.CORNERS[self.current_corner](width, height)
            self.root.geometry(f"{width}x{height}+{x}+{y}")

            self.char_index += 1

            self.typing_timer = self.root.after(self.typing_speed, self.type_next_char)
        else:
            self.typing_timer = None

    def update_label(self):
        """Update the lyrics display based on current playback position"""
        current_line = ""
        while True:
            t = time.time()
            try:
                position_sec = self.spotify_handler.get_current_position() / 1000.0
            except Exception:
                time.sleep(0.05)
                continue
            time_delta = time.time() - t
            position_sec += time_delta
            line_changed = False
            current_line_index = -1

            for i, line in enumerate(self.lyrics_lines):
                start_time = line["start"]
                next_start = (
                    self.lyrics_lines[i + 1]["start"]
                    if i + 1 < len(self.lyrics_lines)
                    else float("inf")
                )

                if start_time <= position_sec < next_start:
                    lyrics_line = line["text"]
                    if i + 1 < len(self.lyrics_lines):
                        lyrics_line += "\n" + self.lyrics_lines[i + 1]["text"]
                    if current_line != lyrics_line:
                        line_changed = True
                        current_line = lyrics_line
                        current_line_index = i
                    break

            if current_line and line_changed and current_line_index >= 0:
                duration = None
                if current_line_index + 1 < len(self.lyrics_lines):
                    duration = (
                        self.lyrics_lines[current_line_index + 1]["start"]
                        - self.lyrics_lines[current_line_index]["start"]
                    )

                self.root.after(
                    0, lambda text=current_line, dur=duration: self.update_ui(text, dur)
                )

            time.sleep(0.05)

    def update_ui(self, text, duration=None):
        """Update the UI with new text and animations"""
        if self.typing_timer:
            self.root.after_cancel(self.typing_timer)
            self.typing_timer = None

        readable_color = Color.get_readable_color("black")
        self.label.config(foreground=readable_color)

        self.full_text = text
        self.typing_text = ""
        self.char_index = 0

        if duration and duration > 0:
            chars_to_type = len(text)
            if chars_to_type > 0:
                self.typing_speed = int((duration * 0.8 * 1000) / chars_to_type)
                self.typing_speed = int(max(10, min(200, self.typing_speed)) // 1.5)
            else:
                self.typing_speed = 50
        else:
            self.typing_speed = 50

        self.type_next_char()

        if random.random() < 0.2:
            self.change_corner()

        self.start_shake()

    def update_song(self):
        """Monitor for song changes and update lyrics"""
        while True:
            try:
                song, artist = self.spotify_handler.get_current_song()
            except Exception:
                time.sleep(2)
                continue
            if (
                song != self.current_song or artist != self.current_artist
            ) and song is not None:
                print(
                    Color.shell(f"Song: {song}", color="blue", bold=True),
                    Color.shell(f"by {artist}", color="green"),
                )

                self.current_song, self.current_artist = song, artist
                self.lyrics_lines = self.lyrics_parser(song, artist)

            time.sleep(2)
