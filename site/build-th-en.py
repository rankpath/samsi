import re, os, json, html

SRC = '../samsi-landing-th-en.html'   # the bilingual master, one folder up
src = open(SRC, encoding='utf-8').read()

# Pull the T dictionary straight out of the source so the two files can never
# drift from the bilingual master.
def grab(lang):
    m = re.search(r"\n %s:\{\n(.*?)\n \}" % lang, src, re.S)
    return m.group(1)

def field(block, key):
    m = re.search(r"\b%s:'((?:[^'\\]|\\.)*)'" % key, block)
    return m.group(1).replace("\\'", "'") if m else None

def steps(block):
    m = re.search(r"steps:\[(.*?)\]\],", block, re.S)
    rows = re.findall(r"\['((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)'\]", m.group(1) + ']')
    return rows

CATS = re.findall(r"\{c:\{en:'([^']*)',th:'([^']*)'\}", src)

DOMAIN = 'https://example.com'   # <-- replace with the real domain before launch

OTHER = {'th': ('en', 'English'), 'en': ('th', 'ไทย')}

for lang in ('th', 'en'):
    blk = grab(lang)
    out = src

    # 1. document language + title + canonical
    out = out.replace('<link rel="alternate" hreflang="th" href="/th/">',
                      '<link rel="alternate" hreflang="th" href="%s/th/">' % DOMAIN, 1)
    out = out.replace('<link rel="alternate" hreflang="en" href="/en/">',
                      '<link rel="alternate" hreflang="en" href="%s/en/">' % DOMAIN, 1)
    out = out.replace('<link rel="alternate" hreflang="x-default" href="/en/">',
                      '<link rel="alternate" hreflang="x-default" href="%s/en/">' % DOMAIN, 1)
    out = out.replace('<html lang="th">', '<html lang="%s">' % lang, 1)
    out = re.sub(r'<title>.*?</title>',
                 '<title>%s</title>\n<link rel="canonical" href="%s/%s/">' % (field(blk, 'title'), DOMAIN, lang),
                 out, count=1, flags=re.S)
    out = out.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                      '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                      '<meta name="description" content="%s">' % html.escape(field(blk, 'lede')[:155]), 1)

    # 2. switcher becomes a crawlable link to the other version
    o_code, o_label = OTHER[lang]
    sw = re.search(r'<div class="langsw".*?</div>', out, re.S).group(0)
    out = out.replace(sw,
        '<a class="langlink" href="../%s/index.html" hreflang="%s" lang="%s">%s</a>' % (o_code, o_code, o_code, o_label), 1)
    out = out.replace('.langsw{', '''.langlink{
  font-size:14px;font-weight:500;color:var(--muted);border:1.5px solid var(--border);
  border-radius:2px;padding:6px 13px;text-decoration:none;transition:all 140ms;
}
.langlink:hover{color:var(--ink);border-color:var(--ink);}
.langsw{''', 1)

    # 3. render every translated string into the markup
    def fill(m):
        tag, key = m.group(2), m.group(3)
        val = field(blk, key)
        return m.group(1) + (html.escape(val) if val else '') + '</%s>' % tag
    out = re.sub(r'(<(\w+)[^>]*data-t="(\w+)"[^>]*>)</\2>', fill, out)

    # 4. pre-render the step cards and category buttons
    step_html = ''.join('<div class="step"><div class="n">%s</div><h3>%s</h3><p>%s</p></div>'
                        % tuple(html.escape(x) for x in r) for r in steps(blk))
    out = out.replace('<div class="steps" id="steps"></div>',
                      '<div class="steps" id="steps">%s</div>' % step_html, 1)
    cat_html = ''.join('<button class="cat" data-i="%d" aria-pressed="%s">%s</button>'
                       % (i, 'true' if i == 2 else 'false',
                          html.escape(c[0] if lang == 'en' else c[1]))
                       for i, c in enumerate(CATS))
    out = out.replace('<div class="cats" id="cats" role="group" aria-label="Categories"></div>',
                      '<div class="cats" id="cats" role="group" aria-label="Categories">%s</div>' % cat_html, 1)

    # 5. lock the runtime to one language and drop the toggle wiring
    out = out.replace("let lang='th', current", "let lang='%s', current" % lang, 1)
    out = out.replace("  document.getElementById('btnTh').setAttribute('aria-pressed',String(l==='th'));\n"
                      "  document.getElementById('btnEn').setAttribute('aria-pressed',String(l==='en'));\n", '')
    out = out.replace("document.getElementById('btnTh').addEventListener('click',()=>setLang('th'));\n"
                      "document.getElementById('btnEn').addEventListener('click',()=>setLang('en'));\n", '')
    out = out.replace("setLang('th');", "setLang('%s');" % lang)

    d = './%s' % lang
    os.makedirs(d, exist_ok=True)
    open(d + '/index.html', 'w', encoding='utf-8').write(out)
    print(lang, len(out), 'bytes ->', d + '/index.html')
