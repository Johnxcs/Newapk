"""Hardcoded folklore sites."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FolkloreSite:
    name: str
    place: str
    lat: float
    lon: float
    radius_m: float
    legend_title: str
    story: str


SITES = [
    FolkloreSite(
        name="Balete Drive",
        place="Quezon City, Philippines",
        lat=14.6237,
        lon=121.0330,
        radius_m=300,
        legend_title="The White Lady of Balete Drive",
        story=(
            "Taxi drivers have whispered about her for generations: a pale woman in "
            "a white dress who waits along the dark, tree-lined road late at night. "
            "Some say she hails a cab, then vanishes from the back seat. Others "
            "claim drivers glimpse her face in the rear-view mirror, only to find "
            "the seat empty when they turn around.\n\n"
            "The old balete trees that line the street are said to be her home, "
            "and locals still hush their voices when passing by after midnight."
        ),
    ),
    FolkloreSite(
        name="Greyfriars Kirkyard",
        place="Edinburgh, Scotland",
        lat=55.9468,
        lon=-3.1925,
        radius_m=250,
        legend_title="The Mackenzie Poltergeist",
        story=(
            "Behind a gated tomb in this centuries-old graveyard rests Sir George "
            "'Bluidy' Mackenzie, a feared 17th-century lawyer. In 1998 a homeless "
            "man reportedly broke into his mausoleum seeking shelter and disturbed "
            "his coffin. Since then, visitors have reported sudden cold spots, "
            "scratches, bruises and a heavy sense of being watched.\n\n"
            "Ghost tours still gather at its iron gate, where some guests say "
            "they feel an unseen hand brush past them in the dark."
        ),
    ),
    FolkloreSite(
        name="Old Dutch Church Bridge",
        place="Sleepy Hollow, New York, USA",
        lat=41.0903,
        lon=-73.8587,
        radius_m=300,
        legend_title="The Headless Horseman",
        story=(
            "Washington Irving immortalized this quiet Hudson Valley village in "
            "1820. The tale tells of a Hessian soldier who lost his head to a "
            "cannonball in battle and now rides every night in search of it.\n\n"
            "The ghost can only be outrun by reaching the bridge by the old "
            "church. Locals say that on windy autumn nights you can still hear "
            "hoofbeats echoing along the road."
        ),
    ),
]
