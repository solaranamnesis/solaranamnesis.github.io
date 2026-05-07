from __future__ import annotations

import importlib.util
import json
import html
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ABOUT_DIR = REPO_ROOT / "about-solar-anamnesis"
PAGE_DIR = ABOUT_DIR / "creating-microscope-panoramas"
TRANSLATIONS_DIR = REPO_ROOT / "translations"
ENGLISH_FILE = PAGE_DIR / "index.html"
ABOUT_ENGLISH_FILE = ABOUT_DIR / "index.html"
PAGE_TRANSLATIONS_FILE = PAGE_DIR / "page_translations.json"
PAGE_TRANSLATIONS_PY_FILE = PAGE_DIR / "page_translations.py"
BASE_URL = "https://blog.solaranamnesis.com/about-solar-anamnesis/creating-microscope-panoramas/"
ALT_PATTERN = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)" />')
HTML_TAG_PATTERN = re.compile(r"<html\b[^>]*>")
OG_LOCALE_PATTERN = re.compile(r'<meta property="og:locale" content="([^"]+)" />')
FILE_CODE_PATTERN = re.compile(r"index-([^.]+)\.html$")
TITLE_PATTERN = re.compile(r"<title>[^<]+</title>")
OG_TITLE_PATTERN = re.compile(r'<meta property="og:title" content="[^"]+" />')
TWITTER_TITLE_PATTERN = re.compile(r'<meta name="twitter:title" content="[^"]+" />')
ENTRY_TITLE_PATTERN = re.compile(r'<h1 class="entry-title">[^<]+</h1>')
META_DESC_PATTERN = re.compile(r'<meta name="description" content="([^"]+)"')
OG_IMAGE_ALT_PATTERN = re.compile(r'<meta property="og:image:alt" content="([^"]+)"')
ENTRY_CONTENT_PATTERN = re.compile(
    r'(<div class="entry-content clear">)(.*?)(\s+</div><!-- \.entry-content -->)',
    re.DOTALL,
)
P_TAG_PATTERN = re.compile(r"<p>(.*?)</p>", re.DOTALL)

ENGLISH_META_DESCRIPTION = (
    "Solar Anamnesis is a meteorite thin section photography blog featuring "
    "high-resolution gigapixel panorama mosaics of chondrites, achondrites, lunar, and…"
)
ENGLISH_OG_IMAGE_ALT = "NWA 980 meteorite thin section gigapixel mosaic"

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


CREATE_PAGE_LINK_PATTERN = re.compile(
    r'href="[^"]*/creating-microscope-panoramas/"[^>]*>([^<]+)<'
)

