###############################################
# imports
###############################################

from parameters import *
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
import urllib.request
import xml.etree.ElementTree as ET
from tkinter import scrolledtext
from html.parser import HTMLParser
import PIL.Image
import PIL.ImageTk
import json
from pprint import pprint
from datetime import datetime

###############################################
# functions
###############################################


def _quit():
    win.quit()
    win.destroy()
    exit()


def _set_win_size(height, width):
    win.minsize(height=height, width=width)


def _set_title(title):
    win.title(title)


im_var = None

###############################################
# procedural code
###############################################
win = tk.Tk()
# win.minsize(height=WIN_MIN_HEIGHT, width=WIN_MIN_WIDTH)
win.title(WIN_TITLE)

# ---------------------------------------------------------------------
# Menu Bar
menu_bar = Menu()
win.config(menu=menu_bar)

# File Menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Exit', command=_quit)
menu_bar.add_cascade(label='File', menu=file_menu)

# ----------------------------------------------------------------------
# Tab Control

tab_controller = ttk.Notebook(win)

tab_1 = ttk.Frame(tab_controller)
tab_controller.add(tab_1, text='NOAA')

tab_2 = ttk.Frame(tab_controller)
tab_controller.add(tab_2, text='Station IDs')

tab_3 = ttk.Frame(tab_controller)
tab_controller.add(tab_3, text='Images')

tab_4 = ttk.Frame(tab_controller)
tab_controller.add(tab_4, text='Open Weather Map')

tab_controller.pack(expand=1, fill='both')

########################################################################
# TAB 1
# -----------------------------------------------------------------------
# weather conditions label frame

weather_conditions_label_frame = ttk.LabelFrame(tab_1, text='Current Weather Conditions')
weather_conditions_label_frame.grid(column=0, row=1, padx=WEATHER_CONDITIONS_LABEL_FRAME_PAD_X,
                                    pady=WEATHER_CONDITIONS_LABEL_FRAME_PAD_Y)

# -----------------------------------------------------------------------
last_update_label = ttk.Label(weather_conditions_label_frame, text='Last Update')
last_update_label.grid(column=0, row=1, sticky='E')
last_update_entry_var = tk.StringVar()
last_update_entry = ttk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH, textvariable=last_update_entry_var,
                              state='readonly')
last_update_entry.grid(column=1, row=1, sticky='W')

# -----------------------------------------------------------------------
weather_label = ttk.Label(weather_conditions_label_frame, text='Weather')
weather_label.grid(column=0, row=2, sticky='E')
weather_var = tk.StringVar()
weather_entry = ttk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH, textvariable=weather_var, state='readonly')
weather_entry.grid(column=1, row=2, sticky='W')

# -----------------------------------------------------------------------
temperature_label = ttk.Label(weather_conditions_label_frame, text='Temperature')
temperature_label.grid(column=0, row=3, sticky='E')
temperature_entry_var = tk.StringVar()
temperature_entry = ttk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH, textvariable=temperature_entry_var,
                              state='readonly')
temperature_entry.grid(column=1, row=3, sticky='W')

# -----------------------------------------------------------------------
dewpoint_label = ttk.Label(weather_conditions_label_frame, text='Dew Point')
dewpoint_label.grid(column=0, row=4, sticky='E')
dew_point_var = tk.StringVar()
dewpoint_entry = tk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH, textvariable=dew_point_var,
                          state='readonly')
dewpoint_entry.grid(column=1, row=4, sticky='W')

# -----------------------------------------------------------------------
relative_humidity = tk.Label(weather_conditions_label_frame, text='Relative Humidity')
relative_humidity_var = tk.StringVar()
relative_humidity.grid(column=0, row=5, sticky='E')
relative_humidity_entry = ttk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH,
                                    textvariable=relative_humidity_var, state='readonly')
relative_humidity_entry.grid(column=1, row=5, sticky='W')

