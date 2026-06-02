import sys
import platform
import tkinter as tk

import matplotlib.pyplot as plt

import config
from excel_backend import ExcelBackend
from app import App


def main():
    # Windows DPI awareness — must run before tk.Tk()
    if platform.system() == "Windows":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()
    root.title("TimeCard")
    root.geometry("1200x760")
    root.minsize(1000, 640)

    if platform.system() == "Windows":
        root.state("zoomed")
    elif platform.system() == "Darwin":
        root.geometry("1300x820")

    def _on_close():
        plt.close("all")   # release matplotlib figures so no threads linger
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", _on_close)

    backend = ExcelBackend(config.EXCEL_PATH)
    App(root, backend)
    root.mainloop()


if __name__ == "__main__":
    main()