LANGUAGE_PREFIX_TO_CODE = {
    "ENGLISH": "en",
    "FRENCH": "fr",
    "GERMAN": "de",
    "SPANISH": "es",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_root_language_codes() -> set[str]:
    return {
        m.group(1)
        for p in REPO_ROOT.glob("index-*.html")
        if (m := FILE_CODE_PATTERN.search(p.name))
    }


def extract_about_language_codes() -> set[str]:
    return {
        m.group(1)
        for p in ABOUT_DIR.glob("index-*.html")
        if (m := FILE_CODE_PATTERN.search(p.name))
    }


def extract_about_metadata(path: Path) -> tuple[str, str, str | None]:
    content = path.read_text(encoding="utf-8")
    html_tag_match = HTML_TAG_PATTERN.search(content)
    og_locale_match = OG_LOCALE_PATTERN.search(content)
    if not html_tag_match or not og_locale_match:
        raise ValueError(f"Missing language metadata in {path}")

    page_title = None
    page_title_match = CREATE_PAGE_LINK_PATTERN.search(content)
    if page_title_match:
        page_title = page_title_match.group(1).strip()

    return html_tag_match.group(0), og_locale_match.group(1), page_title


def load_language_variants() -> tuple[list[tuple[str, str | None]], dict[str, tuple[str, str, str | None]]]:
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

    root_codes = extract_root_language_codes()
    about_codes = extract_about_language_codes()
    variant_codes = {code for hreflang, code in variants if hreflang not in {"en", "x-default"} and code}

    if root_codes != about_codes:
        raise ValueError(f"Root/about language mismatch: {sorted(root_codes ^ about_codes)}")
    if root_codes != variant_codes:
        raise ValueError(f"Root/hreflang language mismatch: {sorted(root_codes ^ variant_codes)}")

    metadata: dict[str, tuple[str, str, str | None]] = {"en": extract_about_metadata(ABOUT_ENGLISH_FILE)}
    for _, file_code in variants:
        if not file_code:
            continue
        metadata[file_code] = extract_about_metadata(ABOUT_DIR / f"index-{file_code}.html")

    return variants, metadata


def build_alternate_block(variants: list[tuple[str, str | None]]) -> str:
    lines: list[str] = []
    for hreflang, file_code in variants:
        href = BASE_URL if file_code is None else f"{BASE_URL}index-{file_code}.html"
        lines.append(f'<link rel="alternate" hreflang="{hreflang}" href="{href}" />')
    return "\n".join(lines)


def render_variant(
    template: str,
    html_tag: str,
    canonical_href: str,
    og_url: str,
    og_locale: str,
    alternate_block: str,
    page_title: str | None,
) -> str:
    rendered = HTML_TAG_PATTERN.sub(html_tag, template, count=1)
    rendered = re.sub(
        r'<link rel="canonical" href="[^"]+" />\n(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+" />\n?)*',
        f'<link rel="canonical" href="{canonical_href}" />\n{alternate_block}\n',
        rendered,
        count=1,
    )
    rendered = re.sub(
        r'<meta property="og:url" content="[^"]+" />',
        f'<meta property="og:url" content="{og_url}" />',
        rendered,
        count=1,
    )
    rendered = OG_LOCALE_PATTERN.sub(f'<meta property="og:locale" content="{og_locale}" />', rendered, count=1)

    if page_title:
        full_title = f"{page_title} | Solar Anamnesis"
        rendered = TITLE_PATTERN.sub(f"<title>{full_title}</title>", rendered, count=1)
        rendered = OG_TITLE_PATTERN.sub(f'<meta property="og:title" content="{full_title}" />', rendered, count=1)
        rendered = TWITTER_TITLE_PATTERN.sub(f'<meta name="twitter:title" content="{full_title}" />', rendered, count=1)
        rendered = ENTRY_TITLE_PATTERN.sub(f'<h1 class="entry-title">{page_title}</h1>', rendered, count=1)

    return rendered


def load_about_page_fallbacks(lang_code: str) -> dict[str, str]:
    about_path = ABOUT_DIR / f"index-{lang_code}.html"
    if not about_path.exists():
        return {}
    content = about_path.read_text(encoding="utf-8")
    fallbacks: dict[str, str] = {}

    m = META_DESC_PATTERN.search(content)
    if m and m.group(1) != ENGLISH_META_DESCRIPTION:
        fallbacks[ENGLISH_META_DESCRIPTION] = m.group(1)

    m = OG_IMAGE_ALT_PATTERN.search(content)
    if m and m.group(1) != ENGLISH_OG_IMAGE_ALT:
        fallbacks[ENGLISH_OG_IMAGE_ALT] = m.group(1)

    return fallbacks


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
        '<h1 class="widget-title">Search</h1>': f'<h1 class="widget-title">{sidebar[0]}</h1>',
        '<h2 class="widget-title">Search</h2>': f'<h2 class="widget-title">{sidebar[0]}</h2>',
        "prefill=Search Solar Anamnesis": f"prefill={sidebar[1]}",
        '<h1 class="widget-title">Meteorite Photo Categories</h1>': f'<h1 class="widget-title">{sidebar[2]}</h1>',
        '<h2 class="widget-title">Meteorite Photo Categories</h2>': f'<h2 class="widget-title">{sidebar[2]}</h2>',
        "Scenes from the Solar System&#039;s Youth": site_description,
        'title="Widgets"': f'title="{nav_elements[0]}"',
        ">Widgets</span>": f">{nav_elements[0]}</span>",
        '<h1 class="menu-toggle">Menu</h1>': f'<h1 class="menu-toggle">{nav_elements[2]}</h1>',
        'title="Skip to content">Skip to content</a>': f'title="{nav_elements[1]}">{nav_elements[1]}</a>',
        'alt="Become a Friend of GNOME"': f'alt="{footer[0]}"',
        'alt="[ GNU Link]"': f'alt="{footer[1]}"',
        ">Proudly powered by WordPress</a>": f">{footer[2]}</a>",
        "Theme: Ryu by ": theme_label,
        'href="https://blog.solaranamnesis.com/" title=': f'href="https://blog.solaranamnesis.com/index-{lang_code}.html" title=',
        'https://blog.solaranamnesis.com/">': f'https://blog.solaranamnesis.com/index-{lang_code}.html">',
        'https://blog.solaranamnesis.com/about-solar-anamnesis/">': f'https://blog.solaranamnesis.com/about-solar-anamnesis/index-{lang_code}.html">',
        'https://store.solaranamnesis.com">': f'https://store.solaranamnesis.com/index-{lang_code}.html">',
        'https://cdn.solaranamnesis.com/SurfacePhotos/krpano/abapanu/Meteorite-Surface-AbaPanu-final.html">': f'https://cdn.solaranamnesis.com/SurfacePhotos/krpano/abapanu/Meteorite-Surface-AbaPanu-final.html?lang={lang_code}">',
    }

    translated_categories = [item["name"] for item in translation["meteorite_categories"]]
    if len(translated_categories) != len(ENGLISH_CATEGORIES):
        raise ValueError(f"Unexpected category count for {lang_code}: {len(translated_categories)}")

    for source, target in zip(ENGLISH_CATEGORIES, translated_categories):
        replacements[f">{source}</a>"] = f">{target}</a>"

    return replacements


