# Translation Instructions for Solar Anamnesis

## Overview

This document provides detailed instructions for creating translated versions of the root `index.html` page of the Solar Anamnesis website. The site is a static HTML site deployed on CDN (originally exported from WordPress 5.4 — WordPress is no longer running). Each language version is a standalone HTML file that mirrors the English original with all user-visible text replaced by translated equivalents.

---

## File Naming Convention

| Language | File Name | `<html lang>` |
|----------|-----------|----------------|
| English (original) | `index.html` | `en-US` |
| French | `index-fr.html` | `fr` |
| German | `index-de.html` | `de` |
| Spanish | `index-es.html` | `es` |
| Italian | `index-it.html` | `it` |
| Portuguese | `index-pt.html` | `pt` |
| Japanese | `index-ja.html` | `ja` |
| Chinese (Simplified) | `index-zh.html` | `zh-Hans` |
| Russian | `index-ru.html` | `ru` |
| Arabic | `index-ar.html` | `ar` |
| _Other_ | `index-{ISO 639-1}.html` | `{code}` |

All translated files live in the **root directory** alongside `index.html`.

---

## Translation JSON Format

Each language has a corresponding JSON file stored in `translations/{lang}.json`. The JSON contains all translatable strings organized by section. See `CLAUDE.md` for the full JSON schema.

---

## Step-by-Step Implementation Plan

### Phase 1: Setup Translation Infrastructure

1. **Create `translations/` directory** at the repository root
2. **Save the provided JSON translation data** as `translations/fr.json` (and similarly for each language)
3. **Keep `index.html` as the canonical English source** — never modify it during translation work

### Phase 2: Generate a Translated HTML File

For each language, follow these steps (using French/`fr` as the example):

#### Step 2.1: Copy the Source File

```bash
cp index.html index-fr.html
```

#### Step 2.2: Update the `<html>` Language Attribute

Change line 2:
```html
<!-- FROM -->
<html lang="en-US">
<!-- TO -->
<html lang="fr">
```

#### Step 2.3: Update `<title>` Tags

There are **two** `<title>` tags in `<head>` (lines 6 and 13). Update both:

```html
<!-- FROM -->
<title>Solar Anamnesis | Scenes from the Solar System&#039;s Youth</title>
<!-- TO -->
<title>Solar Anamnesis | Scènes de la Jeunesse du Système Solaire</title>
```

And:
```html
<!-- FROM -->
<title>Solar Anamnesis &#8211; Scenes from the Solar System&#039;s Youth</title>
<!-- TO -->
<title>Solar Anamnesis &#8211; Scènes de la Jeunesse du Système Solaire</title>
```

#### Step 2.4: Update Navigation Menu Items

The navigation menu appears **twice** in the HTML (once in `#widgets-wrapper` around line 41-45, and once in `#site-navigation` around line 175-179). Update **both** instances:

| English | JSON key | French |
|---------|----------|--------|
| Dashboard | `navigation_main[0]` | Tableau de bord |
| About | `navigation_main[1]` | À propos |
| Gallery | `navigation_main[2]` | Galerie |
| Store | `navigation_main[3]` | Boutique |
| Panorama Gallery | `navigation_main[4]` | Galerie Panorama |

**Important:** Only change the visible link text. Do NOT change `href` URLs, `id` attributes, or `class` names.

#### Step 2.5: Update Widget Titles and Search

- **"Search"** widget title (line 46, `<h1 class="widget-title">`) → `sidebar_widgets[0]`
- **"Search Solar Anamnesis"** — the DuckDuckGo iframe `prefill` parameter (line 46) → `sidebar_widgets[1]`
- **"Meteorite Photo Categories"** widget title (line 49) → `sidebar_widgets[2]`

For the search iframe, update the `prefill` query parameter:
```html
<!-- FROM -->
prefill=Search Solar Anamnesis
<!-- TO -->
prefill=Rechercher dans Solar Anamnesis
```

#### Step 2.6: Update Meteorite Category Names

Lines 50-139 contain the category list. For each `<li>`, update only the **display text** inside the `<a>` tag. The count in parentheses and the `href` URL must remain unchanged.

