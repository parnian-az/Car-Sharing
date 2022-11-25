#Car Sharing
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def date_taker(day_name = " "):
    #this function gets the dates and check them out
    sign = 1
    while True :
        date1 = input("\nPlease enter the %s date: "%(day_name))
        digits = list(date1)
        if len(date1) != 6:
            print("\nWrong format. Please try again.")
            
        elif len(date1) == 6:
            day = int(''.join(digits[4:]))
            month = int(''.join(digits[2:4]))
            if day > 31 or day < 1 or month > 12 or month < 1:
                print("\nWrong format in Days or Month. Please try again.")
            else:
                sign = 0
        if sign == 0:
            return(int(date1))
            break

Sample = pd.read_excel('CarSharing_XLSX\Sample.xlsx')
ID = pd.read_excel('CarSharing_XLSX\CustomerID.xlsx', header = None,  names = ["Customer ID"])
station = pd.read_excel('CarSharing_XLSX\StationID.xlsx',  names = ["Station ID"])

a = date_taker("fisrt")
b = date_taker("second")
date1 = min(a,b)
date2 = max(a,b)
cond1 = date1 <= Sample['روز']
cond2 = Sample['روز']<= date2

#Area is the selected data between the dates
Area = Sample[cond1 & cond2]
#Total number of the Demands
num_demand = len(Area)
#Number of the Canceled requests
num_canceled = len(Area.iloc[:, -1][Area.iloc[:, -1] == '-'])

#Mean and SD of Demands 
Area2 = Area.drop(Area.index[Area.iloc[:,-1]== '-'])
dis_data = Area2.groupby(['روز'])['مسافت'].agg(['count', 'max', 'min', 'sum'])
dis_data['mean'] = dis_data['sum']/dis_data['count']

print("\nStatistical reports: \n")

if len(Area) > 0:
    print("1. Total Number of Requests: %i\n2. Number of Canceled Requests: %i\n3. The Average number of the Requests between these two dates: %f"%(num_demand,num_canceled, dis_data['count'].mean() ))
    if len(dis_data) > 1:
        print("4. The Standard Deviation of the Requests between these dates: %f"%(dis_data['count'].std()))
    elif len(dis_data) == 1:
        print("\n4. No Standard Deviation for one Data.")
    print("5. Total distance between these dates: %f \n6. Average Distance: %f"%(dis_data['sum'].sum(), dis_data['mean'].mean()))
    if len(dis_data) > 1:
        print("7. Standard Deviation of the Distance: %f"%(dis_data['mean'].std()))
    elif len(dis_data) == 1:
        print("7. No Standard Deviation for one Data.")
    #Bar Plot fir Distance per Day
    dis_data.insert(0, 'Date', dis_data.index)
    bar_plot= dis_data.plot.bar(x = 'Date',  y = ['max', 'min', 'mean'],  title = "Max,Min and Average distance per day")
    bar_plot.set_xlabel("Date")

    #Stack Bar Plot for the Accomplished and the Canceled Requests
    Area3 = Area.drop(Area.index[Area.iloc[:,-1]!= '-'])
    canceled = Area3.groupby(['روز'])['مسافت'].agg(['count'])
    #Area4 is the dataset of the Accomplished and the Canceled Requests
    Area4 = Area.groupby(['روز'])['مسافت'].agg(['count'])
    Area4['canceled'] = canceled
    Area4 = Area4.replace(np.nan, 0)
    Area4['accomplished'] = Area4['count'] - Area4['canceled']
    Area4.insert(0, 'Date', Area4.index)
    stacked_plot = Area4.plot.bar(x = 'Date',  y = ['accomplished', 'canceled'], stacked=True,  title = "Number of done and canceled requests")
    stacked_plot.set_xlabel("Date")


    #Bar plot to show car transfer between stations
    s_index = station['Station ID']
    station = station.reindex(index = s_index)
    enter_station = Area.groupby(['از ایستگاه'])['روز'].count()
    exit_station = Area.groupby(['به ایستگاه'])['روز'].count()
    station['Enter'] = enter_station
    station['Exit'] = exit_station
    station['Station ID'] = station.index
    station_plot = station.plot.bar(x = 'Station ID', y = ['Enter','Exit'] ,  title = "Number of cars entering and exiting from each station")

