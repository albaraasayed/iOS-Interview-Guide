#!/usr/bin/env python3
"""
generate.py — Parses Organized_Interviews.md and produces index.html.
Run from inside iOS_Study_Guide/:  python3 generate.py
"""
import re, os, html as H

SOURCE = os.path.join(os.path.dirname(__file__), '..', 'Organized_Interviews.md')

ICONS = {
    'iOS Fundamentals':                             '📱',
    'Objective-C':                                  '⚙️',
    'Swift Fundamentals':                           '🔷',
    'UIKit':                                        '🖼️',
    'Reactive Programming':                         '⚡',
    'Design Patterns & Architecture':               '🏗️',
    'Core Data & Persistence':                      '💾',
    'SwiftUI':                                      '✨',
    'SwiftData':                                    '🗄️',
    'Third-Party Libraries & Dependency Management':'📦',
    'General Computer Science, OS & Multithreading':'🧵',
}

def slugify(s):
    s = re.sub(r'[^\w\s-]', '', s.lower())
    return re.sub(r'[\s_-]+', '-', s).strip('-')

# ════════════════════════════════════════════════════════════════════════════
#  MARKDOWN → HTML  (handles the patterns actually present in the file)
# ════════════════════════════════════════════════════════════════════════════

def md_to_html(md):
    if not md or not md.strip():
        return ''

    # 1 ── Stash fenced code blocks ──────────────────────────────────────────
    code_blocks = []
    def stash_code(m):
        lang = (m.group(1) or '').strip().lower()
        lang_map = {
            '': 'plaintext', 'swift': 'swift', 'objective-c': 'objc',
            'objc': 'objc', 'python': 'python', 'bash': 'bash',
            'sh': 'bash', 'shell': 'bash', 'js': 'javascript',
            'javascript': 'javascript', 'json': 'json', 'xml': 'xml',
        }
        lang = lang_map.get(lang, lang or 'plaintext')
        code = H.escape(m.group(2).rstrip('\n'))
        idx = len(code_blocks)
        code_blocks.append(
            f'<pre><code class="language-{lang} hljs">{code}</code></pre>'
        )
        return f'\x02C{idx:04d}\x03'
    md = re.sub(r'```(\w*)\n?([\s\S]*?)```', stash_code, md)

    # 2 ── Stash inline code ──────────────────────────────────────────────────
    inline_codes = []
    def stash_inline(m):
        idx = len(inline_codes)
        inline_codes.append(
            f'<code class="inline-code">{H.escape(m.group(1))}</code>'
        )
        return f'\x02I{idx:04d}\x03'
    md = re.sub(r'`([^`\n]+)`', stash_inline, md)

    # 3 ── Strip bare horizontal rules ────────────────────────────────────────
    md = re.sub(r'(?m)^---+\s*$', '', md)

    # 4 ── Blockquotes (including GitHub-style alerts) ─────────────────────────
    def render_bq(m):
        inner = re.sub(r'(?m)^>\s?', '', m.group(0)).strip()
        alert = re.match(r'\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n?([\s\S]*)', inner, re.I)
        if alert:
            kind  = alert.group(1).lower()
            body  = alert.group(2).strip()
            return f'<div class="callout callout-{kind}"><span class="callout-label">{kind}</span>{body}</div>\n'
        return f'<blockquote>{inline_fmt(inner)}</blockquote>\n'
    md = re.sub(r'(?m)(?:^>.*(?:\n|$))+', render_bq, md)

    # 5 ── Tables ─────────────────────────────────────────────────────────────
    def render_table(m):
        raw_lines = [l for l in m.group(0).strip().split('\n') if l.strip()]
        # Rows that are NOT pure separator rows (| --- | --- |)
        data_rows = [l for l in raw_lines if not re.match(r'^\s*\|[\s\-:|]+\|\s*$', l)]
        if len(data_rows) < 1:
            return m.group(0)
        def cells(row):
            parts = re.split(r'\s*\|\s*', row.strip('|').strip())
            return [inline_fmt(p.strip()) for p in parts]
        out = ['<div class="table-wrapper"><table><thead><tr>']
        for c in cells(data_rows[0]):
            out.append(f'<th>{c}</th>')
        out.append('</tr></thead><tbody>')
        for row in data_rows[1:]:
            out.append('<tr>')
            for c in cells(row):
                out.append(f'<td>{c}</td>')
            out.append('</tr>')
        out.append('</tbody></table></div>')
        return '\n'.join(out) + '\n'
    md = re.sub(r'(?m)(?:^\|.+\n)+', render_table, md)

    # 6 ── In-answer headings ─────────────────────────────────────────────────
    md = re.sub(r'(?m)^#{4}\s+(.+)$', lambda m: f'<h4>{inline_fmt(m.group(1))}</h4>', md)
    md = re.sub(r'(?m)^#{5}\s+(.+)$', lambda m: f'<h5>{inline_fmt(m.group(1))}</h5>', md)

    # 7 ── Lists ──────────────────────────────────────────────────────────────
    md = process_lists(md)

    # 8 ── Paragraphs ─────────────────────────────────────────────────────────
    BLOCK = re.compile(
        r'^<(?:ul|ol|li|table|div|pre|blockquote|h[1-6]|figure)[\s>]',
        re.IGNORECASE
    )
    parts = []
    for para in re.split(r'\n{2,}', md.strip()):
        para = para.strip()
        if not para:
            continue
        if BLOCK.match(para) or para.startswith('\x02C'):
            parts.append(para)
        else:
            parts.append(f'<p>{inline_fmt(para.replace(chr(10), " "))}</p>')
    md = '\n'.join(parts)

    # 9 ── Restore stashes ────────────────────────────────────────────────────
    for i, b in enumerate(code_blocks):
        md = md.replace(f'\x02C{i:04d}\x03', b)
    for i, c in enumerate(inline_codes):
        md = md.replace(f'\x02I{i:04d}\x03', c)

    return md