# -----------------------------------------------------------------------
wind = tk.Label(weather_conditions_label_frame, text='Wind')
wind_var = tk.StringVar()
wind.grid(column=0, row=6, sticky='E')
wind_entry = ttk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH, textvariable=wind_var, state='readonly')
wind_entry.grid(column=1, row=6, sticky='W')

# -----------------------------------------------------------------------
visibility = tk.Label(weather_conditions_label_frame, text='Visibility')
visibility_var = tk.StringVar()
visibility.grid(column=0, row=7, sticky='E')
visibility_entry = ttk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH, textvariable=visibility_var,
                             state='readonly')
visibility_entry.grid(column=1, row=7, sticky='W')

# -----------------------------------------------------------------------
msl_pressure = tk.Label(weather_conditions_label_frame, text='MSL Pressure')
msl_pressure_var = tk.StringVar()
msl_pressure.grid(column=0, row=8, sticky='E')
msl_pressure_entry = ttk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH, textvariable=msl_pressure_var,
                               state='readonly')
msl_pressure_entry.grid(column=1, row=8, sticky='W')

# -----------------------------------------------------------------------
altimeter = tk.Label(weather_conditions_label_frame, text='Altimeter')
altimeter_var = tk.StringVar()
altimeter.grid(column=0, row=9, sticky='E')
altimeter_entry = ttk.Entry(weather_conditions_label_frame, width=ENTRY_WIDTH, textvariable=altimeter_var,
                            state='readonly')
altimeter_entry.grid(column=1, row=9, sticky='W')

# -----------------------------------------------------------------------
# add space between widgets
for child in weather_conditions_label_frame.winfo_children():
    child.grid_configure(padx=WEATHER_CONDITIONS_CHILD_PAD_X, pady=WEATHER_CONDITIONS_CHILD_PAD_Y)

########################################################################
# weather cities label frame
weather_cities_label_frame = ttk.Labelframe(tab_1, text='Latest Observation For:')
weather_cities_label_frame.grid(column=0, row=0, sticky='W', padx=WEATHER_CITIES_LABEL_FRAME_PAD_X,
                                pady=WEATHER_CITIES_LABEL_FRAME_PAD_Y)

# -----------------------------------------------------------------------
weather_station_id_label = ttk.Label(weather_cities_label_frame, text='Station ID')
weather_station_id_label.grid(column=0, row=0, sticky='E')

station_id_var = tk.StringVar()
station_id_combo = ttk.Combobox(weather_cities_label_frame, width=COMBOBOX_WIDTH, textvariable=station_id_var,
                                state='readonly')
station_id_combo.grid(column=1, row=0, sticky='W')
station_id_combo['values'] = ('KLAX', 'KDEN', 'KNYC')  # Los Angles, Denver, New York City
station_id_combo.current(0)


# -----------------------------------------------------------------------
# call back function to update weather states

def _get_weather():
    station_id = station_id_combo.get()
    get_weather_data(station_id)
    update_weather_data()


# -----------------------------------------------------------------------
get_weather_button = ttk.Button(weather_cities_label_frame, text=' Update Weather', command=_get_weather)
get_weather_button.grid(column=2, row=0, sticky='W')

# -----------------------------------------------------------------------
for child in weather_cities_label_frame.winfo_children():
    child.grid_configure(padx=WEATHER_CITIES_CHILD_PAD_X, pady=WEATHER_CITIES_CHILD_PAD_Y)

########################################################################
# Getting weather information from NOAA website

weather_tags_dict = {
    'observation_time': '',
    'weather': '',
    'temperature_string': '',
    'dewpoint_string': '',
    'relative_humidity': '',
    'wind_kt': '',
    'visibility_mi': '',
    'pressure_string': '',
    'pressure_in': ''
}


def get_weather_data(station_id='KLAX'):
    url_general = 'http://www.weather.gov/xml/current_obs/{}.xml'
    url = url_general.format(station_id)
    request = urllib.request.urlopen(url)
    content = request.read().decode()
    print(content)

    xml_root = ET.fromstring(content)
    print('XML root: {}\n'.format(xml_root))

    for key in weather_tags_dict.keys():
        entry = xml_root.find(key)
        weather_tags_dict[key] = entry.text


