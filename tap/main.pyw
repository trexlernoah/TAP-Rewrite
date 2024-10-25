# import sys
from threading import Event

from tap.menu.main_menu import MainMenu
from tap.daq import DAQ
from tap.classes import Queue, ThreadHandler


def main():
    thread_handler = ThreadHandler(Queue(), Event(), Event())

    tk_thread = MainMenu(thread_handler)

    daq_thread = DAQ(thread_handler)
    daq_thread.start()

    # daq_thread.join()  # ?
    while tk_thread.is_alive:
        pass

    # gracefully exit
    # sys.exit(0)


if __name__ == "__main__":
    main()
