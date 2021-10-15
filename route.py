#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
# Sri Venkata Sai Anoop Bulusu 2000761292
# Shriya Reddy Pulagam         2000770412
# Srinivas Yashvanth Valavala  2000756858
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
from os import pipe
import math
from math import atan2, cos, sin, sqrt, pi, tanh
import sys
import heapq

# We are pulling the data from the dataset city-gps.txt and appending the data into lists.


def get_data_gps(filename):
    list_city = []
    list_latitude = []
    list_longitude = []
    dict_city=dict()
    with open(filename, 'r') as file:
        for attribute in file:
            list_attribute = attribute.split(' ')
            list_city.append(list_attribute[0])
            list_latitude.append(float(list_attribute[1]))
            list_longitude.append(float(list_attribute[2]))
            dict_city[list_attribute[0]] = (list_attribute[1],list_attribute[2][:-2])
    return list_city,list_latitude,list_longitude,dict_city


# We are pulling the data from the dataset road-segments.txt and appending the data into lists.

def get_data_segments(filename):
    list_city1 = []
    list_city2 = []
    miles = []
    speed = []
    highway = []
    dict_miles=dict()
    dict_speed=dict()
    dict_highway=dict()
    with open(filename, 'r') as file:
        for attribute in file:
            list_attribute = attribute.split(' ')
            list_city1.append(list_attribute[0])
            list_city2.append(list_attribute[1])
            dict_miles[(list_attribute[0],list_attribute[1])] = int(list_attribute[2])
            dict_miles[(list_attribute[1],list_attribute[0])] = int(list_attribute[2])
            miles.append(int(list_attribute[2]))
            dict_speed[(list_attribute[0],list_attribute[1])] = int(list_attribute[3])
            dict_speed[(list_attribute[1],list_attribute[0])] = int(list_attribute[3])
            speed.append(int(list_attribute[3]))
            dict_highway[(list_attribute[0],list_attribute[1])] = list_attribute[4]
            dict_highway[(list_attribute[1],list_attribute[0])] = list_attribute[4]
            highway.append((list_attribute[4]))
    return list_city1,list_city2,miles,speed,highway,dict_miles,dict_speed,dict_highway

# We are finding the missing coordinates of the junctions and nodes with the help of the node's nearest successor and it's coordinates.

def missing_coordinates_coordinate_heuristic(city,dict_city,list_city1,list_city2,dict_miles):
    succ_city_distance = []
    index_1 = [i for i, x in enumerate(list_city1) if x == city]
    index_2 = [i for i, x in enumerate(list_city2) if x == city]
    for x in range(len(index_1)):
        city1_next = list_city2[index_1[x]]
        heapq.heappush(succ_city_distance,(dict_miles[(city,city1_next)],city1_next))
    for x in range(len(index_2)):
        city2_next = list_city1[index_2[x]]
        heapq.heappush(succ_city_distance,(dict_miles[(city,city2_next)],city1_next))
    while succ_city_distance:
        minimum_cost, minimum_cost_city = heapq.heappop(succ_city_distance)
        if minimum_cost_city not in dict_city.keys():
            minimum_cost, minimum_cost_city = heapq.heappop(succ_city_distance)
        else:
            minimum_cost = dict_miles[(city,minimum_cost_city)]
            missing_city_coordinates_difference = (minimum_cost/69, minimum_cost/54.6)
            missing_coord_lat = float(dict_city[minimum_cost_city][0]) - missing_city_coordinates_difference[0]
            missing_coord_lon = float(dict_city[minimum_cost_city][1]) - missing_city_coordinates_difference[1]
            return missing_coord_lat,missing_coord_lon

def get_dist_between_points(start,end,dict_city,list_city1,list_city2,dict_miles):
    if start not in dict_city.keys() :
        return 0
    elif end not in dict_city.keys():
        lat2,lon2 = missing_coordinates_coordinate_heuristic(end,dict_city,list_city1,list_city2,dict_miles)
    else:
        lat2,lon2 = dict_city[end]
    lat1,lon1 = dict_city[start]
    p=pi/180
    lat1_rad=float(lat1)*float(p)
    lon1_rad=float(lon1)*float(p)
    lat2_rad=float(lat2)*float(p)
    lon2_rad=float(lon2)*float(p)
    x=sin((lat2_rad-lat1_rad)/2)*sin((lat2_rad-lat1_rad)/2)+cos(lat1_rad)*cos(lat2_rad)*(sin((lon2_rad-lon1_rad)/2)*sin((lon2_rad-lon1_rad)/2))
    y=2*atan2(sqrt(x),sqrt(1-x))
    z=3959.999*y
    return 0.5*z