def update_weather_data():
    last_update_entry_var.set(weather_tags_dict['observation_time'][16:])
    weather_var.set(weather_tags_dict['weather'])
    temperature_entry_var.set(weather_tags_dict['temperature_string'])
    dew_point_var.set(weather_tags_dict['dewpoint_string'])
    relative_humidity_var.set('% ' + weather_tags_dict['relative_humidity'])
    wind_var.set(weather_tags_dict['wind_kt'] + ' knot')
    visibility_var.set(weather_tags_dict['visibility_mi'] + ' mile')
    msl_pressure_var.set(weather_tags_dict['pressure_string'])
    altimeter_var.set(weather_tags_dict['pressure_in'] + 'in Hg')


########################################################################
# TAB 2
# -----------------------------------------------------------------------
# weather states label frame

weather_states_label_frame = ttk.Labelframe(tab_2, text='Weather Station IDs')
weather_states_label_frame.grid(column=0, row=0, padx=WEATHER_CITIES_LABEL_FRAME_PAD_X,
                                pady=WEATHER_STATES_LABEL_FRAME_PAD_Y)

# ----------------------------------------------------------------------
select_state_label = ttk.Label(weather_station_id_label, text='Select a State')
select_state_label.grid(column=0, row=0, sticky='E')

# ----------------------------------------------------------------------
state = tk.StringVar()
state_id_combo = ttk.Combobox(weather_states_label_frame, width=COMBOBOX_WIDTH, textvariable=state, state='readonly')
state_id_combo['values'] = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
                            'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
                            'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
                            'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
                            'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
                            )
state_id_combo.grid(column=1, row=0, sticky='W')
state_id_combo.current(0)

# ----------------------------------------------------------------------
# callback function


def _get_cities():
    state = state_id_combo.get()
    get_city_station_ids(state)


get_cities_button = ttk.Button(weather_states_label_frame, text='Get Cities', command=_get_cities)
get_weather_button.grid(column=2, row=0)

scrolled_text = scrolledtext.ScrolledText(weather_states_label_frame, width=SCROLLED_TEXT_WIDTH, height=SCROLLED_TEXT_HEIGHT, wrap=tk.WORD)
scrolled_text.grid(column=0, row=1, columnspan=3) # scrolled_text occupies 3 columns

# ----------------------------------------------------------------------
for child in weather_states_label_frame.winfo_children():
    child.grid_configure(padx=WEATHER_STATES_CHILD_PAD_X, pady=WEATHER_STATES_CHILD_PAD_Y)

# ----------------------------------------------------------------------
def get_city_station_ids(state='ca'):
    url_general = 'http://w1.weather.gov/xml/current_obs/seek.php?state={}&Find=Find'
    state = state.lower()
    url = url_general.format(state)
    request = urllib.request.urlopen(url)
    content = request.read().decode()
    print(content)
    parser = WeatherHTMLParser()
    parser.feed(content)
    scrolled_text.delete('1.0', tk.END)
    for idx in range(len(parser.stations)):
        city_station = parser.cities[idx] + '(' + parser.stations[idx] + ')'
        scrolled_text.insert(tk.INSERT, city_station+'\n')


class WeatherHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stations = []
        self.cities = []
        self.grab_data = False

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if "display.php?stid" in str(attr):
                cleaned_attr = str(attr)[-6:-2]
                self.stations.append(cleaned_attr)
                self.grab_data = True

    def handle_data(self, data):
        if self.grab_data:
            self.cities.append(data)
            self.grab_data = False


########################################################################
# TAB 3
# -----------------------------------------------------------------------
weather_images_frame = ttk.LabelFrame(tab_3, text='Weather Images')
weather_images_frame.grid(column=1, row=0, padx=WEATHER_IMAGES_LABEL_FRAME_PAD_X, pady=WEATHER_IMAGES_LABEL_FRAME_PAD_X)

