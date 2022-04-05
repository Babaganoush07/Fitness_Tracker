#-*-coding:utf8;-*-
#qpy:console

import datetime, re, sqlite3, colorama, os
from functools import reduce
from operator import add
from colorama import Fore, Style, init
from colorama import init
init(autoreset=True)

fitness_info = ['-',1,2,3,4,5,6,7]

# CREATE A TABLE FOR THE YEAR IF IT DOES NOT ALREADY EXIST IN THE FITNESS DATABASE
table_name = 'fitness_' + str(datetime.date.today().year)
conn = sqlite3.connect('fitness.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS """ + table_name + """ (
            Date real,
            Event real,
            Distance real,
            Time real,
            Pace real,
            Elevation integer,
            Equipment text
            )""")
conn.commit()
conn.close()

class c():
    menu = Fore.CYAN+Style.BRIGHT
    error = Fore.RED
    success = Fore.GREEN
    run = Fore.CYAN
    hike = Fore.YELLOW
    bike = Fore.MAGENTA+Style.BRIGHT
    
# DEFINE AND VERIFY ALL THE DATA INPUTS
def add_date():
    while True:
        date_regex = re.compile(r'^\d{4}\-\d{2}\-\d{2}$')
        today = str(datetime.date.today())
        date = input('Default Date: '  + today + '\nOr enter new Date: ')
        date = date or today
        if date_regex.search(date):
            fitness_info[1] = date
            break
        else:
            print(Fore.RED + '\nDate format is yyyy-mm-dd\n')
            continue
        
def add_event():
    while True:
        event = input('Event type,\nRun, Hike, Bike: ')
        if event.lower() == 'run' or event.lower() == 'hike' or event.lower() == 'bike':
            event = str.title(event.lower())
            fitness_info[2] = event
            break
        elif event == '':
            print(Fore.RED + '\nEnter Event.\n')
            error_sound()
            continue
        else:
            print(Fore.RED + '\nEvent not found.\n')
            continue
    
def add_distance():
    while True:
        dist_reg = re.compile(r'^\d+\.\d{2}$')
        distance = input('Distance format 00.00\nDistance: ')
        if dist_reg.search(distance):
            fitness_info[3] = distance
            break
        else:
            print(Fore.RED + '\nDistance format is ##.##\n')
            continue

def add_time():
    while True:
        time_reg = re.compile(r'^\d+\:\b[0-5][0-9]:\b[0-5][0-9]$')
        time = input('Time format 00:00:00\nTime: ')
        if time_reg.search(time):
            fitness_info[4] = time
            break
        else:
            print(Fore.RED + '\nTime format is ##:##:##\n')
            continue

def add_pace():
    try:
        time = fitness_info[4]
        time_format = "%H:%M:%S"
        time = datetime.datetime.strptime(time, time_format)
        time = datetime.timedelta(seconds=time.second, minutes=time.minute, hours=time.hour)
        calculated_pace = str(time/ float(fitness_info[3]))
        calculated_pace = calculated_pace[2:7]
    except:
       calculated_pace = '00:00'
       
    while True:
        pace_reg = re.compile(r'^\b[0-5][0-9]:\b[0-5][0-9]$')
        pace = input('Calclulated Pace: ' + calculated_pace + '\nOr enter new Pace: ')
        pace = pace or calculated_pace
        if pace_reg.search(pace):
            fitness_info[5] = pace
            break
        else:
            print(Fore.RED + '\nPace format is ##:##\n')
            continue
        
def add_elevation():
    while True:
        elevation_reg = re.compile(r'^\d+$')
        elevation = input('Elevation: ')
        if elevation_reg.search(elevation):
            fitness_info[6] = elevation
            break
        else:
            print(Fore.RED + '\nEnter Elevation.\n')
            continue
        
def  add_equipment():
    number = 1
    numbered_equipment_list = []
    while True:
        if fitness_info[2] == 'Run':
            for each in shoes_list:
                for shoes in each:
                    add_to = (number, shoes)
                    numbered_equipment_list.append(add_to)
                    number += 1
            for each in numbered_equipment_list:
                print(str(each[0])+'. '+each[1])
                
        elif fitness_info[2] == 'Hike':
            for each in boots_list:
                for boots in each:
                    add_to = (number, boots)
                    numbered_equipment_list.append(add_to)
                    number += 1
            for each in numbered_equipment_list:
                print(str(each[0])+'. '+each[1])
            
        elif fitness_info[2] == 'Bike':
            for each in bike_list:
                for bike in each:
                    add_to = (number, bike)
                    numbered_equipment_list.append(add_to)
                    number += 1
            for each in numbered_equipment_list:
                print(str(each[0])+'. '+each[1])

        equipment = input('Equipment: ')
        if equipment != '':
            try:
                equipment = int(equipment)-1
            except:
                equipment
            if equipment in range(len(numbered_equipment_list)):
                fitness_info[7] = numbered_equipment_list[equipment][1]
            else:
                fitness_info[7] = equipment
            break
        else:
            print(Fore.RED + '\nEnter Equipment.\n')
            continue

# CONFIRM USER INPUT
def confirm_record():
    print('Your Fitness Information\n')
    titles = ['ID: ', 'Date: ', 'Event: ', 'Distance: ', 'Time: ', 'Pace: ', 'Elevation: ', 'Equipment: ']
    combined_lists = "\n".join("{} {}".format(x, y) for x, y in zip(titles, fitness_info))
    print(combined_lists)
      
    while True:
        global verify
        verify = input('\nIs this correct?.\nEnter Y / N: ')
        if verify.upper() == 'Y':
            break
        elif verify.upper() == 'N':
            break
        else:
            print(Fore.RED + 'Enter Y or N to continue.')
            continue

# EDIT INFORMATION FUNCTION
def edit_record():
    print('What do you want to edit?\n')
    titles = ['ID: ', 'Date: ', 'Event', 'Distance: ', 'Time: ', 'Pace: ', 'Elevation: ', 'Equipment: ']
    combined_lists = "\n".join("{} {}".format(x, y) for x, y in zip(titles, fitness_info))
    print(combined_lists)
    
    while True:
        edit = input('\nEnter one of the following to edit.\nDate, Event, Distance, Time, Pace, Elevation or Equipment: ')
        if edit.lower() == 'date':
            add_date()
            break
        elif edit.lower() == 'event':
            add_event()
            break
        elif edit.lower() == 'distance':
            add_distance()
            break
        elif edit.lower() == 'time':
            add_time()
            break
        elif edit.lower() == 'pace':
            add_pace()
            break
        elif edit.lower() == 'elevation':
            add_elevation()
            break
        elif edit.lower() == 'equipment':
            add_equipment()
            break
        else:
            print(Fore.RED + 'Entry not recognized.')
            continue

# SELECT EXISTING RECORD
def select_old_record():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    while True:
        global fitness_info
        global rowid
        rowid = input('(X to cancel)\nEnter row id: ')
        if rowid.upper() == 'X':
            break
        else:
            try:
                cursor.execute('SELECT rowid, * FROM ' + table_name +' WHERE rowid = ?',[rowid])
                fitness_info = list(cursor.fetchone())
            except:
                print(Fore.RED + 'Item not found.')
                continue
        # VERIFY THIS IS THE DESIRED RECORD
        confirm_record()
        if verify.upper() == 'Y':
            break
        else:
            continue
    conn.commit()
    conn.close()
    
# DELETE RECORD
def delete_record():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM """+ table_name + """
                WHERE rowid = ?
                """,[fitness_info[0]])
    conn.commit()
    conn.close()
    print(Fore.GREEN + fitness_info[2] + ' Deleted.')

