import random


class Color:
    ANSI = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
    }

    HEX = {
        "white": "#FFFFFF",
        "black": "#000000",
        "light_gray": "#E0E0E0",
        "gray": "#808080",
        "dark_gray": "#404040",
        "yellow": "#FFDD00",
        "light_blue": "#00AAFF",
        "teal": "#00DDDD",
        "lime": "#AAFF00",
        "orange": "#FF8800",
        "pink": "#FF88FF",
        "light_green": "#99FF99",
        "cream": "#FFFFDD",
        "lavender": "#DDBBFF",
    }

    ON_BLACK = [
        "white",
        "light_gray",
        "yellow",
        "light_blue",
        "teal",
        "lime",
        "orange",
        "pink",
        "light_green",
        "cream",
        "lavender",
    ]

    ON_WHITE = ["black", "dark_gray", "gray"]

    @staticmethod
    def shell(text, color="reset", bold=False, underline=False):
        style = ""
        if bold:
            style += Color.ANSI["bold"]
        if underline:
            style += Color.ANSI["underline"]
        color_code = Color.ANSI.get(color, Color.ANSI["reset"])
        return f"{style}{color_code}{text}{Color.ANSI['reset']}"

    @staticmethod
    def get_readable_color(background="black"):
        """Returns a color that will be readable on the specified background"""
        if background.lower() == "black":
            color_name = random.choice(Color.ON_BLACK)
        else:
            color_name = random.choice(Color.ON_WHITE)
        return Color.HEX[color_name]
