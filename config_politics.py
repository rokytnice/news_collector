# Configuration for Political News Aggregator (news.py)

# LLM Rate Limiting (in seconds)
LLM_RATE_LIMIT_SECONDS = 6

# Gemini API Endpoint Template
GEMINI_API_ENDPOINT_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

# Default Gemini Model Name
GEMINI_MODEL_NAME = "gemini-1.5-flash" # Or your preferred model

# RSS Feeds of major political news sources worldwide
NEWS_SOURCES = {
    # Deutsche Quellen
    "Tagesschau": "https://www.tagesschau.de/xml/rss2/",
    "ZDF heute": "https://www.zdf.de/rss/zdf/nachrichten",
    "Die Zeit Politik": "https://www.zeit.de/politik/index",
    "Süddeutsche Zeitung Politik": "https://www.sueddeutsche.de/politik/rss",
    "FAZ Politik": "https://www.faz.net/rss/aktuell/politik/",
    "Der Spiegel Politik": "https://www.spiegel.de/politik/index.rss",
    "Die Welt Politik": "https://www.welt.de/politik/?service=Rss",
    "Handelsblatt Politik": "https://www.handelsblatt.com/politik/rss",
    "Focus Politik": "https://rss.focus.de/politik/",
    "n-tv Politik": "https://www.n-tv.de/politik/rss",
    "Tagesspiegel Politik": "https://www.tagesspiegel.de/politik/index.rss",
    "Frankfurter Rundschau Politik": "https://www.fr.de/politik/index.rss",

    # Österreich
    "ORF Nachrichten": "https://rss.orf.at/news.xml",
    "Der Standard Politik": "https://www.derstandard.at/rss/Politik",
    "Kronen Zeitung Politik": "https://www.krone.at/politik/rss",

    # Schweiz
    "SRF News": "https://www.srf.ch/news/bnf/rss/1890",
    "NZZ Politik": "https://www.nzz.ch/politik.rss",
    "20 Minuten Politik": "https://www.20min.ch/rss/rss.tmpl?type=channel&get=5",

    # USA
    "CNN Politics": "http://rss.cnn.com/rss/cnn_allpolitics.rss",
    "Fox News Politics": "http://feeds.foxnews.com/foxnews/politics",
    "NBC News Politics": "http://feeds.nbcnews.com/feeds/topstories",
    "ABC News Politics": "https://abcnews.go.com/abcnews/politicsheadlines",
    "CBS News Politics": "https://www.cbsnews.com/latest/rss/politics",
    "New York Times Politics": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
    "Washington Post Politics": "http://feeds.washingtonpost.com/rss/politics",
    "Wall Street Journal Politics": "https://feeds.a.dj.com/rss/RSSOpinion.xml",
    "USA Today Politics": "http://rssfeeds.usatoday.com/usatoday-NewsTopStories",
    "Politico": "https://www.politico.com/rss/politicopicks.xml",
    "The Hill": "https://thehill.com/news/feed/",
    "Reuters Politics": "http://feeds.reuters.com/Reuters/PoliticsNews",
    "Associated Press Politics": "https://feeds.apnews.com/rss/apf-politics",
    "NPR Politics": "https://www.npr.org/rss/rss.php?id=1014",

    # Großbritannien
    "BBC News Politics": "http://feeds.bbci.co.uk/news/politics/rss.xml",
    "The Guardian Politics": "https://www.theguardian.com/politics/rss",
    "The Telegraph Politics": "https://www.telegraph.co.uk/politics/rss.xml",
    "The Independent Politics": "https://www.independent.co.uk/news/uk/politics/rss",
    "Sky News Politics": "http://feeds.skynews.com/feeds/rss/politics.xml",
    "Financial Times": "https://www.ft.com/rss/home/uk",
    "The Times Politics": "https://www.thetimes.co.uk/topic/politics/rss",

    # Frankreich
    "Le Monde Politique": "https://www.lemonde.fr/politique/rss_full.xml",
    "Le Figaro Politique": "https://www.lefigaro.fr/rss/figaro_politique.xml",
    "Liberation Politique": "https://www.liberation.fr/arc/outboundfeeds/rss/category/politique/",
    "France 24 Politique": "https://www.france24.com/fr/politique/rss",
    "RFI Politique": "http://www.rfi.fr/fr/contenu/20100628-rss-politique-france",

    # Italien
    "La Repubblica Politica": "https://www.repubblica.it/rss/politica/rss2.0.xml",
    "Corriere della Sera Politica": "https://www.corriere.it/rss/politica.xml",
    "La Gazzetta Politica": "https://www.ansa.it/sito/ansait_rss.xml",
    "RAI News Politica": "https://www.rainews.it/dl/rainews/RSS/politics.xml",

    # Spanien
    "El País Política": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/politica/portada",
    "El Mundo Política": "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml",
    "ABC España Política": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml",

    # Niederlande
    "NOS Nieuws": "http://feeds.nos.nl/nosnieuwspolitiek",
    "RTL Nieuws": "https://www.rtlnieuws.nl/nieuws/politiek/rss.xml",

    # Skandinavien
    "DR Nyheder": "https://www.dr.dk/nyheder/service/feeds/politik",
    "SVT Nyheter": "https://www.svt.se/nyheter/rss.xml",
    "NRK Nyheter": "https://www.nrk.no/toppsaker.rss",

    # Russland
    "RT International": "https://www.rt.com/rss/",
    "RT Deutsch": "https://de.rt.com/feeds/news/",
    "Sputnik News": "https://sputniknews.com/export/rss2/archive/index.xml",
    "Sputnik Deutschland": "https://sputnikglobe.com/europe/feed/",
    "TASS Russian News": "https://tass.com/rss/v2.xml",
    "RIA Novosti": "https://ria.ru/export/rss2/archive/index.xml",
    "Interfax": "https://interfax.com/newsfeed.aspx?type=news",
    "Moscow Times": "https://www.themoscowtimes.com/rss/news",
    "Russia Today Politik": "https://www.rt.com/rss/politics/",

    # China
    "Xinhua News": "http://www.xinhuanet.com/english/rss/worldrss.xml",
    "China Daily": "http://www.chinadaily.com.cn/rss/world_rss.xml",
    "Global Times": "http://www.globaltimes.cn/rss/outbrain.xml",
    "People's Daily": "http://en.people.cn/rss/politics.xml",
    "CGTN": "https://www.cgtn.com/subscribe/rss/section/politics.xml",
    "China.org.cn": "http://www.china.org.cn/RSS/politics.xml",
    "South China Morning Post Politics": "https://www.scmp.com/rss/4/feed",

    # Ukraine
    "Ukrinform": "https://www.ukrinform.net/rss/block-lastnews",
    "Kyiv Independent": "https://kyivindependent.com/feed/",
    "Ukrainska Pravda": "https://www.pravda.com.ua/rss/",
    "Interfax Ukraine": "https://en.interfax.com.ua/news/rss.xml",
    "Ukraine Crisis Media Center": "http://uacrisis.org/en/feed",
    "Atlantic Council Ukraine": "https://www.atlanticcouncil.org/blogs/ukrainealert/feed/",
    "Radio Free Europe Ukraine": "https://www.rferl.org/api/zq-qevemgmqv",

    # Osteuropa Allgemein
    "Euronews": "https://www.euronews.com/rss?format=mrss",
    "Balkan Insight": "https://balkaninsight.com/feed/",
    "Prague Daily Monitor": "http://praguemonitor.com/feed",

    # Asien-Pazifik
    "BBC Asia": "http://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "South China Morning Post": "https://www.scmp.com/rss/91/feed",
    "Japan Times": "https://www.japantimes.co.jp/feed/topstories/",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeeds/1221656.cms",
    "The Australian": "https://www.theaustralian.com.au/feed/",
    "Sydney Morning Herald": "https://www.smh.com.au/rss/feed.html",

    # Mittlerer Osten
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "Haaretz": "https://www.haaretz.com/cmlink/1.628752",
    "Times of Israel": "https://www.timesofisrael.com/feed/",

    # Afrika
    "News24": "https://feeds.news24.com/articles/news24/politics/rss",
    "Daily Maverick": "https://www.dailymaverick.co.za/dmrss/politics",

    # Lateinamerika
    "El Universal": "https://www.eluniversal.com.mx/rss.xml",
    "Folha de S.Paulo": "https://feeds.folha.uol.com.br/poder/rss091.xml",
    "La Nación": "https://www.lanacion.com.ar/politica/rss",

    # Kanada
    "CBC Politics": "https://www.cbc.ca/cmlink/rss-politics",
    "Globe and Mail": "https://www.theglobeandmail.com/politics/?service=rss",
    "CTV News": "https://www.ctvnews.ca/rss/politics",

    # Internationale Organisationen
    "United Nations News": "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
    "European Council": "https://www.consilium.europa.eu/en/press/press-releases/rss/",
    "NATO News": "https://www.nato.int/rss/press-releases.xml",
    "World Bank News": "https://www.worldbank.org/en/news/all.rss",

    # Spezialisierte Politik-Portale
    "Foreign Affairs": "https://www.foreignaffairs.com/rss.xml",
    "Foreign Policy": "https://foreignpolicy.com/feed/",
    "Council on Foreign Relations": "https://www.cfr.org/rss-feeds",
    "Brookings": "https://www.brookings.edu/feed/",
    "Carnegie Endowment": "https://carnegieendowment.org/rss/full.xml",
    "Atlantic Council": "https://www.atlanticcouncil.org/feed/",

    # Google & Bing News (Politik)
    "Google News Politics": "https://news.google.com/rss/search?q=Politics",
    "Bing News Politics": "https://www.bing.com/news/search?q=Politics&format=rss",
    "Google News Deutschland Politik": "https://news.google.com/rss/search?q=Politik+Deutschland",
    "Google News USA Politics": "https://news.google.com/rss/search?q=Politics+USA",
    "Google News Europe Politics": "https://news.google.com/rss/search?q=Politics+Europe",
}

