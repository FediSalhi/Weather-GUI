# Weather-GUI

Weather GUI provides updated weather information for Los Angles, Denver, and New York cities gathered from the National Oceanic and Atmospheric Administration (NOAA) website. It also provides updated weather information for London, Paris, Mumbai, and Beijing according to the openweathermap.com website.

### Prerequisites

The Weather GUI is based on Tkinter, a Python  built-in module. To run the main.py script, you only need to install Pillow module using:
```
pip install Pillow
```
### Running 

The project consists of a main script "main.py" and a parameters script "parameters.py". 
* main.py: contains the main Tkinter window with its widgets (Buttons, Labels, Entries...) and some other functions.
* paramters.py : contains the main GUI parameters of the  such as size, title...

Running the main script will launch the GUI as shown below:

![NOAA](https://user-images.githubusercontent.com/45536639/89029764-c6314080-d337-11ea-99a6-fc9fd666b3ac.JPG)

Select a state station:
- KLAX: Los Angles
- KDEN: Denver
- KNYC: New York City

Click on the "Update Weather" button to get the updated weather information for the chosen sation

To get weather information of Paris, London, Mumbai, and Beijing, select the "Open Weather Map" tab and choose a city:

![Openmap](https://user-images.githubusercontent.com/45536639/89029819-e4973c00-d337-11ea-99e9-662978d1619e.JPG)

![Openmap_2](https://user-images.githubusercontent.com/45536639/89029836-e95bf000-d337-11ea-91a4-e68ab50a8554.JPG)

## Authors

* **Fedi Salhi** - *Initial work* - [FediSalhi](https://github.com/FediSalhi)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for detail
