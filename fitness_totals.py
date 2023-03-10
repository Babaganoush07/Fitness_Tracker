import sqlite3
import datetime

#('2023-03-08',     'Run',       6.64, '0:50:21', '07:34',          105, 'TrailGlove 6 Orange')
#      Date: 0, Event: 1, Distance: 2,   Time: 3, Pace: 4, Elevation: 5, Equipment: 6

def combine_all_tables():
    all_tables = []

    # Connect to Database
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()

    # Get all the table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name ASC")
    table_list = cursor.fetchall()
    # Loop through tables for all data
    for i in range(len(table_list)):
        cursor.execute("SELECT * FROM " + table_list[i][0] + " ORDER BY date ASC")
        table_data = cursor.fetchall()
        all_tables.append(table_data)        
    
    conn.close()
    return all_tables

def get_totals(table):
    events = ['Run', 'Bike', 'Hike']
    # Loop through list of lists
    for i in range(len(table)):
        # Separate by year
        print(f"{table[i][0][0][0:4]:-^30}") #Print table[index][first list of a year][first item of the year][slice year from date]
        # Separate by even
        for e in range(len(events)):
            # Place holders
            total_days = []
            total_miles = 0
            total_time = []
            average_pace = []
            total_elevation = 0

            for a in range(len(table[i])):
                if table[i][a][1] == events[e]:
                    #print(table[i][a])
                    #0 Date
                    if table[i][a][0] not in total_days:
                        total_days.append(table[i][a][0])
                    #2 Miles
                    total_miles = total_miles + table[i][a][2]
                    #3 Time
                    total_time.append(table[i][a][3])
                    #4 Pace
                    average_pace.append(table[i][a][4])
                    #5 Elevation
                    total_elevation = total_elevation + table[i][a][5]
            
            # Final calculations
            try:
                daily_average = round(total_miles/len(total_days),2)
            except ZeroDivisionError:
                daily_average = 0.0

            # Add all the times up
            time_sum = datetime.timedelta()
            for t in total_time:
                (h, m, s) = t.split(':')
                d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                time_sum += d
            total_time = str(time_sum)
            # I stole this and have no idea how it works
            try:
                average_pace = str(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*60 + int(f[1]), map(lambda f: f.split(':'), average_pace)))/len(average_pace)))[2:7]
            except ZeroDivisionError:
                average_pace = '00:00'

            # Print the totals:
            header = len(total_time) + 18
            print(f"{events[e].upper():-^{header}}")
            print(f"{'Total Days:':>15} {len(total_days)}")
            print(f"{'Total Miles:':>15} {round(total_miles,2)}")
            print(f"{'Daily Average:':>15} {daily_average}")
            print(f"{'Total Time:':>15} {total_time}")
            print(f"{'Average Pace:':>15} {average_pace}")
            print(f"{'Elevation Gain:':>15} {total_elevation}")
            print(f"{'-':-^{header}}\n")

all_tables = combine_all_tables()
get_totals(all_tables)
