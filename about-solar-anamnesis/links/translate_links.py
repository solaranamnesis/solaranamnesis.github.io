from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ABOUT_DIR = REPO_ROOT / "about-solar-anamnesis"
LINKS_DIR = ABOUT_DIR / "links"
TRANSLATIONS_DIR = REPO_ROOT / "translations"
LINKS_TRANSLATIONS_DIR = TRANSLATIONS_DIR / "links"
ABOUT_ENGLISH_FILE = ABOUT_DIR / "index.html"
FILE_CODE_PATTERN = re.compile(r"index-([^.]+)\.html$")
ALT_PATTERN = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)" />')

ENGLISH_META_DESCRIPTION = (
    "Solar Anamnesis is a meteorite thin section photography blog featuring "
    "high-resolution gigapixel panorama mosaics of chondrites, achondrites, lunar, and…"
)

ENGLISH_CATEGORIES = [
    "10x/0.25",
    "4x/0.25",
    "A35140U CCD 14MP",
    "A3550UPA CCD 5MP",
    "acapulcoite",
    "achondrite",
    "angrite",
    "aubrite",
    "australia",
    "breccia",
    "calcium-aluminium-rich inclusion",
    "carbonaceous",
    "chondrite",
    "CO",
    "CV",
    "dar al gani",
    "diogenite",
    "dunite",
    "earth",
    "enstatite",
    "eucrite",
    "howardite",
    "LMScope",
    "lodranite",
    "lunar",
    "mars",
    "mesosiderite",
    "metachondrite",
    "named fall",
    "Nikon D810",
    "Nikon Z6",
    "northwest africa",
    "ordinary chondrite",
    "pallasite",
    "polarized",
    "primitive achondrite",
    "rumuruti",
    "scope1",
    "scope2",
    "surface",
    "Tucsen C30 3MP sCMOS",
    "uncovered",
    "ureilite",
    "wave retarder",
    "zerene stacker",
]

