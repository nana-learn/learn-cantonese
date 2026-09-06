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

## How to study

Start on **Everyday L1–L15** (Hong Kong spoken Cantonese). Do them in order:

| Lesson | What you get |
|--------|----------------|
| L1 基礎 | Hello, names, eat / drink |
| L2 日常 | Time, work, shopping, MTR |
| L3 生活 | Weather, food, feeling ill, travel |
| L4 進階 | Opinions, comparing, renting |
| L5 聲調 | The 6 tones (si1–si6, 買 vs 賣) |
| L6 數字同錢 | Numbers, 蚊, Octopus, change |
| L7 屋企人 | Family, partners, 幾耐 |
| L8 飲茶 | Dim sum, 埋單, treating |
| L9 問路 | Where, left/right, getting lost |
| L10 約出嚟 | Making plans, running late |
| L11 一日 | Daily routine, 先至, 攰 |
| L12 身體感覺 | Sick, tired, angry, 請假 |
| L13 語氣助詞 | 喇啦喎啫咩嘅咋啩囉 — how Cantonese actually feels |
| L14 做咗做緊 | Aspect: done / doing / ever / will |
| L15 量詞 | Classifiers 個隻件杯間條張本 |
| L16 問句 | 邊個幾時點解點樣、有冇、可唔可以 |
| L17 覆訊 | Call, reply, 聽唔到, 得閒先覆 |
| L18 天氣 | 悶熱、落雨、掛波、着多件 |
| L19 形容 | 大細新舊、啲 / 比 / 最 |
| L20 開口講 | Speak slower, 即係, 聽唔明 |

**Course 1–11** is later: longer classroom dialogues (interviews, work, culture).

For each lesson: listen to the dialogue → flip vocab → drill flashcards → read grammar → quiz / match / write.

Lesson PDFs and markdown notes for the course track are also in the repo.

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
