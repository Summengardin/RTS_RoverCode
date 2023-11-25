import qwiic_vl53l1x as qwiic_dist
import qwiic_tca9548a as qwiic_mux
import time


Mux = qwiic_mux.QwiicTCA9548A()
Tof_front = qwiic_dist.QwiicVL53L1X()
Tof_back = qwiic_dist.QwiicVL53L1X()


print("Mux channels enabled:")
Mux.list_channels()

time.sleep(5)
	
# Enable channel 3 and 7
Mux.enable_channels(3)
Mux.enable_channels(7)


if (Tof_front.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor in front online!\n")

if (Tof_back.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor in back online!\n")




while(True):
	try:
		distance = Tof_front.get_distance()	 # Get the result of the measurement from the senso

		distanceInches = distance / 25.4
		distanceFeet = distanceInches / 12.0

		print("Distance front(mm): %s Distance front(ft): %s" % (distance, distanceFeet))

		distance = Tof_back.get_distance()	 # Get the result of the measurement from the sensor

		distanceInches = distance / 25.4
		distanceFeet = distanceInches / 12.0

		print("Distance front(mm): %s Distance front(ft): %s" % (distance, distanceFeet))
		time.sleep(1)

	except Exception as e:
		print(e)
		break
