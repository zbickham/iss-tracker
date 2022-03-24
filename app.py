from flask import Flask, request
import xmltodict
import json
import logging
import socket

app = Flask(__name__)

positional_data = {}
sighting_data = {}

@app.route('/load_data', methods=['POST'])
def load_data():
    """
    Loads two data files that contain information about the ISS position and sightings.
    
    Args:
        None
    
    Returns: 
        A string that tells the user the data has been loaded.
    """    
    
    global positional_data
    global sighting_data
    
    with open('ISS.OEM_J2K_EPH.xml', 'r') as f:
        positional_data = xmltodict.parse(f.read())

    with open('XMLsightingData_citiesINT03.xml', 'r') as f:
        sighting_data = xmltodict.parse(f.read())

    return f'Data has been loaded from the files.\n'
    
@app.route('/', methods=['GET'])
def help():
    """
    Provides information on how to interact with the application.
    
    Args:
        None
    
    Returns:
        A string that describes how to interact with the application. 
    """
    
    logging.info("How to interact with the application.")
    
    description = "ISS Tracker\n"
    description += "/                                                                  (GET) interaction information is outputted\n"
    description += "/load_data                                                         (POST) loads the data from file into memory\n"
    description += "Routes to query positional and velocity data:\n\n"
    description += "/epochs                                                            (GET) lists all epochs\n"
    description += "/epochs/<epoch>                                                    (GET) lists all information about a specific epoch\n"
    description += "Routes to query ISS sighting data\n\n"
    description += "/countries                                                         (GET) lists all countries\n"
    description += "/countries/<country>                                               (GET) lists all information about a specific country\n"
    description += "/countries/<country>/regions                                       (GET) lists all regions found in a given country\n"
    description += "/countries/<country>/regions/<region>                              (GET) lists all information about a specific region\n"
    description += "/countries/<country>/regions/<region>/cities                       (GET) lists all cities found in a given region\n"
    description += "/countries/<country>/regions/<region>/cities/<city>                (GET) lists all information about a specific city\n"
    return description
    
