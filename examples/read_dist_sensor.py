import smbus
import qwiic_vl53l1x as qwiic_dist
import qwiic_tca9548a as qwiic_mux
import time


Mux = qwiic_mux.QwiicTCA9548A()
Tof_front = qwiic_dist.QwiicVL53L1X()
Tof_back = qwiic_dist.QwiicVL53L1X()

bus_number = 1  # 1 for Rasp Pi rev 2 and 3
bus = smbus.SMBus(bus_number)
mux_address = 0x70  # Replace with your mux's I2C address

if Mux.begin():
    print("TCA9548A initialized.")
else:
    print("TCA9548A initialization failed!")
    exit(1)
	
# Enable channel 3 and 7
Mux.enable_channels(3)
Mux.enable_channels(7)


if (Tof_front.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor in front online!\n")

if (Tof_back.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor in back online!\n")




while(True):
	try:
		Tof_front.start_ranging()						 # Write configuration bytes to initiate measurement
		time.sleep(.005)
		distance = Tof_front.get_distance()	 # Get the result of the measurement from the sensor
		time.sleep(.005)
		Tof_front.stop_ranging()

		distanceInches = distance / 25.4
		distanceFeet = distanceInches / 12.0

		print("Distance front(mm): %s Distance front(ft): %s" % (distance, distanceFeet))

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
