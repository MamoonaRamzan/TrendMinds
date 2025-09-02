import feedparser

feeds = [
    
  #AI:
    "https://huggingface.co/blog/feed.xml",
    "https://blogs.microsoft.com/ai/feed",
    "https://syncedreview.com/feed/",
    "https://www.marktechpost.com/feed/",
    "https://www.topbots.com/feed/",
    "https://artificialintelligence-news.com/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://aws.amazon.com/blogs/machine-learning/feed/",
    "https://towardsdatascience.com/feed",
    "https://kdnuggets.com/feed",
    "https://datafloq.com/feed",

  #Crypto:
    "https://cointelegraph.com/rss",
    "https://news.bitcoin.com/feed/",
    "https://decrypt.co/feed",
    "https://cryptoslate.com/feed/",

  #Climate:
    "https://www.theguardian.com/environment/climate-crisis/rss",
    "https://www.nature.com/subjects/climate-change.rss",
    "https://cleantechnica.com/feed/",
    "https://grist.org/feed/",
    "https://www.carbonbrief.org/feed/",

  #Tech:
    "https://www.wired.com/feed/rss",
    "https://thenextweb.com/feed/",
    "https://spectrum.ieee.org/rss/fulltext",
    "https://www.technologyreview.com/feed/",
    "https://www.fastcompany.com/section/technology/rss",
    "https://www.zdnet.com/news/rss.xml",
    "https://feeds.feedburner.com/venturebeat/SZYF",
    "https://inc42.com/feed/",
    "https://www.ycombinator.com/blog/rss/",
    "https://futureoflife.org/feed/",

  #Business:
    "https://www.forbes.com/innovation/feed/",
    "https://www.fastcompany.com/section/work-life/rss",
    "https://www.hcamag.com/rss",

  #Health & Biotech:
    "https://www.healthit.gov/buzz-blog/feed/",
    "https://medicalxpress.com/rss-feed/",
    "https://www.digitalhealth.net/feed/",
    "https://www.biotechniques.com/feed/",
    "https://www.labiotech.eu/feed/",
    "https://www.nature.com/subjects/biotechnology.rss",
    "https://www.genengnews.com/feed/",

  #Space:
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://spacenews.com/feed/",
    "https://www.space.com/feeds/all",
    "https://arstechnica.com/science/space/rss",

  #Education (EdTech):
    "https://www.classcentral.com/report/feed/",
    "https://edtechmagazine.com/k12/rss.xml",
    "https://edtechmagazine.com/higher/rss.xml",
    "https://elearningindustry.com/feed",

  #Media & Culture:
    "https://www.creativebloq.com/feed",
    "https://variety.com/c/tech/feed/",

  #Science & Research:
    "https://www.sciencedaily.com/rss/top/science.xml",
    "https://www.sciencenews.org/feed",
    "https://www.newscientist.com/feed/home/",
    "https://phys.org/rss-feed/",

  #Cybersecurity:
    "https://www.schneier.com/feed/atom/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml",

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
