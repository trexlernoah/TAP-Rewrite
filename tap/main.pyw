# import sys

from tap.menu.main_menu import MainMenu
from tap.daq import DAQ
from tap.classes import Queue


def main():
    task_queue = Queue()

    tk_thread = MainMenu(task_queue)

    daq_thread = DAQ(task_queue)
    daq_thread.start()

    # daq_thread.join()  # ?
    while tk_thread.is_alive:
        pass

    # gracefully exit
    # sys.exit(0)


if __name__ == "__main__":
    main()
