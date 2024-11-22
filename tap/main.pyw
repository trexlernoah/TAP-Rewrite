# import sys
from threading import Event

from tap.menu.main_menu import MainMenu
from tap.daq import DAQ
from tap.classes import Queue, ThreadHandler


def main():
    thread_handler = ThreadHandler(Queue(), Event(), Event())

    tk_thread = MainMenu(thread_handler)

    daq_thread = DAQ(thread_handler)
    daq_thread.join()

    tk_thread.join()


if __name__ == "__main__":
    main()