else:
    print("\nNo Request between these two dates.")
    


Sample2 = Sample.drop(Sample.index[Sample.iloc[:,-1]== '-'])
Time = pd.DataFrame(np.zeros((len(Sample2), 10)),  columns = ['Reserve_S_h','Reserve_S_m','Reserve_E_h','Reserve_E_m','Actual_S_h','Actual_S_m','Actual_E_h','Actual_E_m', 'Start_gap', 'End_gap'])
#this loop is to calculate hour and mintues
for i in range(len(Sample2)):
    start_res = list(str(list(Sample2['رزرو از'])[i]))
    end_res = list(str(list(Sample2['رزور تا'])[i]))
    start_act = list(str(list(Sample2['واقعی از'])[i]))
    end_act = list(str(list(Sample2['واقعی تا'])[i]))
    #srart reserved minutes and hour
    sr_m2 = start_res.pop()
    sr_m1 = start_res.pop()
    sr_m = int(sr_m1+sr_m2)
    sr_h = int(''.join(start_res))
    Time['Reserve_S_h'][i] = sr_h
    Time['Reserve_S_m'][i] = sr_m
    #end reserved minutes abd hour
    er_m2 = end_res.pop()
    er_m1 = end_res.pop()
    er_m = int(er_m1+er_m2)
    er_h = int(''.join(end_res))
    Time['Reserve_E_h'][i] = er_h
    Time['Reserve_E_m'][i] = er_m
    #srart actual minutes and hour
    sa_m2 = start_act.pop()
    sa_m1 = start_act.pop()
    sa_m = int(sa_m1+sa_m2)
    sa_h = int(''.join(start_act))
    Time['Actual_S_h'][i] = sa_h
    Time['Actual_S_m'][i] = sa_m
    #end actual minutes and hour
    ea_m2 = end_act.pop()
    ea_m1 = end_act.pop()
    ea_m = int(ea_m1+ea_m2)
    ea_h = int(''.join(end_act))
    Time['Actual_E_h'][i] = ea_h
    Time['Actual_E_m'][i] = ea_m
    if sr_h >= sa_h:
        h = sr_h - sa_h
        if sr_m >= sa_m:
            m = sr_m - sa_m
            gap = h*60 + m
        elif sr_m < sa_m and sa_h >= 1:
            m = sr_m - sa_m + 60
            gap = (h-1)*60 + m
    elif sr_h < sa_h:
        h = sa_h - sr_h
        if sr_m >= sa_m:
            m = sr_m - sa_m
            gap = h*60 + m
        elif sr_m < sa_m and sa_h >= 1:
            m = sr_m - sa_m + 60
            gap = (h-1)*60 + m
    Time['Start_gap'][i] = gap
    if er_h >= ea_h:
        h = er_h - ea_h
        if er_m >= ea_m:
            m = sr_m - ea_m
            gap = h*60 + m
        elif er_m < ea_m and h >= 1:
            m = er_m - ea_m + 60
            gap = (h-1)*60 + m
        else:
            gap = max(er_m, ea_m) -  min(er_m, ea_m)
            
    elif er_h < ea_h:
        h = ea_h - er_h
        if er_m >= ea_m:
            m = er_m - ea_m
            gap = h*60 + m
        elif er_m < ea_m and h >= 1:
            m = er_m - ea_m + 60
            gap = (h-1)*60 + m
        else:
            gap = max(er_m, ea_m) -  min(er_m, ea_m)
    Time['End_gap'][i] = gap
Time['Date']= Sample['روز']
condition1 = date1 <= Time['Date']
condition2 = Time['Date']<= date2
chosen_time = Time[condition1 & condition2]

hlist = pd.DataFrame(np.arange(min(Time.Reserve_S_h),max(Time.Reserve_E_h),1) , columns = ['Hour_list'])

