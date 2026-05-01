#!/usr/bin/env python3
"""Update index.html - add match game, writing modal, achievements, tone colors."""
import re

with open('index.html', 'r') as f:
    text = f.read()

# 1. Add CSS
old = '@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}\n.tone-1{color:#ff6b6b}.tone-2{color:#feca57}.tone-3{color:#48dbfb}.tone-4{color:#0abde3}.tone-5{color:#a29bfe}.tone-6{color:#55efc4}'
new = old + """

/* Matching Game */
.match-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px}
.match-col{display:flex;flex-direction:column;gap:8px}
.match-col h3{font-size:.85em;color:var(--text2);margin-bottom:4px;padding-left:4px}
.match-card{padding:12px 16px;border-radius:8px;border:2px solid var(--surface2);background:var(--surface);cursor:pointer;transition:all .2s;text-align:center;font-size:1em}
.match-card:hover{border-color:var(--accent)}
.match-card.selected{border-color:var(--accent2);background:rgba(108,92,231,0.15)}
.match-card.matched{opacity:.4;border-color:var(--green);cursor:default}
.match-card.wrong{border-color:var(--red);animation:shake .3s}
.match-card.correct{border-color:var(--green);background:rgba(0,184,148,0.15);animation:pop .3s}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
@keyframes pop{0%{transform:scale(1)}50%{transform:scale(1.05)}100%{transform:scale(1)}}
.match-score{padding:12px 16px;background:var(--surface);border:1px solid var(--surface2);border-radius:var(--radius);margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
.match-score .pairs{color:var(--green);font-weight:700;font-size:1.2em}
.match-score .attempts{color:var(--text2)}

/* Writing Grid Modal */
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:1000;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .3s}
.modal-overlay.open{opacity:1;pointer-events:all}
.modal-content{background:var(--surface);border:1px solid var(--surface2);border-radius:var(--radius);padding:24px;max-width:420px;width:90%;text-align:center}
.modal-content h3{font-size:1.8em;margin-bottom:2px;color:var(--text)}
.modal-content .sub{color:var(--text2);font-size:.85em;margin-bottom:14px}
.modal-grid{display:grid;grid-template-columns:repeat(10,1fr);gap:4px;margin:0 auto;max-width:320px}
.modal-cell{aspect-ratio:1;border:1px solid var(--surface2);border-radius:4px;display:flex;align-items:center;justify-content:center;background:var(--surface2);color:var(--text)}
.modal-cell.ref{background:rgba(108,92,231,0.2);border-color:var(--accent);font-size:1.6em;font-weight:700}
.modal-cell.empty{background:transparent;border-color:var(--surface2)}
.modal-close-btn{padding:10px 28px;border-radius:8px;border:1px solid var(--surface2);background:var(--surface2);color:var(--text);cursor:pointer;font-size:.9em;margin-top:16px;transition:all .2s}
.modal-close-btn:hover{border-color:var(--accent);background:var(--accent);color:#fff}
.char-link{cursor:pointer;transition:all .2s;display:inline-block;padding:1px 3px;border-radius:3px;font-weight:700}
.char-link:hover{background:rgba(108,92,231,0.25)}

/* Achievements */
.achievement-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;margin-bottom:16px}
.achievement{padding:12px 8px;border-radius:10px;background:var(--surface);border:1px solid var(--surface2);text-align:center;transition:all .3s}
.achievement.unlocked{border-color:var(--accent);background:rgba(108,92,231,0.08)}
.achievement .icon{font-size:1.6em;margin-bottom:2px}
.achievement .name{font-size:.75em;color:var(--text);font-weight:600}
.achievement .desc{font-size:.6em;color:var(--text2);margin-top:1px}
.achievement.locked{opacity:.35}
.spk-a{color:#ff6b6b}.spk-b{color:#48dbfb}"""

assert old in text, "CSS old not found"
text = text.replace(old, new)