ENGLISH_LINKS_REPLACEMENTS = {
    "Meteorite Links | Solar Anamnesis": "Meteorite Links | Solar Anamnesis",
    ENGLISH_META_DESCRIPTION: ENGLISH_META_DESCRIPTION,
    "Meteorite Links": "Meteorite Links",
    "Meteorite Info/Pictures": "Meteorite Info/Pictures",
    "Virtual Microscope": "Virtual Microscope",
    "Another fantastic resource with fully interactive online panoramas of thin sections.": "Another fantastic resource with fully interactive online panoramas of thin sections.",
    "Photo Atlas of Meteorites (Thomas Witzke)": "Photo Atlas of Meteorites (Thomas Witzke)",
    "Well organized tables with categorization of meteorite classes.": "Well organized tables with categorization of meteorite classes.",
    "Dweir&#8217;s Meteorite Studies": "Dweir&#8217;s Meteorite Studies",
    "Excellent resource for a detailed scientific understanding of individual meteorites.": "Excellent resource for a detailed scientific understanding of individual meteorites.",
    "Jeff Hodges Thin Section Art": "Jeff Hodges Thin Section Art",
    "Beautiful thin section art photographs of a large number of meteorites.": "Beautiful thin section art photographs of a large number of meteorites.",
    "Tom Phillips Micrographic": "Tom Phillips Micrographic",
    "Unique art photographs of meteorite thin sections.": "Unique art photographs of meteorite thin sections.",
    "John Kashuba Pictures": "John Kashuba Pictures",
    "Nice images of meteorite thin sections and meteorite slices.": "Nice images of meteorite thin sections and meteorite slices.",
    "Neil H Buckland": "Neil H Buckland",
    "Meteorite Panoramas of exceptional quality.": "Meteorite Panoramas of exceptional quality.",
    "John Kashuba Articles and Pics": "John Kashuba Articles and Pics",
    "Meteorite Times articles by John Kashuba with pictures and descriptions.": "Meteorite Times articles by John Kashuba with pictures and descriptions.",
    "Collecting Meteorites Thin Section Pics": "Collecting Meteorites Thin Section Pics",
    "Pictures of meteorite thin sections and animated gifs of cross polarization.": "Pictures of meteorite thin sections and animated gifs of cross polarization.",
    "Jeff Barton Pictures": "Jeff Barton Pictures",
    "Meteorite thin section images.": "Meteorite thin section images.",
    "Squatting Dog Thin Section Images": "Squatting Dog Thin Section Images",
    "Meteorite Times Magazine": "Meteorite Times Magazine",
    "Great resource with current meteorite news.": "Great resource with current meteorite news.",
    "Agab Meteorite Thin Section Photos": "Agab Meteorite Thin Section Photos",
    "Nice photographs of various meteorite thin sections.": "Nice photographs of various meteorite thin sections.",
    "Marmet Meteorites": "Marmet Meteorites",
    "IMCA Encyclopedia of Meteorites": "IMCA Encyclopedia of Meteorites",
    "Search the Meteoritical Bulletin Database at the <b>Lunar and Planetary Institute (LPI)</b>": "Search the Meteoritical Bulletin Database at the <b>Lunar and Planetary Institute (LPI)</b>",
    "List of Meteorites by Solar Anamnesis at the <b>Lunar and Planetary Institute (LPI)</b>": "List of Meteorites by Solar Anamnesis at the <b>Lunar and Planetary Institute (LPI)</b>",
    "Utas Collection": "Utas Collection",
    "J.M. Derochette": "J.M. Derochette",
    "Meteorite Picture of the Day &#8211; Tucson Meteorites": "Meteorite Picture of the Day &#8211; Tucson Meteorites",
    "Daily updates with pictures of all kinds of meteorites.": "Daily updates with pictures of all kinds of meteorites.",
    "Martian Meteorites Information.": "Martian Meteorites Information.",
    "The Meteorite Exchange": "The Meteorite Exchange",
    "brite.co Article about Meteorites": "brite.co Article about Meteorites",
    "Space Rocks: The Mineral Composition of Meteorites.": "Space Rocks: The Mineral Composition of Meteorites.",
    "Otto Hahn's Meteorite Works": "Otto Hahn's Meteorite Works",
    "German to English translations of Hahn's works.": "German to English translations of Hahn's works.",
    "CC0 Books and Articles": "CC0 Books and Articles",
    "Remastered Public Domain (CC0) books and articles on the history and study of meteorites.": "Remastered Public Domain (CC0) books and articles on the history and study of meteorites.",
}


