import nidaqmx
import time

class DAQ():
    def __init__(self, device_name='Dev1', pin='ao0'):
        self.device_name = device_name
        self.pin = pin
        self.analog_ouput_name = device_name + "/" + pin

        self.task = nidaqmx.Task('shock_task')
        self.task.ao_channels.add_ao_voltage_chan(self.analog_ouput_name, 0, 5)

    def shock(self, value: float, duration: int):
        if value > .75: value = .75
        self.task.start()
        self.task.write(value)
        time.sleep(duration)
        self.task.stop()

    def test(self, value: float, duration: float):
        print("Sending shock of %f" % value)
        time.sleep(duration / 1000)
        print("Stopping shock")
