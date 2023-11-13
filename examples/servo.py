import time
import pi_servo_hat

TILT_SERVO = 0
PAN_SERVO = 1

# Create an instance of the Servo Phat
servos = pi_servo_hat.PiServoHat()

servos.restart()

try:
    
    servos.move_servo_position(TILT_SERVO, 40)
    servos.move_servo_position(PAN_SERVO, 20)
    print("TILT position: 40")
    print("PAN position: 20")


    # Wait for 1 second
    time.sleep(1)

    servos.move_servo_position(TILT_SERVO, 60)
    servos.move_servo_position(PAN_SERVO, 90)
    print("TILT position: 60")
    print("PAN position: 90")

    # Wait for 1 second
    time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")