def load_language_variants() -> list[tuple[str, str | None]]:
    about_index = ABOUT_ENGLISH_FILE.read_text(encoding="utf-8")
    variants: list[tuple[str, str | None]] = []
    for hreflang, href in ALT_PATTERN.findall(about_index):
        if hreflang in {"en", "x-default"}:
            variants.append((hreflang, None))
            continue
        match = FILE_CODE_PATTERN.search(href)
        if not match:
            raise ValueError(f"Could not determine file code for {hreflang}: {href}")
        variants.append((hreflang, match.group(1)))
    return variants


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_shared_replacements(lang_code: str, translation: dict) -> dict[str, str]:
    nav = translation["navigation_main"]
    sidebar = translation["sidebar_widgets"]
    nav_elements = translation["navigation_elements"]
    footer = translation["site_metadata"]["footer_links"]
    site_description = translation["site_metadata"]["site_description"]

    theme_label = footer[3]
    if theme_label.endswith("WordPress.com"):
        theme_label = theme_label[: -len("WordPress.com")]

    replacements = {
        ">Home</a>": f">{nav[0]}</a>",
        ">About</a>": f">{nav[1]}</a>",
        ">Gallery</a>": f">{nav[2]}</a>",
        ">Store</a>": f">{nav[3]}</a>",
        ">Panorama Gallery</a>": f">{nav[4]}</a>",
        "<h1 class=\"widget-title\">Search</h1>": f"<h1 class=\"widget-title\">{sidebar[0]}</h1>",
        "prefill=Search Solar Anamnesis": f"prefill={sidebar[1]}",
        "<h1 class=\"widget-title\">Meteorite Photo Categories</h1>": f"<h1 class=\"widget-title\">{sidebar[2]}</h1>",
        "Scenes from the Solar System&#039;s Youth": site_description,
        "title=\"Widgets\"": f"title=\"{nav_elements[0]}\"",
        ">Widgets</span>": f">{nav_elements[0]}</span>",
        "<h1 class=\"menu-toggle\">Menu</h1>": f"<h1 class=\"menu-toggle\">{nav_elements[2]}</h1>",
        "title=\"Skip to content\">Skip to content</a>": f"title=\"{nav_elements[1]}\">{nav_elements[1]}</a>",
        "alt=\"Become a Friend of GNOME\"": f"alt=\"{footer[0]}\"",
        "alt=\"[ GNU Link]\"": f"alt=\"{footer[1]}\"",
        ">Proudly powered by WordPress</a>": f">{footer[2]}</a>",
        "Theme: Ryu by ": theme_label,
        "https://blog.solaranamnesis.com/\">": f"https://blog.solaranamnesis.com/index-{lang_code}.html\">",
        "https://blog.solaranamnesis.com/about-solar-anamnesis/\">": f"https://blog.solaranamnesis.com/about-solar-anamnesis/index-{lang_code}.html\">",
        "https://store.solaranamnesis.com\">": f"https://store.solaranamnesis.com/index-{lang_code}.html\">",
        "https://cdn.solaranamnesis.com/SurfacePhotos/krpano/abapanu/Meteorite-Surface-AbaPanu-final.html\">": f"https://cdn.solaranamnesis.com/SurfacePhotos/krpano/abapanu/Meteorite-Surface-AbaPanu-final.html?lang={lang_code}\">",
    }

    translated_categories = [item["name"] for item in translation["meteorite_categories"]]
    if len(translated_categories) != len(ENGLISH_CATEGORIES):
        raise ValueError(f"Unexpected category count for {lang_code}: {len(translated_categories)}")

    for source, target in zip(ENGLISH_CATEGORIES, translated_categories):
        replacements[f">{source}</a>"] = f">{target}</a>"

    return replacements


def load_links_specific_replacements(lang_code: str) -> dict[str, str]:
    path = LINKS_TRANSLATIONS_DIR / f"{lang_code}.json"
    if not path.exists():
        return dict(ENGLISH_LINKS_REPLACEMENTS)

    data = load_json(path)
    replace_block = data.get("replace", {})
    replacements = dict(ENGLISH_LINKS_REPLACEMENTS)
    for key, value in replace_block.items():
        if key in replacements and isinstance(value, str) and value:
            replacements[key] = value
    return replacements


def apply_replacements(content: str, replacements: dict[str, str]) -> str:
    updated = content
    for source, target in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        updated = updated.replace(source, target)
    return updated


def render_language_file(lang_code: str, file_path: Path) -> None:
    shared_translation = load_json(TRANSLATIONS_DIR / f"{lang_code}.json")
    shared_replacements = build_shared_replacements(lang_code, shared_translation)
    links_replacements = load_links_specific_replacements(lang_code)

    content = file_path.read_text(encoding="utf-8")
    content = apply_replacements(content, shared_replacements)
    content = apply_replacements(content, links_replacements)
    file_path.write_text(content, encoding="utf-8")


def main() -> None:
    variants = load_language_variants()
    for _, file_code in variants:
        if not file_code:
            continue
        file_path = LINKS_DIR / f"index-{file_code}.html"
        render_language_file(file_code, file_path)


if __name__ == "__main__":
    main()
