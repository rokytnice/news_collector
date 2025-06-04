# Configuration for IT News Aggregator

# LLM Rate Limiting (in seconds)
LLM_RATE_LIMIT_SECONDS = 6

# Gemini API Endpoint Template
GEMINI_API_ENDPOINT_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

# Default Gemini Model Name
GEMINI_MODEL_NAME = "gemini-1.5-flash" # Or your preferred model

# RSS Feeds of major IT news sources
NEWS_SOURCES = {
    # Deutsche Quellen
    "Heise Online": "https://www.heise.de/rss/heise-atom.xml",
    "Golem.de": "https://rss.golem.de/rss.php?feed=ATOM1.0",
    "t3n": "https://t3n.de/rss.xml",
    "Computerwoche": "https://www.computerwoche.de/rss/news.xml",
    "ZDNet.de": "https://www.zdnet.de/feed/",

    # Internationale Quellen
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index",
    "Wired": "https://www.wired.com/feed/rss",
    "Engadget": "https://www.engadget.com/rss.xml",
    "TechRadar": "https://www.techradar.com/rss",
    "CNET": "https://www.cnet.com/rss/news/",
    "ZDNet": "https://www.zdnet.com/news/rss.xml",  # International ZDNet
    "VentureBeat": "https://venturebeat.com/feed/",
    "Mashable Tech": "https://mashable.com/feeds/rss/tech",
    "Gizmodo": "https://gizmodo.com/rss",
    "Tom's Hardware": "https://www.tomshardware.com/feeds/all",
    "AnandTech": "https://www.anandtech.com/rss/",
    "PCWorld": "https://www.pcworld.com/index.rss",
    "InfoWorld": "https://www.infoworld.com/news/index.rss",
    "Network World": "https://www.networkworld.com/news/index.rss",
    "CSO Online": "https://www.csoonline.com/news/index.rss",
    "Dark Reading": "https://www.darkreading.com/rss_simple.asp",
    "SecurityWeek": "https://www.securityweek.com/feed",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "KrebsOnSecurity": "https://krebsonsecurity.com/feed/",
    "Threatpost": "https://threatpost.com/feed/",
    "IT World Canada": "https://www.itworldcanada.com/feed",
    "ITNews Australia": "https://www.itnews.com.au/RSS/rss.ashx",
    "ComputerWeekly": "https://www.computerweekly.com/rss/latest-it-news.xml",
    "The Register": "https://www.theregister.com/headlines.atom",
    "ITProPortal": "https://www.itpro.com/rss",  # Note: ITPro changed from itpro.co.uk
    "TechTarget": "https://www.techtarget.com/rss/",  # Generic, might need specific sub-feeds
    "eWeek": "https://www.eweek.com/feed/",
    "PCMag": "https://www.pcmag.com/feeds/news.xml",
    "Digital Trends": "https://www.digitaltrends.com/feed/",
    "How-To Geek": "https://www.howtogeek.com/feed/",
    "9to5Mac": "https://9to5mac.com/feed/",
    "9to5Google": "https://9to5google.com/feed/",
    "Android Police": "https://www.androidpolice.com/feed/",
    "XDA Developers": "https://www.xda-developers.com/feed/",
    "Slashgear": "https://www.slashgear.com/feed/",
    "Neowin": "https://www.neowin.net/rss/",
    "TechSpot": "https://www.techspot.com/backend/headlines.xml",
    "Phoronix": "https://www.phoronix.com/rss.php",
    "Linux Today": "https://feeds.feedburner.com/linuxtoday/linux",
    "OMG! Ubuntu!": "https://www.omgubuntu.co.uk/feed",
    "It's FOSS": "https://itsfoss.com/rss/",
    "Hacker News": "https://hnrss.org/frontpage",  # Note: This is a community-curated link aggregator
    "GitHub Blog": "https://github.blog/feed/",
    "Stack Overflow Blog": "https://stackoverflow.blog/feed/",
    "Google AI Blog": "https://ai.googleblog.com/feeds/posts/default",  # Corrected from http
    "Microsoft Tech Community": "https://techcommunity.microsoft.com/gxcuf89792/rss/board?board.id=MicrosoftIgnite",
    # Example, specific boards needed
    "AWS News": "https://aws.amazon.com/about-aws/whats-new/recent/feed/",
    "Docker Blog": "https://www.docker.com/blog/feed/",  # Corrected from /feed/
    "Red Hat Blog": "https://www.redhat.com/en/rss/blog"
}

# Defined IT keywords for pre-filtering
IT_KEYWORDS_PREFILTER = [
    'software', 'hardware', 'tech', 'computer', 'digital',
    'internet', 'cyber', 'security', 'data', 'ai', 'artificial intelligence',
    'programming', 'developer', 'code', 'app', 'mobile', 'cloud',
    'server', 'network', 'database', 'algorithm', 'startup',
    'google', 'microsoft', 'java', 'amazon', 'meta', 'tesla',
    'blockchain', 'cryptocurrency', 'bitcoin', 'web', 'api',
    'machine learning', 'automation', 'robotics', 'iot',
    'virtual reality', 'augmented reality', 'database', 'os', 'kernel',
    'cpu', 'gpu', 'storage', 'devops', 'container', 'kubernetes',
    'exploit', 'vulnerability', 'patch', 'malware', 'ransomware', 'phishing'
]

# String of IT categories for the LLM prompt
IT_CATEGORIES_FOR_LLM_PROMPT = (
    "Softwareentwicklung (Programming, Coding, Frameworks, Libraries, Tools), "
    "Künstliche Intelligenz (AI, Machine Learning, Deep Learning, NLP), "
    "Cybersicherheit (Security, Vulnerabilities, Exploits, Patches, Malware, Data Breaches), "
    "Cloud Computing (AWS, Azure, GCP, SaaS, PaaS, IaaS), "
    "Hardware-Innovationen (CPUs, GPUs, Mobile Devices, IoT), "
    "Betriebssysteme (Linux, Windows, macOS, Android, iOS), "
    "Netzwerktechnologien (5G, Networking Protocols, Infrastructure), "
    "Datenbanken und Datenmanagement (SQL, NoSQL, Big Data), "
    "DevOps und Site Reliability Engineering (SRE), "
    "Web-Technologien (Frontend, Backend, APIs), "
    "Tech-Industrie Nachrichten (Major Companies, Startups, Trends), "
    "Open Source Projekte und Communities."
)