#Processing customers move between given Station
move = Area.groupby(['از ایستگاه','به ایستگاه'])['کد مشتری']
move_record = move.count().values
move_plan = move.count()
moves = move_plan.unstack()
moves2 = pd.DataFrame( Area['از ایستگاه'].values ,  columns = ['From'] )
moves2['To']  =Area['به ایستگاه'].values

s = np.zeros(len(moves2))
for i in range(len(moves2)):
    s[i] = moves.loc[moves2['From'][i],moves2['To'][i]]
moves2.plot.scatter(x = 'From' , y = 'To',  s = s* 100,  title = "Number of trips between stations")
plt.show()

while True:
    stn1 = int(input('\nFirst Station: '))
    if stn1 > station['Station ID'].max() or stn1 < station['Station ID'].min():
        print('\nwrong format, please try again')
    else:
        break
while True:
    stn2 = int(input('\nSecond Station: '))
    if stn2 > station['Station ID'].max() or stn2 < station['Station ID'].min():
        print('\nwrong format, please try again')
    else:
        break
        
#No. Request between the stations
cond1 = Area['از ایستگاه']== stn1
cond2 = Area['به ایستگاه']== stn2
Area5 = Area[cond1 & cond2]

stn_data = Area5.groupby(['روز'])['روز'].count()

sign = 0
print("\nStation report:\n")
if stn_data.count() > 0 :
    print("\n1. Number of trips between these stations: %i"%(stn_data.sum()))
    print("2. Average number of trips per day: %i"%(stn_data.mean()))
    if stn_data.count() == 1:
        print("3. No Standart Deviation for one data.")
    else:
        print("3. Standart Deviation of trips between these stations: %i"%(stn_data.std()))
else :
    sign = 1
    print("\nThere has been No Trip between these two stations.")

timing = pd.DataFrame(np.zeros((4, len(Area5['واقعی از']))).T ,  columns = ['hour', 'minute','numeric time','trip time'])
#this loop is to calculate hour and mintues
for i in range(len(Area5['واقعی از'])):
    a = list(list(Area5['واقعی از'])[i])
    b = list(list(Area5['واقعی تا'])[i])
    m1 = a.pop()
    m2 = a.pop()
    m3 =b.pop()
    m4 = b.pop()
    min1 = int(m2+m1)
    min2 = int(m4+m3)
    hour1 = int(''.join(a))
    hour2 = int(''.join(b))
    if min2 - min1 > 0:
        hour = abs(hour2 - hour1)
        min3 = min2- min1
        time_show = str(hour)+str(min3)
        if len(time_show)<4:
            time_show = '0'+time_show
    else:
        hour = abs(hour2 - hour1 - 1)
        min3 = min2- min1 + 60
        time_show = str(hour)+str(min3)
        if len(time_show)<4:
            time_show = '0'+time_show
    timing['hour'][i] = hour
    timing['minute'][i] = min3
    timing['numeric time'][i] = hour*60 + min3
    timing['trip time'][i] = str(time_show)
    
timing.insert(0, 'Date', Area5['روز'].values)
timing2 = timing.groupby('Date')['numeric time'].agg(['mean','max','min','std'])
timing2 = timing2.replace(np.nan,  '-')

