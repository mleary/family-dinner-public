# family-dinner-public

Public site for dinners we cook at home: one page per dinner with its menu card, courses, and credits, plus site-wide search. Built with Quarto.

Content in `content/dinners/` is written by the private `family-dinner` repo's sync workflow. Don't edit it by hand: the next sync replaces the whole folder. Each dinner has only allowlisted files: `dinner.json`, `menu.jpg`, optional `public.md`, and `photos/*.jpg`. Upcoming dinners appear as soon as they're pushed to the private repo. The home page lists dinners by dinner date, newest first.

## Preview

```
quarto preview
```

`scripts/build_pages.py` runs first and generates `dinners/<folder>/index.qmd` from each `dinner.json`. That folder is generated, so it isn't committed.

## Styling

The site has one plain look. Each dinner's theme shows up in two places only: its menu card, and the colored band at the top of its page. The band's colors and display font come from `style` in `dinner.json`.