def inline_fmt(text):
    """Apply bold, italic, and link formatting to a string."""
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)', r'<em>\1</em>', text)
    return text


def process_lists(text):
    lines = text.split('\n')
    out   = []
    i     = 0
    while i < len(lines):
        ul = re.match(r'^(\s*)[-*+]\s+(.+)$', lines[i])
        ol = re.match(r'^(\s*)\d+[.)]\s+(.+)$', lines[i])
        if ul:
            indent = len(ul.group(1))
            out.append('<ul>')
            while i < len(lines):
                m = re.match(r'^(\s*)[-*+]\s+(.+)$', lines[i])
                if m and len(m.group(1)) == indent:
                    out.append(f'<li>{inline_fmt(m.group(2))}</li>')
                    i += 1
                else:
                    break
            out.append('</ul>')
        elif ol:
            indent = len(ol.group(1))
            out.append('<ol>')
            while i < len(lines):
                m = re.match(r'^(\s*)\d+[.)]\s+(.+)$', lines[i])
                if m and len(m.group(1)) == indent:
                    out.append(f'<li>{inline_fmt(m.group(2))}</li>')
                    i += 1
                else:
                    break
            out.append('</ol>')
        else:
            out.append(lines[i])
            i += 1
    return '\n'.join(out)


# ════════════════════════════════════════════════════════════════════════════
#  PARSE  Organized_Interviews.md
# ════════════════════════════════════════════════════════════════════════════
SUBSEC_SKIP = {'rxswift', 'combine'}

