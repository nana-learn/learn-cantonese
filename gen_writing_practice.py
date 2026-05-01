#!/usr/bin/env python3
"""Generate Chinese character writing practice PDF for Lesson 10.

Format: each vocabulary word gets a section with the word, Jyutping, meaning,
and practice grids for each character in the word.
Grid cells with a gray reference character for tracing, plus blank cells.
"""

from fpdf import FPDF
import os, glob
import warnings
warnings.filterwarnings("ignore")

# ── Lesson 10 vocabulary ──────────────────────────────────────────────
WORDS = [
    ("溝通", "kau1 tung1", "communication"),
    ("表達", "biu2 daat6", "to express"),
    ("重點", "zung6 dim2", "key point"),
    ("清晰", "cing1 sik1", "clear"),
    ("誤會", "ng6 wui6", "misunderstanding"),
    ("提升", "tai4 sing1", "to improve"),
    ("能力", "nang4 lik6", "ability"),
    ("關鍵", "gwaan1 gin6", "key; crucial"),
    ("目的", "muk6 dik1", "purpose"),
    ("思路", "si1 lou6", "train of thought"),
    ("整理", "zing2 lei5", "to organize"),
    ("觀點", "gun1 dim2", "viewpoint"),
    ("補充", "bou2 cung1", "to supplement"),
    ("細節", "sai3 zit3", "details"),
    ("反應", "faan2 jing3", "reaction"),
    ("分歧", "fan1 kei4", "disagreement"),
    ("立場", "lap6 coeng4", "standpoint"),
    ("耐心", "noi6 sam1", "patience"),
    ("反駁", "faan2 bok3", "to retort"),
    ("觀察", "gun1 caat3", "to observe"),
    ("雙向", "soeng1 hoeng3", "two-way"),
    ("基礎", "gei1 co2", "foundation"),
    ("發揮", "faat3 fai1", "to bring into play"),
    ("作用", "zok3 jung6", "effect; function"),
    ("條理", "tiu4 lei5", "coherence"),
    ("反思", "faan2 si1", "to reflect"),
    ("進步", "zeon3 bou6", "to progress"),
    ("捉錯重點", "zuk1 co3 zung6 dim2", "miss the main point"),
    ("搞清楚", "gaau2 cing1 co2", "make clear"),
]

# ── Constants ─────────────────────────────────────────────────────────
CELL = 18             # mm per grid square
PAD = 2               # mm between cells
MARGIN_L = 12
MARGIN_T = 12
PAGE_W = 210
PAGE_H = 297

# 1 reference + 6 practice = 7 cells per row
# 7 * 18 + 6 * 2 = 126 + 12 = 138mm — compact, fits 2 rows side by side if needed
COLS = 7  # 1 ref + 6 practice


def find_cjk_font():
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    # homebrew fallback
    matches = glob.glob("/opt/homebrew/share/fonts/**/*.ttc", recursive=True) + \
              glob.glob("/opt/homebrew/share/fonts/**/*.ttf", recursive=True)
    for m in matches:
        low = os.path.basename(m).lower()
        if any(k in low for k in ("cjk", "heiti", "noto", "songti", "ming", "simsun")):
            return m
    return None


class PracticePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.has_cjk = False
        self._init_font()

    def _init_font(self):
        fp = find_cjk_font()
        if fp:
            kwargs = {}
            if fp.endswith(".ttc"):
                kwargs["collection_font_number"] = 0
            self.add_font("CJK", "", fp, **kwargs)
            self.has_cjk = True
        else:
            print("WARNING: No CJK font found!")

    def grid(self, x, y):
        """Draw a practice grid at (x,y). Returns the center coordinates for placing text."""
        s = CELL
        self.set_line_width(0.5)
        self.set_draw_color(0, 0, 0)
        self.rect(x, y, s, s)
        # light cross-hairs + diagonals
        self.set_line_width(0.15)
        self.set_draw_color(160, 160, 160)
        self.line(x + s / 2, y, x + s / 2, y + s)
        self.line(x, y + s / 2, x + s, y + s / 2)
        self.line(x, y, x + s, y + s)
        self.line(x + s, y, x, y + s)
        self.set_draw_color(0, 0, 0)
        return x + s / 2, y + s / 2

    def ref_char(self, x, y, ch):
        """Draw a gray reference character centered in the grid at (x,y) for tracing."""
        cx, cy = self.grid(x, y)
        if self.has_cjk:
            fs = 36  # font size in points
            self.set_font("CJK", "", fs)
            self.set_text_color(150, 150, 150)  # light gray for tracing
            # Center: char width at fs pt is ~fs*25.4/72 mm
            offset = fs * 25.4 / 144  # half-width in mm
            self.text(cx - offset, cy + offset, ch)
            self.set_text_color(0, 0, 0)

    def blank_grid(self, x, y):
        """Draw a blank practice grid."""
        self.grid(x, y)

    def char_row(self, x, y, ch):
        """Draw one character practice row: 1 ref cell + 7 blank cells."""
        for i in range(COLS):
            cx = x + i * (CELL + PAD)
            if i == 0:
                self.ref_char(cx, y, ch)
            else:
                self.blank_grid(cx, y)

    def word_section(self, x, y, word, jyutping, meaning):
        """Draw a complete word section. Returns the y after the section."""
        n_chars = len(word)

        # ── Word header ──
        if self.has_cjk:
            self.set_font("CJK", "", 12)
            self.set_text_color(0, 0, 0)
            self.text(x, y + 3, word)
            ww = self.get_string_width(word)
        else:
            self.set_font("Helvetica", "", 12)
            self.set_text_color(0, 0, 0)
            ww = 0

        self.set_font("Helvetica", "", 9)
        self.set_text_color(80, 80, 80)
        self.text(x + ww + 3, y + 3, f"  [{jyutping}]")

        # ── Meaning on next line ──
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.text(x, y + 11, meaning)
        self.set_text_color(0, 0, 0)

        header_h = 15  # space used by header

        # ── Character rows ──
        ry = y + header_h
        for i, ch in enumerate(word):
            self.char_row(x, ry + i * (CELL + 1), ch)

        # Draw a thin separator line below each word section
        sep_y = ry + n_chars * (CELL + 1) + 1
        self.set_line_width(0.15)
        self.set_draw_color(200, 200, 200)
        sep_w = COLS * CELL + (COLS - 1) * PAD
        self.line(x, sep_y, x + sep_w, sep_y)
        self.set_draw_color(0, 0, 0)

        return sep_y + 3

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Lesson 10 - Page {self.page_no()}/{{nb}}", align="C")
        self.set_text_color(0, 0, 0)

    def generate(self, words, output_path):
        self.alias_nb_pages()
        self.add_page()

        # ── Page header ──
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Lesson 10: Writing Practice", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "Cantonese Character Practice - Trace the gray character, then write your own",
                  new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(3)
        self.set_text_color(0, 0, 0)

        y = self.get_y()

        for word, jp, en in words:
            # Estimate space needed: header + n_chars * (CELL + 1)
            n = len(word)
            needed = 16 + n * (CELL + 1) + 5
            if y + needed > PAGE_H - MARGIN_T - 5:
                self.add_page()
                # continuation header (smaller)
                self.set_font("Helvetica", "", 8)
                self.set_text_color(100, 100, 100)
                self.cell(0, 5, "Lesson 10: Writing Practice (cont.)",
                          new_x="LMARGIN", new_y="NEXT", align="C")
                self.ln(1)
                self.set_text_color(0, 0, 0)
                y = self.get_y()

            y = self.word_section(MARGIN_L, y, word, jp, en)

        self.output(output_path)
        print(f"Done: {output_path}")
        print(f"Pages: {self.pages_count}")
        print(f"Words: {len(words)}")


if __name__ == "__main__":
    pdf = PracticePDF()
    pdf.generate(
        WORDS,
        "/Users/thanhtoantnt/workspace/cantonese/lesson_10_writing_practice.pdf",
    )