# -----------------------------------------------------------------------
img = PIL.Image.open('few_clouds.png')
photo = PIL.ImageTk.PhotoImage(img)
ttk.Label(weather_images_frame, image=photo).grid(column=2, row=0)

img = PIL.Image.open('night_few_clouds.png')
photo_1 = PIL.ImageTk.PhotoImage(img)
ttk.Label(weather_images_frame, image=photo_1).grid(column=2, row=1)

img = PIL.Image.open('night_fair.png')
photo_2 = PIL.ImageTk.PhotoImage(img)
ttk.Label(weather_images_frame, image=photo_2).grid(column=2, row=2)

# -----------------------------------------------------------------------
for child in weather_images_frame.winfo_children():
    child.grid_configure(padx=WEATHER_IMAGES_CHILD_PAD_X, pady=WEATHER_IMAGES_CHILD_PAD_Y)

########################################################################
# TAB 4
# -----------------------------------------------------------------------
open_weather_cities_frame = ttk.Labelframe(tab_4, text='Latest Observation For')
open_weather_cities_frame.grid(column=0, row=0, padx=OPEN_WEATHER_CITIES_LABEL_FRAME_PAD_X, pady=OPEN_WEATHER_CITIES_LABEL_FRAME_PAD_Y, sticky='W')

open_location_var = tk.StringVar()
ttk.Label(open_weather_cities_frame, textvariable=open_location_var).grid(column=0, row=1)

ttk.Label(open_weather_cities_frame, text='City: ').grid(column=0, row=0)

open_city = tk.StringVar()
open_city_combo = ttk.Combobox(open_weather_cities_frame, width=OPEN_CITY_COMBO_WIDTH, textvariable=open_city, state='readonly')
open_city_combo['values'] = ('Los Angeles, US', 'London, UK', 'Paris, FR', 'Mumbai, IN', 'Beijing, CN')
open_city_combo.grid(column=1, row=0)
open_city_combo.current(0)


# -----------------------------------------------------------------------
# callback function
def _get_station_open():
    city = open_city_combo.get()
    get_open_weather_data(city)


get_open_weather_button = ttk.Button(open_weather_cities_frame, text='Get Weather', command=_get_station_open)
get_weather_button.grid(column=0, row=1)


im = ttk.Label(open_weather_cities_frame, image=im_var)
im.grid(column=1, row=1)

# -----------------------------------------------------------------------
for child in open_weather_cities_frame.winfo_children():
    child.grid_configure(padx=OPEN_WEATHER_CITIES_CHILD_PAD_X, pady=OPEN_WEATHER_CITIES_CHILD_PAD_Y)


# -----------------------------------------------------------------
open_weather_conditions_frame = ttk.Labelframe(tab_4, text='Current Weather Conditions:')
open_weather_conditions_frame.grid(column=0, row=1, padx=OPEN_WEATHER_CONDITIONS_FRAME_PAD_X, pady=OPEN_WEATHER_CONDITIONS_FRAME_PAD_Y)

# -----------------------------------------------------------------------
# add labels and entries

open_last_update_label = ttk.Label(open_weather_conditions_frame, text='Last Update')
open_last_update_label.grid(column=0, row=1, sticky='E')
open_last_update_entry_var = tk.StringVar()
open_last_update_entry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_last_update_entry_var,
                              state='readonly')
open_last_update_entry.grid(column=1, row=1, sticky='W')

# -----------------------------------------------------------------------
open_weather_label = ttk.Label(open_weather_conditions_frame, text='Weather')
open_weather_label.grid(column=0, row=2, sticky='E')
open_weather_var = tk.StringVar()
open_weather_entry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_weather_var, state='readonly')
open_weather_entry.grid(column=1, row=2, sticky='W')

# -----------------------------------------------------------------------
open_temperature_label = ttk.Label(open_weather_conditions_frame, text='Temperature')
open_temperature_label.grid(column=0, row=3, sticky='E')
open_temperature_entry_var = tk.StringVar()
open_temperature_entry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_temperature_entry_var,
                              state='readonly')
