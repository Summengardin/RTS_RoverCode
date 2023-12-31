import qwiic_vl53l1x as qwiic_dist
import qwiic_tca9548a as qwiic_mux
import time
import sys
mux_address = sys.argv[1] if len(sys.argv) > 1 else 112 # 0x70

Mux = qwiic_mux.QwiicTCA9548A(int(mux_address))
Tof_front = qwiic_dist.QwiicVL53L1X()
Tof_back = qwiic_dist.QwiicVL53L1X()

	
if (Mux.is_connected() == False):
    print("The Qwiic Mux device isn't connected to the system. Please check your connection")
    exit(1) 

Mux.enable_all()
time.sleep(1)
Mux.list_channels()
time.sleep(3)

if (Tof_front.sensor_init() == None):
	print("Sensor in front online!\n")

if (Tof_back.sensor_init() == None):
	print("Sensor in back online!\n")

while(True):
    try: 
        distance_front = Tof_front.get_distance()
        distance_back = Tof_back.get_distance()
        print(f"Distance front[mm]: {distance_front} Distance back[mm]: {distance_back}")
        time.sleep(0.1)

    except Exception as e:
        print(e)
        break

