import pytest

from nextgisweb.feature_layer import IWritableFeatureLayer, GEOM_TYPE, FIELD_TYPE

from nextgisweb.wfsserver.nextgis_to_fs import NextgiswebDatasource as DS


class MockFieldDef(object):

    def __init__(self, keyname):
        self.keyname = keyname

class MockVectorLayer():
    def __init__(self, geom_type=None):
        self.srs_id = 'test_srs_id'
        self.geom_col = 'test_geom_col'
        self.fields = [MockFieldDef('test_field1'), MockFieldDef('test_field2')]
        
        if geom_type is None:
            self.geometry_type = GEOM_TYPE.POINT
        else:
            self.geometry_type = geom_type
        
    def feature_query(self):
        return 'QUERY'
        
        

         


class TestDS:
    mock_layer = MockVectorLayer()
    ds = DS('test', layer=mock_layer, title='test_title',
            maxfeatures=120)
    
    def test_ds_init(self):      
        assert self.ds.title == 'test_title'
        assert self.ds.query is None
        assert self.ds.maxfeatures == 120
        
        with pytest.raises(BaseException):
            ds = DS('test', layer=mock_layer, title='test', maxfeatures="120st")
        with pytest.raises(BaseException):
            ds = DS('test', layer=mock_layer, title='test', maxfeatures="-2")
            

    def test_srid_out(self):
        assert self.ds.srid_out is not None
        
        
    def test_default_maxfeatures(self):
        # Test the result is actual maxFeatures or None
        ds = DS('test', layer=self.mock_layer, title='test', maxfeatures="12")
        assert ds.default_maxfeatures == 12
        ds = DS('test', layer=self.mock_layer, title='test')
        assert ds.default_maxfeatures is None
        

    def test_geometry_type(self):
        for gtype in [GEOM_TYPE.POINT, GEOM_TYPE.LINESTRING, GEOM_TYPE.POLYGON, GEOM_TYPE.MULTIPOINT, GEOM_TYPE.MULTILINESTRING, GEOM_TYPE.MULTIPOLYGON]:
            mock_layer = MockVectorLayer(geom_type=gtype)
            ds = DS('test', layer=mock_layer, title='test_title')
            
            result_type = ds.geometry_type
            assert result_type in ['Point', 'Line', 'Polygon', 'MultiPoint', 'MultiLine', 'MultiPolygon']
        
        with pytest.raises(NotImplementedError):
            mock_layer = MockVectorLayer(geom_type='Point')
            ds = DS('test', layer=mock_layer, title='test_title')
            result_type = ds.geometry_type
        

    def test_geom_col(self):
        # Test the result is string and is not None
        assert self.ds.geom_col is not None
        assert self.ds.geom_col != ''
        

    def test_setup_query(self):
        self.ds._setup_query()
        assert self.ds.query is not None
        

    def test_set_attribute_cols(self):
        mock_layer = MockVectorLayer()
        ds = DS('test', layer=mock_layer, title='test_title')
        
        assert ds.attribute_cols is None
        ds.set_attribute_cols()
        assert len(ds.attribute_cols) > 0
        
        for c in ds.attribute_cols:
            assert c in ['test_field1', 'test_field2']
        
    def test_get_attribute_cols(self):
        mock_layer = MockVectorLayer()
        ds = DS('test', layer=mock_layer, title='test_title')
        
        cols = ds.get_attribute_cols()
        for c in cols:
            assert c in ['test_field1', 'test_field2']

    def test_select(self):
        # TODO
        
        # Test if query is correct (result = self.query())
        # Test query results
        assert False
    
