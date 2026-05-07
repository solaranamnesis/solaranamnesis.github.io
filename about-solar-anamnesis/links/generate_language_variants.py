from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ABOUT_DIR = REPO_ROOT / "about-solar-anamnesis"
LINKS_DIR = ABOUT_DIR / "links"
ENGLISH_FILE = LINKS_DIR / "index.html"
ABOUT_ENGLISH_FILE = ABOUT_DIR / "index.html"
BASE_URL = "https://blog.solaranamnesis.com/about-solar-anamnesis/links/"
ALT_PATTERN = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)" />')
HTML_TAG_PATTERN = re.compile(r'<html\b[^>]*>')
OG_LOCALE_PATTERN = re.compile(r'<meta property="og:locale" content="([^"]+)" />')
FILE_CODE_PATTERN = re.compile(r'index-([^.]+)\.html$')


def extract_common_language_codes() -> set[str]:
    def codes_in(directory: Path) -> set[str]:
        return {
            match.group(1)
            for path in directory.glob('index-*.html')
            if (match := FILE_CODE_PATTERN.search(path.name))
        }

    return codes_in(REPO_ROOT) & codes_in(ABOUT_DIR)


def extract_about_metadata(path: Path) -> tuple[str, str]:
    content = path.read_text(encoding='utf-8')
    html_tag_match = HTML_TAG_PATTERN.search(content)
    og_locale_match = OG_LOCALE_PATTERN.search(content)
    if not html_tag_match or not og_locale_match:
        raise ValueError(f'Missing lang metadata in {path}')
    return html_tag_match.group(0), og_locale_match.group(1)


def load_language_variants() -> tuple[list[tuple[str, str | None]], dict[str, tuple[str, str]]]:
    about_index = ABOUT_ENGLISH_FILE.read_text(encoding='utf-8')
    variants: list[tuple[str, str | None]] = []
    for hreflang, href in ALT_PATTERN.findall(about_index):
        if hreflang in {'en', 'x-default'}:
            variants.append((hreflang, None))
            continue
        match = FILE_CODE_PATTERN.search(href)
        if not match:
            raise ValueError(f'Could not determine file code for {hreflang}: {href}')
        variants.append((hreflang, match.group(1)))

    common_codes = extract_common_language_codes()
    variant_codes = {file_code for hreflang, file_code in variants if hreflang not in {'en', 'x-default'} and file_code}
    if common_codes != variant_codes:
        raise ValueError(
            'Language mismatch between root/about directories and about page hreflang tags: '
            f'{sorted(common_codes ^ variant_codes)}'
        )

    metadata = {'en': extract_about_metadata(ABOUT_ENGLISH_FILE)}
    for _, file_code in variants:
        if not file_code:
            continue
        metadata[file_code] = extract_about_metadata(ABOUT_DIR / f'index-{file_code}.html')

    return variants, metadata


def build_alternate_block(variants: list[tuple[str, str | None]]) -> str:
    lines = []
    for hreflang, file_code in variants:
        href = BASE_URL if file_code is None else f'{BASE_URL}index-{file_code}.html'
        lines.append(f'<link rel="alternate" hreflang="{hreflang}" href="{href}" />')
    return '\n'.join(lines)


def render_variant(template: str, html_tag: str, canonical_href: str, og_url: str, og_locale: str, alternate_block: str) -> str:
    rendered = HTML_TAG_PATTERN.sub(html_tag, template, count=1)
    rendered = re.sub(
        r'<link rel="canonical" href="[^"]+" />\n(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+" />\n?)*',
        f'<link rel="canonical" href="{canonical_href}" />\n{alternate_block}\n',
        rendered,
        count=1,
    )
    rendered = re.sub(r'<meta property="og:url" content="[^"]+" />', f'<meta property="og:url" content="{og_url}" />', rendered, count=1)
    rendered = OG_LOCALE_PATTERN.sub(f'<meta property="og:locale" content="{og_locale}" />', rendered, count=1)
    return rendered


def main() -> None:
    variants, metadata = load_language_variants()
    template = ENGLISH_FILE.read_text(encoding='utf-8')
    alternate_block = build_alternate_block(variants)

    en_lang, en_og_locale = metadata['en']
    ENGLISH_FILE.write_text(
        render_variant(template, en_lang, BASE_URL, BASE_URL, en_og_locale, alternate_block),
        encoding='utf-8',
    )

    for _, file_code in variants:
        if not file_code:
            continue
        html_lang, og_locale = metadata[file_code]
        localized_url = f'{BASE_URL}index-{file_code}.html'
        output_path = LINKS_DIR / f'index-{file_code}.html'
        output_path.write_text(
            render_variant(template, html_lang, localized_url, localized_url, og_locale, alternate_block),
            encoding='utf-8',
        )


if __name__ == '__main__':
    main()
