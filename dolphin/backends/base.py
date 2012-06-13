from dolphin.middleware import LocalStoreMiddleware
from dolphin.utils import calc_dist

class Backend(object):
    """A base backend"""
    def _get_request(self, **kwargs):
        if kwargs.get('request', None) is not None:
            return kwargs['request']
        return LocalStoreMiddleware.request()

    def _in_circle(self, ff, lat, lon):
        if isinstance(ff, (tuple, list)):
            f_lat = ff[0]
            f_lon = ff[1]
        else:
            f_lat = ff.center.latitude
            f_lon = ff.center.longitude
        dist = calc_dist(float(f_lat), float(f_lon), lat, lon)
        if dist <= ff.radius:
            return True
        return False

    def _once_per_req(self, name, key, func):
        d = LocalStoreMiddleware.local.setdefault(name, {})

        if key in d:
            return d[key]

        val = func()
        d[key] = val
        return val

    def is_active(self, key, *args, **kwargs):
        raise NotImplementedError("Must be overriden by backend")

    def delete(self, key, *args, **kwargs):
        raise NotImplementedError("Must be overriden by backend")

    def active_flags(self, key, *args, **kwargs):
        raise NotImplementedError("Must be overriden by backend")