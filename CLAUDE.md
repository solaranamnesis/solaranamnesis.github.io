# CLAUDE.md — Project Context for AI Agents

## Project Overview

**Solar Anamnesis** (`solaranamnesis.github.io`) is a static website deployed on CDN via GitHub Pages. It was originally a WordPress 5.4 blog (Ryu theme) about meteorite thin-section photography, which has been exported to fully static HTML. WordPress is no longer running — the site serves purely static HTML with no build system, no static site generator, no JavaScript framework, and no server-side rendering.

## Repository Structure

```
/                           ← Root of the GitHub Pages site
├── index.html              ← Main homepage (paginated blog, page 1)
├── README.md
├── robots.txt
├── sitemap.html
├── sitemap.xml
├── xmlrpc.php              ← WordPress artifact (static)
├── about-solar-anamnesis/  ← About page
├── author/                 ← Author archive pages
├── category/               ← Category archive pages
├── feed/                   ← RSS feed
├── page/                   ← Paginated blog pages (page/2/, page/3/, etc.)
├── wp-content/             ← WordPress theme assets, uploads, images
├── wp-includes/            ← WordPress core JS/CSS assets
├── wp-json/                ← WordPress REST API artifact (static)
├── linux-commands/         ← Misc content
├── 2015/ ... 2020/         ← Individual blog post pages organized by date
│   └── MM/DD/post-slug/index.html
└── CLAUDE.md               ← This file
```

## Key Technical Details

- **Hosting:** Static site deployed on CDN via GitHub Pages
- **History:** Originally a WordPress 5.4 site (Ryu theme), exported to fully static HTML and now served as a pure static site on CDN. WordPress is no longer running — all references to `blog.solaranamnesis.com` and WordPress artifacts (e.g., `xmlrpc.php`, `wp-json/`) are remnants of the export.
- **No build system:** No `package.json`, no `_config.yml`, no static site generator, no server-side processing
- **All HTML is static** — edits are made directly to `.html` files
- **External assets:** CSS, JS, fonts, and some images are loaded from `blog.solaranamnesis.com` and CDNs (jQuery, Google Fonts)
- **Content images** are served from both `blog.solaranamnesis.com/wp-content/uploads/` and `cdn.solaranamnesis.com/`
- **Panorama viewers:** Posts embed krpano and Gigapan panorama viewers via iframes

## Root `index.html` Structure

The root `index.html` is a ~27KB WordPress-exported HTML page with these sections:

1. **`<head>`** — Meta tags, title, stylesheets, scripts
2. **Widgets panel** (`#widgets-wrapper`) — Collapsible top panel containing:
   - Navigation menu (Dashboard, About, Gallery, Store, Panorama Gallery)
   - Search widget (DuckDuckGo iframe)
   - Meteorite Photo Categories sidebar (46 categories with counts)
3. **Triggers** (`#triggers-wrapper`) — Widget toggle button
4. **Header** (`#masthead`) — Site logo, title ("Solar Anamnesis"), description ("Scenes from the Solar System's Youth"), and main navigation menu (duplicated from widgets)
5. **Main content** (`#main`) — Three article entries (blog posts) with:
   - Category tags
   - Post title
   - Date and author
   - Featured image with caption
   - Body text
   - Panorama viewer links (Gigapan, krpano)
   - Embedded krpano iframe with click-to-load
   - Store/purchase links
6. **Post navigation** — "Older posts" link
7. **Footer** (`#colophon`) — GNOME friend badge, GNU link, WordPress credit, theme credit
8. **Scripts** — Inline JS for iframe loading, plus theme JS files

## Translation Approach

Translations are implemented as separate static HTML files at the root level:

- `index.html` — English (original, canonical)
- `index-fr.html` — French
- `index-de.html` — German
- `index-{lang}.html` — Other languages as needed

Each translated file is a full copy of `index.html` with text content replaced according to a JSON translation file. The HTML structure, CSS classes, IDs, URLs, and image sources remain identical.

### What to Translate

- Page `<title>` tags
- Site title and description text
- Navigation menu link text
- Widget titles and search placeholder text
- Category names (display text only, not URLs or slugs)
- Article titles, dates, body paragraphs, image captions
- Footer text
- Accessibility/screen-reader text (e.g., "Skip to content", "Widgets", "Menu", "Post navigation")
- Navigation text ("Older posts")

### What NOT to Translate

- HTML tags, attributes, CSS classes, or IDs
- URLs, `href` values, `src` values
- Image filenames or CDN paths
- WordPress CSS/JS asset paths
- HTML entities that are structural (e.g., `&larr;`)
- The site name "Solar Anamnesis" (proper noun, keep as-is)
- Author name "solaranamnesis"
- Technical identifiers: post IDs, menu item IDs, category slugs
- Equipment/software names that are proper nouns (e.g., "Nikon D810", "Nikon Z6", "LMScope", "zerene stacker" — though these may have translated display names per the JSON)

## Translation JSON Format

Translation data is provided as a JSON object with these top-level keys:

```json
{
  "extraction_date": "...",
  "source_file": "...",
  "website_title": "Site title | subtitle",
  "navigation_main": ["nav item 1", "nav item 2", ...],
  "sidebar_widgets": ["widget title 1", "search placeholder", ...],
  "meteorite_categories": [{"name": "...", "count": N}, ...],
  "articles": [
    {
      "title": "...",
      "date": "...",
      "time": "...",
      "author": "...",
      "categories": ["...", ...],
      "body_text": ["paragraph 1", "paragraph 2", ...],
      "image_caption": "..."
    }
  ],
  "site_metadata": {
    "platform": "...",
    "theme": "...",
    "site_description": "...",
    "footer_links": ["...", ...]
  },
  "navigation_elements": ["...", ...],
  "all_plain_text_strings": ["...", ...]
}
```

## Commands

- **Lint/Build/Test:** None — this is a static HTML site deployed on CDN with no build system
- **History:** Exported from WordPress 5.4 to static HTML; WordPress is no longer running
- **Validation:** Use an HTML validator or browser to check translated files render correctly
- **Diff check:** Compare translated file structure against `index.html` to ensure only text was changed

## Conventions

- File naming: `index-{ISO 639-1 language code}.html` (e.g., `index-fr.html`, `index-de.html`, `index-es.html`)
- The `<html lang="...">` attribute must be updated to match the target language (e.g., `lang="fr"` for French)
- Keep all whitespace, indentation, and line structure identical to the English original
- Translation JSON files should be stored in a `translations/` directory as `{lang}.json`
- Category counts must remain unchanged (they are data, not text)
- Dates should be formatted per the target language conventions
