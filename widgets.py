"""
Shared custom widgets.
tk.Button ignores bg/fg on macOS Aqua. All styled buttons here use
Frame+Label so colors render identically on Mac and Windows.
"""
import tkinter as tk
from tkinter import ttk
import config


def _darken(hex_color, f=0.85):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "#{:02x}{:02x}{:02x}".format(
        min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f))
    )


class FlatButton(tk.Frame):
    """Flat button — full color control on Mac and Windows."""

    DIS_BG = "#DEDAD5"
    DIS_FG = config.FL_03

    def __init__(self, parent, text, bg, fg,
                 command=None, padx=20, pady=10, font=None, **kw):
        super().__init__(parent, bg=bg, **kw)
        self._bg      = bg
        self._hov_bg  = _darken(bg)
        self._fg      = fg
        self._cmd     = command
        self._active  = True

        _f = font or (config.FONT_FAMILY, 10, "bold")
        self._lbl = tk.Label(
            self, text=text, bg=bg, fg=fg,
            font=_f, padx=padx, pady=pady, cursor="hand2"
        )
        self._lbl.pack(fill=tk.BOTH, expand=True)
        self.configure(cursor="hand2")

        for w in (self, self._lbl):
            w.bind("<Button-1>", self._click)
            w.bind("<Enter>",    self._enter)
            w.bind("<Leave>",    self._leave)

    def _click(self, _=None):
        if self._active and self._cmd:
            self._cmd()

    def _enter(self, _=None):
        if self._active:
            self.configure(bg=self._hov_bg)
            self._lbl.configure(bg=self._hov_bg)

    def _leave(self, _=None):
        if self._active:
            self.configure(bg=self._bg)
            self._lbl.configure(bg=self._bg)

    def set_enabled(self, enabled):
        self._active = enabled
        if enabled:
            self.configure(bg=self._bg,      cursor="hand2")
            self._lbl.configure(bg=self._bg, fg=self._fg, cursor="hand2")
        else:
            self.configure(bg=self.DIS_BG,      cursor="")
            self._lbl.configure(bg=self.DIS_BG, fg=self.DIS_FG, cursor="")

    def set_text(self, t):
        self._lbl.configure(text=t)


class NavItem(tk.Frame):
    """Sidebar navigation row."""

    def __init__(self, parent, text, command=None, **kw):
        super().__init__(parent, bg=config.SIDEBAR_BG, height=44, **kw)
        self.pack_propagate(False)
        self._cmd = command

        self._accent = tk.Frame(self, bg=config.SIDEBAR_BG, width=3)
        self._accent.pack(side=tk.LEFT, fill=tk.Y)

        self._lbl = tk.Label(
            self, text=text,
            bg=config.SIDEBAR_BG, fg=config.SIDEBAR_TEXT,
            font=(config.FONT_FAMILY, 11),
            anchor="w", padx=14, cursor="hand2"
        )
        self._lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for w in (self, self._lbl):
            w.bind("<Button-1>", self._click)
            w.bind("<Enter>",    self._enter)
            w.bind("<Leave>",    self._leave)

    def _click(self, _=None):
        if self._cmd:
            self._cmd()

    def _enter(self, _=None):
        if not getattr(self, "_is_active", False):
            self.configure(bg="#1F221F")
            self._lbl.configure(bg="#1F221F")

    def _leave(self, _=None):
        if not getattr(self, "_is_active", False):
            self.configure(bg=config.SIDEBAR_BG)
            self._lbl.configure(bg=config.SIDEBAR_BG)

    def set_active(self, active):
        self._is_active = active
        if active:
            self.configure(bg=config.SIDEBAR_ACTIVE_BG)
            self._lbl.configure(
                bg=config.SIDEBAR_ACTIVE_BG,
                fg=config.MORNING_WHITE
            )
            self._accent.configure(bg=config.CORAL)
        else:
            self.configure(bg=config.SIDEBAR_BG)
            self._lbl.configure(
                bg=config.SIDEBAR_BG,
                fg=config.SIDEBAR_TEXT
            )
            self._accent.configure(bg=config.SIDEBAR_BG)


def card_frame(parent, padx=40, pady=(8, 8)):
    """White card with a 1-px FL-03 border. Returns the inner Frame."""
    outer = tk.Frame(
        parent, bg=config.CARD_BG,
        highlightbackground="#CCCDC9",
        highlightthickness=1
    )
    outer.pack(fill=tk.X, padx=padx, pady=pady)
    inner = tk.Frame(outer, bg=config.CARD_BG, padx=28, pady=22)
    inner.pack(fill=tk.X)
    return inner


def section_title(parent, text, bg=None):
    bg = bg or config.CARD_BG
    return tk.Label(
        parent, text=text.upper(),
        bg=bg, fg=config.FL_03,
        font=(config.FONT_FAMILY, 8, "bold")
    )


def h1(parent, text="", bg=None):
    bg = bg or config.CONTENT_BG
    return tk.Label(
        parent, text=text,
        bg=bg, fg=config.FL_01,
        font=(config.FONT_FAMILY, 20, "bold")
    )


def body_label(parent, text="", bg=None, fg=None):
    bg = bg or config.CARD_BG
    fg = fg or config.FL_02
    return tk.Label(parent, text=text, bg=bg, fg=fg,
                    font=(config.FONT_FAMILY, 10))
