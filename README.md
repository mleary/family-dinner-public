# family-dinner-public

Public site for dinners we cook at home: one page per dinner with its menu card, courses, and credits, plus site-wide search. Built with Quarto.

Content in `content/dinners/` comes from the private `family-dinner` repo. Only allowlisted files are copied: `dinner.json`, `menu.png`, optional `public.md`, and listed photos. Don't add recipe text from books here.

## Preview

```
quarto preview
```

`scripts/build_pages.py` runs first and generates `dinners/<folder>/index.qmd` from each `dinner.json`. That folder is generated, so it isn't committed.

## Styling

The site has one plain look. Each dinner's theme shows up in two places only: its menu card, and the colored band at the top of its page. The band's colors and display font come from `style` in `dinner.json`.
