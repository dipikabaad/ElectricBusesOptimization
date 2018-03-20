import numpy as np
import pandas as pd
import math
import datetime
bus_types = [{'type':'LE','cost':350000,'capacity':95}, {'type':'LF','cost':390000,'capacity':121},{'type':'LFA','cost':570000,'capacity':176}]

import json

slots = json.load(open('./busRoute.json'))

### input
route = 1
month = 3

#print(slots[0]['$data'][1]['waiting_time'])

#lf = 121 #math.floor((19500-10645)/73)
#lfa = 176 #math.floor((29000-16125)/73)
#le = 95 #math.floor((14870-7930)/73)

trip_duration = slots[0]['$data'][route]['waiting_time'] + slots[0]['$data'][route]['duration']

print('trip duration', trip_duration)

#Slot 1
num_buses = math.ceil(trip_duration/slots[0]['$data'][route]['frequency']) + 1

num_trips_per_slot = (4*60)/slots[0]['$data'][route]['frequency']


capacity_required = math.ceil(slots[0]['$data'][route]['passengers'])/num_trips_per_slot

chosen_bus_type = 'LE'

for key in bus_types:
	cap = key['capacity']
	if capacity_required <= cap:
		chosen_bus_type = key
		break

months = [1.5, 1.5, 1.5, 1.5, 1.5, 0.9, 0.9, 0.9, 0.9, 0.9, 1.5, 1.5]

mileage_per_km = months[month-1]

battery_start = 50
increment = 50
max_battery = 401

batteries = [(x) for x in range(battery_start,max_battery, increment)]
	

chosen_batteries = [{'capacity':0,'type':''} for i in range(num_buses)]

for i in range(num_buses):
	for capacity in batteries:
		num_trips_bus = math.ceil((4*60)/slots[0]['$data'][route]['duration']) + i
		print(i,num_trips_bus)
		distance_required = num_trips_bus * slots[0]['$data'][route]['tripDistance']

		distance_predicted = (0.85 * capacity)/mileage_per_km

		if (distance_predicted >= distance_required):
			chosen_batteries[i]['capacity'] = capacity
			chosen_batteries[i]['num_trips'] = num_trips_bus 
			chosen_batteries[i]['bus_duration'] = trip_duration
          chosen_batteries[i]['Bus_Info'] = chosen_bus_type
			#if trip_duration >= 50:
			#	chosen_batteries[i]['type'] = 'MP'
			#else:
			chosen_batteries[i]['type'] = 'HP'
			break

charging_times = {'MP':50,'HP':30}
battery_costs = {'HP': '1150 €/kWh', 'MP': '720 €/kWh'}

#def charge_time(capacity, battery_type='HP', charging_station='Fast'):	
#	if battery_type


print(chosen_batteries)