def apply_replacements(content: str, replacements: dict[str, str]) -> str:
    updated = content
    for source, target in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        updated = updated.replace(source, target)
    return updated


def load_python_page_translations() -> dict:
    if not PAGE_TRANSLATIONS_PY_FILE.exists():
        return {}

    spec = importlib.util.spec_from_file_location("page_translations_py", PAGE_TRANSLATIONS_PY_FILE)
    if not spec or not spec.loader:
        raise ValueError(f"Could not load {PAGE_TRANSLATIONS_PY_FILE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    source_headings = getattr(module, "SOURCE_HEADINGS", None)
    source_paragraphs = getattr(module, "SOURCE_PARAGRAPHS", None)
    if source_headings is None or source_paragraphs is None:
        raise ValueError("page_translations.py must define SOURCE_HEADINGS and SOURCE_PARAGRAPHS")

    source_entry_title = getattr(module, "SOURCE_ENTRY_TITLE", "Creating Microphotographic Panoramas")
    language_codes = getattr(module, "LANGUAGE_CODES", {})

    translations: dict[str, dict] = {}
    for key, value in vars(module).items():
        if not key.endswith("_HEADINGS") or key == "SOURCE_HEADINGS":
            continue
        prefix = key[: -len("_HEADINGS")]
        headings = value
        paragraphs = getattr(module, f"{prefix}_PARAGRAPHS", None)
        if paragraphs is None:
            raise ValueError(f"Missing {prefix}_PARAGRAPHS in page_translations.py")

        lang_code = language_codes.get(prefix) or LANGUAGE_PREFIX_TO_CODE.get(prefix)
        if not lang_code and len(prefix) == 2 and prefix.isalpha():
            lang_code = prefix.lower()
        if not lang_code:
            raise ValueError(
                f"Unknown language prefix '{prefix}'. Add it to LANGUAGE_CODES in page_translations.py."
            )

        entry_title = getattr(module, f"{prefix}_ENTRY_TITLE", None)
        translation = {
            "headings": headings,
            "paragraphs": paragraphs,
        }
        if entry_title:
            translation["entry_title"] = entry_title
        translations[lang_code] = translation

    return {
        "source": {
            "entry_title": source_entry_title,
            "headings": source_headings,
            "paragraphs": source_paragraphs,
        },
        "translations": translations,
    }


def load_page_translations() -> dict:
    data: dict = {}
    if PAGE_TRANSLATIONS_FILE.exists():
        data = load_json(PAGE_TRANSLATIONS_FILE)

    py_data = load_python_page_translations()
    if not py_data:
        return data

    if not data:
        data = {"schema_version": "1.0", "source_file": str(ENGLISH_FILE.relative_to(REPO_ROOT))}

    data["source"] = py_data["source"]
    merged_translations = dict(data.get("translations", {}))
    merged_translations.update(py_data.get("translations", {}))
    data["translations"] = merged_translations
    return data


def _strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value)


