# -*- coding: utf-8 -*-
"""
daily_brief.py — 晨间信息流晨报生成器（v0.10 卡片式）
- 卡片网格布局（Google News 风格），大字，缩略图 16:9，源徽章
- 抓取失败源静默隐藏（不渲染占位条目）
- 输出: self-contained HTML → <repo>/public/morning/index.html
运行: python scripts/daily_brief.py
v0.10: +header 返回首页链接
v0.9: +新浪 7x24 中文快讯源；收藏区 +Lyn Alden/Glassnode/Kobeissi Letter
v0.8: +RH Chain 加密源（Google News 聚合）
"""
import os, re, html as htmlmod, datetime, difflib, xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'public', 'morning', 'index.html')
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36'}
NS_MEDIA = '{http://search.yahoo.com/mrss/}'
NS_DC = '{http://purl.org/dc/elements/1.1/}'

# ---------- 全局去重（跨区块、跨源） ----------
_seen = []   # 已保留条目的归一化标题

def _norm(t):
    t = t.lower()
    t = re.sub(r'[\W_]+', '', t, flags=re.UNICODE)
    return t.strip()

def is_dup(title):
    n = _norm(title)
    if not n:
        return True
    for k in _seen:
        if n == k:
            return True
        if len(n) >= 10 and len(k) >= 10:
            if n in k or k in n:                       # 包含关系（短含于长）
                return True
            if difflib.SequenceMatcher(None, n, k).ratio() >= 0.87:  # 模糊相似
                return True
    return False

def mark_seen(title):
    _seen.append(_norm(title))

def clean_desc(d):
    if not d:
        return ''
    d = re.sub(r'<[^>]+>', ' ', d)
    d = htmlmod.unescape(d)
    d = re.sub(r'\s+', ' ', d).strip()
    return d[:150]

def fetch_rss(url, limit=4):
    out = []
    try:
        r = requests.get(url, headers=H, timeout=15)
        root = ET.fromstring(r.content)
        for it in root.findall('.//item')[:limit]:
            t = it.findtext('title')
            l = it.findtext('link')
            pd = it.findtext('pubDate') or it.findtext(NS_DC + 'date') or ''
            if t and l:
                out.append({'title': t.strip(), 'link': l.strip(), 'date': pd,
                            'thumb': get_thumb(it), 'desc': clean_desc(it.findtext('description'))})
    except Exception:
        return []   # 抓取失败 → 静默隐藏
    return out

def get_thumb(it):
    m = it.find(NS_MEDIA + 'thumbnail')
    if m is not None and m.get('url'):
        return m.get('url')
    mc = it.find(NS_MEDIA + 'content')
    if mc is not None and mc.get('url'):
        return mc.get('url')
    enc = it.find('enclosure')
    if enc is not None and enc.get('url') and 'image' in (enc.get('type') or ''):
        return enc.get('url')
    desc = it.findtext('description') or ''
    m = re.search(r'<img[^>]+src="([^"]+)"', desc)
    return m.group(1) if m else None

def fetch_wscn(limit=6):
    out = []
    try:
        r = requests.get('https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=%d' % limit,
                         headers={**H, 'Referer': 'https://wallstreetcn.com/'}, timeout=10)
        for it in r.json().get('data', {}).get('items', []):
            t = (it.get('content_text') or '').strip()
            if t:
                out.append({'title': t, 'link': 'https://wallstreetcn.com/live/global', 'date': '', 'thumb': None})
    except Exception:
        return []
    return out

def fetch_sina(limit=6):
    """新浪财经 7x24 全球直播快讯（公开 API，无需签名，稳定）"""
    out = []
    try:
        r = requests.get('https://zhibo.sina.com.cn/api/zhibo/feed?page=1&page_size=%d&zhibo_id=152&tag_id=0&dire=f&dpc=1' % (limit + 4),
                         headers=H, timeout=10)
        for it in r.json().get('result', {}).get('data', {}).get('feed', {}).get('list', []):
            t = clean_desc(it.get('rich_text') or '')
            if t:
                out.append({'title': t,
                            'link': it.get('docurl') or 'https://zhibo.sina.com.cn/7x24',
                            'date': it.get('create_time') or '', 'thumb': None})
    except Exception:
        return []
    return out

