#!/usr/bin/env python3
"""Fix Jyutping in index.html using pycantonese."""

import re
import sys
import json
import subprocess
import pycantonese
import unicodedata

HTML_FILE = "index.html"

PUNCT = set("，。？！、；：""''（）【】《》…—・~！,")


def strip_punct(text):
    return "".join(ch for ch in text if ch not in PUNCT and unicodedata.category(ch)[0] not in ("P", "S"))


def extract_lessons_js(html):
    start = html.index("const LESSONS=") + len("const LESSONS=")
    depth = 0
    i = start
    while i < len(html):
        if html[i] == "[":
            depth += 1
        elif html[i] == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    return html[start : i + 1]


def parse_with_node(raw_js):
    js_code = f"const LESSONS={raw_js};\nconsole.log(JSON.stringify(LESSONS));"
    result = subprocess.run(["node", "-e", js_code], capture_output=True, text=True)
    if result.returncode != 0:
        print("Node error:", result.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def chars_to_jp_spaced(text):
    text = strip_punct(text)
    if not text.strip():
        return "", None
    try:
        result = pycantonese.characters_to_jyutping(text)
    except Exception as e:
        return None, str(e)
    parts = []
    for char_word, jp_word in result:
        if jp_word is None:
            return None, f"unknown char in '{char_word}'"
        syllables = re.findall(r'[a-z]+[1-6]', jp_word)
        parts.extend(syllables)
    return " ".join(parts), None


def normalize(jp):
    if jp is None:
        return None
    return re.sub(r'\s+', '', jp.strip().lower())


def fix_vocab(html, lessons):
    fixes = 0
    for lesson in lessons:
        lid = lesson["id"]
        for v in lesson.get("vocab", []):
            c = v["c"]
            file_jp = v["j"]
            file_norm = normalize(file_jp)
            gen_jp, err = chars_to_jp_spaced(c)
            if err or gen_jp is None:
                continue
            gen_norm = normalize(gen_jp)
            if file_norm != gen_norm:
                old = f'j:"{file_jp}"'
                if old in html:
                    html = html.replace(old, f'j:"{gen_jp}"', 1)
                    print(f"  L{lid} {c}: {file_jp} -> {gen_jp}")
                    fixes += 1
                else:
                    print(f"  L{lid} {c}: COULD NOT FIND '{old}' in html")
    return html, fixes


def fix_dialogue(html, lessons):
    fixes = 0
    for lesson in lessons:
        lid = lesson["id"]
        for d in lesson.get("dialogue", []):
            c = d["c"]
            file_jp = d["j"]
            file_norm = normalize(file_jp)
            gen_jp, err = chars_to_jp_spaced(c)
            if err or gen_jp is None:
                print(f"  L{lid} dialogue: SKIP ({err}) for: {c[:40]}...")
                continue
            gen_norm = normalize(gen_jp)
            if file_norm != gen_norm:
                old = f'j:"{file_jp}"'
                count = html.count(old)
                if count == 1:
                    html = html.replace(old, f'j:"{gen_jp}"', 1)
                    print(f"  L{lid} dialogue: updated ({len(c)} chars)")
                    fixes += 1
                elif count > 1:
                    print(f"  L{lid} dialogue: AMBIGUOUS ({count} matches), skipping: {c[:30]}...")
                else:
                    print(f"  L{lid} dialogue: NOT FOUND for: {c[:30]}...")
    return html, fixes


def main():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    raw_js = extract_lessons_js(html)
    lessons = parse_with_node(raw_js)
    print(f"Found {len(lessons)} lessons\n")

    print("=== Fixing Vocab ===")
    html, v_fixes = fix_vocab(html, lessons)
    print(f"  {v_fixes} vocab fixes applied\n")

    print("=== Fixing Dialogue ===")
    html, d_fixes = fix_dialogue(html, lessons)
    print(f"  {d_fixes} dialogue fixes applied\n")

    print(f"{'='*60}")
    print(f"Total: {v_fixes + d_fixes} fixes")

    if v_fixes + d_fixes > 0:
        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Written to {HTML_FILE}")
    else:
        print("No changes needed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