open_temperature_entry.grid(column=1, row=3, sticky='W')


# -----------------------------------------------------------------------
open_relative_humidity = tk.Label(open_weather_conditions_frame, text='Relative Humidity')
open_relative_humidity_var = tk.StringVar()
open_relative_humidity.grid(column=0, row=4, sticky='E')
open_relative_humidity_entry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH,
                                    textvariable=open_relative_humidity_var, state='readonly')
open_relative_humidity_entry.grid(column=1, row=4, sticky='W')

# -----------------------------------------------------------------------
open_wind = tk.Label(open_weather_conditions_frame, text='Wind')
open_wind_var = tk.StringVar()
open_wind.grid(column=0, row=5, sticky='E')
open_wind_entry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_wind_var, state='readonly')
open_wind_entry.grid(column=1, row=5, sticky='W')

# -----------------------------------------------------------------------
open_visibility = tk.Label(open_weather_conditions_frame, text='Visibility')
open_visibility_var = tk.StringVar()
open_visibility.grid(column=0, row=6, sticky='E')
open_visibility_entry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_visibility_var,
                             state='readonly')
open_visibility_entry.grid(column=1, row=6, sticky='W')

# -----------------------------------------------------------------------
open_msl_pressure = tk.Label(open_weather_conditions_frame, text='MSL Pressure')
open_msl_pressure_var = tk.StringVar()
open_msl_pressure.grid(column=0, row=7, sticky='E')
open_msl_pressure_entry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_msl_pressure_var,
                               state='readonly')
open_msl_pressure_entry.grid(column=1, row=7, sticky='W')


# -----------------------------------------------------------------------
for child in open_weather_conditions_frame.winfo_children():
    child.grid_configure(padx=OPEN_WEATHER_CONDITIONS_CHILD_PAD_X, pady=OPEN_WEATHER_CONDITIONS_CHILD_PAD_Y)


# -----------------------------------------------------------------------
# OpenWeatherMap data collection
def unix_to_datetime(unix_time):
    return datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


def get_open_weather_data(city='London,uk'):
    city = city.replace(' ', '%20')
    url_general = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    url = url_general.format(city, API_KEY)
    request = urllib.request.urlopen(url)
    content = request.read().decode()
    json_data = json.loads(content)
    pprint(json_data)

    lat_long = json_data['coord']
    lastupdate_unix = json_data['dt']
    city_id = json_data['id']
    humidity = json_data['main']['humidity']
    pressure = json_data['main']['pressure']
    temp_kelvin = json_data['main']['temp']
    city_name = json_data['name']
    city_country = json_data['sys']['country']
    sunrise_unix = json_data['sys']['sunrise']
    sunset_unix = json_data['sys']['sunset']
    try:
        visibility_meter = json_data['visibility']+'m'
    except:
        visibility_meter = 'N/A'
    owm_weather = json_data['weather'][0]['description']
    weather_icon = json_data['weather'][0]['icon']
    wind_deg = json_data['wind']['deg']
    wind_speed_meter_sec = json_data['wind']['speed']

    # updating entries
    open_last_update_entry_var.set(unix_to_datetime(lastupdate_unix))
    open_weather_var.set(owm_weather)
    open_temperature_entry_var.set(str(temp_kelvin)+' K')
    open_relative_humidity_var.set(str(humidity)+' %')
    open_wind_var.set(str(wind_speed_meter_sec)+' m/s')
    open_visibility_var.set(str(visibility_meter))
    open_msl_pressure_var.set(str(pressure)+' mb')

    url_icon = "http://openweathermap.org/img/w/{}.png".format(weather_icon)
    ico = urllib.request.urlopen(url_icon)
    open_im = PIL.Image.open(ico)
    open_photo = PIL.ImageTk.PhotoImage(open_im)

    global im_var
    im_var = open_photo
    im = ttk.Label(open_weather_cities_frame, image=im_var)
    im.grid(column=1, row=1)
    win.update()

###############################################
# endless loop
###############################################
win.mainloop()

