from py_stealth import *

import os
import urllib.request
import xml.etree.ElementTree as ET
from typing import Optional, Tuple


REGIONS_URL = (
    "https://raw.githubusercontent.com/"
    "ServUO/ServUO/pub57/Data/Regions.xml"
)

CACHE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "servuo_regions.xml",
)

# Stealth WorldNum() -> ServUO facet name
FACETS = {
    0: "Felucca",
    1: "Trammel",
    2: "Ilshenar",
    3: "Malas",
    4: "Tokuno",
    5: "TerMur",
}

# These standard ServUO region classes are guarded.
GUARDED_REGION_TYPES = {
    "GuardedRegion",
    "TownRegion",
}


def download_regions(force: bool = False) -> str:
    """
    Download ServUO's Regions.xml and cache it beside this script.
    """

    if os.path.exists(CACHE_FILE) and not force:
        return CACHE_FILE

    print("Downloading ServUO guarded-region data...")

    try:
        urllib.request.urlretrieve(REGIONS_URL, CACHE_FILE)
    except Exception as error:
        raise RuntimeError(
            f"Could not download ServUO Regions.xml: {error}"
        )

    return CACHE_FILE


def _bool_value(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default

    return value.strip().lower() in {
        "true",
        "yes",
        "1",
        "on",
    }


def _region_guards_disabled(region: ET.Element) -> bool:
    guards = region.find("guards")

    if guards is None:
        return False

    return _bool_value(guards.get("disabled"), False)


def _point_in_rect(x: int, y: int, rect: ET.Element) -> bool:
    """
    ServUO Rectangle2D semantics:
        start <= coordinate < start + size
    """

    rect_x = int(rect.get("x", "0"))
    rect_y = int(rect.get("y", "0"))
    width = int(rect.get("width", "0"))
    height = int(rect.get("height", "0"))

    return (
        rect_x <= x < rect_x + width
        and rect_y <= y < rect_y + height
    )


def guarded_region_at(
    x: int,
    y: int,
    facet: str,
) -> Optional[str]:
    """
    Return the guarded-region name containing X/Y,
    or None when the position is not actively guarded.
    """

    xml_path = download_regions()
    root = ET.parse(xml_path).getroot()

    facet_element = None

    for candidate in root.findall("Facet"):
        if candidate.get("name", "").lower() == facet.lower():
            facet_element = candidate
            break

    if facet_element is None:
        return None

    # Only top-level regions are needed for standard towns.
    # Their rectangles also cover any nested child regions.
    for region in facet_element.findall("region"):
        region_type = region.get("type", "")

        if region_type not in GUARDED_REGION_TYPES:
            continue

        if _region_guards_disabled(region):
            continue

        for rect in region.findall("rect"):
            if _point_in_rect(x, y, rect):
                return region.get("name", region_type)

    return None


def is_guard_zone(
    x: Optional[int] = None,
    y: Optional[int] = None,
    world: Optional[int] = None,
) -> bool:
    """
    Check arbitrary coordinates or the player's current position.

    Examples:
        is_guard_zone()
        is_guard_zone(1496, 1628, 1)
    """

    if x is None:
        x = GetX(Self())

    if y is None:
        y = GetY(Self())

    if world is None:
        world = WorldNum()

    facet = FACETS.get(world)

    if facet is None:
        print(f"Unknown facet/world number: {world}")
        return False

    return guarded_region_at(x, y, facet) is not None


def print_guard_status() -> None:
    x = GetX(Self())
    y = GetY(Self())
    z = GetZ(Self())
    world = WorldNum()

    facet = FACETS.get(world, f"Unknown facet {world}")

    if world not in FACETS:
        print(
            f"X={x}, Y={y}, Z={z}, world={world}: "
            "unknown facet"
        )
        return

    region_name = guarded_region_at(x, y, facet)

    if region_name:
        print(
            f"GUARDED: {region_name} | "
            f"{facet} X={x}, Y={y}, Z={z}"
        )
    else:
        print(
            f"NOT GUARDED | "
            f"{facet} X={x}, Y={y}, Z={z}"
        )


print_guard_status()
