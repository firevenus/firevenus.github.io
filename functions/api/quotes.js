// Cloudflare Pages Function: GET /api/quotes?s=^GSPC,GC=F,BTC-USD
// Proxies Yahoo Finance chart API (keyless), adds caching to stay within free tiers.
const YAHOO = 'https://query1.finance.yahoo.com/v8/finance/chart';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131 Safari/537.36';

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const symbols = (url.searchParams.get('s') || '^GSPC,^IXIC,^DJI,GC=F,BTC-USD')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, 30);

  const results = await Promise.allSettled(symbols.map(fetchQuote));
  const quotes = results.map((r, i) =>
    r.status === 'fulfilled' ? r.value : { symbol: symbols[i], error: true }
  );

  return new Response(
    JSON.stringify({ updated: new Date().toISOString(), quotes }),
    {
      headers: {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': 'public, max-age=60',
        'access-control-allow-origin': '*',
      },
    }
  );
}

async function fetchQuote(symbol) {
  const u = `${YAHOO}/${encodeURIComponent(symbol)}?range=1d&interval=15m`;
  const res = await fetch(u, { headers: { 'User-Agent': UA } });
  if (!res.ok) throw new Error(`yahoo ${res.status}`);
  const j = await res.json();
  const result = j?.chart?.result?.[0];
  if (!result) throw new Error('empty');
  const meta = result.meta || {};
  const price = meta.regularMarketPrice;
  const prev = meta.previousClose ?? meta.chartPreviousClose;
  const closes = (result.indicators?.quote?.[0]?.close || []).filter(
    (c) => typeof c === 'number'
  );
  return {
    symbol,
    name: meta.shortName || meta.longName || symbol,
    currency: meta.currency || '',
    exchange: meta.fullExchangeName || meta.exchangeName || '',
    price: typeof price === 'number' ? price : null,
    previousClose: typeof prev === 'number' ? prev : null,
    change: typeof price === 'number' && typeof prev === 'number' ? price - prev : null,
    marketTime: meta.regularMarketTime ? meta.regularMarketTime * 1000 : null,
    spark: closes.slice(-60),
  };
}
