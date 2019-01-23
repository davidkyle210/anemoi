from context import anemoi as an
import pandas as pd
import numpy as np
import pytest

def return_test_mast():
    index = pd.date_range(start='2000-01-01', periods=52596, freq='10min')
    sensors = ['T_78_AVG','T_4_AVG','SPD_79_NW_AVG','SPD_79_SW_AVG','SPD_76_NW_AVG','SPD_57_NW_AVG','SPD_57_SW_AVG','SPD_34_NW_AVG','SPD_34_SW_AVG','DIR_76_AVG','DIR_30_AVG']
    mast_data = pd.DataFrame(index=index, columns=sensors, data=np.random.randn(len(index), len(sensors)))
    mast_data.columns.name = 'sensor'
    mast = an.MetMast(name=1, data=mast_data, lat=45, lon=-90, primary_ano='SPD_79_NW_AVG', primary_vane='DIR_76_AVG')
    return mast

def test_is_mast():
    mast = return_test_mast()
    assert isinstance(mast, an.MetMast)

def test_mast_name():
    mast = return_test_mast()
    assert mast.name == 1

def test_mast_lat():
    mast = return_test_mast()
    assert mast.lat == 45

def test_mast_lon():
    mast = return_test_mast()
    assert mast.lon == -90

def test_mast_primary_ano():
    mast = return_test_mast()
    assert mast.primary_ano == 'SPD_79_NW_AVG'

def test_mast_primary_vane():
    mast = return_test_mast()
    assert mast.primary_vane == 'DIR_76_AVG'

def test_mast_data():
    mast = return_test_mast()
    assert isinstance(mast.data, pd.DataFrame)

def test_mast_data_index():
    mast = return_test_mast()
    index = pd.date_range(start='2000-01-01', periods=52596, freq='10min').values
    assert np.array_equal(mast.data.index.values, index)

def test_mast_data_columns():
    mast = return_test_mast()
    types = ['DIR','DIR','SPD','SPD','SPD','SPD','SPD','SPD','SPD','T','T']
    heights = [30.0, 76.0, 34.0, 34.0, 57.0, 57.0, 76.0, 79.0, 79.0, 4.0, 78.0]
    orients = ['-','-','NW','SW','NW','SW','NW','NW','SW','-','-']
    signals = ['AVG','AVG','AVG','AVG','AVG','AVG','AVG','AVG','AVG','AVG','AVG']
    sensors = ['DIR_30_AVG','DIR_76_AVG','SPD_34_NW_AVG','SPD_34_SW_AVG','SPD_57_NW_AVG','SPD_57_SW_AVG','SPD_76_NW_AVG','SPD_79_NW_AVG','SPD_79_SW_AVG','T_4_AVG','T_78_AVG']
    index = pd.MultiIndex.from_arrays([types,heights,orients,signals,sensors],names=['type','height','orient','signal','sensor'])
    pd.testing.assert_index_equal(mast.data.columns, index)

def test_mast_get_sensors():
    mast = return_test_mast()
    

##
# Test Sensor class
#

def test_repr():
    s = an.Sensor(type='dir', height=1.5, orient='NE', signal='max')
    s1 = an.Sensor(height=1000, tag='A')
    assert repr(s) == 'DIR_2_NE_MAX'
    assert repr(s1) == 'SPD_1000_AVG_A'
    
def test_asTup():
    s = an.Sensor(type='dir', height=1.5, orient='NE', signal='max')
    s1 = an.Sensor(height=1000, tag='A')
    assert s.asTup() == ('DIR', 1.5, 'NE', 'MAX', 'DIR_2_NE_MAX')
    assert s1.asTup() == ('SPD', 1000, '-', 'AVG', 'SPD_1000_AVG_A')

def test_sector():
    assert an.Sensor._sector(None) == '-'
    assert an.Sensor._sector(-1) == 'SM'
    assert an.Sensor._sector(0) == 'N'
    assert an.Sensor._sector(0.1) == 'N'
    assert an.Sensor._sector(359.9) == 'N'
    assert an.Sensor._sector(180+365.0/16 + 0.1) == 'SW'
    assert an.Sensor._sector(180+365.0/16 - 0.1) == 'S'

def test_checkOrientIsConsistentWithAngle():
    an.Sensor._checkOrientIsConsistentWithAngle('-', None)
    an.Sensor._checkOrientIsConsistentWithAngle('-', 359)
    an.Sensor._checkOrientIsConsistentWithAngle('NW', None)
    an.Sensor._checkOrientIsConsistentWithAngle('SW', 180+365.0/16 + 0.1)
    an.Sensor._checkOrientIsConsistentWithAngle('S', 180+365.0/16 - 0.1)
    with pytest.raises(Exception):
        an.Sensor._checkOrientIsConsistentWithAngle('S', 180+365.0/16 + 0.1)
    with pytest.raises(Exception):
        an.Sensor._checkOrientIsConsistentWithAngle('SW', 180+365.0/16 - 0.1)


def test_checkOrient():
    an.Sensor._checkOrient('-')
    an.Sensor._checkOrient('NE')
    with pytest.raises(Exception):
        an.Sensor._checkOrient('EN')

def test_check_orient_angle_behavior_in_constructor():
    x = an.Sensor()
    assert x.orient == '-'
    assert x.angle is None
    y = an.Sensor(angle=90)
    assert y.orient == 'E'
    assert y.angle == 90
    z = an.Sensor(orient='SW')
    assert z.orient == 'SW'
    assert z.angle is None
    with pytest.raises(Exception):
        an.Sensor(orient='SW', angle=90)
