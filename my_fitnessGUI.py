from tkinter import *
from tkinter import ttk, messagebox
import datetime, re, sqlite3, pickle
from pprint import pprint
# frames: #119DA4
# BLACK: #040404
# BACKGROUND: #119DA4
# Labels: #13505B
# Buttons: #0C7489
class Database:
    ''' constructor: Needs Database Name and Table Name,
        querry: Uses self,
        get_tables staticmethod: Gets a list of available tables
        instert: Needs all data fields,
        update: Needs all data filds and the rowid
        delete: Needs the rowid,
        destructor: closes connection'''
    def __init__(self, database, table_name):
        
        self.database = database
        self.table_name = table_name

        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS """ + self.table_name + """ (
                    Date real,
                    Event real,
                    Distance real,
                    Time real,
                    Pace real,
                    Elevation integer,
                    Equipment text
                    )""")
        self.conn.commit()

    def querry(self):
        self.cursor.execute('SELECT rowid, * FROM ' + self.table_name + ' ORDER BY rowid DESC')
        database = self.cursor.fetchall()
        return database

    @staticmethod
    def get_tables(database):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name DESC")
        table_list = cursor.fetchall()
        return table_list

    def insert(self, date, event, distance, time, pace, elevation, equipment):
        self.cursor.execute("INSERT INTO " + self.table_name + " VALUES (?,?,?,?,?,?,?)",
                (date, event, distance, time, pace, elevation, equipment))
        self.conn.commit()

    def update(self, rowid, date, event, distance, time, pace, elevation, equipment):
        self.cursor.execute("UPDATE "+ self.table_name + " SET Date=?, Event=?, Distance=?, Time=?, Pace=?, Elevation=?, Equipment=? WHERE rowid = ?",
                                (date, event, distance, time, pace, elevation, equipment, rowid))
        self.conn.commit()

    def delete(self, rowid):
        self.cursor.execute("DELETE FROM "+ self.table_name + " WHERE rowid=?",
                            (rowid,))
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()

def build_dict(database):
    #database = Database('fitness.db',table_name).querry()
    year_dict = {}
    month_dict = {}

    def convert_to_hours(delta):
        total_seconds = delta.total_seconds()
        hours = str(int(total_seconds // 3600)).zfill(2)
        minutes = str(int((total_seconds % 3600) // 60)).zfill(2)
        seconds = str(int(total_seconds % 60)).zfill(2)
        delta = f"{hours}:{minutes}:{seconds}"
        return delta

    "Level 1 Dictionaries"
    for item in database:
        #ADD EVENT DICTS TO YEAR_DICT
        if item[2] not in year_dict:
            year_dict.update({item[2]:{'days':[], 'distance':[], 'time':[], 'pace':[], 'elevation':[], 'equipment':{}}})
        # ADD MONTH DICTS TO MONT_DICT  
        if item[1][5:7] not in month_dict:
            month_dict.update({item[1][5:7]:{'distance':{}, 'time':{}, 'pace':{}, 'elevation':{}}})

    "Level 2 Dictionaries"
    for item in database:
        # ADD EVENT DICTS TO MONT_DICT
        if item[2] not in month_dict[item[1][5:7]]['distance']:
            month_dict[item[1][5:7]]['distance'].update({item[2]:[]})
        if item[2] not in month_dict[item[1][5:7]]['time']:
            month_dict[item[1][5:7]]['time'].update({item[2]:[]})
        if item[2] not in month_dict[item[1][5:7]]['pace']:
            month_dict[item[1][5:7]]['pace'].update({item[2]:[]})
        if item[2] not in month_dict[item[1][5:7]]['elevation']:
            month_dict[item[1][5:7]]['elevation'].update({item[2]:[]})
        #ADD EQUIPMENT TO YEAR DICT
        if item[2] in year_dict:
            year_dict[item[2]]['equipment'].update({item[7]:[]})

    "Populate the Data"
    for item in database:
        # ADD DATA TO YEAR DICT
        if item[2] in year_dict:
            if item[1] not in year_dict[item[2]]['days']:
                year_dict[item[2]]['days'].append(item[1])                                          
            year_dict[item[2]]['distance'].append(item[3])
            year_dict[item[2]]['time'].append(item[4])
            year_dict[item[2]]['pace'].append(item[5])
            year_dict[item[2]]['elevation'].append(item[6])
            year_dict[item[2]]['equipment'][item[7]].append(item[3])
        # ADD DATA TO MONTH DICT
        if item[1][5:7] in month_dict:
            month_dict[item[1][5:7]]['distance'][item[2]].append(item[3])
            month_dict[item[1][5:7]]['time'][item[2]].append(item[4])
            month_dict[item[1][5:7]]['pace'][item[2]].append(item[5])
            month_dict[item[1][5:7]]['elevation'][item[2]].append(item[6])

    "Process the Data"
    # PROCESS YEAR_DICT
    for event, category in year_dict.items():
        if 'days' in category:
            category['days'] = len(category['days'])
        if 'distance' in category:
            category['distance'] = round(sum(category['distance']),2)
        if 'elevation' in category:
            category['elevation'] = round(sum(category['elevation']),2)
        if 'pace' in category:
            category['pace'] = str(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*60 + int(f[1]), map(lambda f: f.split(':'), category['pace'])))/len(category['pace']))).split('.',1)[0][2:]
        if 'time' in category:
            category['time'] = convert_to_hours(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), category['time'])))))
        for key, value in category['equipment'].items():
            category['equipment'][key] = round(sum(value),2)
    # PROCESS MONTH_DICT
    for month, category in month_dict.items():
        for key, value in category['distance'].items():
            category['distance'][key] = round(sum(value),2)
        for key, value in category['elevation'].items():
            category['elevation'][key] = round(sum(value),2)
        for key, value in category['pace'].items():
            category['pace'][key] = str(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*60 + int(f[1]), map(lambda f: f.split(':'), value)))/len(value))).split('.',1)[0][2:]
        for key, value in category['time'].items():
            category['time'][key] = convert_to_hours(datetime.timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), value)))))   

    return month_dict, year_dict

def pt_window():
    day_of_year = str(datetime.datetime.now().timetuple().tm_yday)
    year_pt = pickle.load(open('year_pt.pkl','rb'))
    todays_pt = (year_pt[day_of_year])
    # Build a frame to act as the screen
    pt_screen = Frame(app, bg='#119DA4')
    pt_screen.pack(expand=TRUE, fill=BOTH)
    # Add a title frame
    title_frame = Frame(pt_screen, bg='#040404')
    title_frame.pack(padx=5, pady=5, fill=X)
    main_title = Label(title_frame, text='DAY: '+day_of_year, font=('veranda',14,'bold'), bg='#13505B', fg='white')
    main_title.pack(padx=5, pady=5, fill=X)

    pt_frame = Frame(pt_screen,bg='#040404')
    pt_frame.pack( padx=10, fill=X)

    pt_scroll = Scrollbar(pt_frame)
    pt_scroll.pack(side=RIGHT, pady=5, padx=(0, 5), fill=Y)
    pt_label = Text(pt_frame, yscrollcommand=pt_scroll.set, font=('veranda',14,'bold'), height=7, bg='#D7D9CE')
    pt_label.pack(side=LEFT, pady=5, padx=(5, 0))
    pt_label.insert(END, todays_pt)
    pt_label.configure(state='disabled')
    pt_scroll.config(command=pt_label.yview)
    
    button_frame = Frame(pt_screen, bg='#040404')
    button_frame.pack(padx=5, pady=5)
    back_button = Button(button_frame, text='BACK', font=('veranda',9), bg='#0C7489', fg='white',activebackground='#13505B', command=lambda:[main_window(),pt_screen.pack_forget()])
    back_button.pack(padx=5, pady=5)

def data_window():
    table_list = Database.get_tables('fitness.db')
    def filter_the_listboxes(event):
        table_name='fitness_'+str(table_lb.get(table_lb.curselection()))
        connection = Database('fitness.db',table_name)
        database = connection.querry()
        month_dict, year_dict = build_dict(database)
        event_lb.delete(0, END)
        for event in sorted(year_dict,reverse=True):
            event_lb.insert(END, event)

        category_lb.delete(0, END)
        loop = 0
        while loop < 1:
            for month, category in month_dict.items():
                for key in category:
                    category_lb.insert(END,key.upper())
                    loop += 1

    def show_year_data():
        table_name='fitness_'+str(table_lb.get(table_lb.curselection()))
        connection = Database('fitness.db',table_name)
        database = connection.querry()
        month_dict, year_dict = build_dict(database)
        try:
            if str(event_lb.get(event_lb.curselection())) == 'Run':
                data_label.configure(state='normal',fg='Blue')
                data_label.delete(1.0, END)
                data_label.insert(END,'\nRUNNING TOTALS FOR: ' +str(table_name[-4:])+'\n')
                data_label.insert(END,'Days Ran: ' + str(year_dict['Run']['days'])+'\n')
                data_label.insert(END,'Miles: ' + str(year_dict['Run']['distance'])+'\n')
                data_label.insert(END,'Time: ' + str(year_dict['Run']['time'])+'\n')
                data_label.insert(END,'Elevation: ' + str(year_dict['Run']['elevation'])+'\n')
                data_label.insert(END,'Pace: ' + str(year_dict['Run']['pace'])+'\n')
                data_label.insert(END,'Daily Mile Average: ' + str(round(year_dict['Run']['distance'] / year_dict['Run']['days'],2))+'\n')
                data_label.insert(END,'\nMiles Per Shoe: \n')
                for key in year_dict['Run']['equipment']:
                    data_label.insert(END,key+': '+ str(year_dict['Run']['equipment'][key]) +'\n')
                data_label.configure(state='disabled')
                
            elif str(event_lb.get(event_lb.curselection())) == 'Hike':
                data_label.configure(state='normal',fg='Orange')
                data_label.delete(1.0, END)
                data_label.insert(END,'\nHIKING TOTALS FOR: ' +str(table_name[-4:])+'\n')
                data_label.insert(END,'Days Hiked: ' + str(year_dict['Hike']['days'])+'\n')
                data_label.insert(END,'Miles: ' + str(year_dict['Hike']['distance'])+'\n')
                data_label.insert(END,'Time: ' + str(year_dict['Hike']['time'])+'\n')
                data_label.insert(END,'Elevation: ' + str(year_dict['Hike']['elevation'])+'\n')
                data_label.insert(END,'Pace: ' + str(year_dict['Hike']['pace'])+'\n')
                data_label.insert(END,'Daily Mile Average: ' + str(round(year_dict['Hike']['distance'] / year_dict['Hike']['days'],2))+'\n')
                data_label.insert(END,'\nMiles Per Boot: \n')
                for key in year_dict['Hike']['equipment']:
                    data_label.insert(END,key+': '+ str(year_dict['Hike']['equipment'][key]) +'\n')
                data_label.configure(state='disabled')

            elif str(event_lb.get(event_lb.curselection())) == 'Bike':
                data_label.configure(state='normal',fg='Purple')
                data_label.delete(1.0, END)
                data_label.insert(END,'\nBIKING TOTALS FOR: ' +str(table_name[-4:])+'\n')
                data_label.insert(END,'Days Biked: ' + str(year_dict['Bike']['days'])+'\n')
                data_label.insert(END,'Miles: ' + str(year_dict['Bike']['distance'])+'\n')
                data_label.insert(END,'Time: ' + str(year_dict['Bike']['time'])+'\n')
                data_label.insert(END,'Elevation: ' + str(year_dict['Bike']['elevation'])+'\n')
                data_label.insert(END,'Pace: ' + str(year_dict['Bike']['pace'])+'\n')
                data_label.insert(END,'Daily Mile Average: ' + str(round(year_dict['Bike']['distance'] / year_dict['Bike']['days'],2))+'\n')
                data_label.insert(END,'\nMiles Per Bike: \n')
                for key in year_dict['Bike']['equipment']:
                    data_label.insert(END,key+': '+ str(year_dict['Bike']['equipment'][key]) +'\n')
                data_label.configure(state='disabled')
        except KeyError:
        	pass

    def show_month_data():
        table_name='fitness_'+str(table_lb.get(table_lb.curselection()))
        connection = Database('fitness.db',table_name)
        database = connection.querry()
        month_dict, year_dict = build_dict(database)
        def add_colors():
            data_label.tag_config('run_tag', foreground='Blue')
            data_label.tag_config('hike_tag', foreground='Orange')
            data_label.tag_config('bike_tag', foreground='Purple')
            events=['Run','Hike','Bike']
            for word in events:
                pos_start = data_label.search(word, '1.0', END)
                while pos_start:
                    pos_end = str(float(pos_start) + 1.0)
                    if word == 'Run':
                        data_label.tag_add('run_tag', pos_start, pos_end)
                    elif word == 'Hike':
                        data_label.tag_add('hike_tag', pos_start, pos_end)
                    elif word == 'Bike':
                        data_label.tag_add('bike_tag', pos_start, pos_end)
                    pos_start = data_label.search(word, pos_end, END)

        try:
            if str(category_lb.get(category_lb.curselection())) == 'DISTANCE':
                data_label.configure(state='normal', fg = 'Black')
                data_label.delete(1.0, END)
                data_label.insert(END,'\nMONTHLY DISTANCES '+ table_name[-4:]+'\n')
                for month, category in sorted(month_dict.items(), reverse=False):
                    data_label.insert(END, '----'+str(datetime.datetime.strptime(month,'%m').strftime('%B').upper())+'----\n')
                    for key, value in sorted(category['distance'].items(), reverse=True):
                        if key =='Run':
                            data_label.insert(END, key+':  '+ '▓'*(int(float(value / 10)))+' '+ str(value)+'\n')
                        else:
                            data_label.insert(END, key+': '+ '▓'*(int(float(value / 10)))+' '+ str(value)+'\n')

            elif str(category_lb.get(category_lb.curselection())) == 'TIME':
                data_label.configure(state='normal', fg = 'Black')
                data_label.delete(1.0, END)
                data_label.insert(END, '\nMONTHLY TIME '+ table_name[-4:]+'\n')
                for month, category in sorted(month_dict.items(), reverse=False):
                    data_label.insert(END, '----'+str(datetime.datetime.strptime(month,'%m').strftime('%B').upper())+'----\n')
                    for key, value in sorted(category['time'].items(), reverse=True):
                        if key =='Run':
                            data_label.insert(END, key+':  '+ '▓'*int((int(value[0:2])*3600 + int(value[3:5])*60 + int(value[6:])) / 6000)+' '+ str(value)+'\n')
                        else:
                            data_label.insert(END, key+': '+ '▓'*int((int(value[0:2])*3600 + int(value[3:5])*60 + int(value[6:])) / 6000)+' '+ str(value)+'\n')


            elif str(category_lb.get(category_lb.curselection())) == 'PACE':
                data_label.configure(state='normal',fg = 'Black')
                data_label.delete(1.0, END)
                data_label.insert(END, '\nMONTHLY PACE '+ table_name[-4:]+'\n')
                for month, category in sorted(month_dict.items(), reverse=False):
                    data_label.insert(END, '----'+str(datetime.datetime.strptime(month,'%m').strftime('%B').upper())+'----\n')
                    for key, value in sorted(category['pace'].items(), reverse=True):
                        if key =='Run':
                            data_label.insert(END, key+':  '+ '▓'*int((int(value[0:2])*60 + int(value[3:])) / 60)+' '+ str(value)+'\n')
                        else:
                            data_label.insert(END, key+': '+ '▓'*int((int(value[0:2])*60 + int(value[3:])) / 60)+' '+ str(value)+'\n')
                
            elif str(category_lb.get(category_lb.curselection())) == 'ELEVATION':
                data_label.configure(state='normal')
                data_label.delete(1.0, END)
                data_label.insert(END, '\nMONTHLY ELEVATION '+ table_name[-4:]+'\n')
                for month, category in sorted(month_dict.items(), reverse=False):
                    data_label.insert(END, '----'+str(datetime.datetime.strptime(month,'%m').strftime('%B').upper())+'----\n')
                    for key, value in sorted(category['elevation'].items(), reverse=True):
                        if key =='Run':
                            data_label.insert(END, key+':  '+ '▓'*int(float(value)/1000)+' '+ str(value)+'\n')
                        else:
                            data_label.insert(END, key+': '+ '▓'*int(float(value)/1000)+' '+ str(value)+'\n')
        except KeyError:
            pass
        add_colors()
   
    # Build a frame to act as the screen
    data_screen = Frame(app, bg='#119DA4')
    data_screen.pack(expand=TRUE, fill=BOTH)
    # Add a title frame
    title_frame = Frame(data_screen, bg='#040404')
    title_frame.pack(padx=5, pady=5, fill=X)
    main_title = Label(title_frame, text='VIEW DATA', font=('veranda',14,'bold'), bg='#13505B', fg='white')
    main_title.pack(padx=5, pady=5, fill=X)
    
    parameters_frame = Frame(data_screen, bg='#040404')
    parameters_frame.pack(side=LEFT, pady=5, expand=True, anchor=N)
    table_lb = Listbox(parameters_frame, font=('veranda',8), selectmode=SINGLE, height=3, justify='center', exportselection=False)
    table_lb.pack(pady=5, padx=5)
    table_lb.bind('<<ListboxSelect>>',filter_the_listboxes)

    for year in table_list:
        table_lb.insert(END, str(year)[-7:-3:])

    event_lb = Listbox(parameters_frame, font=('veranda',8), selectmode=SINGLE, height=3, justify='center', exportselection=False)
    event_lb.pack(padx=5)
    category_lb = Listbox(parameters_frame, font=('veranda',7), selectmode=SINGLE, height=4, justify='center', exportselection=False)
    category_lb.pack(pady=5, padx=5, fill=X)
    year_button = Button(parameters_frame, text='YEARLY DATA', font=('veranda',7), bg='#0C7489', fg='white',activebackground='#13505B', command=show_year_data)
    year_button.pack(padx=5, fill=X)
    month_button = Button(parameters_frame, text='MONTH GRAPHS', font=('veranda',7), bg='#0C7489', fg='white',activebackground='#13505B', command=show_month_data)
    month_button.pack(pady=5, padx=5, fill=X)
    close_button = Button(parameters_frame, text='BACK', font=('veranda',7), bg='#0C7489', fg='white',activebackground='#13505B', command=lambda:[main_window(),data_screen.pack_forget()])
    close_button.pack(pady=(0, 5), padx=5, fill=X)

    text_frame = Frame(data_screen, bg='#040404')
    text_frame.pack(side=LEFT,padx=(0,10), pady=5, anchor=N)
    text_scroll = Scrollbar(text_frame)
    text_scroll.pack(side=RIGHT, padx=(0, 5), pady=5, fill=Y)
    data_label = Text(text_frame, yscrollcommand=text_scroll.set, font=('veranda',6), bg='#D7D9CE', height=19, width=80)
    data_label.pack(side=LEFT, padx=(5, 0), pady=5)
    data_label.insert(END,'\n'*3 + '''
    WELCOME TO THE DATA SCREEN.\n
    USE THE FILTERS TO SEE YOUR DATA.\n
    FIRST SELECT A YEAR,
    TO SEE A BREAKDOWN FOR THE YEAR:
    SELECT AN EVENT AND PRESS THE YEARLY DATA BUTTON.\n
    TO SEE BAR GRAPHS FOR THE YEAR:
    SELECT A CATEGORY AND PRESD THE MONTH GRAPHS BUTTON.''')
    data_label.configure(state='disabled')
    text_scroll.config(command=data_label.yview)    
    
def entry_window():
    table_name = 'fitness_' + str(datetime.date.today().year)
    connection = Database('fitness.db',table_name)
    database = connection.querry()
    month_dict, year_dict = build_dict(database)        

    # Window FUNCTIONS
    def add_equipment(event):
        equipment_height=0
        equipment_lb.delete(0, END)
        try:
            for key in year_dict[event_var.get()]['equipment'].keys():
                equipment_lb.insert(END,key)
                equipment_height+=1
        except KeyError:
            equipment_lb.insert(END,'None Found.')
        if equipment_height > 3:
            equipment_lb.configure(height=3, justify=LEFT)
            equipment_scroll.pack(side=RIGHT, fill=Y)
            equipment_scroll.config(command=equipment_lb.yview)
        else:
            equipment_lb.configure(height=equipment_height, justify=LEFT)
    
    def calculate_pace(event):
        pace.delete(0, END)
        try:    
            time_var = time.get()
            time_format = "%H:%M:%S"
            time_var = datetime.datetime.strptime(time_var, time_format)
            time_var = datetime.timedelta(seconds=time_var.second, minutes=time_var.minute, hours=time_var.hour)
            calculated_pace = str(time_var/ float(distance.get()))
            calculated_pace = calculated_pace[2:7]
            pace.insert(0,calculated_pace)
        except ValueError:
            pace.insert(0,'00:00')

    def insert_equipment(event):
        equipment.delete(0, END)
        try:
            equipment.insert(0, equipment_lb.get(equipment_lb.curselection()))
        except:
            pass
        
    def clear_distance(event):
        distance.delete(0, END)
    def clear_elevation(event):
        elevation.delete(0, END)
 
    def save_record():
        check_counter=0
        date_regex = re.compile(r'^\d{4}\-\d{2}\-\d{2}$')
        dist_reg = re.compile(r'^\d+\.\d{2}$')
        time_reg = re.compile(r'^\d+\:\b[0-5][0-9]:\b[0-5][0-9]$')
        pace_reg = re.compile(r'^\b[0-5][0-9]:\b[0-5][0-9]$')
        elevation_reg = re.compile(r'^\d+$')
        if equipment.get() == '':
            warn = 'Select Equipment'
        else:
            check_counter += 1

        if elevation_reg.search(elevation.get()):
            check_counter += 1
        else:
            warn = 'Fix Elevation'

        if pace_reg.search(pace.get()):
            check_counter += 1
        else:
            warn = 'Fix Pace'

        if time_reg.search(time.get()):
            check_counter += 1
        else:
            warn = 'Fix Time 0:00:00'

        if dist_reg.search(distance.get()):
            check_counter += 1
        else:
            warn = 'Fix distance 0.00'

        if event_var.get() == "SELECT":
            warn = 'Select Event'
        else:
            check_counter += 1

        if date_regex.search(date.get()):
            check_counter += 1
        else:
            warn = 'Enter date'
                        
        if check_counter == 7:
            try:
                if form_mode == 'ADD':
                    connection.insert(date.get(), event_var.get(), distance.get(), time.get(), pace.get(), elevation.get(), equipment.get())
                    
                elif form_mode == 'EDIT':
                    connection.update(values[0], date.get(), event_var.get(), distance.get(), time.get(), pace.get(), elevation.get(), equipment.get())
                messagebox.showinfo('Saved',date.get()+'\n'+event_var.get())
                main_window()
                entry_screen.pack_forget()
            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            error_label.config(text=warn)
        
        
    # Build a frame to act as the screen
    entry_screen = Frame(app, bg='#119DA4')
    entry_screen.pack(expand=TRUE, fill=BOTH)
    # Add a title frame
    title_frame = Frame(entry_screen, bg='#040404')
    title_frame.pack(padx=5, pady=5, fill=X)
    main_title = Label(title_frame, text=form_mode+'\nRECORD', font=('veranda',14,'bold'), bg='#13505B', fg='white')
    main_title.pack(padx=5, pady=5, fill=X)

    entry_frame = Frame(entry_screen, bg='#040404')
    entry_frame.pack(padx=5, pady=(15, 5))

    line1 = Frame(entry_frame, bg='#13505B')
    line1.pack(padx=5, pady=(5, 0), fill=X)
    date_label = Label(line1, text='Date: ', font=('veranda',12), width=9, bg='#13505B', fg='white', justify=RIGHT)
    date_label.pack(side=LEFT, pady=(0, 5))
    date = Entry(line1, font=('veranda',12), width=15, justify=CENTER)
    date.pack(side=LEFT, pady=(0, 5))
    date.insert(0, str(datetime.date.today()))
    
    event_label = Label(line1, text='Event: ', font=('veranda',12), width=9,bg='#13505B', fg='white', justify=RIGHT)
    event_label.pack(side=LEFT, pady=(0, 5), padx=(10,0))
    event_options = ['SELECT','Run','Hike','Bike']
    event_var = StringVar()
    event_var.set(event_options[0])
    event = OptionMenu(line1, event_var, *event_options, command=add_equipment)
    event.config(font=('veranda',12))
    event.pack(side=LEFT,padx=5, pady=5)

    line2 = Frame(entry_frame, bg='#13505B')
    line2.pack(padx=5, fill=X)
    distance_label = Label(line2, text='Distance: ', font=('veranda',12), width=9, bg='#13505B', fg='white', justify=RIGHT)
    distance_label.pack(side=LEFT, pady=(0, 5))
    distance = Entry(line2, font=('veranda',12), width=15, justify=CENTER)
    distance.pack(side=LEFT, pady=(0, 5))
    distance.insert(0, 00.00)
    distance.bind("<ButtonRelease-1>", clear_distance)
    
    time_label = Label(line2, text='Time: ', font=('veranda',12), width=9, bg='#13505B', fg='white', justify=RIGHT)
    time_label.pack(side=LEFT, pady=(0, 5), padx=(10,0))
    time = Entry(line2, font=('veranda',12), width=15, justify=CENTER)
    time.pack(side=LEFT,padx=5, pady=(0, 5))
    time.insert(0, 'h:mm:ss')

    line3 = Frame(entry_frame, bg='#13505B')
    line3.pack(padx=5, fill=X)
    pace_label = Label(line3, text='Pace: ', font=('veranda',12), width=9, bg='#13505B', fg='white', justify=RIGHT)
    pace_label.pack(side=LEFT, pady=10)
    pace = Entry(line3, font=('veranda',12), width=15, justify=CENTER)
    pace.pack(side=LEFT, pady=10)
    pace.insert(0, '00:00')
    pace.bind("<ButtonRelease-1>", calculate_pace)
    elevation_label = Label(line3, text='Elevation: ', font=('veranda',12), width=9, bg='#13505B', fg='white', justify=RIGHT)
    elevation_label.pack(side=LEFT, pady=10, padx=(10,0))
    elevation = Entry(line3, font=('veranda',12), width=15, justify=CENTER)
    elevation.pack(side=LEFT,padx=5, pady=10)
    elevation.insert(0, 0)
    elevation.bind("<ButtonRelease-1>", clear_elevation)

    line4 = Frame(entry_frame, bg='#13505B')
    line4.pack(padx=5, fill=X)
    equipment_label = Label(line4, text='Equipment: ', font=('veranda',12), width=9, bg='#13505B', fg='white', justify=RIGHT)
    equipment_label.pack(side=LEFT, pady=(0, 5))
    scroll_frame = Frame(line4)
    scroll_frame.pack(side=LEFT)
    equipment_scroll = Scrollbar(scroll_frame)
    equipment_lb = Listbox(scroll_frame, font=('veranda',8), yscrollcommand=equipment_scroll.set, selectmode=SINGLE, width=22, height=1, justify=CENTER)
    equipment_lb.pack(side=LEFT)
    equipment_lb.insert(END,'SELECT AN EVENT')
    equipment_lb.bind('<<ListboxSelect>>', insert_equipment)
    error_label = Label(line4, text='', font=('veranda',14,'bold'), bg='#13505B', fg ='red', justify='center')
    error_label.pack(side=RIGHT, padx=10, pady=5)

    line5 = Frame(entry_frame, bg='#13505B')
    line5.pack(padx=5, pady=(0, 5), fill=X)
    buffer_label = Label(line5, text='Add New: ', font=('veranda',8), width=8, bg='#13505B', fg='white', justify=RIGHT)
    buffer_label.pack(side=LEFT, pady=5)
    equipment = Entry(line5, font=('veranda',12), width=20, justify=CENTER)
    equipment.pack(side=LEFT,padx=5, pady=5)


    cancel_button = Button(line5, text='CANCEL', font=('veranda',9), bg='#0C7489', fg='white', activebackground='#13505B', command=lambda:[main_window(),entry_screen.pack_forget()])
    cancel_button.pack(side=RIGHT, padx=10, pady=5)
    save_button = Button(line5, text='SAVE', font=('veranda',9), bg='#0C7489', fg='white', activebackground='#13505B', command=save_record)
    save_button.pack(side=RIGHT, padx=10, pady=5)

    if form_mode == 'ADD':
        pass                    
    elif form_mode == 'EDIT':
        date.delete(0, END)
        date.insert(0, values[1])
        event_var.set(values[2])
        distance.delete(0, END)
        distance.insert(0, values[3])
        time.delete(0, END)
        time.insert(0, values[4])
        pace.delete(0, END)
        pace.insert(0, values[5])
        elevation.delete(0, END)
        elevation.insert(0, values[6])
        equipment.insert(0, values[7])

def main_window():
    table_name = 'fitness_' + str(datetime.date.today().year)
    connection = Database('fitness.db',table_name)
    def populate_screen_data():
        database = connection.querry()
        month_dict, year_dict = build_dict(database)

        try:
            run_miles.set('Run Miles: '+str(year_dict['Run']['distance']))
        except KeyError:
            run_miles.set('Run Miles: 0')
        try:
            hike_miles.set('Hike Miles: '+str(year_dict['Hike']['distance']))
        except KeyError:
            hike_miles.set('Hike Miles: 0')
        try:
            bike_miles.set('Bike Miles: '+str(year_dict['Bike']['distance']))
        except KeyError:
            bike_miles.set('Bike Miles: 0')
        
        #TREEVIEW STUFF
        fitness_tree.delete(*fitness_tree.get_children())
        count = 0
        for record in database:
            if count % 2 == 0:
                if record[2] =='Run':
                    fitness_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('evenrow','run',))
                elif record[2] =='Hike':
                    fitness_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('evenrow','hike',))
                elif record[2] =='Bike':
                    fitness_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('evenrow','bike',))        
            else:
                if record[2] =='Run':
                    fitness_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('oddrow','run',))
                elif record[2] =='Hike':
                    fitness_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('oddrow','hike',))
                elif record[2] =='Bike':
                    fitness_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('oddrow','bike',))
            count += 1
        
    # Define all the button presses
    def new_record():
        global form_mode
        form_mode = 'ADD'
        entry_window()
        main_screen.pack_forget()
        
    def edit_record():
        try:
            values
            global form_mode
            form_mode = 'EDIT'
            entry_window()
            main_screen.pack_forget()
        except NameError:
            messagebox.showerror('Error', 'Select a Record')

    def delete_record():
        try:
            values
            response = messagebox.askyesno("Delete Entry", "Do you want to DELETE "+ values[2]+"?")
            if response == 1:
                connection.delete(values[0])
                populate_screen_data()
        except NameError:
            messagebox.showerror('Error', 'Select a Record')

    def view_data():
        data_window()
        main_screen.pack_forget()

    def show_pt():
        pt_window()
        main_screen.pack_forget()

    def select_record(event):
        global values
        selected = fitness_tree.focus()
        values = fitness_tree.item(selected, 'values')
    
    # Build a frame to act as the screen
    main_screen = Frame(app, bg='#119DA4')
    main_screen.pack(expand=TRUE, fill=BOTH)
    # Add a title frame
    title_frame = Frame(main_screen, bg='#040404')
    title_frame.pack(padx=5, pady=5, fill=X)
    main_title = Label(title_frame, text=table_name.upper(), font=('veranda',14,'bold'), bg='#13505B', fg='white')
    main_title.pack(padx=5, pady=(5, 0), fill=X)
    # data frame inside the title frame
    data_frame = Frame(title_frame)
    data_frame.pack(padx=5, pady=(0, 5), fill=X)
    run_miles=StringVar()
    run_label = Label(data_frame, textvariable=run_miles, font=('veranda',10), bg='#13505B', fg='white', justify=CENTER)
    run_label.pack(side=LEFT, expand=TRUE, fill=X)
    hike_miles=StringVar()
    hike_label = Label(data_frame, textvariable=hike_miles, font=('veranda',10), bg='#13505B', fg='white', justify=CENTER)
    hike_label.pack(side=LEFT, expand=TRUE, fill=X)
    bike_miles=StringVar()
    bike_label = Label(data_frame, textvariable=bike_miles, font=('veranda',10), bg='#13505B', fg='white', justify=CENTER)
    bike_label.pack(side=LEFT, expand=TRUE, fill=X)
    # button frame under title
    button_frame = Frame(main_screen, bg='#040404')
    button_frame.pack(padx=5)
    new_button = Button(button_frame, text='NEW', font=('veranda',9), bg='#0C7489', fg='white',activebackground='#13505B', command=new_record)
    new_button.pack(side=LEFT,padx=5, pady=5)
    edit_button = Button(button_frame, text='EDIT', font=('veranda',9), bg='#0C7489', fg='white',activebackground='#13505B', command=edit_record)
    edit_button.pack(side=LEFT,padx=5, pady=5)
    delete_button = Button(button_frame, text='DELETE', font=('veranda',9), bg='#0C7489', fg='white',activebackground='#13505B', command=delete_record)
    delete_button.pack(side=LEFT,padx=5, pady=5)
    data_button = Button(button_frame, text='DATA', font=('veranda',9), bg='#0C7489', fg='white',activebackground='#13505B', command=view_data)
    data_button.pack(side=LEFT,padx=5, pady=5)
    pt_button = Button(button_frame, text='DAILY PT', font=('veranda',9), bg='#0C7489', fg='white',activebackground='#13505B', command=show_pt)
    pt_button.pack(side=LEFT,padx=5, pady=5)
    # Add the treeiew
    fitness_tree_frame = Frame(main_screen, bg='#040404')
    fitness_tree_frame.pack(padx=5, pady=5, expand=True, fill=BOTH)
    fitness_tree = ttk.Treeview(fitness_tree_frame, selectmode='extended')
    fitness_tree.pack(padx=5, pady=5, expand=True, fill=BOTH)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview", background="#F8F8FF", foreground="black", rowheight=55, fieldbackground="#D3D3D3")
    style.map('Treeview',background=[('selected', "#347083")])

    fitness_tree['columns'] = ("rowid","Date", "Event", "Distance", "Time", "Pace", "Elevation", "Equipment")
    #Format Our Columns
    fitness_tree.column("#0", width=0, stretch=NO)
    fitness_tree.column("rowid", width=0, stretch=NO)
    fitness_tree.column("Date", anchor=CENTER, width=70)
    fitness_tree.column("Event", anchor=CENTER, width=45)
    fitness_tree.column("Distance", anchor=CENTER, width=65)
    fitness_tree.column("Time", anchor=CENTER, width=55)
    fitness_tree.column("Pace", anchor=CENTER, width=50)
    fitness_tree.column("Elevation", anchor=CENTER, width=70)
    fitness_tree.column("Equipment", anchor=W, width=110)
    #Create Headings
    fitness_tree.heading("#0",text="", anchor=W)
    fitness_tree.heading("rowid",text="", anchor=W)
    fitness_tree.heading("Date",text="Date", anchor=CENTER)
    fitness_tree.heading("Event",text="Event", anchor=CENTER)
    fitness_tree.heading("Distance",text="Distance", anchor=CENTER)
    fitness_tree.heading("Time",text="Time", anchor=CENTER)
    fitness_tree.heading("Pace",text="Pace", anchor=CENTER)
    fitness_tree.heading("Elevation",text="Elevation", anchor=CENTER)
    fitness_tree.heading("Equipment",text="Equipment", anchor=CENTER)
    #Create Striped Row Tags
    fitness_tree.tag_configure('run', foreground="blue")
    fitness_tree.tag_configure('hike', foreground="orange")
    fitness_tree.tag_configure('bike', foreground="purple")
    fitness_tree.tag_configure('oddrow', background="white")
    fitness_tree.tag_configure('evenrow', background="lightblue")
    #Bind the Treeview
    fitness_tree.bind("<ButtonRelease-1>", select_record)
    populate_screen_data()

if __name__=='__main__':
    app = Tk()
    #entry_window()
    main_window()
    app.mainloop()
