from ctypes import c_int, c_void_p

from django.apps import AppConfig


def force_traditional_gis_order():
    """
    Since GDAL 3, EPSG:4326 follows the authority axis order (lat, lng), so
    OGR serializes points as [lat, lng] in GeoJSON. Django >= 3.1 forces the
    traditional (lng, lat) order on every SpatialReference: backport the same
    fix for Django 2.2. Remove this once Django is upgraded to >= 3.1
    """

    from django.contrib.gis.gdal import SpatialReference
    from django.contrib.gis.gdal.libgdal import GDAL_VERSION, lgdal

    if GDAL_VERSION < (3, 0) or getattr(
            SpatialReference, "_traditional_gis_order", False):
        return

    set_axis_strategy = lgdal.OSRSetAxisMappingStrategy
    set_axis_strategy.argtypes = [c_void_p, c_int]
    set_axis_strategy.restype = None

    # OAMS_TRADITIONAL_GIS_ORDER
    traditional_gis_order = 0

    original_init = SpatialReference.__init__

    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        set_axis_strategy(self.ptr, traditional_gis_order)

    SpatialReference.__init__ = __init__
    SpatialReference._traditional_gis_order = True


class BackendConfig(AppConfig):
    name = 'backend'

    def ready(self):
        force_traditional_gis_order()
