"""Location providers: simulated and real (plyer)."""

from kivy.clock import Clock

from folklore.config import START_POSITION, TICK_SECONDS, WALK_SPEED_MPS
from folklore.core.geo_utils import haversine_m


class SimulatedGPS:
    """Fake GPS that can teleport and walk toward a target."""

    def __init__(self, on_location, start=START_POSITION):
        self.on_location = on_location
        self.lat, self.lon = start
        self.target = None
        self._event = None

    def start(self):
        if self._event is None:
            self._event = Clock.schedule_interval(self._tick, TICK_SECONDS)
        self.on_location(self.lat, self.lon)

    def stop(self):
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def teleport(self, lat, lon):
        self.lat, self.lon = lat, lon
        self.target = None
        self.on_location(self.lat, self.lon)

    def walk_to(self, lat, lon):
        self.target = (lat, lon)

    def _tick(self, _dt):
        if not self.target:
            return
        tlat, tlon = self.target
        dist = haversine_m(self.lat, self.lon, tlat, tlon)
        step = WALK_SPEED_MPS * TICK_SECONDS
        if dist <= step:
            self.lat, self.lon = tlat, tlon
            self.target = None
        else:
            frac = step / dist
            self.lat += (tlat - self.lat) * frac
            self.lon += (tlon - self.lon) * frac
        self.on_location(self.lat, self.lon)


class RealGPS:
    """Device GPS through plyer (Android only)."""

    def __init__(self, on_location):
        self.on_location = on_location

    def start(self):
        from plyer import gps
        gps.configure(on_location=self._on_loc)
        gps.start(minTime=1000, minDistance=1)

    def stop(self):
        from plyer import gps
        gps.stop()

    def _on_loc(self, **kwargs):
        lat, lon = kwargs.get("lat"), kwargs.get("lon")
        if lat is not None and lon is not None:
            self.on_location(float(lat), float(lon))
