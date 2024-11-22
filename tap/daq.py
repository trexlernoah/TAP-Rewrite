import time
import threading
import nidaqmx
import queue

import line_profiler

from tap.classes import ThreadHandler, ShockTask


class DAQ(threading.Thread):
    def __init__(self, thread_handler: ThreadHandler, device_name="Dev1", pin="ao0"):
        super(DAQ, self).__init__(target=self.run)
        self.thread_handler = thread_handler

        self.device_name = device_name
        self.pin = pin
        self.analog_ouput_name = device_name + "/" + pin

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

    def current_to_volts(self, mA: float) -> float:
        # TODO bad
        # mA = mA / 1000
        if mA > 5.0 or mA < 0.0:
            return 0.0
        return mA / 2

    def run(self):
        while not self.thread_handler.kill_event.is_set():
            self.watch_queue()

    @line_profiler.profile
    def watch_queue(self):
        while (
            not self.thread_handler.halt_event.is_set()
            and not self.thread_handler.kill_event.is_set()
        ):
            try:
                # See if there is an event listener
                # Getting rid of timeout and setting block=False results in too much processing in this while loop
                shock_task: ShockTask = self.thread_handler.task_queue.get(timeout=0.1)
                print(shock_task)
            except queue.Empty:
                pass
            else:
                print("Sending shock of %f" % shock_task.shock)
                volts = self.current_to_volts(shock_task.shock)
                print(f"volts: {volts} V")

                try:
                    with nidaqmx.Task() as task:
                        task.ao_channels.add_ao_voltage_chan(
                            "Dev1/ao0", min_val=0.0, max_val=2.5
                        )
                        task.start()
                        task.write(volts)
                        task.stop()

                    with nidaqmx.Task() as task:
                        task.do_channels.add_do_chan("Dev1/port0/line0:0")
                        task.start()
                        task.write(True)
                        task.stop()

                    self.thread_handler.halt_event.wait(shock_task.duration)
                    print("Stopping shock")

                    with nidaqmx.Task() as task:
                        task.do_channels.add_do_chan("Dev1/port0/line0:0")
                        task.start()
                        task.write(False)
                        task.stop()

                    with nidaqmx.Task() as task:
                        task.ao_channels.add_ao_voltage_chan(
                            "Dev1/ao0", min_val=0.0, max_val=2.5
                        )
                        task.start()
                        task.write(0.0)
                        task.stop()

                    self.thread_handler.halt_event.wait(shock_task.cooldown)
                except Exception as e:
                    print("EXCEPTION %s" % e)
                    self.thread_handler.halt_event.set()

                # self.test(task.shock, task.duration, task.cooldown)
                self.thread_handler.task_queue.task_done()
                print("task done")
        # Clean up here
        self.thread_handler.task_queue.clear()
        self.thread_handler.halt_event.clear()