def parse(filepath):
    with open(filepath, encoding='utf-8') as f:
        raw = f.read()

    sections = []
    cur_sec  = None
    cur_q    = None
    cur_ans  = []

    for line in raw.split('\n'):
        # ── Main section header ──────────────────────────────────────────────
        if line.startswith('## ') and 'Table of Contents' not in line:
            _flush_q(cur_sec, cur_q, cur_ans)
            cur_q, cur_ans = None, []
            cur_sec = {'name': line[3:].strip(), 'questions': []}
            sections.append(cur_sec)

        # ── Question (###) ───────────────────────────────────────────────────
        elif line.startswith('### ') and cur_sec:
            title = line[4:].strip()
            has_tag = bool(re.search(r'\[(Easy|Mid|Expert)\]', title, re.I))
            is_skip = (title.lower().split()[0] in SUBSEC_SKIP) and not has_tag

            if is_skip:
                _flush_q(cur_sec, cur_q, cur_ans)
                cur_q, cur_ans = None, []
                continue

            _flush_q(cur_sec, cur_q, cur_ans)
            cur_q, cur_ans = title, []

        # ── Answer content ───────────────────────────────────────────────────
        elif cur_q is not None:
            s = line.strip()
            # Skip the italic section description line at the top of an answer
            if re.match(r'^\*.+\*$', s) and not cur_ans:
                continue
            cur_ans.append(line)

    _flush_q(cur_sec, cur_q, cur_ans)
    return [s for s in sections if s['questions']]


def _flush_q(sec, q, ans):
    if sec and q:
        # Clean up answer: strip leading/trailing --- and blank lines
        text = '\n'.join(ans).strip()
        text = re.sub(r'^---+\s*\n?', '', text)
        text = re.sub(r'\n?---+\s*$', '', text).strip()
        sec['questions'].append({'q': q, 'a': text})


# ════════════════════════════════════════════════════════════════════════════
#  GENERATE  index.html
# ════════════════════════════════════════════════════════════════════════════
def extract_diff(q):
    m = re.search(r'\[(Easy|Mid|Expert)\]$', q.strip(), re.I)
    return m.group(1) if m else None

def clean_q(q):
    return re.sub(r'\s*\[(Easy|Mid|Expert)\]\s*$', '', q.strip(), flags=re.I)