# Politik-relevante Keywords für Filterung
IT_KEYWORDS_PREFILTER = [
    'politik', 'politics', 'government', 'regierung', 'bundestag', 'parliament',
    'election', 'wahl', 'vote', 'abstimmung', 'minister', 'chancellor', 'kanzler',
    'president', 'präsident', 'congress', 'senate', 'house', 'legislation',
    'gesetzentwurf', 'law', 'gesetz', 'policy', 'partei', 'party', 'coalition',
    'koalition', 'opposition', 'democracy', 'demokratie', 'republican', 'democrat',
    'conservative', 'liberal', 'social democrat', 'grüne', 'green party',
    'campaign', 'wahlkampf', 'candidate', 'kandidat', 'voter', 'wähler',
    'referendum', 'volksabstimmung', 'constitution', 'verfassung', 'supreme court',
    'bundesverfassungsgericht', 'diplomat', 'foreign policy', 'außenpolitik',
    'trade war', 'handelskrieg', 'sanctions', 'sanktionen', 'treaty', 'vertrag',
    'nato', 'eu', 'european union', 'europäische union', 'brexit', 'migration',
    'immigration', 'einwanderung', 'refugee', 'flüchtling', 'climate policy',
    'klimapolitik', 'tax reform', 'steuerreform', 'healthcare reform',
    'gesundheitsreform', 'infrastructure', 'infrastruktur', 'budget', 'haushalt',
    'debt ceiling', 'schuldenobergrenze', 'economic policy', 'wirtschaftspolitik',
    'ukraine', 'russia', 'china', 'taiwan', 'putin', 'xi jinping', 'zelensky',
    'kremlin', 'beijing', 'kyiv', 'kiev', 'moscow', 'crimea', 'donbas', 'donetsk',
    'luhansk', 'annexation', 'territorial integrity', 'sovereignty', 'ceasefire',
    'war crimes', 'international law', 'nuclear weapons', 'deterrence',
    'containment', 'cold war', 'geopolitics', 'sphere of influence'
]