def apply_page_translations(content: str, lang_code: str, page_data: dict) -> str:
    if not page_data:
        return content

    translations = page_data.get("translations", {})
    source = page_data.get("source", {})
    lang_data = translations.get(lang_code)
    if not lang_data:
        return content

    source_headings = source.get("headings", [])
    source_paragraphs = source.get("paragraphs", [])
    target_headings = lang_data.get("headings", [])
    target_paragraphs = lang_data.get("paragraphs", [])
    target_entry_title = lang_data.get("entry_title")

    if len(source_headings) == len(target_headings):
        for src, dst in zip(source_headings, target_headings):
            content = content.replace(f"<h2>{src}</h2>", f"<h2>{dst}</h2>")

    if target_entry_title:
        content = ENTRY_TITLE_PATTERN.sub(f'<h1 class="entry-title">{target_entry_title}</h1>', content, count=1)

    m = ENTRY_CONTENT_PATTERN.search(content)
    if not m:
        return content

    prefix, body, suffix = m.groups()
    p_matches = list(P_TAG_PATTERN.finditer(body))
    if not p_matches:
        return content

    def replace_paragraph(match: re.Match, idx: int) -> str:
        if idx >= len(source_paragraphs) or idx >= len(target_paragraphs):
            return match.group(0)
        inner = match.group(1)
        source_plain = source_paragraphs[idx]
        target_plain = target_paragraphs[idx]
        inner_plain = html.unescape(_strip_tags(inner)).strip()
        if inner_plain != source_plain:
            return match.group(0)
        if "<a " in inner:
            return match.group(0)
        escaped = html.escape(target_plain, quote=False)
        return f"<p>{escaped}</p>"

    rebuilt_parts: list[str] = []
    last = 0
    for i, pm in enumerate(p_matches):
        rebuilt_parts.append(body[last : pm.start()])
        rebuilt_parts.append(replace_paragraph(pm, i))
        last = pm.end()
    rebuilt_parts.append(body[last:])
    rebuilt_body = "".join(rebuilt_parts)
    return content[: m.start()] + prefix + rebuilt_body + suffix + content[m.end() :]


def render_language_file(
    lang_code: str,
    metadata: tuple[str, str, str | None],
    alternate_block: str,
    page_data: dict,
) -> None:
    html_tag, og_locale, page_title = metadata
    localized_url = f"{BASE_URL}index-{lang_code}.html"

    template = ENGLISH_FILE.read_text(encoding="utf-8")
    content = render_variant(
        template,
        html_tag,
        localized_url,
        localized_url,
        og_locale,
        alternate_block,
        page_title,
    )

    shared_translation = load_json(TRANSLATIONS_DIR / f"{lang_code}.json")
    shared_replacements = build_shared_replacements(lang_code, shared_translation)
    about_fallbacks = load_about_page_fallbacks(lang_code)

    content = apply_replacements(content, shared_replacements)
    content = apply_replacements(content, about_fallbacks)
    content = apply_page_translations(content, lang_code, page_data)

    (PAGE_DIR / f"index-{lang_code}.html").write_text(content, encoding="utf-8")


def main() -> None:
    variants, metadata = load_language_variants()
    alternate_block = build_alternate_block(variants)
    page_data = load_page_translations()

    en_html_tag, en_og_locale, en_page_title = metadata["en"]
    en_template = ENGLISH_FILE.read_text(encoding="utf-8")
    ENGLISH_FILE.write_text(
        render_variant(
            en_template,
            en_html_tag,
            BASE_URL,
            BASE_URL,
            en_og_locale,
            alternate_block,
            en_page_title,
        ),
        encoding="utf-8",
    )

    for _, file_code in variants:
        if not file_code:
            continue
        render_language_file(file_code, metadata[file_code], alternate_block, page_data)


if __name__ == "__main__":
    main()