#  WE are finding out the havesine distance between start and end cities.

def distance(start,end,dict_city,list_city1,list_city2,dict_miles):
    H_DISTANCE = get_dist_between_points(start,end,dict_city,list_city1,list_city2,dict_miles)
    return H_DISTANCE

# We are finding the heuristic for time using the haversine distance and maximum speed limit.

def time(start,end,speed,dict_city,list_city1,list_city2,dict_miles):
    MAX_SPEED=max(speed)
    H_TIME=distance(start,end,dict_city,list_city1,list_city2,dict_miles)/MAX_SPEED
    return H_TIME
    
    
# We are finding the heuristic for segment using the haversine distance and max segment size.

def segment(start,end,dict_city,miles,list_city1,list_city2,dict_miles):
    MAX_SEGMENT=max(miles)
    H_SEGMENTS=(distance(start,end,dict_city,list_city1,list_city2,dict_miles)/MAX_SEGMENT)
    return H_SEGMENTS

# We are finding the heuristic for delivery time using the haversine distance and max speed.

def delivery(start,end,dict_city,speed,list_city1,list_city2,dict_miles):
    delivery_h = time(start,end,speed,dict_city,list_city1,list_city2,dict_miles)
    return delivery_h



def is_goal(city,end):
    if city == end:
        return True

# We are finding the successors of a city for distance using the dataset road-segmemnts.txt.

def successors_for_distance(city,end,path,g_dist,dict_city,list_city1,list_city2,dict_miles):
    succ_city = []
    index_1 = [i for i, x in enumerate(list_city1) if x == city]
    index_2 = [i for i, x in enumerate(list_city2) if x == city]
    for x in range(len(index_1)):
        city1 = list_city2[index_1[x]]
        paths = path+[list_city2[index_1[x]]]
        gdist = g_dist+dict_miles[city,list_city2[index_1[x]]]
        hdist = distance(list_city2[index_1[x]],end,dict_city,list_city1,list_city2,dict_miles)
        succ_city.append([city1, paths, gdist, hdist])
    for x in range(len(index_2)):
        city2 = list_city1[index_2[x]]
        paths = path + [list_city1[index_2[x]]]
        gdist1 = g_dist+dict_miles[city,list_city1[index_2[x]]]
        hdist1 = distance(list_city1[index_2[x]],end,dict_city,list_city1,list_city2,dict_miles)                           
        succ_city.append([city2, paths, gdist1, hdist1])
    return succ_city

# We are finding the successors of a city for time  using the dataset road-segmemnts.txt.

def successors_for_time(city,end,path,g_time,speed,list_city1,list_city2,dict_miles,dict_speed,dict_city):
    succ_city = []
    index_1 = [i for i, x in enumerate(list_city1) if x == city]
    index_2 = [i for i, x in enumerate(list_city2) if x == city]
    for x in range(len(index_1)):
        city1 = list_city2[index_1[x]]
        paths = path+[list_city2[index_1[x]]]
        gtime = g_time+(dict_miles[city,list_city2[index_1[x]]]/dict_speed[city, list_city2[index_1[x]]])
        htime = time(list_city2[index_1[x]],end,speed,dict_city,list_city1,list_city2,dict_miles)
        succ_city.append([city1, paths, gtime, htime])
    for x in range(len(index_2)):
        city2 = list_city1[index_2[x]]
        paths = path + [list_city1[index_2[x]]]
        gtime1 = g_time+(dict_miles[city,list_city1[index_2[x]]]/dict_speed[city, list_city1[index_2[x]]])
        htime1 = time(list_city1[index_2[x]],end,speed,dict_city,list_city1,list_city2,dict_miles)                           
        succ_city.append([city2, paths, gtime1, htime1])
    return succ_city

# We are finding the successors of a city for segments using the dataset road-segmemnts.txt.
def successors_for_segment(city,end,path,g_segment,miles,dict_city,list_city1,list_city2,dict_miles):
    succ_city = []
    index_1 = [i for i, x in enumerate(list_city1) if x == city]
    index_2 = [i for i, x in enumerate(list_city2) if x == city]
    gseg = 0
    for x in range(len(index_1)):
        city1 = list_city2[index_1[x]]
        paths = path+[list_city2[index_1[x]]]
        gseg = g_segment+1
        hseg = segment(list_city2[index_1[x]],end,dict_city,miles,list_city1,list_city2,dict_miles)
        succ_city.append([city1, paths, gseg, hseg])
    gseg = 0
    gseg1 = 0
    for x in range(len(index_2)):
        city2 = list_city1[index_2[x]]
        paths = path + [list_city1[index_2[x]]]
        gseg1 = g_segment+1
        hseg1 = segment(list_city1[index_2[x]],end,dict_city,miles,list_city1,list_city2,dict_miles)                           
        succ_city.append([city2, paths, gseg1, hseg1])
    gseg1 = 0
    return succ_city

