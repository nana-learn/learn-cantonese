# Cantonese Learner

Interactive lessons, vocab flashcards, and writing practice for learning Cantonese.

**Live site:** https://nana-learn.github.io/learn-cantonese/

## What is this?

A single-page study app covering classroom lessons with:

- **Dialogues** with Jyutping and English toggles
- **Vocab cards** and spaced-repetition flashcards
- **Grammar notes** from each lesson
- **Writing practice** for characters
- **Progress / streaks** stored in the browser (`localStorage`)

Lesson PDFs and markdown notes are also published next to the app.

## Tech Stack

- Static `index.html` (no build step)
- **GitHub Pages** for deployment

## Development

Open `index.html` in a browser, or serve the repo root:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

Push to `main` — GitHub Actions deploys automatically.
