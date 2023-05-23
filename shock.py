import nidaqmx
import time

# Parameters:
    # value - Value of voltage to output (in milliamps - ex: value=3 would output 3 milliamps of current).
    # timer - How long the shock will persist for.

def analog_out(value, timer):
    # Create a new task, called 'task', and set it equal to the output of the nidaqmx Task function\n,
    task = nidaqmx.Task()

    # Create a new channel to send a signal to Device 'Dev1' via pin 'ao0', with th minimum nad maximum voltage values at 0 and 5 volts respectively.
    # More info: https://nidaqmx-python.readthedocs.io/en/latest/ao_channel_collection.html?highlight=add_ao_voltage#nidaqmx._task_modules.ao_channel_collection.AOChannelCollection.add_ao_voltage_chan
    task.ao_channels.add_ao_voltage_chan('Dev1/ao0', 0, 5)

    # Start the task.
    task.start()

    # Create and send a signal of <value> volts over the channel.
    # More info: https://nidaqmx-python.readthedocs.io/en/latest/task.html?highlight=write#nidaqmx.task.Task.write 
    task.write(value)
    time.sleep(timer)

    value = 0
    task.write(value)

    # Stop the task.
    task.stop()
    task.close()

    print("Successfully sent signal on channel ao0")

# Test with 2 milliamp for 2 seconds
analog_out(2, 2)
