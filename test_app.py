import pytest
from app import *
load_data()

def test_epoch_data():
    with pytest.raises(ValueError):
        epoch_data('test')

def test_country_data():
    with pytest.raises(TypeError):
        country_data('test')

def test_region_data():
    with pytest.raises(TypeError):
        region_data('test')

def test_city_data():
    with pytest.raises(TypeError):
        city_data('test')
        
def test_help():
    assert isinstance(help(), str) == True