@app.route('/epochs', methods=['GET'])
def get_epochs():
    """
    Provides a list of all of the epochs in the positional data.
    
    Args:
        None
    
    Returns:
        A string that lists all of the epochs found in the positional data.
    """

    logging.info("Querying route to get all epochs...")

    epoch = ""
    for i in range(len(positional_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        epoch += positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH'] + '\n'
    return epoch
    
@app.route('/epochs/<epoch>', methods=['GET'])
def epoch_data(epoch: str):
    """
    Provides all of the information about a specific epoch in the positional data.
    
    Args:
        epoch: A string that represents the epoch value.
    
    Returns:
        A dictionary with position and velocity data for the specific epoch.
    """

    logging.info(f'Querying route to get information about epoch {epoch}')

    num_epoch = 0
    for i in range(len(positional_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        if epoch == positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH']:
            num_epoch = i
            break
    position_velocity_data = ['X', 'Y', 'Z', 'X_DOT', 'Y_DOT', 'Z_DOT']
    epoch_dict = {}
    for numbers in position_velocity_data:
        epoch_dict[numbers] = positional_data['ndm']['oem']['body']['segment']['data']['stateVector'][num_epoch][numbers]
    return epoch_dict
    
@app.route('/countries', methods=['GET'])
def get_countries():
    """
    Provides a list of all of the countries in the sighting data.
    
    Args:
        None
    
    Returns:
        A string that lists all of the countries found in the sighting data.
    """

    logging.info("Querying route to get all countries...")
    
    countries = {}
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        individual_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if individual_country in countries:
            countries[individual_country] += 1
        else:
            countries[individual_country] = 1
    return countries
    
@app.route('/countries/<country>', methods=['GET'])
def country_data(country: str):
    """
    Provides all of the information about a specific country in the sighting data.
    
    Args:
        country: A string that represents the name of a specific country.
    
    Returns:
        A dictionary with sighting data for the specific country.
    """

    logging.info(f'Querying route to get information about {country}')

    list_of_dicts = []
    list_of_country_data = ['region','city','spacecraft','sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time','utc_date']
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        individual_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == individual_country:
            country_dict = {}
            for j in list_of_country_data:
                country_dict[j] = sighting_data['visible_passes']['visible_pass'][i][j]
            list_of_dicts.append(country_dict)
    return (json.dumps(list_of_dicts, indent=2) + '\n')
    
@app.route('/countries/<country>/regions', methods=['GET'])
def get_regions(country: str):
    """
    Provides a list of all of the regions in a specific country in the sighting data.
    
    Args:
        country: A string that represents the name of a specific country.
   
    Returns:
        A string that lists all of the regions in a specific country found in the sighting data.
    """

    logging.info(f'Querying route to get all regions in {country}')

    regions = {}
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        individual_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == individual_country:
            individual_region = sighting_data['visible_passes']['visible_pass'][i]['region']
            if individual_region in regions:
                regions[individual_region] += 1
            else:
                regions[individual_region] = 1
    return regions

@app.route('/countries/<country>/regions/<region>', methods=['GET'])
def region_data(country: str, region: str) -> str:
    """
    Provides all of the information about a specific region in the sighting data.
    
    Args:
        country: A string that represents the name of a specific country.
        region: A string that represents the name of a specific region.
   
   Returns:
        A dictionary with sighting data for the specific region.
    """

    logging.info(f'Querying route to get information about {region}')

    list_of_dicts = []
    list_of_region_data = ['region','city','spacecraft','sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time','utc_date']
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        individual_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == individual_country:
            individual_region = sighting_data['visible_passes']['visible_pass'][i]['region']
            if region == individual_region:
                region_dict = {}
                for j in list_of_region_data:
                    region_dict[j] = sighting_data['visible_passes']['visible_pass'][i][j]
                list_of_dicts.append(region_dict)
    return (json.dumps(list_of_dicts, indent=2) + '\n')
    
@app.route('/countries/<country>/regions/<region>/cities', methods = ['GET'])
def get_cities(country: str, region: str):
    """
    Provides a list of all of the cities in a specific region in the sighting data.
    
    Args:
        country: A string that represents the name of a specific country.
        region: region: A string that represents the name of a specific region.
    
    Returns:
        A string that lists all of the cities in a specific region found in the sighting data.
    """

    logging.info(f'Querying route to get all cities in {region}')

    cities = {}
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        individual_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == individual_country:
            individual_region = sighting_data['visible_passes']['visible_pass'][i]['region']
            if region == individual_region:
                individual_city = sighting_data['visible_passes']['visible_pass'][i]['city']
                if individual_city in cities:
                    cities[individual_city] += 1
                else:
                    cities[individual_city] = 1
    return cities

@app.route('/countries/<country>/regions/<region>/cities/<city>', methods = ['GET'])
def city_data(country: str, region: str, city: str):
    """
    Provides all of the information about a specific city in the sighting data.
    
    Args:
        country: A string that represents the name of a specific country.
        region: A string that represents the name of a specific region.
        city: A string that represents the name of a specific city.
    
    Returns:
        A dictionary with sighting data for the specific city.
    """

    logging.info(f'Querying route to get information about {city}')

    list_of_dicts = []
    list_of_city_data = ['region','city','spacecraft','sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time','utc_date']
    for i in range(len(sighting_data['visible_passes']['visible_pass'])):
        individual_country = sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == individual_country:
            individual_region = sighting_data['visible_passes']['visible_pass'][i]['region']
            if region == individual_region:
                individual_city = sighting_data['visible_passes']['visible_pass'][i]['city']
                if city == individual_city:
                    city_dict = {}
                    for j in list_of_city_data:
                        city_dict[j] = sighting_data['visible_passes']['visible_pass'][i][j]
                    list_of_dicts.append(city_dict)
    return (json.dumps(list_of_dicts, indent=2) + '\n')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
