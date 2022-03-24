# ISS Position and Sighting Tracker
This folder contains a containerization script (`Dockerfile`), two Python scripts (`app.py` and `test_app.py`), and a script to build a container and to start the containerized Flask application (`Makefile`)

## Project Summary
The objective of this project was to build a containerized Flask application for querying and returning interesting information from ISS data sets. The data being used is positional data for the International Space Station (ISS) and includes position and velocity data at given times, as well as when the ISS can be seen over select cities.

## Description of Files
### app.py
This Python script is the Flask application for tracking ISS position and sighting. 
### test_app.py
This Python script runs different unit tests. These tests check the validity of the functions defined in the `app.py` script.
### Makefile
This file contains commands to build a container and to start the containerized Flask application.
### Dockerfile
This file contains commands that containerize the application and both data sets. It also sets a default command to launch the Flask application.

## Instructions to Download the Data
The data used throughout this project can be located [here](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq). Specifically, the 'Public Distribution File' and 'XMLsightingData_citiesINT03' will be used.

To download these files, enter the following commands in the terminal:

```bash
$ wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml 
$ wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT03.xml 
```

## Instructions to Build the Containerized App
You can use the included `Makefile` to build a container and to start the containerized Flask application. To do this, enter the following command in your terminal:

```bash
$ make all
docker build -t zbickham/iss_tracker_flask:latest .
Sending build context to Docker daemon  5.146MB
Step 1/9 : FROM python:3.9
```

## Instructions to Pull a Pre-Containerized Copy from Docker Hub
To pull a pre-containerized copy of the app from Docker Hub, enter the following command in your terminal:

```bash
$ docker pull zbickham/iss_tracker_flask:latest
latest: Pulling from zbickham/iss_tracker_flask
```

## Instructions to Interact With the Application
To interact with the containerized application, you can use HTTP curl. To do this, you will first need to load the XML data files to memory using the following command in the terminal:

```bash
$ curl -X POST localhost:5003/load_data
```

Now, you can begin interacting with the application. The following command will serve as the basis to navigating the application:

```bash
$ curl localhost:5003/
```

Using the above command as the basis, you can enter a number of commands after the `/` to access various information routes in the application. Listed below are all the possible commands that can be used to interact with the application along with their purpose.

- `/` - interaction information is outputted
- `/load_data` - loads the data from file into memory
- Routes to query positional and velocity data:
- `/epochs` - lists all epochs
- `/epochs/<epoch>` - lists all information about a specific epoch
- Routes to query ISS sighting data:
- `/countries` - lists all countries
- `/countries/<country>` - lists all information about a specific country
- `/countries/<country>/regions` - lists all regions found in a given country
- `/countries/<country>/regions/<region>` - lists all information about a specific region
- `/countries/<country>/regions/<region>/cities` - lists all cities found in a given region
- `/countries/<country>/regions/<region>/cities/<city>` - lists all information about a specific city

When you are done using the application, use the following command in the terminal to stop the container:

```bash
$ docker stop iss_flask
iss_flask
```

Lastly, you can enter the following command in the terminal to test the functions in `app.py`:
```bash
$ pytest test_app.py
================================================= test session starts ==================================================
platform linux -- Python 3.6.8, pytest-7.0.1, pluggy-1.0.0
rootdir: /home/zekeb/coe-332/iss-tracker
collected 3 items

test_app.py ...                                                                                                  [100%]

================================================== 3 passed in 0.30s ===================================================
```


## How to Interpret the Results
By using the application, you can discover interesting data about ISS positions and sightings. If you use one of the above commands that does not specify a location, the application will return a list of all of the information for that type (epochs, countries, regions, or cities). However, if you specify a location that is found in the data, the application will return specific information for that epoch or location. When querying positional and velocity data with the application, data will be returned as x, y, and z coordinates for position (in km) and x_dot, y_dot, and z_dot coordinates for velocity (in km/s). When querying the ISS sighting data, information suh as region, city, spacecraft, sighting date, duration in minutes, and max elevation will be returned.