# 2. Add Match + Game tabs (before Progress tab)
old = '<div class="tab\'+(s===\'progress\'?\' active\':\'\')+\'" onclick="showSection(\'progress\',this)">📊 Progress</div>\'+'
new = '<div class="tab\'+(s===\'quiz\'?\' active\':\'\')+\'" onclick="showSection(\'quiz\',this)">❓ Quiz</div>\'+\n    \'<div class="tab\'+(s===\'match\'?\' active\':\'\')+\'" onclick="showSection(\'match\',this);initMatch()">🎯 Match</div>\'+\n    \'<div class="tab\'+(s===\'game\'?\' active\':\'\')+\'" onclick="showSection(\'game\',this)">✍️ Write</div>\'+\n    \'<div class="tab\'+(s===\'progress\'?\' active\':\'\')+\'" onclick="showSection(\'progress\',this)">📊 Progress</div>\'+'

# Find the line with progress tab
idx = text.find("'<div class=\"tab\\'+(s===\\'progress\\'?\\' active\\':\\'\\')+\\'\" onclick=\"showSection(\\\\\\'progress\\\\\\',this)\">📊 Progress</div>\\'+")
if idx > 0:
    # Find the start of this block (previous tab)
    prev = text.rfind("'<div", 0, idx)
    if prev > 0:
        block = text[prev:idx+len("'<div class=\"tab\\'+(s===\\'progress\\'?\\' active\\':\\'\\')+\\'\" onclick=\"showSection(\\\\\\'progress\\\\\\',this)\">📊 Progress</div>\\'+")]
        new_block = block.replace(
            "'<div class=\"tab\\'+(s===\\'progress\\'?\\' active\\':\\'\\')+\\'\" onclick=\"showSection(\\\\\\'progress\\\\\\',this)\">📊 Progress</div>\\'+",
            "'<div class=\"tab\\'+(s===\\'match\\'?\\' active\\':\\'\\')+\\'\" onclick=\"showSection(\\\\\\'match\\\\\\',this);initMatch()\">🎯 Match</div>\\'+\\n    '<div class=\"tab\\'+(s===\\'game\\'?\\' active\\':\\'\\')+\\'\" onclick=\"showSection(\\\\\\'game\\\\\\',this)\">✍️ Write</div>\\'+\\n    '<div class=\"tab\\'+(s===\\'progress\\'?\\' active\\':\\'\\')+\\'\" onclick=\"showSection(\\\\\\'progress\\\\\\',this)\">📊 Progress</div>\\'+"
        )
        text = text[:prev] + new_block + text[prev+len(block):]
        print("Tabs: OK")
    else:
        print("Tabs: prev not found")
else:
    print("Tabs: pattern not found")
    # Show what's around progress
    idx2 = text.find("progress',this")
    print(f"  Found at {idx2}: {repr(text[idx2-20:idx2+80])}")


# 3. Add Match + Game section divs
old_sec = "'<div id=\"sec-quiz\" class=\"section\\'+(s===\\'quiz\\'?\\' active\\':\\'\\')+\\'\">\\'+renderQuiz(L)+\\'</div>\\'+"
new_sec = old_sec + "\n    '<div id=\"sec-match\" class=\"section\\'+(s===\\'match\\'?\\' active\\':\\'\\')+\\'\">\\'+renderMatch(L)+\\'</div>\\'+\\n    '<div id=\"sec-game\" class=\"section\\'+(s===\\'game\\'?\\' active\\':\\'\\')+\\'\">\\'+renderGame(L)+\\'</div>\\'+"

if old_sec in text:
    text = text.replace(old_sec, new_sec)
    print("Sections: OK")
else:
    print("Sections: not found")
    idx = text.find("sec-quiz")
    if idx > 0:
        print(f"  at {idx}: {repr(text[idx:idx+100])}")

