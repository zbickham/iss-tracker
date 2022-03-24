import pytest
from app import load_data, help, get_epochs, epoch_data, get_countries, country_data,\
    get_regions, region_data, get_cities, city_data

def test_region_data():
    with pytest.raises(TypeError):
        region_data('test')

def test_city_data():
    with pytest.raises(TypeError):
        city_data('test')
        
def test_help():
    assert isinstance(help(), str) == True
