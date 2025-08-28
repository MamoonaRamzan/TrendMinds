import feedparser

feeds = [
    "https://venturebeat.com/category/ai/feed/",
    "https://spectrum.ieee.org/artificial-intelligence/rss",
    "https://feeds.feedburner.com/thenextweb",
    "https://huggingface.co/blog/feed.xml",
    "https://feeds.feedburner.com/oreilly/radar/atom",
    "https://syncedreview.com/feed/",
    "http://export.arxiv.org/rss/cs.AI",
    "http://export.arxiv.org/rss/cs.LG",
    "https://blogs.microsoft.com/ai/feed/",
    "https://aws.amazon.com/blogs/machine-learning/feed/",
    "https://engineering.fb.com/feed/",
]

print("🔎 Checking feeds...\n")

for url in feeds:
    try:
        d = feedparser.parse(url)
        if d.bozo:
            print(f"❌ Error parsing: {url}")
        elif not d.entries:
            print(f"⚠️ No entries found: {url}")
        else:
            print(f"✅ Working: {url} ({len(d.entries)} entries)")
    except Exception as e:
        print(f"❌ Exception for {url}: {e}")

print("\n✅ Feed check complete.")