if sign == 0:
    print('4. This Frame shows Average, Standard Deviation, Maximum and Minimum Time for each trip Per Day : \n')
    print(timing2)
    total_time= (timing.groupby('Date')['numeric time'].sum()).sum()
    total_distance = Area5['مسافت'][Area5['مسافت'] != '-'].sum()
    print("\n5. The Average Velocity between these stations (Km/h): %f"%(total_distance/(total_time/60)))

    #shows the trips that their destination is stn1 and stn2
    Enter_data1 = Area[Area['به ایستگاه'] == stn1 ]
    Enter_data2 = Area[Area['به ایستگاه'] == stn2]
    Enter_data3 = Area[Area['از ایستگاه'] == stn1]
    Enter_data4 = Area[Area['از ایستگاه'] == stn2]

    a = Enter_data1.groupby(['از ایستگاه'])['از ایستگاه']
    b = Enter_data2.groupby(['از ایستگاه'])['از ایستگاه']
    c = Enter_data3.groupby(['به ایستگاه'])['به ایستگاه']
    d = Enter_data4.groupby(['به ایستگاه'])['به ایستگاه']

    s1= pd.DataFrame(a.count())
    s2= pd.DataFrame(b.count())
    s3= pd.DataFrame(c.count())
    s4= pd.DataFrame(d.count())

    # Trips Ending with station number stn1
    pie1 = s1.plot.pie(subplots = True, autopct='%1.1f%%',  title = "Percentage of the Cars entering station %i from other stations."%(stn1))
    plt.show()
    # Trips Ending with station number stn2
    pie2 = s2.plot.pie(subplots = True, autopct='%1.1f%%',  title = "Percentage of the Cars entering station %i from other stations."%(stn2))
    plt.show()
    # Trips Starting with station number stn1
    pie3 = s3.plot.pie(subplots = True, autopct='%1.1f%%',  title = "Percentage of the Cars exiting station %i to other stations."%(stn1))
    plt.show()
    # Trips Starting with station number stn2
    pie4 = s4.plot.pie(subplots = True, autopct='%1.1f%%',  title = "Percentage of the Casr exiting station %i to other stations."%(stn2))
    plt.show()
#plt.show()


Time['Total_Gap'] = Time['Start_gap'] +Time['End_gap']
Time.insert(0, 'Customers', Sample['کد مشتری'])
Unreliable_list = Time.groupby(['Customers'])['Total_Gap'].sum()
Unreliable_list = Unreliable_list.sort_values(ascending=False)
Gap = int(input("\nHow much delay would make a customer Unreliable? (in minutes) "))
print("\nHere is the list of the Unreliable Customers: \n")
print(Unreliable_list[Unreliable_list>= Gap])

Month = pd.Series(np.zeros(len(Sample)))
for j in range(len(Sample)):
    total_date = str(list(Sample['روز'])[j])
    listed_date = [total_date[i:i+2] for i in range(0, len(total_date), 2)]
    Month[j] = int(listed_date[1])
Sample['Month'] = Month

start_month = int([str(date1)[i:i+2] for i in range(0, len(str(date1)), 2)][1])
stop_month = int([str(date2)[i:i+2] for i in range(0, len(str(date2)), 2)][1])

distance_data = Sample.replace('-', 0)
distance = distance_data.groupby(['Month'])['مسافت'].sum()
selected_distance = distance[start_month: stop_month]
distance_frame = pd.DataFrame(selected_distance)
dis_plot = distance_frame.plot.pie(subplots = True, autopct='%1.1f%%')

total_request_data = Sample.groupby(['Month'])['مسافت'].count()
cancel_free = Sample.drop(Sample.index[Sample.iloc[:,-2]== '-'])
cancel_free_data = cancel_free.groupby(['Month'])['مسافت'].count()
cancel_free_data.name = 'Done'
total_request_data.name = 'Total'

Request = pd.concat([total_request_data, cancel_free_data], axis=1)
Request['Canceled'] = Request['Total'] - Request['Done']
Request['Month'] = Request.index
#Done and Canceled Requestes in each Month
Req_plot = Request.plot.bar(stacked = True ,  x = 'Month',  y = ['Done', 'Canceled'], title = "Number of done and canceled requests")
#plt.show()
Req_plot

while True:
    customer = int(input("\nPlease enter Customer Code: "))
    if customer in ID.values:
        break
    else:
        print("Not found. Try again.")

customer_data =distance_data[distance_data['کد مشتری']==customer]
C1 = customer_data['Month']>= start_month
C2 = customer_data['Month']<= stop_month
customer_data2 = customer_data[C1 &  C2]
for i in range(stop_month-start_month+1):
    c_data = customer_data2[customer_data2['Month'] == start_month+i]
    c = c_data.plot.scatter(x = 'از ایستگاه',  y = 'به ایستگاه', s = 'مسافت', title = 'Month %i'%(start_month+i))
    c.set(xlabel="To", ylabel="From")
    
    plt.show()

#plt.show()




