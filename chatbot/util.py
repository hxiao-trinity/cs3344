

def printWithColor(text, color="", end=''):

    colors = {
        "": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m",
    }
    
    color_code = colors.get(color.lower(), color)
    print(f"{color_code}{text}\033[0m", end=end)

