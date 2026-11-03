"""Main KivyMD application: wires UI, GPS and geofencing together."""

from kivy.metrics import dp
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar

from folklore.config import APPROACH_OFFSET_M, START_POSITION, USE_REAL_GPS
from folklore.core.geo_utils import haversine_m
from folklore.core.geofence import GeofenceManager
from folklore.core.gps_providers import RealGPS, SimulatedGPS
from folklore.data.sites import SITES
from folklore.ui.dialogs import FolkloreDialogManager
from folklore.ui.widgets import SiteCard, StatusCard


class FolkloreApp(MDApp):
    def build(self):
        self.title = "Folklore Guide"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Amber"

        self.site_cards = {}
        self.dialogs = FolkloreDialogManager(self.theme_cls)
        self.geofence = GeofenceManager(SITES, self.on_enter_zone, self.on_exit_zone)

        use_real = USE_REAL_GPS and platform == "android"
        self.gps = (RealGPS if use_real else SimulatedGPS)(self.on_location)
        return self._build_ui()

    # ---- layout ----------------------------------------------------------
    def _build_ui(self):
        screen = MDScreen()
        root = MDBoxLayout(orientation="vertical")
        root.add_widget(
            MDTopAppBar(title="Folklore & Urban Legends", elevation=4, anchor_title="left")
        )

        body = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=dp(16),
            spacing=dp(14),
        )
        self.status_card = StatusCard(
            on_reset=self.reset_position,
            md_bg_color=self.theme_cls.primary_dark,
        )
        body.add_widget(self.status_card)
        body.add_widget(MDLabel(text="Legends Nearby", font_style="H5", adaptive_height=True))

        for site in SITES:
            card = SiteCard(site, on_visit=self.simulate_visit)
            self.site_cards[site.name] = card
            body.add_widget(card)

        scroll = MDScrollView()
        scroll.add_widget(body)
        root.add_widget(scroll)
        screen.add_widget(root)
        return screen

    # ---- lifecycle -------------------------------------------------------
    def on_start(self):
        if platform == "android":
            try:
                from android.permissions import Permission, request_permissions
                request_permissions(
                    [Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION]
                )
            except Exception as exc:  # noqa: BLE001
                print("Permission request failed:", exc)
        self.gps.start()

    def on_stop(self):
        self.gps.stop()

    # ---- simulation controls ---------------------------------------------
    def reset_position(self):
        if isinstance(self.gps, SimulatedGPS):
            self.gps.teleport(*START_POSITION)

    def simulate_visit(self, site):
        """Drop the simulated user near the site, then walk in."""
        if not isinstance(self.gps, SimulatedGPS):
            return
        self.gps.teleport(site.lat - APPROACH_OFFSET_M / 111320.0, site.lon)
        self.gps.walk_to(site.lat, site.lon)

    # ---- GPS / geofence callbacks ----------------------------------------
    def on_location(self, lat, lon):
        self.geofence.update(lat, lon)  # update zone state first
        self.status_card.set_position(lat, lon)

        nearest, nearest_d = None, float("inf")
        for site in SITES:
            d = haversine_m(lat, lon, site.lat, site.lon)
            self.site_cards[site.name].set_distance(d, site.name in self.geofence.inside)
            if d < nearest_d:
                nearest, nearest_d = site, d
        self.status_card.set_nearest(nearest, nearest_d)

    def on_enter_zone(self, site, _dist):
        self.status_card.set_state(f"Entered {site.name}")
        self.dialogs.show(site)

    def on_exit_zone(self, site):
        self.status_card.set_state(f"Left {site.name}. Roaming...")
