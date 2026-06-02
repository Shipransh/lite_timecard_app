# Genpact Brand Playbook (v0.5) — **Design Reference Packet**

> **Source of truth for this packet:** <File>Genpact_Brand.pdf</File> (Brand Playbook, Version 0.5). citeturn1search1turn2search3  
> **Related internal file found:** <File>Genpact-playbook-v-0-5.pdf</File> appears to be the same playbook version hosted in enterprise storage. citeturn2search6  

This document is a **developer- and builder-oriented extraction** of everything in the playbook that pertains to **design**: logo, clear space, co-branding, wayfinder grid, color palette & hierarchy, color flood/accent combinations, typography (font, weights, alignment, line heights, color rules, misuse), imagery style guidance, and brand-in-video specifications.

> **Note on visuals:** Several sections of the playbook are primarily visual layouts (e.g., PowerPoint templates, signage, business card, email signature, video-call backgrounds). The PDF text extract does not include the full detailed specs for those pages beyond the headings shown; where that occurs, this packet **only states what is explicitly present** in the source and marks visual-only items accordingly. citeturn1search1turn2search3

---

## Table of Contents

1. [Core Design Components](#core-design-components)
2. [Logo System](#logo-system)
   1. [Minimum Size](#minimum-size)
   2. [Clear Space](#clear-space)
   3. [Icon Clear Space](#icon-clear-space)
   4. [Icon as Graphic Device](#icon-as-graphic-device)
   5. [Co-branding](#co-branding)
   6. [Acquisitions / Sub-brand Identifier](#acquisitions--sub-brand-identifier)
   7. [Logo Misuse](#logo-misuse)
   8. [AI Innovation Center Logo](#ai-innovation-center-logo)
3. [Wayfinder System (Grid)](#wayfinder-system-grid)
4. [Color System](#color-system)
   1. [Palette (HEX / RGB / CMYK / PMS / RAL)](#palette-hex--rgb--cmyk--pms--ral)
   2. [Color Hierarchy](#color-hierarchy)
   3. [Color Flood & Accent Combinations](#color-flood--accent-combinations)
5. [Typography System](#typography-system)
   1. [Typeface](#typeface)
   2. [Weights](#weights)
   3. [Alignment](#alignment)
   4. [Line Heights & Spacing](#line-heights--spacing)
   5. [Typography Color Combinations](#typography-color-combinations)
   6. [Typography Misuse](#typography-misuse)
6. [Imagery System](#imagery-system)
7. [Brand in Video (Motion + On-screen Text)](#brand-in-video-motion--on-screen-text)
   1. [Opening Frame](#opening-frame)
   2. [Opening Frame (Co-branding)](#opening-frame-co-branding)
   3. [End Frame](#end-frame)
   4. [Text On Screen — Basic](#text-on-screen--basic)
   5. [Text On Screen — Expressive](#text-on-screen--expressive)
   6. [Text On Screen — On Imagery](#text-on-screen--on-imagery)
   7. [Transitions](#transitions)
   8. [People On Screen](#people-on-screen)
   9. [Lower Third + Logo Bug](#lower-third--logo-bug)
8. [Brand in Action (Templates / Applications)](#brand-in-action-templates--applications)
9. [Implementation Packs (Design Tokens)](#implementation-packs-design-tokens)
   1. [CSS Variables](#css-variables)
   2. [JSON Tokens](#json-tokens)
   3. [Suggested UI Token Mapping (Non-source)](#suggested-ui-token-mapping-non-source)
10. [Quick Compliance Checklist](#quick-compliance-checklist)

---

# Core Design Components

The playbook’s design toolkit and brand platform include the following design-relevant sections and outputs:

- **Logo & Icon** (including clear space, minimum size, icon usage, co-branding, acquisitions, misuse). citeturn1search1turn2search3  
- **Wayfinder device** (grid foundation and application). citeturn1search1turn2search3  
- **Color palette**, plus **color hierarchy** and **color flood & accent combinations**. citeturn1search1turn2search3  
- **Typography** (typeface, weights, alignment rules, line heights, permitted color combos, misuse). citeturn1search1turn2search3  
- **Imagery** (style & quality). citeturn1search1turn2search3  
- **Video guidelines** (opening/end frames, text-on-screen, transitions, framing people, lower third, logo bug). citeturn1search1turn2search3  
- **Brand in action** output templates (PowerPoint light/dark, signage, business card, email signature, video call backgrounds) are present as pages/titles. citeturn1search1turn2search3  

---

# Logo System

## Minimum Size

- **Minimum logo size:** `50px` (explicitly stated). citeturn1search1turn2search3

---

## Clear Space

The playbook includes a dedicated page for **logo clear space & minimum size**. The only explicit numeric detail in extracted text is the **minimum size (50px)**. citeturn1search1turn2search3

> Where the playbook’s clearspace is illustrated visually but not described in extracted text, follow the artwork in the source file as the authority. citeturn1search1turn2search3

---

## Icon Clear Space

When using the logo **icon** as an icon:

- Leave at least **space of two diamonds** from the **sides**.
- Leave at least **one-and-a-half diamonds** from the **top or bottom**. citeturn1search1turn2search3

---

## Icon as Graphic Device

The playbook explicitly allows leveraging the **“G”** as a **graphic device**:

- Use as a dynamic graphical element to create engaging layouts.
- **Crop rule:** crop the device **halfway between the inside and outside elements** of the shape.
- **Stroke rule:** match the stroke to the **weight of the logo used** in the design to maintain harmony and prevent it from looking too heavy/light. citeturn1search1turn2search3

---

## Co-branding

When showing a partnership:

- Place a **vertical bar** between the two logos, allowing correct clear space from Genpact’s logo.
- **Visually balance** the two logos in size (no strict metric; should “feel balanced”).
- The separating line’s **stroke weight is always one-third** of the stroke weight of the **“G”** logo. citeturn1search1turn2search3

---

## Acquisitions / Sub-brand Identifier

When a Genpact acquisition/relationship has its own established logo:

- Acquired/related logos should appear in their **original colors**.
- Genpact logo appears underneath the main logo (all lower case) with the words **“a genpact company”**.
- The “a genpact company” line is in **black or white**, depending on background color.
- Spacing examples show cases where Genpact identifier is left- or right-aligned with **spacing fractions (e.g., 1/3 of X or 2/3 of X)** to accommodate low-hanging elements. citeturn1search1turn2search3

---

## Logo Misuse

The playbook provides explicit “avoid” guidance:

- Don’t use the word “genpact” without the icon.
- Don’t rearrange the logo and icon.
- Don’t rotate the logo or icon.
- Don’t crop the logo and icon when they’re together (icon cropping is permitted when used as an icon/graphic).
- Don’t recolor the logo or icon.
- Don’t place on backgrounds without adequate contrast.
- Don’t change the perspective of the logo.
- Don’t squash/distort.
- Don’t add effects.
- Don’t put more than one logo/icon in close proximity.
- Don’t obscure the logo with other visual elements.
- Don’t use the logo or icon with companies Genpact has acquired (handled via the acquisitions rule instead). citeturn1search1turn2search3

---

## AI Innovation Center Logo

The playbook includes a dedicated section for **Genpact AI Innovation Center** logos:

- Two logo variants are shown: **Linear** and **Stacked**.
- The separating line’s stroke weight is always **one-third** of the stroke weight of the **“G”** logo. citeturn1search1turn2search3

---

# Wayfinder System (Grid)

## What it is

- The **Wayfinder device** is derived from the logo.
- It forms the foundation of a **tech-inspired grid system**. citeturn1search1turn2search3

## How it behaves

- The Wayfinder grid is **always inward-facing**.
- Its purpose is to align content to:
  - emphasize messaging, and
  - subtly direct focus to key points. citeturn1search1turn2search3

## Standard aspect ratio

- Examples are shown using **16:9**. citeturn1search1turn2search3

---

# Color System

## Palette (HEX / RGB / CMYK / PMS / RAL)

> The playbook lists the palette with multiple color system representations. citeturn1search1turn2search3

### Core / Neutrals

- **Midnight**
  - HEX: `#161916`
  - RGB: `22/25/22`
  - CMYK: `12/0/12/90`
  - “Black 3C/U”
  - RAL: `000 20 00` (“Slate Black”) citeturn1search1turn2search3

- **Morning White**
  - HEX: `#FFFFFF`
  - RGB: `255/255/255`
  - CMYK: `0/0/0/0` citeturn1search1turn2search3

- **First Light 01**
  - HEX: `#444744`
  - RGB: `68/71/68`
  - CMYK: `4/0/4/72`
  - RAL: `000 35 00` (“Briquette Grey”) citeturn1search1turn2search3

- **First Light 02**
  - HEX: `#6D706B`
  - RGB: `109/112/107`
  - CMYK: `3/0/4/56`
  - RAL: `000 55 00` (“Medium Grey”) citeturn1search1turn2search3

- **First Light 03**
  - HEX: `#ADB1AC`
  - RGB: `173/177/172`
  - CMYK: `2/0/3/31`
  - RAL: `000 70 00` (“Light Grey”) citeturn1search1turn2search3

### Warm Neutrals

- **Sunrise White**
  - HEX: `#FFFAF4`
  - RGB: `255/250/244`
  - CMYK: `0/2/4/0`
  - PMS: “not available”
  - RAL: `070 93 05` (“Anemone White”) citeturn1search1turn2search3

- **Sunrise Cream**
  - HEX: `#FFF2DF`
  - RGB: `255/242/223`
  - CMYK: `0/5/13/0`
  - PMS: `9225C` / `9184U`
  - RAL: `070 90 05` (“Off White”) citeturn1search1turn2search3

### Accents

- **Coral**
  - HEX: `#FF555F`
  - RGB: `255/85/95`
  - CMYK: `0/75/43/0`
  - PMS: `1785 C/U`
  - RAL: “Not available (use paint mix from PMS)” citeturn1search1turn2search3

- **Sunrise Gold**
  - HEX: `#FFAD28`
  - RGB: `255/173/40`
  - CMYK: `0/30/85/0`
  - PMS: `1235 C` / `116 U`
  - RAL: `080 80 90` (“Summer Yellow”) citeturn1search1turn2search3

---

## Color Hierarchy

The playbook includes a page explicitly titled “Color hierarchy” and distinguishes:

- **Primary palette**
- **Secondary palette** citeturn1search1turn2search3

> The exact mapping of which swatches are primary vs secondary is shown visually; the palette itself is listed explicitly above. citeturn1search1turn2search3

---

## Color Flood & Accent Combinations

The playbook provides example combinations grouped by background contexts:

- **On Midnight backgrounds** — includes Sunrise White / First Light 03 / First Light 01 with **Coral (accent)**.
- **On Morning White backgrounds** — includes Sunrise Cream / Morning White / First Light 02 with **Sunrise Gold (accent)**.
- **On Sunrise White backgrounds** — multiple variants shown, including combinations of First Light 03 / First Light 01 / Sunrise Cream / First Light 02 with **Coral (accent)** and/or **Sunrise Gold (accent)**.
- A note indicates: “*See typography section for permitted color combinations*.” citeturn1search1turn2search3

> These are presented visually as recommended “flood” backgrounds with accent highlights. Follow the referenced typography color rules for text-on-background permission. citeturn1search1turn2search3

---

# Typography System

## Typeface

- Primary typeface: **Funnel Sans** (modern sans-serif).
- The playbook describes it as:
  - inspired by movement and shapes of data points,
  - functional yet personal,
  - featuring both square and circular shapes in letterforms.
- Download is explicitly referenced at: `https://fonts.google.com/specimen/Funnel+Sans`. citeturn1search1turn2search3

External reference (same font page): <External>Funnel Sans - Google Fonts</External>. citeturn2search16

---

## Weights

The playbook lists:

- Funnel Sans Variable
- Funnel Sans Light
- Funnel Sans Regular
- Funnel Sans Medium
- Funnel Sans Semi Bold
- Funnel Sans Bold
- Funnel Sans Extra Bold citeturn1search1turn2search3

---

## Alignment

The playbook explicitly allows only:

- **Left-aligned** typography
- **Centered** typography citeturn1search1turn2search3

---

## Line Heights & Spacing

- **Headlines** are set in **Funnel Sans Bold** with **100% line heights**.
- **Supporting copy** is in **Funnel Sans** with **120% line heights**, **regular spacing**. citeturn1search1turn2search3

---

## Typography Color Combinations

The playbook includes a page titled “Color combinations” in the typography section. Examples shown include:

- On **Midnight backgrounds**:
  - Headline in **White**
  - Body copy in **White**
  - Accent/headline elements using **Coral**
  - Small headline using **Coral** with Midnight body copy (as shown in examples) citeturn1search1turn2search3

- On **white / Sunrise White backgrounds**:
  - Headline treatment shown with dark text (Midnight) on light backgrounds in examples
  - Sunrise Gold appears as a headline color in some examples citeturn1search1turn2search3

> Because the combinations are partially shown as visuals, treat the typography “Color combinations” page as the source of truth for exact allowed pairings. citeturn1search1turn2search3

---

## Typography Misuse

The playbook lists “things to avoid”:

- Don’t right align text.
- Don’t run text in **Sunrise Gold** on anything but a **Midnight** background.
- Don’t use tight leading.
- Don’t use sizes that are too similar together.
- Don’t rotate typography.
- Don’t use other fonts (even for campaigns).
- Don’t use all caps in headline.
- Don’t use color in body copy. citeturn1search1turn2search3

---

# Imagery System

## Style & Quality

- Imagery is a key source of **vibrancy**.
- While black and white provide a bold foundation, visuals introduce **dynamic pops of color**.
- Imagery adds contrast and energy; core colors maintain a clean, sophisticated look. citeturn1search1turn2search3

## Composition guidance

- Imagery should show the **scope and scale** of Genpact’s impact.
- Photography should be **modern, clear, and optimistic**.
- Avoid strong perspective lines.
- Prefer lots of **parallel lines** to create calm; drama comes from **scale**. citeturn1search1turn2search3

---

# Brand in Video (Motion + On-screen Text)

## Opening Frame

- Use at the beginning of Genpact videos.
- Video begins with a **Midnight** screen.
- Logo fades in.
- Motion description:
  - Logo **ease in and ease out**.
  - **Fast to slow**.
  - Opacity **0% → 100%**. citeturn1search1turn2search3

---

## Opening Frame (Co-branding)

- Use at the beginning of co-branded Genpact videos.
- Video begins with **Midnight**.
- Genpact logo fades in, then moves left.
- Partner logo and dividing line fade in.
- Motion description:
  - Genpact logo ease in/out, fast-to-slow, opacity **0% → 100%**.
  - Partner logo ease in/out, fast-to-slow, opacity **0% → 100%**. citeturn1search1turn2search3

---

## End Frame

- Use at the end of Genpact videos.
- Ends with logo on screen before fading out.
- Motion description:
  - Logo ease out and ease in.
  - Fast to slow.
  - Opacity **100% → 0%**. citeturn1search1turn2search3

---

## Text On Screen — Basic

The playbook shows basic text frames:

- Centered text frames:
  - Midnight background with **white text**, or
  - White background with **Midnight text**.
- Left aligned text frames:
  - Midnight background with **white text**, or
  - White background with **Midnight text**.
- For numbered points:
  1. Left-aligned text
  2. Numbered points
  3. Avoid using more than **3 points** citeturn1search1turn2search3

---

## Text On Screen — Expressive

Expressive text frames:

- 01–02: centered expressive text on:
  - Midnight background with white text, or
  - White background with Midnight text.
- 03–04: centered expressive text on:
  - Midnight background with **Sunrise Gold** and **white** text, or
  - White background with Midnight text. citeturn1search1turn2search3

---

## Text On Screen — On Imagery

Rules for text on footage/imagery:

- 01–02: centered expressive text on dark and light imagery (respectively):
  - Set text in **white**.
  - Use drop shadow with:
    - Position: `X0 Y0`
    - Blur: `15`
    - Colour: **Midnight**
    - Opacity: `60%`
- 03: centered expressive text on very bright imagery:
  - Set text in **Midnight**.
  - Avoid drop shadow on very bright imagery (creates a “grubby effect”).
- 04:
  - Avoid text over complex images due to low contrast/readability. citeturn1search1turn2search3

---

## Transitions

Two transition examples:

- **“Genpact icon zoom in”**:
  - Quick zoom into the icon.
  - Ends with dissolve.
- **“Genpact icon grow”**:
  - Quick scaling of icon from bottom-left to top-right.
  - Ends with dissolve. citeturn1search1turn2search3

---

## People On Screen

Composition guidance:

- Use the **rule of thirds** for framing.
- Position subject off-center along a vertical line.
- Place the subject’s eyes on one of the top third nodes.
- Have the subject face the opposite side of the frame. citeturn1search1turn2search3

---

## Lower Third + Logo Bug

The playbook defines a consistent “Titles with Wayfinder” approach:

### Lower third
- Text background: **Midnight** with **50% opacity**.
- Edge: **35 degree angle**.
- Wayfinder device: **Sunrise Gold**.
- Text: **White**, set in **Funnel Sans Bold and Light**. citeturn1search1turn2search3

### Logo bug
- Appears as a **white watermark** over footage in bottom right corner.
- Opacity: **75%**.
- White is preferred for contrast on most backgrounds. citeturn1search1turn2search3

---

# Brand in Action (Templates / Applications)

The playbook includes “Brand in action” pages titled:

- PowerPoint: **light mode** citeturn1search1turn2search3
- PowerPoint: **dark mode** citeturn1search1turn2search3
- **Signage** citeturn1search1turn2search3
- **Business card** citeturn1search1turn2search3
- **Email signature** citeturn1search1turn2search3
- **Video call backgrounds** citeturn1search1turn2search3

> These pages appear primarily visual in the provided text extraction; refer to the layouts inside <File>Genpact_Brand.pdf</File> for exact spacing, sizing, and positioning specifics. citeturn1search1turn2search3

---

# Implementation Packs (Design Tokens)

Everything in this section is **derived from explicit palette values** in the playbook. citeturn1search1turn2search3

## CSS Variables

```css
:root {
  /* Core */
  --gp-midnight: #161916;
  --gp-morning-white: #FFFFFF;

  /* Neutrals */
  --gp-first-light-01: #444744;
  --gp-first-light-02: #6D706B;
  --gp-first-light-03: #ADB1AC;

  /* Warm neutrals */
  --gp-sunrise-white: #FFFAF4;
  --gp-sunrise-cream: #FFF2DF;

  /* Accents */
  --gp-coral: #FF555F;
  --gp-sunrise-gold: #FFAD28;
}

/* Typography */
@font-face {
  /* Use Funnel Sans via Google Fonts or local hosting per your build setup */
}

body {
  font-family: "Funnel Sans", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

.gp-headline {
  font-weight: 700; /* Funnel Sans Bold */
  line-height: 1.0; /* 100% */
}

.gp-body {
  font-weight: 400; /* Funnel Sans Regular */
  line-height: 1.2; /* 120% */
}
```

Typeface/line-height rules above are explicitly defined in the playbook. citeturn1search1turn2search3

## JSON Tokens

```json
{
  "color": {
    "midnight": {"hex": "#161916", "rgb": [22, 25, 22], "cmyk": [12, 0, 12, 90]},
    "morningWhite": {"hex": "#FFFFFF", "rgb": [255, 255, 255], "cmyk": [0, 0, 0, 0]},

    "firstLight01": {"hex": "#444744", "rgb": [68, 71, 68], "cmyk": [4, 0, 4, 72]},
    "firstLight02": {"hex": "#6D706B", "rgb": [109, 112, 107], "cmyk": [3, 0, 4, 56]},
    "firstLight03": {"hex": "#ADB1AC", "rgb": [173, 177, 172], "cmyk": [2, 0, 3, 31]},

    "sunriseWhite": {"hex": "#FFFAF4", "rgb": [255, 250, 244], "cmyk": [0, 2, 4, 0]},
    "sunriseCream": {"hex": "#FFF2DF", "rgb": [255, 242, 223], "cmyk": [0, 5, 13, 0]},

    "coral": {"hex": "#FF555F", "rgb": [255, 85, 95], "cmyk": [0, 75, 43, 0]},
    "sunriseGold": {"hex": "#FFAD28", "rgb": [255, 173, 40], "cmyk": [0, 30, 85, 0]}
  },
  "typography": {
    "family": "Funnel Sans",
    "headline": {"weight": "Bold", "lineHeight": "100%", "alignment": ["left", "center"]},
    "body": {"weight": "Regular", "lineHeight": "120%", "alignment": ["left", "center"]}
  }
}
```

Palette and typography source values are from the playbook. citeturn1search1turn2search3

## Suggested UI Token Mapping (Non-source)

> The following is a **practical suggestion** for application builds and decks. It is **not explicitly specified** by the playbook; it is a mapping approach you can adopt for consistency.

- `background/default` → `--gp-morning-white` (light UI) or `--gp-midnight` (dark UI)
- `text/primary` → `--gp-midnight` (on light) or `--gp-morning-white` (on dark)
- `text/secondary` → `--gp-first-light-01` / `--gp-first-light-02`
- `surface/subtle` → `--gp-sunrise-white` / `--gp-sunrise-cream`
- `accent/primary` → `--gp-coral`
- `accent/secondary` → `--gp-sunrise-gold`

---

# Quick Compliance Checklist

Use this as a pre-flight check before shipping UI, decks, or motion.

## Logo

- [ ] Logo is **≥ 50px**. citeturn1search1turn2search3
- [ ] Icon clear space respected (2 diamonds sides; 1.5 diamonds top/bottom when used as icon). citeturn1search1turn2search3
- [ ] No recoloring, rotation, distortion, effects, or low-contrast placement. citeturn1search1turn2search3

## Co-branding

- [ ] Vertical divider used; divider stroke = **1/3** “G” stroke.
- [ ] Logos feel balanced; neither dominates. citeturn1search1turn2search3

## Wayfinder

- [ ] Grid is inward-facing and supports content emphasis.
- [ ] 16:9 layouts follow the playbook examples. citeturn1search1turn2search3

## Typography

- [ ] Funnel Sans only; no substitutes.
- [ ] Headline: Bold + 100% line-height.
- [ ] Body: Funnel Sans + 120% line-height.
- [ ] Only left or centered alignment.
- [ ] No all-caps headlines; no colored body text.
- [ ] Sunrise Gold text appears only on Midnight background. citeturn1search1turn2search3

## Color

- [ ] Only palette colors are used.
- [ ] Accent colors used as accents (not as body copy).
- [ ] Flood/accent combinations align with playbook examples and typography combo constraints. citeturn1search1turn2search3

## Video

- [ ] Opening begins on Midnight; logo fades in 0→100 with ease in/out.
- [ ] End frame fades out 100→0.
- [ ] Text-on-imagery uses correct shadow specs and avoids complex images.
- [ ] Lower third matches Midnight@50%, 35° edge, Wayfinder in Sunrise Gold, white Funnel Sans type; logo bug is white@75% bottom-right. citeturn1search1turn2search3

---

## Appendix: Where these rules live in the playbook

These sections are explicitly present in <File>Genpact_Brand.pdf</File> as headings and/or described content:

- Logo & Icon overview, clear space, icon clear space, icon as graphic, co-branding, wayfinder, acquisitions, logo misuse, AI Innovation Center. citeturn1search1turn2search3
- Color palette, color hierarchy, color flood & accent combinations. citeturn1search1turn2search3
- Typography overview, alignment, color combinations, typography misuse. citeturn1search1turn2search3
- Imagery style & quality. citeturn1search1turn2search3
- Video guidelines: opening/end frames, text treatments, transitions, people on screen, lower third + logo bug. citeturn1search1turn2search3
- Brand in action templates: PowerPoint light/dark, signage, business card, email signature, video call backgrounds. citeturn1search1turn2search3