def scheduler():

	times = []

	time_slots = [{'start':'06', 'minutes':240},{'start':'10', 'minutes':360},{'start':'16', 'minutes':240},{'start':'20', 'minutes':240} ]

	for i in range(4):
		interval = slots[i]['$data'][route]['frequency']
		

		today = datetime.datetime.strptime('2018-03-17 '+time_slots[i]['start']+':00:00','%Y-%m-%d %H:%M:%S')

		date_list = [today + datetime.timedelta(hours = x//60, minutes=x%60) for x in range(0,time_slots[i]['minutes'],interval)]

		times.extend(date_list)

	bus_events = [{'bus_number':x, 'num_trips':0, 'event_log':[]} for x in range(num_buses)]

	available_queue = [{'bus_number':x, 'start_time':None, 'trips_remaining':chosen_batteries[x]['num_trips'],'duration':chosen_batteries[x]['bus_duration']} for x in range(num_buses)]

	running_queue = []

	charging_queue = []

	#print(available_queue)
	
 

	for i,time in enumerate(times):
		#print("RUNNNN",i)
		#print("AVAILABLE_QUEUE",len(available_queue))
		#print("RUNNING_QUEUE",len(running_queue))
		#print("CHARGING_QUEUE",len(charging_queue))
		
		if(len(running_queue) > 0):
			for index, running_bus in enumerate(running_queue):
				bus_duration = running_bus['duration']
				time1 = running_bus['start_time']+datetime.timedelta(hours=bus_duration//60, minutes=bus_duration%60)
				if time1 <= time:			
					#running_bus['trips_remaining'] -= 1
					event = {'start_time':time1.strftime('%Y-%m-%d %H:%M')}
					if(running_bus['trips_remaining'] == 0):
						#running_bus['trips_remaining']=chosen_batteries[running_bus['bus_number']]['num_trips']
						time2 = time1 + datetime.timedelta(minutes=30)
						event['end_time']=time2.strftime('%Y-%m-%d %H:%M')
						event['event']='charging'
                     
						bus_events[running_bus['bus_number']]['event_log'].append(event)
						running_bus['start_time'] = time1
						charging_queue.append(running_bus)
					else:
						available_queue.append(running_bus)
					running_queue.pop(index)
		if(len(charging_queue) > 0):
			for index1, charging_bus in enumerate(charging_queue):
				time1 = charging_bus['start_time']+datetime.timedelta(minutes=30)
				if time1 < time:
					charging_bus['start_time'] = time1
					charging_bus['trips_remaining'] = chosen_batteries[charging_bus['bus_number']]['num_trips']
					available_queue.append(charging_bus)
					charging_queue.pop(index1)
		#print("JUST BEFORE",len(available_queue))
		if(len(available_queue) > 0):
			
			available_bus = available_queue[0]
			bus_duration = available_bus['duration']
			time2 = time+datetime.timedelta(hours=bus_duration//60, minutes=bus_duration%60)
			event = {'start_time':time.strftime('%Y-%m-%d %H:%M'),'event':'running','end_time':time2.strftime('%Y-%m-%d %H:%M')}
			bus_events[available_bus['bus_number']]['event_log'].append(event)
          bus_events[running_bus['bus_number']]['num_trips'] = bus_events[running_bus['bus_number']]['num_trips'] + 1
			available_bus['start_time'] = time
			available_bus['trips_remaining'] -= 1
			running_queue.append(available_bus)
			available_queue.pop(0)
			#print(time,available_queue)
		else:
			
			print('############## FAIL #################')
			print(time)
			print(charging_queue)
			print(running_queue)
		
			print("=========================================")
    return bus_events  #print(bus_events)
    

bus_events = scheduler()
start_time = []
end_time = []
type_activity = []
Month = []
Route = []
Bus = []
bus_events= []
for x in bus_events:
    for y in x['event_log']:
        Bus.append(x['bus_number'])
        start_time.append(y['start_time'])
        end_time.append(y['end_time'])
        type_activity.append(y['event'])
        Month.append('March')
        Route.append(route)
data = {'Bus': Bus, 'start': start_time, 'end': end_time, 'type': type_activity, 'Month': Month, 'Route':Route}
df_schedule =pd.DataFrame.from_dict(data, orient='columns')
        
f2 = open("./Output.csv","w")
pd.DataFrame(df_schedule).to_csv( f2, index=False)
f2.close()

Battery_Capacity = []
Bus_Duration = []
Bus_Type = []
Bus_Cost  = []
Bus_Passenger_Capacity = []
Battery_Type = []
Bus =[]
Num_trips = []
for x in bus_events:
    Num_trips.append(x['num_trips'])
for x in chosen_batteries:
    Bus.append(x+1)
    Battery_Capacity.append(x['capacity'])
    Bus_Trip_Duration.append(x['bus_duration'])
    Bus_Type.append(x['Bus_Info']['type'])
    Bus_Cost.append(x['Bus_Info']['cost'])
    Bus_Passenger_Capacity.append(x['Bus_Info']['capacity'])
    Battery_Type.append(x['type'])
    Battery_Cost.append(battery_costs[x['type']])
data = {'Bus': Bus, 'Bus Type': Bus_type, 'Bus Cost': Bus_Cost, 'Passengers': Bus_Passenger_Capacity, 'Battery Type': Battery_Type, 'Battery Capacity':Battery_Capacity, 'Battery Cost': Battery_Cost}
df_schedule =pd.DataFrame.from_dict(data, orient='columns')
        
f2 = open("./Output.csv","w")
pd.DataFrame(df_schedule).to_csv( f2, index=False)
f2.close()