# We are finding the successors of a city for delivery time using the dataset road-segmemnts.txt.
def successors_for_delivery(city,end,path,g_delivery,list_city1,list_city2,dict_miles,dict_speed,speed,dict_city):
    succ_city = []
    index_1 = [i for i, x in enumerate(list_city1) if x == city]
    index_2 = [i for i, x in enumerate(list_city2) if x == city]
    gdel = 0
    for x in range(len(index_1)):
        city1 = list_city2[index_1[x]]
        paths = path+[list_city2[index_1[x]]]
        if dict_speed[(city,city1)] <= 50:
            gdel = g_delivery + (dict_miles[(city,city1)]/dict_speed[(city,city1)])
        else:
            gdel = g_delivery + (dict_miles[(city,city1)]/dict_speed[(city,city1)] + (math.tanh(dict_miles[(city,city1)]/1000)*2*((dict_miles[(city,city1)]/dict_speed[(city,city1)])+g_delivery)))
        hdel = delivery(list_city2[index_1[x]],end,dict_city,speed,list_city1,list_city2,dict_miles)
        succ_city.append([city1, paths, gdel, hdel])
    gdel = 0
    gdel1 = 0
    for x in range(len(index_2)):
        city2 = list_city1[index_2[x]]
        paths = path + [list_city1[index_2[x]]]
        if dict_speed[(city,city2)] <= 50:
            gdel1 = g_delivery + (dict_miles[(city,city2)]/dict_speed[(city,city2)])
        else:
            gdel1 = g_delivery + (dict_miles[(city,city2)]/dict_speed[(city,city2)] + (math.tanh(dict_miles[(city,city2)]/1000)*2*((dict_miles[(city,city2)]/dict_speed[(city,city2)])+g_delivery)))
        hdel1 = delivery(list_city1[index_2[x]],end,dict_city,speed,list_city1,list_city2,dict_miles)                           
        succ_city.append([city2, paths, gdel1, hdel1])
    gdel1 = 0
    return succ_city