Example:
```html
<!-- FROM -->
<li class="cat-item cat-item-22"><a href="https://blog.solaranamnesis.com/category/australia/">australia</a> (3)
<!-- TO -->
<li class="cat-item cat-item-22"><a href="https://blog.solaranamnesis.com/category/australia/">australie</a> (3)
```

Use the `meteorite_categories` array from the JSON, matching by position (the order matches the HTML order).

**Note:** Some category names are proper nouns or technical terms that may stay the same (e.g., "CO", "CV", "LMScope", "Nikon D810"). Use whatever the JSON provides.

#### Step 2.7: Update Accessibility & UI Strings

| English | Location | JSON source |
|---------|----------|-------------|
| `Widgets` | Line 151, `<span class="screen-reader-text">` | `navigation_elements[0]` |
| `Skip to content` | Line 173, `<a>` text | `navigation_elements[1]` |
| `Menu` | Line 172, `<h1 class="menu-toggle">` | `navigation_elements[2]` |
| `Older posts` | Line 333, `<span class="text-nav">` | `navigation_elements[3]` |
| `Post navigation` | Line 329, `<h1 class="screen-reader-text">` | (translate as appropriate) |
| `Standard` | Lines 231, 277, 323, `<span class="screen-reader-text">` | (translate as appropriate) |

#### Step 2.8: Update Site Description

Line 167:
```html
<!-- FROM -->
<h2 class="site-description">Scenes from the Solar System&#039;s Youth</h2>
<!-- TO -->
<h2 class="site-description">Scènes de la Jeunesse du Système Solaire</h2>
```

Note: The apostrophe in "System's" is encoded as `&#039;` in the English. In French, there is no possessive apostrophe in "Système Solaire", so the entity is not needed.

#### Step 2.9: Update Article Content

For each of the three articles (posts), update:

