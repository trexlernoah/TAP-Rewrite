import nidaqmx
import time

# Parameters:
    # value - Value of voltage to output (in milliamps - ex: value=3 would output 3 milliamps of current).
    # timer - How long the shock will persist for.
    # device_name - The name of the DAQ card. This can be chaged in the Ni MAX software. I belive the default name assigned by the software is 'Dev1'.
    # pin - The pin to output the signal from. Either pin ao0 or ao1 should work fine, if using pin ao1 be sure to set it as such in the parameters.

def analog_out(value, timer, device_name='Dev1', pin='ao0'):

    # The function assumes that the device is named 'Dev1' and that the output pin being used is 'ao0'. If they're not, then simply change the parameters to reflect this.    
    output = device_name + "/" + pin
    print(output)

    # Create a new task, called 'task', and set it equal to the output of the nidaqmx Task function\n,
    task = nidaqmx.Task()

    # Create a new channel to send a signal to the specified device via the specified pin with the minimum and maximum voltage values at 0 and 5 volts respectively.
    # More info: https://nidaqmx-python.readthedocs.io/en/latest/ao_channel_collection.html?highlight=add_ao_voltage#nidaqmx._task_modules.ao_channel_collection.AOChannelCollection.add_ao_voltage_chan
    task.ao_channels.add_ao_voltage_chan(str(output), 0, 5)

    # Start the task.
    task.start()

    # Create and send a signal of <value> volts over the newly created channel.
    # More info: https://nidaqmx-python.readthedocs.io/en/latest/task.html?highlight=write#nidaqmx.task.Task.write 
    task.write(value)

    # Wait for the specified amount of time, then reset the DAQ card to output 0 volts. This should signal to the shock box to stop the shock.
    time.sleep(timer)
    value = 0
    task.write(value)

    # Stop the task.
    task.stop()
    task.close()

    # Print a message that shows that the process has finished properly.
    print("Successfully sent signal of " + str(value) + " on channel " + str(output) + " for " + str(timer) + " seconds.")

# Test with 2 milliamp for 2 seconds
analog_out(2, 2)
