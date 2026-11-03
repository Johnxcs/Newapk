"""Reusable KivyMD widgets."""

from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from folklore.core.geo_utils import format_distance


class StatusCard(MDCard):
    """Top card showing live coordinates and geofence state."""

    def __init__(self, on_reset=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(6),
            size_hint_y=None,
            height=dp(190),
            radius=[dp(24)],
            elevation=3,
            **kwargs,
        )
        self.add_widget(
            MDLabel(text="Simulated GPS Tracker", font_style="H6", adaptive_height=True)
        )
        self.coord_label = MDLabel(text="Lat/Lon: --", adaptive_height=True)
        self.nearest_label = MDLabel(text="Nearest legend: --", adaptive_height=True)
        self.state_label = MDLabel(
            text="Status: Roaming...", theme_text_color="Secondary", adaptive_height=True
        )
        self.add_widget(self.coord_label)
        self.add_widget(self.nearest_label)
        self.add_widget(self.state_label)
        if on_reset:
            self.add_widget(
                MDFlatButton(text="RESET TO START", on_release=lambda *_: on_reset())
            )

    def set_position(self, lat, lon):
        self.coord_label.text = f"Lat/Lon: {lat:.5f}, {lon:.5f}"

    def set_nearest(self, site, meters):
        self.nearest_label.text = f"Nearest legend: {site.name} ({format_distance(meters)})"

    def set_state(self, text):
        self.state_label.text = f"Status: {text}"


class SiteCard(MDCard):
    """Card for one folklore site with live distance and a demo button."""

    def __init__(self, site, on_visit, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(6),
            size_hint_y=None,
            height=dp(170),
            radius=[dp(20)],
            elevation=2,
            **kwargs,
        )
        self.site = site
        self.add_widget(MDLabel(text=site.name, font_style="H6", adaptive_height=True))
        self.add_widget(
            MDLabel(
                text=f"{site.place}  |  Trigger radius {site.radius_m:.0f} m",
                theme_text_color="Secondary",
                font_style="Caption",
                adaptive_height=True,
            )
        )
        self.distance_label = MDLabel(
            text="Distance: --", font_style="Subtitle1", adaptive_height=True
        )
        self.add_widget(self.distance_label)
        self.add_widget(
            MDRaisedButton(text="SIMULATE VISIT", on_release=lambda *_: on_visit(site))
        )

    def set_distance(self, meters, inside):
        tag = "  (INSIDE ZONE)" if inside else ""
        self.distance_label.text = f"Distance: {format_distance(meters)}{tag}"
