""" 
simple_goto.py: GUIDED mode "simple goto" example (Copter Only) 
 
The example demonstrates how to arm and takeoff in Copter and how to navigate to  points using Vehicle.commands.goto. 
 
Full documentation is provided at 
http://python.dronekit.io/examples/simple_goto.html 
"""  import time 
from droneapi.lib import VehicleMode, Location from pymavlink import mavutil 
 
api = local_connect() vehicle = api.get_vehicles()[0] 
 def probe_link(ip_address): 
    import errno     import subprocess     try:         if subprocess.call(["fping", ip_address]) != 0: 
            return False     except OSError, ex:         if ex.errno == errno.ENOENT:             print("install fping")     return True 
 
# base on goto example in 
# dronekit-python/docs/_build/singlehtml/index.html#example-guidedmode-setting-speed-yaw def blocking_goto(target_location): 
    """ 
    Moves the vehicle to a position dNorth metres North and dEast metres East of the current position. 
 
    The method takes a function pointer argument with a single 
`droneapi.lib.Location` parameter for  
    the target position. This allows it to be called with different position-setting commands.  
    By default it uses the standard method: 
droneapi.lib.Vehicle.commands.goto(). 
 
    The method reports the distance to target every two seconds. 
    """ 
    current_location = vehicle.location 
    target_distance = distance_to_point(current_location, target_location) 
    vehicle.commands.goto(target_location)     vehicle.flush() 
     while not api.exit and vehicle.mode.name == "GUIDED": #Stop action if we are no longer in guided mode. 
        remaining_distance = distance_to_point(vehicle.location, target_location) * 1000 
        print "Distance to target: ", remaining_distance         if remaining_distance <= 10# target_distance * 0.01  : #Just below target, in case of undershoot.             print "Reached target"             break;         time.sleep(2) 
 def in_radians(n): 
    return n * math.pi() / 180.0 
 def distance_to_point(locationA, locationB): 
    """ Returns the distance in KM between locationA and locationB.     The computation is based on the Great Circle distance     https://en.wikipedia.org/wiki/Great-circle_distance 
    """ 
    lat1 = in_radians(locationA.latitude)     lon1 = in_radians(locationA.longitude)     lat2 = in_radians(locationB.latitude)     lon2 = in_radians(locationB.longitude)     dlat = lat2 - lat1 
    # Law of Cosines for Spherical Trigonometry     dlon = lon2 - lon1 
    a = math.pow(math.sin(dlat / 2.0), 2) + (math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon / 2.0), 2))     rad = 2.0 * math.asin(math.sqrt(a))     # return EARTH_MEAN_RADIUS_KM = 6371.0088     return 6371.0088 * rad 
 def arm_and_takeoff(aTargetAltitude): 
    """ 
    Arms vehicle and fly to aTargetAltitude. 
    """  
    print "Basic pre-arm checks" 
    # Don't let the user try to fly autopilot is booting     if vehicle.mode.name == "INITIALISING": 
        print "Waiting for vehicle to initialise"         time.sleep(1)     while vehicle.gps_0.fix_type < 2: 
        print "Waiting for GPS...:", vehicle.gps_0.fix_type         time.sleep(1) 
 
    print "Arming motors" 
    # Copter should arm in GUIDED mode     vehicle.mode    = VehicleMode("GUIDED")     vehicle.armed   = True     vehicle.flush() 
     while not vehicle.armed and not api.exit: 
        print " Waiting for arming..."         time.sleep(1) 
 
    print "Taking off!" 
    vehicle.commands.takeoff(aTargetAltitude) # Take off to target altitude     vehicle.flush() 
 
    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command  
    #  after Vehicle.commands.takeoff will execute immediately).     while not api.exit: 
        print " Altitude: ", vehicle.location.alt 
        if vehicle.location.alt>=aTargetAltitude*0.95: #Just below target, in case of undershoot. 
            print "Reached target altitude"             break;         time.sleep(1) 
 
def main(altitude=20, # altitude in meters 
         max_transfer_time=30, # max_transfer_time in seconds, per image          ): 
    arm_and_takeoff(20) 
 
    print "Going to first point..." 
    point1 = Location(-35.361354, 149.165218, 20, is_relative=True)     blocking_goto(point1) 
 
    print "Going to second point..." 
    point2 = Location(-35.363244, 149.168801, 20, is_relative=True)     blocking_goto(point2) 
     has_connection = False     for _ in range(5):         if probe_link("10.100.25.1"):             has_connection = True             break; 
     if (has_connection): 
        images_transfer.start(MAX_TRANSFER_TIME) 
     print "Returning to Launch"     vehicle.mode = VehicleMode("RTL")     vehicle.flush() 
 if __name__ == "__main__": 
    import sys 
    print "Recordar!!!: los puntos aun estan fijos"     print "crear un archivo con el plan de vuelo"     print "y leer ese archivo inicialmente"     sys.exit(main()) 
