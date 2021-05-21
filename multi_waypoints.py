from dronekit import connect,VehicleMode,LocationGlobalRelative,LocationGlobal
import time
vehicle=connect("udp:127.0.0.1:14550",wait_ready=True)

def arm_and_takeoff(altitude):
    print("basic checkup")
    while not vehicle.is_armable:
        print("waiting to initialize")
        time.sleep(1)
    print("arming motors")
    vehicle.mode=VehicleMode("GUIDED")
    vehicle.armed=True


    while not vehicle.armed:
        print("waiting to be armed")
        time.sleep(1)
    print(vehicle.home_location)
    print("taking off")
    vehicle.simple_takeoff(altitude)

    while True:
        print("altitude: {val}".format(val=vehicle.location.global_relative_frame.alt))
        
        if vehicle.location.global_relative_frame.alt>=altitude*0.95:
            print("target altitude reached")
            break
        time.sleep(1)

arm_and_takeoff(50)

vehicle.gimbal.rotate(-90, 0, 0)


pt1 = LocationGlobalRelative(-35.365335,149.165172,20)
vehicle.simple_goto(pt1)
time.sleep(10)

pt2 = LocationGlobalRelative(-35.365335,149.161839,20)
vehicle.simple_goto(pt2)
time.sleep(10)

pt3 = LocationGlobalRelative(-35.361729,149.162950,20)
vehicle.simple_goto(pt3)
time.sleep(10)

pt4 = LocationGlobalRelative(-35.361729,149.168449,20)
vehicle.simple_goto(pt4)
time.sleep(10)

pt5 = LocationGlobalRelative(-35.365326,149.168449,20)
vehicle.simple_goto(pt5)
time.sleep(10)

pt6 = LocationGlobalRelative(-35.365335,149.1651729,20)
vehicle.simple_goto(pt6)
time.sleep(10)

pt7 =  vehicle.home_location
vehicle.simple_goto(pt7)
time.sleep(10)

vehicle.close()
print("Completed")
