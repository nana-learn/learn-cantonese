#!/usr/bin/env python3
"""Verify Jyutping in index.html using pycantonese.

Checks vocab words and dialogue lines against pycantonese's output.
Strips punctuation, normalizes spacing, and reports only genuine mismatches.
"""

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


def extract_array(html, const_name):
    start = html.index(f"const {const_name}=") + len(f"const {const_name}=")
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


def parse_with_node(html):
    levels = extract_array(html, "LEVELS")
    course = extract_array(html, "COURSE")
    js_code = f"const LEVELS={levels};\nconst COURSE={course};\nconst LESSONS=LEVELS.concat(COURSE);\nconsole.log(JSON.stringify(LESSONS));"
    result = subprocess.run(["node", "-e", js_code], capture_output=True, text=True)
    if result.returncode != 0:
        print("Node error:", result.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def chars_to_jp(text):
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
        parts.append(jp_word)
    return " ".join(parts), None


def normalize(jp):
    if jp is None:
        return None
    jp = jp.strip().lower()
    jp = re.sub(r'\s+', ' ', jp)
    jp = jp.replace(' ', '')
    return jp


def main():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    lessons = parse_with_node(html)
    print(f"Found {len(lessons)} lessons\n")

    real_errors = []
    total_vocab = 0
    total_dialogue = 0

    for lesson in lessons:
        lid = lesson["id"]
        title = lesson["title"]
        print(f"=== Lesson {lid}: {title} ===")

        # --- VOCAB ---
        vocab_ok = 0
        vocab_mismatch = []
        for v in lesson.get("vocab", []):
            total_vocab += 1
            c = v["c"]
            file_jp = normalize(v["j"])
            gen_jp, err = chars_to_jp(c)
            if err:
                vocab_mismatch.append((c, v["j"], f"ERROR: {err}"))
                continue
            gen_jp = normalize(gen_jp)
            if file_jp == gen_jp:
                vocab_ok += 1
            else:
                vocab_mismatch.append((c, v["j"], gen_jp or ""))

        total = len(lesson.get("vocab", []))
        if vocab_mismatch:
            print(f"  Vocab: {vocab_ok}/{total} OK, {len(vocab_mismatch)} mismatches:")
            for chars, file_val, gen_val in vocab_mismatch:
                print(f"    {chars}: file={file_val} | pycantonese={gen_val}")
                real_errors.append(("vocab", lid, chars, file_val, gen_val))
        else:
            print(f"  Vocab: {total}/{total} OK")

        # --- DIALOGUE ---
        dial_ok = 0
        dial_mismatch = []
        for idx, d in enumerate(lesson.get("dialogue", [])):
            total_dialogue += 1
            c = d["c"]
            file_jp = normalize(d["j"])
            gen_jp, err = chars_to_jp(c)
            if err:
                dial_mismatch.append((idx, c[:60], d["j"][:80], f"ERROR: {err}"))
                continue
            gen_jp = normalize(gen_jp)
            if file_jp == gen_jp:
                dial_ok += 1
            else:
                dial_mismatch.append((idx, c[:60], d["j"][:80], gen_jp or ""))

        total_d = len(lesson.get("dialogue", []))
        if dial_mismatch:
            print(f"  Dialogue: {dial_ok}/{total_d} OK, {len(dial_mismatch)} mismatches:")
            for idx, preview, file_val, gen_val in dial_mismatch:
                print(f"    line {idx}: {preview}...")
                print(f"      file:         {file_val}")
                print(f"      pycantonese:  {gen_val}")
                real_errors.append(("dialogue", lid, preview, file_val, gen_val))
        else:
            print(f"  Dialogue: {total_d}/{total_d} OK")

        # --- GRAMMAR ---
        grammar_issues = []
        for idx, g in enumerate(lesson.get("grammar", [])):
            for field in ("pattern", "ex", "ex_jp"):
                val = g.get(field, "")
                if not val:
                    continue
                jp_candidates = re.findall(r'\b([a-z]{1,6}[1-6](?:[a-z]{1,6}[1-6])*)\b', val)
                for jp_str in jp_candidates:
                    if len(jp_str) < 2:
                        continue
                    try:
                        pycantonese.parse_jyutping(jp_str)
                    except ValueError:
                        grammar_issues.append((idx, field, jp_str))

        if grammar_issues:
            print(f"  Grammar: {len(grammar_issues)} invalid Jyutping:")
            for idx, field, jp_str in grammar_issues:
                print(f"    grammar[{idx}].{field}: '{jp_str}'")
                real_errors.append(("grammar", lid, field, jp_str, "INVALID"))
        else:
            print(f"  Grammar: {len(lesson.get('grammar', []))} OK")

        print()

    # --- QUIZ ---
    print("=== Quiz Jyutping Validation ===")
    quiz_issues = 0
    for lesson in lessons:
        lid = lesson["id"]
        for qi, q in enumerate(lesson.get("quiz", [])):
            qj = q.get("j", "")
            if qj:
                try:
                    pycantonese.parse_jyutping(qj)
                except ValueError as e:
                    print(f"  L{lid} quiz[{qi}]: '{qj}' - {e}")
                    quiz_issues += 1
    if quiz_issues == 0:
        total_q = sum(len(l.get("quiz", [])) for l in lessons)
        print(f"  All {total_q} quiz Jyutping entries valid")
    print()

    # --- SUMMARY ---
    total_errors = len(real_errors) + quiz_issues
    print(f"{'='*60}")
    print(f"Checked {total_vocab} vocab entries, {total_dialogue} dialogue lines")
    if total_errors == 0:
        print("ALL JYUTPING VERIFIED - no issues found!")
    else:
        print(f"FOUND {total_errors} ISSUE(S)")
        vocab_errors = [e for e in real_errors if e[0] == "vocab"]
        dial_errors = [e for e in real_errors if e[0] == "dialogue"]
        if vocab_errors:
            print(f"\n--- Vocab Tone/Pronunciation Mismatches ({len(vocab_errors)}) ---")
            for _, lid, chars, file_val, gen_val in vocab_errors:
                print(f"  L{lid} {chars}: file={file_val} | correct={gen_val}")
        if dial_errors:
            print(f"\n--- Dialogue Mismatches ({len(dial_errors)}) ---")
            for _, lid, preview, file_val, gen_val in dial_errors:
                print(f"  L{lid} {preview}")
                print(f"    file={file_val}")
                print(f"    pycantonese={gen_val}")

    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
