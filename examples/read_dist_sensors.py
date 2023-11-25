import qwiic
import time
import smbus

Tof_front = qwiic.QwiicVL53L1X()
Tof_back = qwiic.QwiicVL53L1X()

bus_number = 1  # 1 for Rasp Pi rev 2 and 3
bus = smbus.SMBus(bus_number)
mux_address = 0x70  # Replace with your mux's I2C address

# Function to set the channel on the mux
def set_mux_channel(channel):
    bus.write_byte(mux_address, 1 << channel)

set_mux_channel(0)
if (Tof_front.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor in front online!\n")

set_mux_channel(1)
if (Tof_back.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor in back online!\n")




while(True):
	try:
		set_mux_channel(0)
		Tof_front.start_ranging()						 # Write configuration bytes to initiate measurement
		time.sleep(.005)
		distance = Tof_front.get_distance()	 # Get the result of the measurement from the sensor
		time.sleep(.005)
		Tof_front.stop_ranging()

		distanceInches = distance / 25.4
		distanceFeet = distanceInches / 12.0

		print("Distance front(mm): %s Distance front(ft): %s" % (distance, distanceFeet))

		set_mux_channel(1)
		Tof_back.start_ranging()						 # Write configuration bytes to initiate measurement
		time.sleep(.005)
		distance = Tof_back.get_distance()	 # Get the result of the measurement from the sensor
		time.sleep(.005)
		Tof_back.stop_ranging()

		distanceInches = distance / 25.4
		distanceFeet = distanceInches / 12.0

		print("Distance front(mm): %s Distance front(ft): %s" % (distance, distanceFeet))

	except Exception as e:
		print(e)
		break
