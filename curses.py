import curses
import time

def animate_curses(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    x = 0
    while x < width - 1:
        stdscr.clear()
        stdscr.addstr(0, x, "O")
        stdscr.refresh()
        time.sleep(0.1)
        x += 1

curses.wrapper(animate_curses)
