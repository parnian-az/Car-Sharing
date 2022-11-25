# Car-Sharing
Car-sharing is a service that allows drivers to use a shared vehicle and it represents one of the pillars of sustainable urban mobility. Cars are distributed in cities within a defined business area and can be spontaneously and flexibly picked up and dropped off there at any time.

In this project, we have a dataset on a Car Renting Company. This data includes the date of each trip, station codes of origins and destinations, customer IDs, and also reserved time of the trip and the actual time.

By having this data, a model was developed for the administrators of the company for easier analysis of the trips and customers’ behavior. The code was developed by Python, using the Pandas library, and in what follows, each section’s purpose and details are presented.

In the first part, the user enters two dates (from 990101 to 991229 in this dataset), and the following reports will be presented:
1. Totals number of orders and canceled reserves between the dates
2. Average number and standard deviations of orders on each day between the dates
3. Summation, average, and standard deviation of the traveled distance between the dates
4. Bar plot of the average distance traveled each day, as well as maximum and minimum distance traveled, all in one chart on each day (x-axis in the days)
5. Stacked bar plot for accomplished and canceled orders each day
6. Bar plot showing the number of cars entering in and exiting from each station (x-axis in the stations)
7. Scatter plot showing the density of travel between the stations

In the second part, the user enters two stations (from 10 to 30 in this dataset) and will be provided with the following reports (between the same two dates):

1. Total number, average number, and standard deviations of travels between two stations (from to)
2. Pie chart showing the number of cars entering the stations from other stations (for both stations)
3. Pie chart showing the number of cars exiting the stations to other stations (for both stations)

In this third part, the user is asked about the amount of delay time that would make a customer categorized as “Unreliable” and shows a list of these customers.

In this fourth part, we analyze the travels between the months entered in the beginning (for example, the month of 990525 would be 5) and the user will be provided with the following reports:

1. Pie chart for comparison of traveled distance in each month
2. Bar plot for accomplished a canceled demand in each month (x-axis in the month)
3. Asking customer’s ID and showing the density of travels between stations in each month with a scatter plot (the size of the circles represents the total traveled distance in each month)