# 4. Add modal overlay after progress section
old_end = "'<div id=\"sec-progress\" class=\"section\\'+(s===\\'progress\\'?\\' active\\':\\'\\')+\\'\">\\'+renderProgress(L)+\\'</div>';"
new_end = old_end + "\n    '<div id=\"writingModal\" class=\"modal-overlay\" onclick=\"closeModal(event)\"><div class=\"modal-content\" id=\"modalInner\"></div></div>';"

if old_end in text:
    text = text.replace(old_end, new_end)
    print("Modal: OK")
else:
    print("Modal: not found")
    idx = text.find("sec-progress")
    print(f"  at {idx}: {repr(text[idx:idx+100])}")

# 5. Tone colors in vocab: jyutping line
old_jp = "'<div class=\"jp\">'+v.j+'</div>'+masteryDots"
new_jp = "'<div class=\"jp\">'+colorJyutping(v.j)+'</div>'+masteryDots"

if old_jp in text:
    text = text.replace(old_jp, new_jp)
    print("Vocab tones: OK")
else:
    print("Vocab tones: not found")

# 6. Tone colors in dialogue (full mode jyutping)
old_dj = "'<div class=\"jyutping\" style=\"display:'+(showJp?'block':'none')+'\">'+d.j+'</div>'"
new_dj = "'<div class=\"jyutping\" style=\"display:'+(showJp?'block':'none')+'\">'+colorJyutping(d.j)+'</div>'"
if old_dj in text:
    text = text.replace(old_dj, new_dj)
    print("Dialogue tones: OK")

# 7. Tone colors in sentence mode
old_sj0 = "'<div class=\"sn-jp\" style=\"display:'+(showJp?'block':'none')+'\">'+(jsents[0]||d.j)+'</div>'"
new_sj0 = "'<div class=\"sn-jp\" style=\"display:'+(showJp?'block':'none')+'\">'+colorJyutping(jsents[0]||d.j)+'</div>'"
if old_sj0 in text:
    text = text.replace(old_sj0, new_sj0)
    print("Sent tones 1: OK")

old_sji = "'<div class=\"sn-jp\" style=\"display:'+(showJp?'block':'none')+'\">'+(jsents[i]||'')+'</div>'"
new_sji = "'<div class=\"sn-jp\" style=\"display:'+(showJp?'block':'none')+'\">'+colorJyutping(jsents[i]||'')+'</div>'"
if old_sji in text:
    text = text.replace(old_sji, new_sji)
    print("Sent tones 2: OK")

# 8. Speaker colors
old_spk = "'<div class=\"speaker\">'+d.speaker+' <button class=\"speak-btn\""
new_spk = "'<div class=\"speaker\"><span class=\"spk-'+d.speaker.toLowerCase()+'\">'+d.speaker+'</span> <button class=\"speak-btn\""
if old_spk in text:
    text = text.replace(old_spk, new_spk)
    print("Speaker colors: OK")

# 9. Add char links in vocab
old_vc = "'<div class=\"front\"><div class=\"word\">'+v.c+' <button class=\"speak-btn\""
new_vc = "'<div class=\"front\"><div class=\"word\">'+v.c.split('').map(c=>'<span class=\"char-link\" onclick=\"event.stopPropagation();showCharModal(\"'+c+'\")\">'+c+'</span>').join('')+' <button class=\"speak-btn\""
if old_vc in text:
    text = text.replace(old_vc, new_vc)
    print("Char links: OK")
else:
    print("Char links: not found")
    idx = text.find('class="front"><div class="word">')
    print(f"  at {idx}: {repr(text[idx:idx+70])}")

