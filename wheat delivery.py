import pandas as pd
from itertools import combinations

def calculate_wheat_delivered(stops, total_wheat, total_distance, carriage_capacity, consumption_rate, verbose=False):

    if sum(stops) > total_distance: # check if sum of stops doesnt exceed distance
        return None  
    wheat_on_hand = total_wheat

    if verbose:
        travelled = 0
        print("km\tconsumed\tavailable")
        print(travelled,"km\t0 kg\t\t",wheat_on_hand,"kg")

    for i in range(len(stops)):
        travel_distance = stops[i] # distance travelled

        # calculate number of trips needed according to wheat on hand
        if wheat_on_hand > 2 * carriage_capacity: # >200
            trips = 5 
        elif wheat_on_hand > carriage_capacity: # >100
            trips = 3 
        elif wheat_on_hand <= carriage_capacity: # <=100
            trips = 1 
        
        # calculate wheat consumed
        wheat_consumed = trips * travel_distance * consumption_rate
        wheat_on_hand -= wheat_consumed

        # check if wheat finished
        if wheat_on_hand < 0:
            return None  # Not enough wheat to complete the journey
        
        # update wheat on hand by subtracting wheat wasted at stop (wheat that less than expected consumption will be left at the stop)
        if wheat_on_hand > 2 * carriage_capacity:
            if travel_distance*2 >= wheat_on_hand - 2 * carriage_capacity:
                wheat_on_hand -= wheat_on_hand - 2 * carriage_capacity
        elif wheat_on_hand > carriage_capacity:
            if travel_distance*2 >= wheat_on_hand - carriage_capacity:
                wheat_on_hand -= wheat_on_hand - carriage_capacity
        
        # check if current transport should be continued
        if wheat_on_hand > carriage_capacity: # when wheat on hand is more than carriage capacity
            if travel_distance*2 >= carriage_capacity or travel_distance*2 == wheat_on_hand: 
                return None # not enough wheat to return for fetching the remaining (two-way distance more than carriage capacity or wheat on hand) 
        else: # when wheat on hand is less than carriage capacity (only one way trip possible)
            if travel_distance*2 >= wheat_on_hand and trips > 1: 
                return None # not enough wheat to travel more than one trip / return
        
        if verbose:
            travelled = travelled + travel_distance
            print(travelled,"km\t",wheat_consumed,"kg\t\t",wheat_on_hand,"kg")

    return wheat_on_hand


total_wheat = 300  # kg
total_distance = 100  # km
carriage_capacity = 100  # kg
consumption_rate = 1  # kg/km

results = []
for num_stops in range(2, 4): # number of stops to try
    print("Finding solutions for", num_stops, "stops...")
    for stops in combinations(range(1, total_distance + 1), num_stops):

        if sum(stops) < total_distance: # only proceed when stops are within 100km
            stops_list = list(stops) + [total_distance - sum(stops)] # add travel distance needed to reach last stop
            wheat_delivered = calculate_wheat_delivered(stops_list, total_wheat, total_distance, carriage_capacity, consumption_rate)
            
            # if result valid, add to results list
            if wheat_delivered is not None:
                formatted_stops_list = []
                current_stop_km = 0
                for stop_distance in stops_list:
                    current_stop_km = current_stop_km + stop_distance
                    if current_stop_km < total_distance: # ignore the 100km stop
                        formatted_stops_list.append(str(current_stop_km)) # list of stops at each km 
                results.append([num_stops, ",".join(formatted_stops_list), wheat_delivered])

# write results into csv
df = pd.DataFrame(results, columns=['Number of Stops', 'Stops', 'Wheat Delivered (kg)'])
df = df.sort_values(by=['Wheat Delivered (kg)', 'Number of Stops'], ascending=[False, True])
df.to_csv('wheat_delivery_results.csv', index=False)

print("Results have been written to 'wheat_delivery_results.csv'.")


# run first optimal solution step by step
print("------------------\nRunning optimal solution step-by-step:", df.iloc[0,1].split(","))

# get stops distance
optimal_stops = []
prev_stop_km = 0
for stop_km in list(map(int, df.iloc[0,1].split(","))):
    optimal_stops.append(stop_km - prev_stop_km)
    prev_stop_km = stop_km

optimal_stops = optimal_stops + [total_distance - sum(optimal_stops)] # add 100km stop 
wheat_delivered = calculate_wheat_delivered(optimal_stops, total_wheat, total_distance, carriage_capacity, consumption_rate, True)
print("Wheat delivered:", wheat_delivered, "kg\n------------------")