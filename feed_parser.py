# updated_feed_check.py
import feedparser
import requests
from time import sleep

feeds = [
    # === AI & Data Science ===
    "https://huggingface.co/blog/feed.xml",
    "https://rss.arxiv.org/atom/cs.AI",      # arXiv atom (cs.AI)
    "https://rss.arxiv.org/atom/cs.LG",      # arXiv atom (cs.LG)
    "https://syncedreview.com/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://towardsdatascience.com/feed",

    # === Market & Business Innovation ===
    "https://www.forbes.com/innovation/feed/",
    "https://www.fastcompany.com/section/technology/rss",
    "https://feeds.feedburner.com/venturebeat/SZYF",

    # === Biotech & Healthcare Innovation ===
    "https://www.nature.com/subjects/biotechnology.rss",
    "https://www.genengnews.com/feed/",
    "https://www.labiotech.eu/feed/",
    "https://medicalxpress.com/rss-feed/",

    # === Climate & Sustainability ===
    "https://www.nature.com/subjects/climate-change.rss",
    "https://www.carbonbrief.org/feed/",
    "https://grist.org/feed/",
    "https://cleantechnica.com/feed/",

    # === Space & Frontier Tech ===
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://spacenews.com/feed/",
    "https://www.space.com/feeds/all",
    "https://arstechnica.com/science/space/rss",

    # === Cybersecurity & Risk ===
    "https://www.schneier.com/feed/atom/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.cybersecuritydive.com/feeds/news/",
    "https://www.securityweek.com/rss.xml",

    # === Science & Research ===
    "https://www.sciencedaily.com/rss/top/science.xml",
    "https://phys.org/rss-feed/",
    "https://www.newscientist.com/feed/home/",

    # === FinTech & Digital Economy ===
    "https://www.finextra.com/rss/rss.aspx",         # replaced (Finextra RSS page)
    "https://www.pymnts.com/feed/",
    "https://www.americanbanker.com/feed",          # replaced (in lieu of The Financial Brand)
    "https://www.crowdfundinsider.com/feed/",

    # === Policy & Regulation ===
    "https://www.justsecurity.org/feed/",           # replaced (in lieu of Lawfare feed)
    "https://oecd.ai/rss",                          # try OECD (if it fails, fallback will show)
    "https://agenda.weforum.org/feed/",             # replaced (WEF Agenda feed)
    "https://www.brookings.edu/topic/technology/feed/",

    # === Venture Capital & Startups ===
    "https://news.crunchbase.com/feed/",
    "https://future.a16z.com/feed/",
    "https://tech.eu/feed/",
    # cbinsights is often behind auth; leave commented or use their API:
    # "https://www.cbinsights.com/research/feed",

    # === Future of Work & Productivity ===
    "https://www.mckinsey.com/featured-insights/rss-feed",  # updated McKinsey feed endpoint
    "https://www2.deloitte.com/feeds/insights/rss.xml",    # Deloitte Insights (try this)
    "https://www.gartner.com/en/newsroom/rss",

    # === Supply Chain & Industry 4.0 ===
    "https://www.manufacturing.net/rss.xml",
    "https://www.industryweek.com/rss/industryweek-news",   # try IW endpoint
    "https://www.logisticsmgmt.com/rss",                    # try LM rss endpoint

    # === Energy & CleanTech ===
    "https://www.eia.gov/rss/todayinenergy.xml",    # replaced (EIA Today in Energy)
    "https://www.renewableenergyworld.com/feed/",
    "https://www.energymonitor.ai/feed/",
    "https://www.pv-tech.org/feed/",

    # === Healthcare & Digital Health Business ===
    "https://healthtechmagazine.net/rss.xml",
    "https://www.fiercehealthcare.com/rss/xml",
    "https://www.medtechdive.com/feeds/news/",
    "https://feeds.feedburner.com/beckershospitalreview",
]

# Helpful headers to avoid simple bot-blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept": "application/rss+xml, application/atom+xml, text/xml, */*;q=0.1"
}

print("🔎 Checking feeds...\n")

for url in feeds:
    try:
        # 1) try fetching via requests (better for sites that block basic clients)
        r = requests.get(url, headers=HEADERS, timeout=12, allow_redirects=True)
        r.raise_for_status()
        d = feedparser.parse(r.content)

        # fallback: sometimes direct parse(url) works even if content parse fails
        if d.bozo and (not d.entries):
            # try direct parse (lets feedparser follow canonical feed locations)
            d2 = feedparser.parse(url)
            if not d2.bozo and d2.entries:
                d = d2

        if d.bozo:
            # print bozo exception if available
            bozo_exc = getattr(d, "bozo_exception", None)
            if bozo_exc:
                print(f"❌ Error parsing: {url} — {type(bozo_exc).__name__}: {bozo_exc}")
            else:
                print(f"❌ Error parsing: {url} (bozo flag set, unknown reason)")
        elif not d.entries:
            print(f"⚠️ No entries found: {url}")
        else:
            print(f"✅ Working: {url} ({len(d.entries)} entries)")
    except requests.exceptions.HTTPError as he:
        print(f"❌ HTTPError for {url}: {he}")
    except requests.exceptions.ConnectTimeout:
        print(f"❌ Timeout connecting to {url}")
    except Exception as e:
        # Last-ditch: try feedparser.parse(url) (some servers behave differently to direct fetch)
        try:
            d = feedparser.parse(url)
            if d.entries:
                print(f"✅ Working via feedparser.parse(): {url} ({len(d.entries)} entries)")
            else:
                print(f"❌ Exception for {url}: {e}")
        except Exception as e2:
            print(f"❌ Exception for {url}: {e} / fallback failed: {e2}")

    # be polite (avoid hammering)
    sleep(0.3)

print("\n✅ Feed check complete.")
