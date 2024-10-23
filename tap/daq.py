import time
import threading
import nidaqmx

from tap.classes import Queue, ShockTask


class DAQ(threading.Thread):
    def __init__(self, task_queue: Queue, device_name="Dev1", pin="ao0"):
        super(DAQ, self).__init__()
        print("daq init")
        self.task_queue = task_queue

        self.device_name = device_name
        self.pin = pin
        self.analog_ouput_name = device_name + "/" + pin

        self.running = True
        self.watch_queue()

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

    def watch_queue(self):
        while self.running:
            task: ShockTask = self.task_queue.get()
            print(task)
            self.test(task.shock, task.duration, task.cooldown)
            self.task_queue.task_done()