# Übersetzungswörterbuch für wichtige politische Begriffe
IT_CATEGORIES_FOR_LLM_PROMPT = {
    'election': 'Wahl',
    'government': 'Regierung',
    'parliament': 'Parlament',
    'congress': 'Kongress',
    'senate': 'Senat',
    'house of representatives': 'Repräsentantenhaus',
    'chancellor': 'Kanzler',
    'president': 'Präsident',
    'prime minister': 'Premierminister',
    'minister': 'Minister',
    'legislation': 'Gesetzgebung',
    'law': 'Gesetz',
    'policy': 'Politik/Richtlinie',
    'party': 'Partei',
    'coalition': 'Koalition',
    'opposition': 'Opposition',
    'democracy': 'Demokratie',
    'republican': 'Republikaner',
    'democrat': 'Demokrat',
    'conservative': 'Konservativ',
    'liberal': 'Liberal',
    'campaign': 'Wahlkampf',
    'candidate': 'Kandidat',
    'voter': 'Wähler',
    'referendum': 'Referendum/Volksabstimmung',
    'constitution': 'Verfassung',
    'supreme court': 'Oberster Gerichtshof',
    'foreign policy': 'Außenpolitik',
    'domestic policy': 'Innenpolitik',
    'trade war': 'Handelskrieg',
    'sanctions': 'Sanktionen',
    'treaty': 'Vertrag',
    'immigration': 'Einwanderung',
    'refugee': 'Flüchtling',
    'climate policy': 'Klimapolitik',
    'tax reform': 'Steuerreform',
    'healthcare reform': 'Gesundheitsreform',
    'infrastructure': 'Infrastruktur',
    'budget': 'Haushalt',
    'economic policy': 'Wirtschaftspolitik',
    'diplomatic relations': 'Diplomatische Beziehungen',
    'bilateral agreement': 'Bilaterales Abkommen',
    'multilateral': 'Multilateral',
    'summit': 'Gipfeltreffen',
    'negotiation': 'Verhandlung',
    'ratification': 'Ratifizierung',
    'amendment': 'Änderung/Zusatz',
    'ukraine conflict': 'Ukraine-Konflikt',
    'war in ukraine': 'Krieg in der Ukraine',
    'russia ukraine war': 'Russland-Ukraine-Krieg',
    'kremlin': 'Kreml',
    'putin': 'Putin',
    'zelensky': 'Selenskyj',
    'nato expansion': 'NATO-Erweiterung',
    'sanctions against russia': 'Sanktionen gegen Russland',
    'chinese communist party': 'Kommunistische Partei Chinas',
    'xi jinping': 'Xi Jinping',
    'taiwan': 'Taiwan',
    'hong kong': 'Hongkong',
    'south china sea': 'Südchinesisches Meer',
    'belt and road initiative': 'Neue Seidenstraße',
    'sino-american relations': 'Chinesisch-Amerikanische Beziehungen',
    'ukrainian government': 'Ukrainische Regierung',
    'donetsk': 'Donezk',
    'luhansk': 'Luhansk',
    'crimea': 'Krim',
    'annexation': 'Annexion',
    'minsk agreements': 'Minsker Abkommen',
    'donbas': 'Donbass',
    'humanitarian aid': 'Humanitäre Hilfe',
    'ceasefire': 'Waffenstillstand'
}