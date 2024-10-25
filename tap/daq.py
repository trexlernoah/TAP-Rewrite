import time
import threading
import nidaqmx

from tap.classes import ThreadHandler, ShockTask


class DAQ(threading.Thread):
    def __init__(self, thread_handler: ThreadHandler, device_name="Dev1", pin="ao0"):
        super(DAQ, self).__init__(target=self.run)
        self.thread_handler = thread_handler

        self.device_name = device_name
        self.pin = pin
        self.analog_ouput_name = device_name + "/" + pin

        self.running = True
        self.start()

        # self.task = nidaqmx.Task("shock_task")
        # self.task.ao_channels.add_ao_voltage_chan(self.analog_ouput_name, 0, 5)

    # TODO convert to decimal
    def shock(self, value: float, duration: int):
        if value > 0.75:
            value = 0.75
        # if value < 0
        self.task.start()
        self.task.write(value)
        time.sleep(duration)
        self.task.stop()

    def test(self, value: float, duration: int, cooldown: int):
        print("Sending shock of %f" % value)
        time.sleep(duration)
        print("Stopping shock")
        time.sleep(cooldown)

    def run(self):
        while not self.thread_handler.kill_event.is_set():
            self.watch_queue()

    def watch_queue(self):
        while (
            not self.thread_handler.halt_event.is_set()
            and not self.thread_handler.kill_event.is_set()
        ):
            # see if this behavior exists with queue.get()
            if self.thread_handler.task_queue.empty():
                continue

            task: ShockTask = self.thread_handler.task_queue.get()
            print(task)

            print("Sending shock of %f" % task.shock)
            print(self.thread_handler.halt_event.is_set())
            self.thread_handler.halt_event.wait(task.duration)
            print("Stopping shock")
            self.thread_handler.halt_event.wait(task.cooldown)

            # self.test(task.shock, task.duration, task.cooldown)
            self.thread_handler.task_queue.task_done()
        # Clean up here
        self.thread_handler.task_queue.clear()
        self.thread_handler.halt_event.clear()
