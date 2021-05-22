import pygame
from dronekit import connect,LocationGlobalRelative,VehicleMode,LocationGlobal,Command
import  time 
from pymavlink import mavutil
pygame.init()
win=pygame.display.set_mode((500,500))
pygame.display.set_caption("first game")


print('Connecting to vehicle on: "udp:127.0.0.1:14550" ')
vehicle = connect("udp:127.0.0.1:14550", wait_ready=True)
print("connected successfully")
gnd_speed=40


 
def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
    
def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
        # Set up velocity mappings
        # velocity_x > 0 => fly North
        # velocity_x < 0 => fly South
        # velocity_y > 0 => fly East
        # velocity_y < 0 => fly West
        # velocity_z < 0 => ascend
        # velocity_z > 0 => descend

    # send command to vehicle 
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


    
print("control the vehicle with keyboard keys")
## keyboard inputs
def keyboard():
    while True:  
        event = pygame.event.wait()  
        if event.type == pygame.QUIT:  
            break  
   #WHEN THE KEY IS PRESSED
        if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  #UP ARROW=FORWARD
                    print("moving forward") 
                    send_ned_velocity(gnd_speed,0,0,4)  
                elif event.key == pygame.K_DOWN:         #DOWN ARROW=BACKWARD
                    print("moving backward")
                    send_ned_velocity(-gnd_speed,0,0,4)  
                elif event.key == pygame.K_LEFT:          #LEFT ARROW=LEFT
                    print("moving left")
                    send_ned_velocity(0,-gnd_speed,0,4)  #RIGHT ARROW=RIGHTR
                elif event.key == pygame.K_RIGHT:
                    print("moving right ")
                    send_ned_velocity(0,gnd_speed,0,4)  #
                elif event.key == pygame.K_SPACE:             #SPACE BAR= UP
                    print("moving up ")
                    send_ned_velocity(0,0,-gnd_speed,4)
                elif event.key == pygame.K_s:                  #S BUTTON= DOWN
                    print("moving dowm")
                    send_ned_velocity(0,0,gnd_speed,4)
                

    ###WHEN THE KEY IS RELEASED
        if  event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    print("STOP moving forward") 
                    send_ned_velocity(0,0,0,1)
                elif event.key == pygame.K_DOWN:
                    print(" STOP moving backward")
                    send_ned_velocity(0,0,0,1)
                elif event.key == pygame.K_LEFT:
                    print(" STOP moving left")
                    send_ned_velocity(0,0,0,1)
                elif event.key == pygame.K_RIGHT:
                    print(" STOP moving right ")
                    send_ned_velocity(0,0,0,1)
                elif event.key == pygame.K_SPACE:
                    print(" STOP moving up ")
                    send_ned_velocity(0,0,0,1)
                elif event.key == pygame.K_s:
                    print(" STOP moving dowm")
                    send_ned_velocity(0,0,0,1)
                
                

           

        

    # main function
arm_and_takeoff(50) 
keyboard()
