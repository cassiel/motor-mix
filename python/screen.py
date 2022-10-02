"""
Screen driving via curses. Separated here so we can add a queue for thread-safety.
"""

import curses
import threading

class Screen:
    def __init__(self, stdscr):
        self.__stdscr = stdscr
        self.__mutex = threading.Lock()

    def addstr(self, y, x, s):
        with self.__mutex:
            self.__stdscr.addstr(y, x, s)

        return self

    def refresh(self):
        with self.__mutex:
            self.__stdscr.refresh()

        return self