def fmt_sina_time(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M')
    except Exception:
        return ''

def fmt_date(s):
    try:
        return datetime.datetime.strptime(s[:25], '%a, %d %b %Y %H:%M:%S').strftime('%m-%d %H:%M')
    except Exception:
        return ''

def render_section(icon, title, sources, accent):
    cards = []
    for name, color, items in sources:
        if not items:
            continue
        for it in items:
            if is_dup(it['title']):
                continue
            mark_seen(it['title'])
            thumb = ''
            if it.get('thumb'):
                thumb = f'<img class="thumb" src="{htmlmod.escape(it["thumb"], quote=True)}" alt="" loading="lazy" onerror="this.parentNode.classList.add(\'noimg\')">'
            d = fmt_date(it['date']) or fmt_sina_time(it['date'])
            meta = f'<span class="meta-time">{d}</span>' if d else ''
            tip = f'<div class="tip">{htmlmod.escape(it["desc"])}</div>' if it.get('desc') else ''
            cards.append(
                f'<a class="item" style="--src:{color}" href="{htmlmod.escape(it["link"], quote=True)}" target="_blank" rel="noopener">'
                f'<div class="thumb-wrap">{thumb}<span class="src-badge">{name}</span></div>'
                f'<div class="item-body">{tip}<div class="item-title">{htmlmod.escape(it["title"])}</div>'
                f'<div class="item-meta">{meta}<span class="meta-src">{name}</span></div></div></a>')
    if not cards:
        return ''
    grid = '\n'.join(cards)
    return (f'<section class="sec" style="--ac:{accent}"><h2><span class="ic">{icon}</span>{title}</h2>'
            f'<div class="grid">{grid}</div></section>')

def render_links(title, items, accent):
    h = f'<section class="sec" style="--ac:{accent}"><h2><span class="ic">🔖</span>{title}</h2><div class="links">'
    for name, url, note in items:
        h += (f'<a class="link-card" href="{htmlmod.escape(url, quote=True)}" target="_blank" rel="noopener">'
              f'<span class="lc-name">{name}</span><span class="lc-note">{note}</span></a>')
    h += '</div></section>'
    return h

CSS = '''
:root{--bg:#f4f5f7;--card:#fff;--ink:#16181d;--mut:#71717a;--line:#e7e8ec}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter','SF Pro Text','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,sans-serif;background:var(--bg);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:28px 20px 48px}
header{padding:12px 2px 6px}
.home{display:inline-block;font-size:13px;font-weight:600;color:var(--mut);text-decoration:none;margin-bottom:10px}
.home:hover{color:var(--ac,#2563eb)}
h1{font-size:31px;font-weight:800;letter-spacing:-.5px}
.sub{color:var(--mut);font-size:14px;margin-top:8px}
.sub b{color:var(--ac,#2563eb);font-weight:600}
.sec{background:var(--card);border-radius:18px;padding:22px 22px 26px;margin:20px 0;box-shadow:0 1px 3px rgba(22,24,29,.05);border-top:4px solid var(--ac,#2563eb)}
h2{font-size:20px;font-weight:800;margin-bottom:16px;display:flex;align-items:center;gap:9px;letter-spacing:-.2px}
.ic{font-size:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.item{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;transition:transform .15s,box-shadow .15s;box-shadow:0 1px 2px rgba(22,24,29,.04)}
.item:hover{transform:translateY(-2px);box-shadow:0 10px 24px -10px rgba(22,24,29,.18)}
.thumb-wrap{position:relative;aspect-ratio:16/9;background:linear-gradient(135deg,color-mix(in srgb,var(--src,#888) 18%,#fff),color-mix(in srgb,var(--src,#888) 42%,#f0f0f0));display:flex;align-items:center;justify-content:center}
.thumb{width:100%;height:100%;object-fit:cover;display:block}
.thumb-wrap.noimg::before{content:attr(data-ini);font-size:34px;font-weight:800;color:color-mix(in srgb,var(--src,#888) 55%,#fff);letter-spacing:1px}
.src-badge{position:absolute;top:8px;left:8px;background:rgba(15,17,21,.72);color:#fff;font-size:11px;font-weight:600;padding:3px 9px;border-radius:999px;backdrop-filter:blur(4px)}
.item-body{padding:13px 15px 14px;display:flex;flex-direction:column;gap:7px;flex:1;position:relative}
.tip{position:absolute;left:8px;right:8px;bottom:46px;background:#20242e;color:#e9ebf2;font-size:13px;line-height:1.55;padding:10px 13px;border-radius:10px;opacity:0;visibility:hidden;transition:opacity .18s;z-index:6;box-shadow:0 8px 22px rgba(0,0,0,.25);pointer-events:none}
.item:hover .tip{opacity:1;visibility:visible}
.item-title{font-size:16.5px;font-weight:600;line-height:1.5;color:#1b1d23;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.item-meta{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#9a9aa5;margin-top:auto}
.meta-time{white-space:nowrap}
.meta-src{color:var(--src,#888);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.links{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.link-card{display:block;background:#f8f9fb;border:1px solid var(--line);border-radius:12px;padding:13px 16px;text-decoration:none;transition:all .15s}
.link-card:hover{background:#eef2fb;border-color:#c6d4f2;transform:translateY(-1px)}
.lc-name{display:block;font-size:15px;font-weight:700;color:#1b1d23}
.lc-note{display:block;font-size:13px;color:var(--mut);margin-top:3px}
footer{color:#a3a3ad;font-size:12.5px;text-align:center;padding:24px 0 8px}
@media(max-width:640px){.wrap{padding:18px 12px 36px}h1{font-size:26px}h2{font-size:18px}.grid{grid-template-columns:1fr 1fr;gap:10px}.item-title{font-size:15px}}
@media(max-width:420px){.grid{grid-template-columns:1fr}}
'''

def main():
    world = [('全球要闻', '#b91c1c', fetch_rss('https://feeds.bbci.co.uk/news/world/rss.xml')),
             ('科技', '#7c3aed', fetch_rss('https://feeds.bbci.co.uk/news/technology/rss.xml')),
             ('商业', '#1d4ed8', fetch_rss('https://feeds.bbci.co.uk/news/business/rss.xml')),
             ('市场', '#047857', fetch_rss('https://www.investing.com/rss/news_25.rss'))]
    ai = [('量子位', '#6d28d9', fetch_rss('https://www.qbitai.com/feed')),
          ('TechCrunch AI', '#0f766e', fetch_rss('https://techcrunch.com/category/artificial-intelligence/feed/'))]
    game = [('Game Developer', '#4f46e5', fetch_rss('https://www.gamedeveloper.com/rss.xml')),
            ('Eurogamer', '#be185d', fetch_rss('https://www.eurogamer.net/feed')),
            ('机核 GCORES', '#7c2d12', fetch_rss('https://www.gcores.com/rss'))]
    crypto = [('Cointelegraph', '#b45309', fetch_rss('https://cointelegraph.com/rss')),
              ('RH Chain', '#dc2626', fetch_rss('https://news.google.com/rss/search?q=robinhood%20chain&hl=en-US&gl=US&ceid=US:en')),
              ('中文聚合', '#0e7490', fetch_rss('https://news.google.com/rss/search?q=bitcoin%20crypto&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'))]
    # 中文快讯（华尔街见闻 + 新浪 7x24 各取 5 条，合并去重）
    cn = [('华尔街见闻', '#be123c', fetch_wscn(5)),
          ('新浪 7x24', '#ea580c', fetch_sina(5))]
    # 收藏与信号源（第 3/4 层直达卡片，非抓取）
    now = datetime.datetime.now().strftime('%Y-%m-%d %A')
    page = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>晨间信息流 · {now}</title>
<style>{CSS}</style></head><body><div class="wrap">
<header><a class="home" href="/">← 返回首页</a><h1>☕ 晨间信息流</h1>
<div class="sub">{now} · 更新于 <b>{datetime.datetime.now().strftime('%H:%M')}</b> · 点击卡片直达原文</div></header>
{render_section('🌍', '全球重要新闻', world, '#2563eb')}
{render_section('🤖', 'AI 产业', ai, '#7c3aed')}
{render_section('🎮', '游戏产业', game, '#4f46e5')}
{render_section('📈', '加密行业', crypto, '#f7931a')}
{render_section('⚡', '中文快讯', cn, '#e11d48')}
{render_links('收藏与信号源', [
    ('财联社电报', 'https://www.cls.cn/telegraph', '中文实时电报'),
    ('金十数据', 'https://www.jin10.com/', '宏观速递'),
    ('Rob Carver 博客', 'https://qoppac.blogspot.com', '系统化交易'),
    ('QuantStart', 'https://www.quantstart.com/articles/', '量化教程'),
    ('Lyn Alden', 'https://www.lynalden.com/', '宏观 + BTC 深度'),
    ('Glassnode Insights', 'https://insights.glassnode.com/', '链上数据周报'),
    ('Chris Camillo (X)', 'https://x.com/chriscamillo', '社交套利信号源'),
    ('Kobeissi Letter (X)', 'https://x.com/KobeissiLetter', '美股市场快评'),
    ('因子清单', 'https://github.com/firevenus/firevenus.github.io', 'BTC 因子注册表(本地)'),
], '#0f6e56')}
<footer>晨间信息流 v0.10 · 每日 07:00 自动更新 · 数据来自公开 RSS/API</footer>
</div></body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(page)
    print('OK ->', OUT)

if __name__ == '__main__':
    import requests
    main()
