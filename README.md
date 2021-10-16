# Find_roads_through_maps
The goal is to find routes through maps based on four cost functions. 

– segments tries to find a route with the fewest number of road segments (i.e. edges of the graph).
– distance tries to find a route with the shortest total distance.
– time finds the fastest route, assuming one drives the speed limit.
– delivery finds the fastest route, in expectation, for a certain delivery driver. Whenever this driver drives on a road with a speed limit ≥ 50 mph, there is a chance that a package will fall out of their truck and be destroyed. They will have to drive to the end of that road, turn around, return to the start city to get a replacement, then drive all the way back to where they were (they won’t make the same mistake the second time they drive on that road).
Consequently, this mistake will add an extra 2 · (troad + ttrip ) hours to their trip, where ttrip is the time it took to get from the start city to the beginning of the road, and troad is the time it takes to drive the length of the road segment.
For a road of length l miles, the probability p of this mistake happening is equal to tanh 􏰀 l 􏰁 1000
if the speed limit is ≥ 50 mph, and 0 otherwise.1 This means that, in expectation, it will take troad + p · 2(troad + ttrip) hours to drive on this road.


This is a simple dataset of North American (though mostly U.S.) major roads.

city-gps.txt contains one line per city, with three fields per line, 
delimited by spaces. The first field is the city, followed by the latitude,
followed by the longitude.

road-segments.txt has one line per road segment connecting two cities.
The space delimited fields are:

- first city
- second city
- length (in miles)
- speed limit (in miles per hour)
- name of highway


Note that there are mistakes and bugs in these files and your code should
still operate correctly; e.g. not all cities that appear in road-segments.txt
have a corresponding line in city-gps.txt. You should assume that all roads
in road-segments.txt are bidirectional, i.e. none are one-way roads, so
that it's possible to travel from the first city to the second city at the
same distance at speed as from the second city to the first city.