1. **Article title** in `<h1 class="entry-title">` → `articles[N].title`
2. **Category tag links** in `<span class="categories-links">` → `articles[N].categories`
3. **Date** in `<time>` element text → `articles[N].date`
   - Keep the `datetime` attribute unchanged (it's ISO 8601)
   - Update the `title` attribute on the parent `<a>` tag → `articles[N].time`
4. **Author name** — keep "solaranamnesis" unchanged (it's a username)
5. **Image caption** in `<figcaption>` → `articles[N].image_caption`
6. **Body paragraphs** in `<p>` tags → `articles[N].body_text`
   - "Beautiful thin section..." → body_text[0]
   - "Full Screen Meteorite Thin Section Panoramas:" → body_text[1]
   - "View on Gigapan" → body_text[2]
   - "View with krpano" → body_text[3]
   - "Click to Load" → body_text[4]
   - "Purchase Prints" / "Visit Store" links → see `body_text[5]` and `body_text[6]` if provided

**Important:** The "View on Gigapan | View with krpano" text has both link texts on one line separated by " | ". Replace each link text individually.

#### Step 2.10: Update Footer

Lines 346-353:

| English | French |
|---------|--------|
| `Become a Friend of GNOME` (alt text) | `Devenez ami de GNOME` |
| `[ GNU Link]` (alt text) | `Lien GNU` |
| `Proudly powered by WordPress` | `Fièrement propulsé par WordPress` |
| `Theme: Ryu by WordPress.com` | `Thème : Ryu par WordPress.com` |

#### Step 2.11: Final Validation

After all replacements:

1. **Verify the HTML is valid** — open the file in a browser and check rendering
2. **Diff against `index.html`** to ensure only text content changed:
   ```bash
   diff index.html index-fr.html
   ```
3. **Check that all URLs remain unchanged**
4. **Check that all HTML structure (tags, classes, IDs) is preserved**
5. **Check that the `<html lang="...">` attribute is correct**
6. **Spot-check character encoding** — ensure special characters (accents, etc.) display correctly

---

## Detailed Text Replacement Map

Below is the complete mapping of English text → location in HTML for the root `index.html`. Use this as a checklist when creating each translation.

### Head Section
| # | English Text | Line(s) | HTML Context |
|---|-------------|---------|--------------|
| 1 | `Scenes from the Solar System's Youth` | 6 | `<title>` (first) |
| 2 | `Scenes from the Solar System's Youth` | 13 | `<title>` (second) |

### Navigation Menu (appears twice)
| # | English Text | Lines | HTML Context |
|---|-------------|-------|--------------|
| 3 | `Dashboard` | 41, 175 | `<a>` in menu |
| 4 | `About` | 42, 176 | `<a>` in menu |
| 5 | `Gallery` | 43, 177 | `<a>` in menu |
| 6 | `Store` | 44, 178 | `<a>` in menu |
| 7 | `Panorama Gallery` | 45, 179 | `<a>` in menu |

### Widgets
| # | English Text | Line | HTML Context |
|---|-------------|------|--------------|
| 8 | `Search` | 46 | `<h1 class="widget-title">` |
| 9 | `Search Solar Anamnesis` | 46 | iframe `prefill=` parameter |
| 10 | `Meteorite Photo Categories` | 49 | `<h1 class="widget-title">` |

### Category Names (46 items)
| # | English Text | Line | HTML Context |
|---|-------------|------|--------------|
| 11-56 | (see `meteorite_categories` in JSON) | 50-139 | `<a>` text in `<li class="cat-item">` |

### UI/Accessibility Strings
| # | English Text | Line | HTML Context |
|---|-------------|------|--------------|
| 57 | `Widgets` | 151 | `<span class="screen-reader-text">` |
| 58 | `Menu` | 172 | `<h1 class="menu-toggle">` |
| 59 | `Skip to content` | 173 | `<a>` text |
| 60 | `Post navigation` | 329 | `<h1 class="screen-reader-text">` |
| 61 | `Older posts` | 333 | `<span class="text-nav">` |

### Site Header
| # | English Text | Line | HTML Context |
|---|-------------|------|--------------|
| 62 | `Scenes from the Solar System's Youth` | 167 | `<h2 class="site-description">` |

### Article 1 (NWA 980)
| # | English Text | Line | HTML Context |
|---|-------------|------|--------------|
| 63 | `NWA 980 Meteorite Thin Section` | 194 | `<h1 class="entry-title">` |
| 64 | Category tag texts | 194 | `<span class="categories-links">` |
| 65 | `April 23, 2020` | 197 | `<time>` text |
| 66 | `2:24 am` | 197 | `<a title="...">` |
| 67 | `NWA 980 Meteorite Thin Section` | 203 | `<figcaption>` |
| 68 | `Beautiful thin section...` | 207 | `<p>` |
| 69 | `Full Screen Meteorite Thin Section Panoramas:` | 211 | `<p>` |
| 70 | `View on Gigapan` | 215 | `<a>` text |
| 71 | `View with krpano` | 215 | `<a>` text |
| 72 | `Click to Load` | 220 | `<a>` text |
| 73 | `Purchase Prints` | 224 | `<p>` text |
| 74 | `Visit Store` | 228 | `<a>` text |

### Article 2 (NWA 7859 — polarized)
| # | English Text | Line | HTML Context |
|---|-------------|------|--------------|
| 75 | `NWA 7859 Meteorite Thin Section` | 240 | `<h1 class="entry-title">` |
| 76 | Category tag texts | 240 | `<span class="categories-links">` |
| 77 | `April 12, 2020` | 243 | `<time>` text |
| 78 | `5:59 pm` | 243 | `<a title="...">` |
| 79 | `NWA 7859 Meteorite Thin Section` | 249 | `<figcaption>` |
| 80 | `The same thin section...` | 253 | `<p>` |
| 81 | `Full Screen Meteorite Thin Section Panoramas:` | 257 | `<p>` |
| 82 | `View on Gigapan` | 261 | `<a>` text |
| 83 | `View with krpano` | 261 | `<a>` text |
| 84 | `Click to Load` | 266 | `<a>` text |
| 85 | `Purchase Prints` | 270 | `<p>` text |
| 86 | `Visit Store` | 274 | `<a>` text |

### Article 3 (NWA 7859 — visible light)
| # | English Text | Line | HTML Context |
|---|-------------|------|--------------|
| 87 | `NWA 7859 Meteorite Thin Section` | 286 | `<h1 class="entry-title">` |
| 88 | Category tag texts | 286 | `<span class="categories-links">` |
| 89 | `April 8, 2020` | 289 | `<time>` text |
| 90 | `9:31 pm` | 289 | `<a title="...">` |
| 91 | `NWA 7859 Meteorite Thin Section` | 295 | `<figcaption>` |
| 92 | `This visible light thin section...` | 299 | `<p>` |
| 93 | `Full Screen Meteorite Thin Section Panoramas:` | 303 | `<p>` |
| 94 | `View on Gigapan` | 307 | `<a>` text |
| 95 | `View with krpano` | 307 | `<a>` text |
| 96 | `Click to Load` | 312 | `<a>` text |
| 97 | `Purchase Prints` | 316 | `<p>` text |
| 98 | `Visit Store` | 320 | `<a>` text |

### Footer
| # | English Text | Line | HTML Context |
|---|-------------|------|--------------|
| 99 | `Become a Friend of GNOME` | 348 | `<img alt="...">` |
| 100 | `[ GNU Link]` | 349 | `<img alt="...">` |
| 101 | `Proudly powered by WordPress` | 350 | `<a>` text |
| 102 | `Theme: Ryu by` | 352 | text node |
| 103 | `WordPress.com` | 352 | `<a>` text (keep as-is, it's a proper noun/brand) |

### Screen Reader / Format Badges
| # | English Text | Lines | HTML Context |
|---|-------------|-------|--------------|
| 104 | `Standard` | 231, 277, 323 | `<span class="screen-reader-text">` inside `.entry-format-badge` |

---

## Automation Approach (Recommended)

For generating translated files programmatically:

1. **Parse `index.html`** as a text file (not DOM, to preserve exact formatting)
2. **Apply a series of find-and-replace operations** using the text replacement map above
3. **Use the JSON translation data** as the source of replacement strings
4. **Write the result** to `index-{lang}.html`

### Important Notes on Find-and-Replace

- Some strings appear multiple times (e.g., navigation menu appears twice, "Full Screen Meteorite Thin Section Panoramas:" appears three times). Ensure **all** instances are replaced.
- Some strings appear in different HTML contexts (e.g., article titles appear in both `<h1>` and `<figcaption>`). The same translated string applies to both.
- Be careful with partial matches — e.g., "NWA 7859 Meteorite Thin Section" appears multiple times but in different articles. Use surrounding HTML context to disambiguate if needed.
- Special characters: Use proper HTML entities or UTF-8 encoding as needed. The file uses UTF-8 (`<meta charset="UTF-8" />`).

### Suggested Script Pseudocode

```
for each language in [fr, de, es, ...]:
    translations = load_json(f"translations/{lang}.json")
    html = read_file("index.html")

    # 1. Update html lang attribute
    html = replace('lang="en-US"', f'lang="{lang_code}"')

    # 2. Update titles
    html = replace(english_title, translations.website_title)

    # 3. Update navigation (both instances)
    for i, nav_item in enumerate(english_nav):
        html = replace_all(nav_item, translations.navigation_main[i])

    # 4. Update widget titles
    ...

    # 5. Update categories (careful: match by surrounding HTML)
    ...

    # 6. Update article content
    ...

    # 7. Update footer
    ...

    write_file(f"index-{lang}.html", html)
```

---

## Adding a New Language

To add a new language translation:

1. Prepare a translation JSON file following the schema in `CLAUDE.md`
2. Save it as `translations/{lang}.json`
3. Follow the Step-by-Step process in Phase 2 above
4. Add the new language to the file naming table in this document
5. Optionally add a language selector to the site (future enhancement)

---

## Future Enhancements (Out of Scope for Now)

- **Language selector widget** — Add a dropdown or flag icons to switch between languages
- **Subdirectory translations** — Translate individual blog post pages in `/2015/`, `/2016/`, etc.
- **Hreflang tags** — Add `<link rel="alternate" hreflang="fr" href="index-fr.html" />` tags to each page for SEO
- **RTL support** — For Arabic (`ar`) and Hebrew (`he`), add `dir="rtl"` to `<html>` tag
- **Automated CI validation** — GitHub Action to validate translated files haven't drifted from the English structure