# 10. Add new JS functions before init();
old_init = "init();\n</script>"
new_js = r"""
// ── Matching Game ──
let matchData = [], matchSelected = null, matchMatched = 0, matchAttempts = 0, matchLocked = false;
function initMatch(){
  const L = LESSONS[currentLesson];
  const picked = shuffle(L.vocab).slice(0, 8);
  matchData = picked.map(v => ({id: v.c, text: v.c, pair: v.e, type: 'cn'}))
    .concat(picked.map(v => ({id: v.c, text: v.e, pair: v.c, type: 'en'})));
  matchData = shuffle(matchData);
  matchSelected = null; matchMatched = 0; matchAttempts = 0; matchLocked = false;
  const el = document.getElementById('sec-match');
  if(el) el.innerHTML = renderMatch(L);
}
function renderMatch(L){
  const total = matchData.length / 2;
  let h = '<div class="match-score"><span><span class="pairs">' + matchMatched + '/' + total + '</span> matched</span><span class="attempts">Attempts: ' + matchAttempts + '</span></div>';
  h += '<div class="match-grid"><div class="match-col"><h3>Cantonese</h3>';
  matchData.filter(d => d.type === 'cn').forEach(d => {
    const cls = 'match-card' + (d._matched ? ' matched' : '') + (matchSelected === d.id && !d._matched ? ' selected' : '');
    h += '<div class="' + cls + '" data-id="' + d.id + '" data-pair="' + d.pair + '" onclick="pickMatch(this)">' + d.text + '</div>';
  });
  h += '</div><div class="match-col"><h3>English</h3>';
  matchData.filter(d => d.type === 'en').forEach(d => {
    const cls = 'match-card' + (d._matched ? ' matched' : '') + (matchSelected === d.id && !d._matched ? ' selected' : '');
    h += '<div class="' + cls + '" data-id="' + d.id + '" data-pair="' + d.pair + '" onclick="pickMatch(this)">' + d.text + '</div>';
  });
  h += '</div></div>';
  if(matchMatched === total && total > 0) h += '<div class="session-summary"><h3>🎉 All matched!</h3><p style="color:var(--text2);margin:8px 0">' + matchAttempts + ' attempts</p><button class="fc-btn got-it" onclick="initMatch()">Play Again</button></div>';
  return h;
}
function pickMatch(el){
  if(matchLocked || el.classList.contains('matched')) return;
  if(!matchSelected){ matchSelected = el.dataset.id; el.classList.add('selected'); return; }
  if(matchSelected === el.dataset.id){ el.classList.remove('selected'); matchSelected = null; return; }
  matchLocked = true; matchAttempts++;
  const first = document.querySelector('.match-card[data-id="' + matchSelected + '"]');
  const firstPair = first ? first.dataset.pair : '';
  const correct = el.dataset.pair === first.dataset.id;
  if(correct){
    el.classList.add('correct'); first.classList.add('correct');
    setTimeout(() => {
      el.classList.add('matched'); first.classList.add('matched');
      el.classList.remove('correct','selected'); first.classList.remove('correct','selected');
      matchData.forEach(d => { if(d.id === el.dataset.id || d.id === matchSelected) d._matched = true; });
      matchMatched++; matchSelected = null; matchLocked = false;
      const sec = document.getElementById('sec-match');
      if(sec) sec.innerHTML = renderMatch(LESSONS[currentLesson]);
    }, 400);
  } else {
    el.classList.add('wrong'); first.classList.add('wrong');
    setTimeout(() => { el.classList.remove('wrong'); first.classList.remove('wrong','selected'); matchSelected = null; matchLocked = false; }, 500);
  }
}

// ── Writing Grid Modal ──
function showCharModal(ch){
  const modal = document.getElementById('writingModal');
  const inner = document.getElementById('modalInner');
  if(!modal || !inner) return;
  let ctx = '', jp = '';
  for(const L of LESSONS){ for(const v of L.vocab){ if(v.c.includes(ch)){ ctx = v.c; jp = v.j; break; } } if(ctx) break; }
  inner.innerHTML = '<h3 style="font-size:2em;margin-bottom:2px">' + ch + '</h3><div class="sub">' + (ctx ? ctx + ' [' + jp + ']' : '') + '</div><div class="modal-grid">' +
    '<div class="modal-cell ref">' + ch + '</div>' + Array(9).fill(0).map(() => '<div class="modal-cell empty"></div>').join('') +
    '</div><div style="margin-top:8px;color:var(--text2);font-size:.7em">Trace the character, then practice in blank squares</div>' +
    '<button class="modal-close-btn" onclick="document.getElementById(\'writingModal\').classList.remove(\'open\')">Close</button>';
  modal.classList.add('open');
}
function closeModal(e){
  if(e && e.target !== document.getElementById('writingModal') && e.target.closest('.modal-content')) return;
  document.getElementById('writingModal').classList.remove('open');
}

// ── Writing Game ──
const practicedChars = new Set(JSON.parse(localStorage.getItem('cantonese-practiced') || '[]'));
function renderGame(L){
  const allChars = [...new Set(L.vocab.flatMap(v => v.c.split('')))];
  let h = '<div class="match-score"><span><span class="pairs">' + practicedChars.size + '</span> chars practiced</span><span class="attempts">Click a character to see a writing grid</span></div>';
  h += '<div class="write-grid">';
  allChars.forEach(ch => {
    h += '<div class="write-card' + (practicedChars.has(ch) ? ' practiced' : '') + '" onclick="showCharModal(\'' + ch + '\');practicedChars.add(\'' + ch + '\');localStorage.setItem(\'cantonese-practiced\',JSON.stringify([...practicedChars]));this.classList.add(\'practiced\')">' + ch + '</div>';
  });
  return h + '</div>';
}

// ── Achievements ──
function renderAchievements(){
  const allWords = {}; LESSONS.forEach(l => l.vocab.forEach(v => { if(progress.words[v.c]) allWords[v.c] = progress.words[v.c]; }));
  const stats = { total: Object.keys(allWords).length, mastered: Object.values(allWords).filter(w => w.box >= 4).length, streak: progress.streak.count, practiced: practicedChars.size };
  const achs = [
    { icon: '🌱', name: 'First Steps', desc: 'Study 1 word', check: stats.total >= 1 },
    { icon: '📖', name: 'Getting Started', desc: 'Study 10 words', check: stats.total >= 10 },
    { icon: '📚', name: 'Dedicated', desc: 'Study 50 words', check: stats.total >= 50 },
    { icon: '⭐', name: 'Star Student', desc: 'Master 5 words', check: stats.mastered >= 5 },
    { icon: '🌟', name: 'Word Master', desc: 'Master 10 words', check: stats.mastered >= 10 },
    { icon: '🔥', name: 'On Fire', desc: '3-day streak', check: stats.streak >= 3 },
    { icon: '💪', name: 'Consistent', desc: '7-day streak', check: stats.streak >= 7 },
    { icon: '✍️', name: 'Penman', desc: 'Practice 5 chars', check: stats.practiced >= 5 },
    { icon: '🖌️', name: 'Calligrapher', desc: 'Practice 20 chars', check: stats.practiced >= 20 },
    { icon: '🏆', name: 'Explorer', desc: 'Open all 10 lessons', check: true },
  ];
  const unlocked = achs.filter(a => a.check).length;
  let h = '<div class="match-score" style="margin-top:24px"><span><span class="pairs">' + unlocked + '/' + achs.length + '</span> achievements</span></div>';
  h += '<div class="achievement-grid">';
  achs.forEach(a => { h += '<div class="achievement' + (a.check ? ' unlocked' : ' locked') + '"><div class="icon">' + a.icon + '</div><div class="name">' + a.name + '</div><div class="desc">' + a.desc + '</div></div>'; });
  return h + '</div>';
}

init();
</script>"""

if old_init in text:
    text = text.replace(old_init, new_js)
    print("JS: OK")
else:
    print("JS: init() not found")

with open('index.html', 'w') as f:
    f.write(text)
print("Done!")