def get_route(start, end, cost):
   
    list_city,list_latitude,list_longitude,dict_city = get_data_gps('city-gps.txt')
    list_city1,list_city2,miles,speed,highway,dict_miles,dict_speed,dict_highway = get_data_segments('road-segments.txt')
    fringe=[]
    cost_function = cost
    closed_list = []
    g_distance = 0
    cost = 0
    path_taken = [start]
    heapq.heappush(fringe,(cost,start,path_taken,g_distance))
    if cost_function == 'distance': 
        route_taken = []
        while fringe:
            cost, curr_city, path,g_distance = heapq.heappop(fringe)
            closed_list.append(curr_city)
            if is_goal(curr_city,end):
                total_time = 0
                total_delivery = 0
                for i in range(0,len(path)-1):
                    first_city = path[i]
                    second_city = path[i+1]
                    total_time = total_time + (dict_miles[first_city,second_city]/dict_speed[first_city,second_city])
                    if dict_speed[(first_city,second_city)] <= 50:
                        total_delivery = total_delivery + (dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)])
                    else:
                        total_delivery = total_delivery + (dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)] + (math.tanh(dict_miles[(first_city,second_city)]/1000)*2*((dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)])+total_delivery)))
                    
                    route_taken.append((path[i+1],str(dict_highway[(path[i],path[i+1])]) + " for " + str(dict_miles[(path[i],path[i+1])]) + "miles"))
                return{"total-segments" : len(path)-1, 
                    "total-miles" : float(g_distance), 
                    "total-hours" : total_time, 
                    "total-delivery-hours" : total_delivery,
                    "route-taken" : route_taken}
            else:
                for i_city,path,g_distance,h_distance in successors_for_distance(curr_city,end,path,g_distance,dict_city,list_city1,list_city2,dict_miles):                 
                    if i_city in closed_list:
                        continue
                    else:
                        cost = g_distance+h_distance
                        heapq.heappush(fringe,(cost,i_city,path,g_distance))
                                
                        
    if cost_function == 'time':
        route_taken = []
        while fringe:
            cost, curr_city, path,g_time = heapq.heappop(fringe)
            closed_list.append(curr_city)
            if is_goal(curr_city,end):
                total_miles = 0
                total_delivery = 0
                for i in range(0,len(path)-1):
                    first_city = path[i]
                    second_city = path[i+1]
                    total_miles = total_miles + dict_miles[(first_city,second_city)]
                    if dict_speed[(first_city,second_city)] <= 50:
                        total_delivery = total_delivery + (dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)])
                    else:
                        total_delivery = total_delivery + (dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)] + (math.tanh(dict_miles[(first_city,second_city)]/1000)*2*((dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)])+total_delivery)))
                    route_taken.append((path[i+1],str(dict_highway[(path[i],path[i+1])]) + " for " + str(dict_miles[(path[i],path[i+1])]) + "miles"))
                return{"total-segments" : len(path)-1, 
                    "total-miles" : float(total_miles), 
                    "total-hours" : g_time, 
                    "total-delivery-hours" : total_delivery,
                    "route-taken" : route_taken}
            else:
                for i_city,path,g_time,h_time in successors_for_time(curr_city,end,path,g_time,speed,list_city1,list_city2,dict_miles,dict_speed,dict_city):                  
                    if i_city in closed_list:
                        continue
                    else:
                        cost = g_time+h_time
                        heapq.heappush(fringe,(cost,i_city,path,g_time))
    elif cost_function == 'segments':
        route_taken = []
        while fringe:
            cost, curr_city, path,g_segment = heapq.heappop(fringe)
            closed_list.append(curr_city)
            if is_goal(curr_city,end):
                total_time = 0
                total_miles = 0
                total_delivery = 0
                for i in range(0,len(path)-1):
                    first_city = path[i]
                    second_city = path[i+1]
                    total_time = total_time + (dict_miles[first_city,second_city]/dict_speed[first_city,second_city])
                    total_miles = total_miles + dict_miles[first_city,second_city]
                    if dict_speed[(first_city,second_city)] <= 50:
                        total_delivery = total_delivery + (dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)])
                    else:
                        total_delivery = total_delivery + (dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)] + (math.tanh(dict_miles[(first_city,second_city)]/1000)*2*((dict_miles[(first_city,second_city)]/dict_speed[(first_city,second_city)])+total_delivery)))
                    route_taken.append((path[i+1],str(dict_highway[(path[i],path[i+1])]) + " for " + str(dict_miles[(path[i],path[i+1])]) + "miles"))
                return{"total-segments" : g_segment, 
                    "total-miles" : float(total_miles), 
                    "total-hours" : total_time, 
                    "total-delivery-hours" : total_delivery, 
                    "route-taken" : route_taken}
            else:
                for i_city,path,g_segment,h_segment in successors_for_segment(curr_city,end,path,g_segment,miles,dict_city,list_city1,list_city2,dict_miles):                  
                    if i_city in closed_list:
                        continue
                    else:
                        cost = g_segment+h_segment
                        heapq.heappush(fringe,(cost,i_city,path,g_segment))

    elif cost_function == 'delivery':
        route_taken = []
        while fringe:
            cost, curr_city, path,g_delivery = heapq.heappop(fringe)
            closed_list.append(curr_city)
            if is_goal(curr_city,end):
                total_time = 0
                total_miles = 0
                for i in range(0,len(path)-1):
                    first_city = path[i]
                    second_city = path[i+1]
                    total_time = total_time + (dict_miles[first_city,second_city]/dict_speed[first_city,second_city])
                    total_miles = total_miles + dict_miles[first_city,second_city]    
                    route_taken.append((path[i+1],str(dict_highway[(path[i],path[i+1])]) + " for " + str(dict_miles[(path[i],path[i+1])]) + "miles"))
                return{"total-segments" : len(path)-1, 
                    "total-miles" : float(total_miles), 
                    "total-hours" : total_time,
                    "total-delivery-hours" : g_delivery,  
                    "route-taken" : route_taken}
            else:
                for i_city,path,g_delivery,h_delivery in successors_for_delivery(curr_city,end,path,g_delivery,list_city1,list_city2,dict_miles,dict_speed,speed,dict_city):                  
                    if i_city in closed_list:
                        continue
                    else:
                        cost = g_delivery+h_delivery
                        heapq.heappush(fringe,(cost,i_city,path,g_delivery))





    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    # return {"total-segments" : len(route_taken), 
    #         "total-miles" : 51., 
    #         "total-hours" : 1.07949, 
    #         "total-delivery-hours" : 1.1364, 
    #         "route-taken" : route_taken}


# Please don't modify anything below this 

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
