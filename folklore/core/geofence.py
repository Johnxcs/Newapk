"""Geofence enter/exit detection."""

from folklore.core.geo_utils import haversine_m


class GeofenceManager:
    """Fires callbacks when the user enters or leaves a site's radius."""

    def __init__(self, sites, on_enter, on_exit=None):
        self.sites = sites
        self.on_enter = on_enter
        self.on_exit = on_exit
        self.inside = set()

    def update(self, lat, lon):
        for site in self.sites:
            dist = haversine_m(lat, lon, site.lat, site.lon)
            if dist <= site.radius_m and site.name not in self.inside:
                self.inside.add(site.name)
                self.on_enter(site, dist)
            elif dist > site.radius_m and site.name in self.inside:
                self.inside.discard(site.name)
                if self.on_exit:
                    self.on_exit(site)