# UPDATE RECORD IN DATABASE
def update_record():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.executemany("""UPDATE """+ table_name + """ SET
                Date=?,
                Event=?,
                Distance=?,
                Time=?,
                Pace=?,
                Elevation=?,
                Equipment=?
                WHERE rowid = ?
                """,[(fitness_info[1], fitness_info[2], fitness_info[3], fitness_info[4], fitness_info[5], fitness_info[6], fitness_info[7], fitness_info[0])])
    conn.commit()
    conn.close()
    print(Fore.GREEN + fitness_info[2] + ' Updated.')

# ADD A NEW RECORD TO DATABASE
def add_new_record(list):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO """ + table_name + """
                VALUES (?,?,?,?,?,?,?)""",
                (fitness_info[1], fitness_info[2], fitness_info[3], fitness_info[4], fitness_info[5], fitness_info[6], fitness_info[7]))
    conn.commit()
    conn.close()
    print(Fore.GREEN + fitness_info[2] + ' Added.')

# STEPS TO ADD A NEW RECORD        
def new_record():
    add_date()
    add_event()
    add_distance()
    add_time()
    add_pace()
    add_elevation()
    add_equipment()
    while True:
        confirm_record()
        if verify.upper() == 'Y':
            add_new_record(list)
            break
        else:
            edit_record()
            continue

# QUERRY AND FETCHALL DATA
def querry_data():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rowid, * FROM ' + table_name)
    database = cursor.fetchall()
    conn.commit()
    conn.close()
    return database

# PRINT THE DATABASE ITEMS
def print_data(list):
    # Add headers
    header = ['ID', 'Date', 'Event', 'Distance', 'Time','Pace','Elevation','Equipment']
    database = querry_data()
    print("{: >3} {: >10} {: >5} {: >8} {: >8} {: >5} {: >9} {: >8}".format(*header).ljust(10))

    for row in database:
        if row[2] == 'Run':
            print(Fore.CYAN + "{: >3} {: >10} {: >5} {: >8} {: >8} {: >5} {: >9} {: >8}".format(*row).center(10))
        elif row[2] == 'Hike':
            print(Fore.YELLOW + "{: >3} {: >10} {: >5} {: >8} {: >8} {: >5} {: >9} {: >8}".format(*row).center(10))
        elif row[2] == 'Bike':
            print(Fore.MAGENTA + Style.BRIGHT + "{: >3} {: >10} {: >5} {: >8} {: >8} {: >5} {: >9} {: >8}".format(*row).center(10))

    print(Fore.GREEN + 'Done' + Style.RESET_ALL)
    
# GET TOTALS BREAKDOWN
def get_totals():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    # RUNNING TOTALS___________________________________________________

    # TOTAL DAYS
    cursor.execute("SELECT DISTINCT Date, Event FROM " + table_name + " WHERE Event = 'Run'")
    total_days_tuple = cursor.fetchall()

    print(Fore.CYAN + '\nRUNNING TOTALS FOR: ' +str(table_name[-4:]))

    if table_name[-4:] == str(datetime.date.today().year):
        print(Fore.CYAN + 'Total Days Ran: ' + str(len(total_days_tuple))+ ' / ' + str(datetime.datetime.now().timetuple().tm_yday))
    else:
        print(Fore.CYAN + 'Total Days Ran: ' + str(len(total_days_tuple)))

    # TOTAL DISTANCE
    cursor.execute("SELECT round(sum(Distance),2), Event FROM " + table_name + " WHERE Event = 'Run'")
    total_distance_tuple = cursor.fetchone()

    total_distance_float = total_distance_tuple[0]
    print(Fore.CYAN + 'Total Miles: '+str(total_distance_float))
    
    # TOTAL TIME
    cursor.execute("SELECT Time, Event FROM " + table_name + " WHERE Event = 'Run'")
    total_time_tuple = cursor.fetchall()
    total_time_lst = []

    try:
        for each in total_time_tuple:
            total_time_lst.append(each[0])
        total_time = datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), total_time_lst))))
        def convert_to_hours(delta):
            total_seconds = delta.total_seconds()
            hours = str(int(total_seconds // 3600)).zfill(2)
            minutes = str(int((total_seconds % 3600) // 60)).zfill(2)
            seconds = str(int(total_seconds % 60)).zfill(2)
            print(Fore.CYAN + 'Total Time: ' + f"{hours}:{minutes}:{seconds}")
        convert_to_hours(total_time)
    except:
        print(Fore.CYAN + 'Total Time: None')
        
    # TOTAL ELEVATION
    cursor.execute("SELECT sum(Elevation), Event FROM " + table_name + " WHERE Event = 'Run'")
    total_elevation_tuple = cursor.fetchone()

    try:
        total_elevation = "{:,}".format(int(total_elevation_tuple[0]))
        print(Fore.CYAN + 'Total Elevation: '+str(total_elevation)+"'")
    except:
        print(Fore.CYAN + 'Total Elevation: None')

    # AVERAGE PACE
    cursor.execute("SELECT Pace, Event FROM " + table_name + " WHERE Event = 'Run'")
    total_pace_tuple = cursor.fetchall()
    total_pace_lst = []

    try:
        for each in total_pace_tuple:
            total_pace_lst.append(each[0])
        average_pace = str(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*60 + int(f[1]), map(lambda f: f.split(':'), total_pace_lst)))/len(total_pace_lst)))
        print(Fore.CYAN + 'Average Pace: '+(average_pace[2:7]))
    except:
        print(Fore.CYAN + 'Average Pace: None')

    # DAILY MILE AVERAGE
    try:
        print(Fore.CYAN + 'Daily Mile Average: ' + str(round(total_distance_float / len(total_days_tuple),2)))
    except:
        print(Fore.CYAN + 'Daily Mile Average: None')

    # MILES PER SHOE
    cursor.execute("SELECT Equipment, round(sum(Distance),2), Event FROM " + table_name + " WHERE Event = 'Run' GROUP BY Equipment")
    total_shoes_tuple = cursor.fetchall()

    print(Fore.CYAN + '\nMiles per Shoe:')
    for each in total_shoes_tuple:
        print(Fore.CYAN + str(each[0])+': '+str(each[1]))

    # HIKING TOTALS______________________________________________________________________________
    print(Fore.YELLOW + '\nHIKING TOTALS FOR: ' +str(table_name[-4:]))

    # TOTAL DAYS
    cursor.execute("SELECT DISTINCT Date, Event FROM " + table_name + " WHERE Event = 'Hike'")
    total_days_tuple = cursor.fetchall()

    if table_name[-4:] == str(datetime.date.today().year):
        print(Fore.YELLOW + 'Total Hike Days: ' + str(len(total_days_tuple))+ ' / ' + str(datetime.datetime.now().timetuple().tm_yday))
    else:
        print(Fore.YELLOW + 'Total Hike Days: ' + str(len(total_days_tuple)))

    # TOTAL DISTANCE
    cursor.execute("SELECT round(sum(Distance),2), Event FROM " + table_name + " WHERE Event = 'Hike'")
    total_distance_tuple = cursor.fetchone()

    total_distance_float = total_distance_tuple[0]
    print(Fore.YELLOW + 'Total Miles: '+str(total_distance_float))
    
    # TOTAL TIME
    cursor.execute("SELECT Time, Event FROM " + table_name + " WHERE Event = 'Hike'")
    total_time_tuple = cursor.fetchall()
    total_time_lst = []

    try:
        for each in total_time_tuple:
            total_time_lst.append(each[0])
        total_time = datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), total_time_lst))))
        def convert_to_hours(delta):
            total_seconds = delta.total_seconds()
            hours = str(int(total_seconds // 3600)).zfill(2)
            minutes = str(int((total_seconds % 3600) // 60)).zfill(2)
            seconds = str(int(total_seconds % 60)).zfill(2)
            print(Fore.YELLOW + 'Total Time: ' + f"{hours}:{minutes}:{seconds}")
        convert_to_hours(total_time)
    except:
        print(Fore.YELLOW + 'Total Time: None')
        
    # TOTAL ELEVATION
    cursor.execute("SELECT sum(Elevation), Event FROM " + table_name + " WHERE Event = 'Hike'")
    total_elevation_tuple = cursor.fetchone()

    try:
        total_elevation = "{:,}".format(int(total_elevation_tuple[0]))
        print(Fore.YELLOW + 'Total Elevation: '+str(total_elevation)+"'")
    except:
        print(Fore.YELLOW + 'Total Elevation: None')

    # AVERAGE PACE
    cursor.execute("SELECT Pace, Event FROM " + table_name + " WHERE Event = 'Hike'")
    total_pace_tuple = cursor.fetchall()
    total_pace_lst = []

    try:
        for each in total_pace_tuple:
            total_pace_lst.append(each[0])
        average_pace = str(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*60 + int(f[1]), map(lambda f: f.split(':'), total_pace_lst)))/len(total_pace_lst)))
        print(Fore.YELLOW + 'Average Pace: '+(average_pace[2:7]))
    except:
        print(Fore.YELLOW + 'Average Pace: None')

    # DAILY MILE AVERAGE
    try:
        print(Fore.YELLOW + 'Daily Mile Average: ' + str(round(total_distance_float / len(total_days_tuple),2)))
    except:
        print(Fore.YELLOW + 'Daily Mile Average: None')

    # MILES PER BOOT
    cursor.execute("SELECT Equipment, round(sum(Distance),2), Event FROM " + table_name + " WHERE Event = 'Hike' GROUP BY Equipment")
    total_shoes_tuple = cursor.fetchall()

    print(Fore.YELLOW + '\nMiles per Boot:')
    for each in total_shoes_tuple:
        print(Fore.YELLOW + str(each[0])+': '+str(each[1]))

    # BIKING TOTALS______________________________________________________________________________
    print(Fore.MAGENTA + Style.BRIGHT + '\nBIKING TOTALS FOR: ' +str(table_name[-4:]))

    # TOTAL DAYS
    cursor.execute("SELECT DISTINCT Date, Event FROM " + table_name + " WHERE Event = 'Bike'")
    total_days_tuple = cursor.fetchall()

    if table_name[-4:] == str(datetime.date.today().year):
        print(Fore.MAGENTA + Style.BRIGHT + 'Total Bike Days: ' + str(len(total_days_tuple))+ ' / ' + str(datetime.datetime.now().timetuple().tm_yday))
    else:
        print(Fore.MAGENTA + Style.BRIGHT + 'Total Bike Days: ' + str(len(total_days_tuple)))

    # TOTAL DISTANCE
    cursor.execute("SELECT round(sum(Distance),2), Event FROM " + table_name + " WHERE Event = 'Bike'")
    total_distance_tuple = cursor.fetchone()

    total_distance_float = total_distance_tuple[0]
    print(Fore.MAGENTA + Style.BRIGHT + 'Total Miles: '+str(total_distance_float))
    
    # TOTAL TIME
    cursor.execute("SELECT Time, Event FROM " + table_name + " WHERE Event = 'Bike'")
    total_time_tuple = cursor.fetchall()
    total_time_lst = []

    try:
        for each in total_time_tuple:
            total_time_lst.append(each[0])
        total_time = datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), total_time_lst))))
        def convert_to_hours(delta):
            total_seconds = delta.total_seconds()
            hours = str(int(total_seconds // 3600)).zfill(2)
            minutes = str(int((total_seconds % 3600) // 60)).zfill(2)
            seconds = str(int(total_seconds % 60)).zfill(2)
            print(Fore.MAGENTA + Style.BRIGHT + 'Total Time: ' + f"{hours}:{minutes}:{seconds}")
        convert_to_hours(total_time)
    except:
        print(Fore.MAGENTA + Style.BRIGHT + 'Total Time: None')
        
    # TOTAL ELEVATION
    cursor.execute("SELECT sum(Elevation), Event FROM " + table_name + " WHERE Event = 'Bike'")
    total_elevation_tuple = cursor.fetchone()

    try:
        total_elevation = "{:,}".format(int(total_elevation_tuple[0]))
        print(Fore.MAGENTA + Style.BRIGHT + 'Total Elevation: '+str(total_elevation)+"'")
    except:
        print(Fore.MAGENTA + Style.BRIGHT + 'Total Elevation: None')

    # AVERAGE PACE
    cursor.execute("SELECT Pace, Event FROM " + table_name + " WHERE Event = 'Bike'")
    total_pace_tuple = cursor.fetchall()
    total_pace_lst = []

    try:
        for each in total_pace_tuple:
            total_pace_lst.append(each[0])
        average_pace = str(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*60 + int(f[1]), map(lambda f: f.split(':'), total_pace_lst)))/len(total_pace_lst)))
        print(Fore.MAGENTA + Style.BRIGHT + 'Average Pace: '+(average_pace[2:7]))
    except:
        print(Fore.MAGENTA + Style.BRIGHT + 'Average Pace: None')

    # DAILY MILE AVERAGE
    try:
        print(Fore.MAGENTA + Style.BRIGHT + 'Daily Mile Average: ' + str(round(total_distance_float / len(total_days_tuple),2)))
    except:
        print(Fore.MAGENTA + Style.BRIGHT + 'Daily Mile Average: None')

    # MILES PER BIKE
    cursor.execute("SELECT Equipment, round(sum(Distance),2), Event FROM " + table_name + " WHERE Event = 'Bike' GROUP BY Equipment")
    total_shoes_tuple = cursor.fetchall()

    print(Fore.MAGENTA + Style.BRIGHT + '\nMiles per Bike:')
    for each in total_shoes_tuple:
        print(Fore.MAGENTA + Style.BRIGHT + str(each[0])+': '+str(each[1]))

    conn.commit()
    conn.close()
    
def build_dict():
    database = querry_data()   
    data_dict = {'distance':{}, 'elevation':{}, 'pace':{}, 'time':{}}
    
    for item in database:
        # ADD MONTH TO DISTANCE
        if item[1][5:7] not in data_dict['distance']:
            data_dict['distance'].update({item[1][5:7]:{}})
        # ADD EVENTS TO MONTHS
        if item[1][5:7] in data_dict['distance']:
            data_dict['distance'][item[1][5:7]].update({item[2]:[]})

        # ADD MONTH TO ELEVATION
        if item[1][5:7] not in data_dict['elevation']:
            data_dict['elevation'].update({item[1][5:7]:{}})
        # ADD EVENTS TO MONTHS
        if item[1][5:7] in data_dict['elevation']:
            data_dict['elevation'][item[1][5:7]].update({item[2]:[]})            

        # ADD MONTH TO PACE
        if item[1][5:7] not in data_dict['pace']:
            data_dict['pace'].update({item[1][5:7]:{}})
        # ADD EVENTS TO MONTHS
        if item[1][5:7] in data_dict['pace']:
            data_dict['pace'][item[1][5:7]].update({item[2]:[]})

        # ADD MONTH TO TIME
        if item[1][5:7] not in data_dict['time']:
            data_dict['time'].update({item[1][5:7]:{}})
        # ADD EVENTS TO MONTHS
        if item[1][5:7] in data_dict['time']:
            data_dict['time'][item[1][5:7]].update({item[2]:[]})
    
    for item in database:
        # ADD DISTANCES TO EVENTS
        if item[2] in data_dict['distance'][item[1][5:7]]:
            data_dict['distance'][item[1][5:7]][item[2]].append(item[3])

        # ADD ELEVATION TO EVENTS
        if item[2] in data_dict['elevation'][item[1][5:7]]:
            data_dict['elevation'][item[1][5:7]][item[2]].append(item[6])

        # ADD PACE TO EVENTS
        if item[2] in data_dict['pace'][item[1][5:7]]:
            data_dict['pace'][item[1][5:7]][item[2]].append(item[5])

        # ADD TIME TO EVENTS
        if item[2] in data_dict['time'][item[1][5:7]]:
            data_dict['time'][item[1][5:7]][item[2]].append(item[4])
      
    # GET AVERAGES FOR DISTANCE
    for month, event in data_dict['distance'].items():
        for key, value in event.items():
            event[key] = str(round(sum(value)/len(value),2))

    # GET AVERAGES FOR ELEVATION
    for month, event in data_dict['elevation'].items():
        for key, value in event.items():
            event[key] = str(round(sum(value)/len(value),2))

    # GET AVERAGES FOR PACE
    for month, event in data_dict['pace'].items():
        for key, value in event.items():
            event[key] = str(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*60 + int(f[1]), map(lambda f: f.split(':'), value)))/len(value))).split('.',1)[0][2:]
    
    # GET AVERAGES FOR TIME
    for month, event in data_dict['time'].items():
        for key, value in event.items():
            event[key] = str(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), value)))/len(value))).split('.',1)[0]
    
    return data_dict

def print_distance(data_dict): 
    print('\nAVERAGE DISTANCES ' + table_name[-4:])
    for month, event in data_dict['distance'].items():
        print('----',datetime.datetime.strptime(month,'%m').strftime('%B').upper(),'----')
        for key, value in sorted(event.items(), reverse=True):
            if key =='Run':
                print(c.run+key,'', c.run+'▓'*(int(float(value))), c.run+value)
            elif key =='Bike':
                print(c.bike+key, c.bike+'▓'*(int(float(value))), c.bike+value)
            elif key =='Hike':
                print(c.hike+key, c.hike+'▓'*(int(float(value))), c.hike+value)

def print_time(data_dict):
    print('\nAVERAGE TIMES ' + table_name[-4:])
    for month, event in data_dict['time'].items():
        print('----',datetime.datetime.strptime(month,'%m').strftime('%B').upper(),'----')
        for key, value in sorted(event.items(), reverse=True):
            if key =='Run':
                print(c.run+key,'', c.run+'▓'*int((int(value[0])*3600 + int(value[2:4])*60 + int(value[5:])) / 600), c.run+value)
            elif key =='Bike':
                print(c.bike+key, c.bike+'▓'*int((int(value[0])*3600 + int(value[2:4])*60 + int(value[5:])) / 600), c.bike+value)
            elif key =='Hike':
                print(c.hike+key, c.hike+'▓'*int((int(value[0])*3600 + int(value[2:4])*60 + int(value[5:])) / 600), c.hike+value)

def print_pace(data_dict): 
    print('\nAVERAGE PACE ' + table_name[-4:])
    for month, event in data_dict['pace'].items():
        print('----',datetime.datetime.strptime(month,'%m').strftime('%B').upper(),'----')
        for key, value in sorted(event.items(), reverse=True):
            if key =='Run':
                print(c.run+key,'', c.run+'▓'*int((int(value[0:2])*60 + int(value[3:])) / 60), c.run+value)
            elif key =='Bike':
                print(c.bike+key, c.bike+'▓'*int((int(value[0:2])*60 + int(value[3:])) / 60), c.bike+value)
            elif key =='Hike':
                print(c.hike+key, c.hike+'▓'*int((int(value[0:2])*60 + int(value[3:])) / 60), c.hike+value)

def print_elevation(data_dict):
    print('\nAVERAGE ELEVATION ' + table_name[-4:])
    for month, event in data_dict['elevation'].items():
        print('----',datetime.datetime.strptime(month,'%m').strftime('%B').upper(),'----')
        for key, value in sorted(event.items(), reverse=True):
            if key =='Run':
                print(c.run+key,'', c.run+'▓'*int(float(value)/100), c.run+value)
            elif key =='Bike':
                print(c.bike+key, c.bike+'▓'*int(float(value)/100), c.bike+value)
            elif key =='Hike':
                print(c.hike+key, c.hike+'▓'*int(float(value)/100), c.hike+value)


# GET DISTINCT LIST OF EQUIPMENT FOR ADD_EQUIPMENT FUNTION
conn = sqlite3.connect('fitness.db')
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT Equipment FROM " + table_name + " WHERE Event = 'Run'")
shoes_list = list(cursor.fetchall())
cursor.execute("SELECT DISTINCT Equipment FROM " + table_name + " WHERE Event = 'Hike'")
boots_list = list(cursor.fetchall())
cursor.execute("SELECT DISTINCT Equipment FROM " + table_name + " WHERE Event = 'Bike'")
bike_list = list(cursor.fetchall())
# GET YEARS FROM TABLE NAMES
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name ASC")
table_list = list(cursor.fetchall())
conn.commit()
conn.close()


# NAVIGATION MENUS
def home_menu():
    while True:
        print(
            Fore.CYAN+Style.BRIGHT +'''
     +------------------------+
     |'''+Fore.WHITE+'''       HOME MENU        '''+Fore.CYAN+Style.BRIGHT+'''|
     +-----+------------------+
     |'''+Fore.WHITE+'''  1  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  ADD A RECORD    '''+Fore.CYAN+Style.BRIGHT+'''|
     |'''+Fore.WHITE+'''  2  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  EDIT A RECORD   '''+Fore.CYAN+Style.BRIGHT+'''|
     |'''+Fore.WHITE+'''  3  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  DELETE A RECORD '''+Fore.CYAN+Style.BRIGHT+'''| 
     |'''+Fore.WHITE+'''  4  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  VIEW DATA       '''+Fore.CYAN+Style.BRIGHT+'''|
     |'''+Fore.WHITE+'''  5  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  EXIT            '''+Fore.CYAN+Style.BRIGHT+'''|
     +-----+------------------+''')
        action = input('     Enter Selection: ')

        if action == '':
            print(Fore.RED + '\nSelection Not Found.')
            continue
        elif action.lower().startswith('add') or action == '1':
            print('\nADD A NEW RECORD')
            new_record()
        elif action.lower().startswith('edit') or action == '2':
            querry_data()
            print_data(list)
            print('\nEDIT A RECORD')
            select_old_record()
            if rowid.upper() == 'X':
                continue
            else:
                edit_record()
                update_record()
        elif action.lower().startswith('delete') or action == '3':
            querry_data()
            print_data(list)
            print('\nDELETE A RECORD')
            select_old_record()
            if rowid.upper() == 'X':
                continue
            else:
                delete_record()
        elif action.lower().startswith('view')or action == '4':
            break
        elif action.lower().startswith('exit')or action == '5':
            exit()
        else:
            print(Fore.RED + '\nSelection Not Found.')
            continue

home_menu()
while True:
    print(
        Fore.CYAN+Style.BRIGHT +'''
     +------------------------+
     |'''+Fore.WHITE+'''       DATA MENU        '''+Fore.CYAN+Style.BRIGHT+'''|
     +-----+------------------+ 
     |'''+Fore.WHITE+'''  1  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  GET TOTALS      '''+Fore.CYAN+Style.BRIGHT+'''|
     |'''+Fore.WHITE+'''  2  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  SHOW GRAPHS     '''+Fore.CYAN+Style.BRIGHT+'''|
     |'''+Fore.WHITE+'''  3  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  VIEW ALL        '''+Fore.CYAN+Style.BRIGHT+'''|
     |'''+Fore.WHITE+'''  4  '''+Fore.CYAN+Style.BRIGHT+'''|'''+Fore.WHITE+'''  MAIN MENU       '''+Fore.CYAN+Style.BRIGHT+'''|
     +-----+------------------+''')
    action = input('     Enter Selection: ')

    if action == '':
        print(Fore.RED + '\nSelection Not Found.')
        continue
    elif action.lower().startswith('get')or action == '1':
        print('\nGET TOTALS')
        for year in table_list:
            print(year[0][-4:])
        year = str(datetime.date.today().year)
        table_name = input('Default Year: '  + year + '\nOr enter Year: ')
        table_name = table_name or year
        table_name = 'fitness_'+table_name
        try:
            get_totals()
        except:
            print(Fore.RED + 'Table not found.')

    elif action.lower().startswith('show')or action == '2':
        print('\nSHOW GRAPHS')
        for year in table_list:
            print(year[0][-4:])
        year = str(datetime.date.today().year)
        table_name = input('Default Year: '  + year + '\nOr enter Year: ')
        table_name = table_name or year
        table_name = 'fitness_'+table_name
        try:
            querry_data()
        except:
            print(Fore.RED + 'Table not found.')
            continue
        while True:
            print('\nGRAPH OPTIONS FOR: '+table_name)
            print("1. Average Distances\n2. Average Times\n3. Average Pace\n4. Average Elevation\n5. EXIT")
            graph = input('Enter Selection: ')
            if graph == '':
                print(Fore.RED + '\nSelection Not Found.')
                continue
            elif graph == '1':
                print_distance(build_dict())
                break
            elif graph == '2':
                print_time(build_dict())
                break
            elif graph == '3':
                print_pace(build_dict())
                break
            elif graph == '4':
                print_elevation(build_dict())
                break
            elif graph == '5':
                break
            else:
                print(Fore.RED + '\nSelection Not Found.')
                continue

    elif action.lower().startswith('view')or action == '3':
        for year in table_list:
            print(year[0][-4:])
        year = str(datetime.date.today().year)
        table_name = input('Default Year: '  + year + '\nOr enter Year: ')
        table_name = table_name or year
        table_name = 'fitness_'+table_name
        try:
            querry_data()
            print_data(list)
        except:
            print(Fore.RED + 'Table not found.')

    elif action.lower().startswith('main')or action == '4':
        table_name = 'fitness_' + str(datetime.date.today().year)
        home_menu()
    else:
        print(Fore.RED + '\nSelection Not Found.')
        continue

home_menu()