def build_html(sections):
    total = sum(len(s['questions']) for s in sections)

    # ── Sidebar nav ──────────────────────────────────────────────────────────
    nav = []
    for s in sections:
        sl = slugify(s['name'])
        ic = ICONS.get(s['name'], '📌')
        n  = len(s['questions'])
        nav.append(
            f'<a class="nav-item" href="#{sl}" data-target="{sl}">'
            f'<span class="nav-ico">{ic}</span>'
            f'<span class="nav-lbl">{H.escape(s["name"])}</span>'
            f'<span class="nav-cnt">{n}</span>'
            f'</a>'
        )
    nav_html = '\n      '.join(nav)

    # ── Sections ─────────────────────────────────────────────────────────────
    secs = []
    for s in sections:
        sl   = slugify(s['name'])
        icon = ICONS.get(s['name'], '📌')
        items = []
        for qi, q in enumerate(s['questions']):
            diff    = extract_diff(q['q'])
            cq      = clean_q(q['q'])
            ans_html = md_to_html(q['a'])
            dc       = diff.lower() if diff else ''
            badge    = (f'<span class="badge badge-{dc}">{diff}</span>'
                        if diff else '')
            iid = f'{sl}-q{qi}'
            items.append(f'''
    <div class="accordion-item" data-difficulty="{dc}" id="{iid}">
      <button class="accordion-btn" aria-expanded="false" aria-controls="body-{iid}">
        <span class="q-text">{H.escape(cq)}</span>
        <span class="btn-meta">
          {badge}
          <span class="chevron" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M5 7l4 4 4-4" stroke="currentColor" stroke-width="1.75"
                    stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </span>
      </button>
      <div class="accordion-body" id="body-{iid}">
        <div class="accordion-inner">{ans_html}</div>
      </div>
    </div>''')

        secs.append(f'''
  <section class="cat-section" id="{sl}">
    <div class="section-hd">
      <span class="section-emoji">{icon}</span>
      <div>
        <h2 class="section-name">{H.escape(s["name"])}</h2>
        <p class="section-meta">{len(s["questions"])} questions</p>
      </div>
    </div>
    <div class="accordion-group">{''.join(items)}
    </div>
  </section>''')

    secs_html = '\n'.join(secs)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>iOS Interview Study Guide</title>
  <meta name="description" content="Comprehensive, deduplicated iOS developer interview prep — {total} questions across {len(sections)} categories.">
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
</head>
<body>
<div class="app">

  <!-- ══════════════════════════════ SIDEBAR ══════════════════════════════ -->
  <aside class="sidebar" id="sidebar">

    <div class="sidebar-logo">
      <div class="logo-mark">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32" rx="9" fill="#0A84FF"/>
          <path d="M16 6c-3 4.5-5.5 7-5.5 10s2.5 5.5 5.5 5.5 5.5-2.5 5.5-5.5S19 10.5 16 6z"
                fill="white" opacity=".9"/>
          <circle cx="16" cy="20" r="3" fill="#0A84FF"/>
        </svg>
      </div>
      <div>
        <p class="logo-title">iOS Study Guide</p>
        <p class="logo-subtitle">{total} questions</p>
      </div>
    </div>

    <div class="sidebar-search">
      <svg class="s-ico" width="15" height="15" viewBox="0 0 15 15" fill="none">
        <circle cx="6.5" cy="6.5" r="4.5" stroke="#636366" stroke-width="1.5"/>
        <path d="M10 10l3.5 3.5" stroke="#636366" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
      <input id="search-input" type="search" placeholder="Search questions… ⌘K" autocomplete="off" spellcheck="false">
    </div>

    <nav class="sidebar-nav" id="sidebar-nav">
      <p class="nav-group">Categories</p>
      {nav_html}
    </nav>

    <div class="sidebar-filters">
      <p class="nav-group" style="padding-top:0">Difficulty</p>
      <div class="filter-pills">
        <button class="pill pill-all active"    data-diff="all">All</button>
        <button class="pill pill-easy"          data-diff="easy">Easy</button>
        <button class="pill pill-mid"           data-diff="mid">Mid</button>
        <button class="pill pill-expert"        data-diff="expert">Expert</button>
      </div>
    </div>

  </aside>

  <!-- ══════════════════════════════ MAIN ════════════════════════════════ -->
  <main class="main" id="main">

    <header class="page-hero">
      <h1 class="hero-title">iOS Interview <span class="text-accent">Study Guide</span></h1>
      <p class="hero-sub">Senior-level preparation &middot; {total} deduplicated questions &middot; {len(sections)} categories</p>
      <div class="hero-pills">
        <span class="hp easy"><span class="dot"></span>Easy</span>
        <span class="hp mid"><span class="dot"></span>Mid</span>
        <span class="hp expert"><span class="dot"></span>Expert</span>
      </div>
    </header>

    <div id="search-banner" class="search-banner hidden">
      Showing results for <strong id="search-term"></strong>
      <button id="search-clear">Clear</button>
    </div>

    {secs_html}

  </main>
</div>

<!-- Mobile overlay -->
<div id="mobile-overlay" class="hidden"
     style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:40"></div>

<!-- Back to top -->
<button class="fab" id="fab" title="Back to top" aria-label="Back to top">
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M5 12l5-5 5 5" stroke="white" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</button>

<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/swift.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/objectivec.min.js"></script>
<script src="script.js"></script>
</body>
</html>'''


# ════════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════════
def main():
    print(f'📖 Parsing  {os.path.abspath(SOURCE)} …')
    sections = parse(SOURCE)
    total    = sum(len(s['questions']) for s in sections)
    print(f'✅ {len(sections)} sections · {total} questions\n')
    for s in sections:
        print(f'   {ICONS.get(s["name"], "•")} {s["name"]}: {len(s["questions"])}')

    print('\n🔨 Building index.html …')
    html = build_html(sections)

    out = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)

    size = os.path.getsize(out)
    print(f'✅ {out}  ({size:,} bytes / {size//1024} KB)')

if __name__ == '__main__':
    main()
