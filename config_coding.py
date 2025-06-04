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
    "NBC News Politics": "http://feeds.nbcnews.com/feeds/topstories", # Allgemein, oft mit Politikfokus
    "ABC News Politics": "https://abcnews.go.com/abcnews/politicsheadlines",
    "CBS News Politics": "https://www.cbsnews.com/latest/rss/politics",
    "New York Times Politics": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
    "Washington Post Politics": "http://feeds.washingtonpost.com/rss/politics",
    "Wall Street Journal Politics": "https://feeds.a.dj.com/rss/RSSOpinion.xml", # Meinungen, oft politisch
    "USA Today Politics": "http://rssfeeds.usatoday.com/usatoday-NewsTopStories", # Allgemein, oft mit Politikfokus
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
    "Financial Times": "https://www.ft.com/rss/home/uk", # Fokus Wirtschaft, aber starke politische Implikationen
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
    "ANSA Politica": "https://www.ansa.it/sito/ansait_rss.xml", # Allgemein, enthält Politik
    "RAI News Politica": "https://www.rainews.it/dl/rainews/RSS/politics.xml",

    # Spanien
    "El País Política": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/politica/portada",
    "El Mundo Política": "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml", # Spanien-Fokus, enthält Politik
    "ABC España Política": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml", # Spanien-Fokus, enthält Politik

    # Niederlande
    "NOS Nieuws Politiek": "http://feeds.nos.nl/nosnieuwspolitiek",
    "RTL Nieuws Politiek": "https://www.rtlnieuws.nl/nieuws/politiek/rss.xml",

    # Skandinavien
    "DR Nyheder Politik": "https://www.dr.dk/nyheder/service/feeds/politik", # Dänemark
    "SVT Nyheter": "https://www.svt.se/nyheter/rss.xml", # Schweden, allgemein
    "NRK Nyheter": "https://www.nrk.no/toppsaker.rss", # Norwegen, allgemein

    # Russland
    # Hinweis: Die Verfügbarkeit und der Inhalt dieser Quellen können starken staatlichen Einflüssen unterliegen.
    "RT International": "https://www.rt.com/rss/",
    # "RT Deutsch": "https://de.rt.com/feeds/news/", # Oft eingeschränkt erreichbar
    "Sputnik News": "https://sputniknews.com/export/rss2/archive/index.xml",
    # "Sputnik Deutschland": "https://sputnikglobe.com/europe/feed/", # Oft eingeschränkt erreichbar
    "TASS Russian News": "https://tass.com/rss/v2.xml",
    "RIA Novosti": "https://ria.ru/export/rss2/archive/index.xml", # Russischsprachig
    "Interfax": "https://interfax.com/newsfeed.aspx?type=news",
    "Moscow Times": "https://www.themoscowtimes.com/rss/news",
    "Russia Today Politik": "https://www.rt.com/rss/politics/",

    # China
    # Hinweis: Die Verfügbarkeit und der Inhalt dieser Quellen können starken staatlichen Einflüssen unterliegen.
    "Xinhua News World": "http://www.xinhuanet.com/english/rss/worldrss.xml",
    "China Daily World": "http://www.chinadaily.com.cn/rss/world_rss.xml",
    "Global Times": "http://www.globaltimes.cn/rss/outbrain.xml",
    "People's Daily Politics": "http://en.people.cn/rss/politics.xml",
    "CGTN Politics": "https://www.cgtn.com/subscribe/rss/section/politics.xml",
    "China.org.cn Politics": "http://www.china.org.cn/RSS/politics.xml",
    "South China Morning Post Politics": "https://www.scmp.com/rss/4/feed", # Hongkong-basiert, kritischer

    # Ukraine
    "Ukrinform": "https://www.ukrinform.net/rss/block-lastnews",
    "Kyiv Independent": "https://kyivindependent.com/feed/",
    "Ukrainska Pravda": "https://www.pravda.com.ua/rss/", # Ukrainisch/Russisch, oft mit engl. Zusammenfassungen
    "Interfax Ukraine": "https://en.interfax.com.ua/news/rss.xml",
    "Ukraine Crisis Media Center": "http://uacrisis.org/en/feed",
    "Atlantic Council Ukraine Alert": "https://www.atlanticcouncil.org/blogs/ukrainealert/feed/",
    "Radio Free Europe Ukraine Service": "https://www.rferl.org/api/zq-qevemgmqv", # RFE/RL

    # Osteuropa Allgemein
    "Euronews": "https://www.euronews.com/rss?format=mrss", # Multilingual
    "Balkan Insight": "https://balkaninsight.com/feed/",
    "Prague Daily Monitor": "http://praguemonitor.com/feed", # Tschechien

    # Weitere Internationale Quellen / Asien-Pazifik
    "BBC Asia": "http://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "Al Jazeera English": "https://www.aljazeera.com/xml/rss/all.xml", # Global, mit starkem Fokus auf den Globalen Süden
    "Reuters World": "http://feeds.reuters.com/Reuters/worldNews", # Ergänzung zu Reuters Politics
    "Associated Press World": "https://feeds.apnews.com/rss/apf-worldnews", # Ergänzung zu AP Politics
    "Nikkei Asia": "https://asia.nikkei.com/rss/feed/nar", # Japan/Asien Fokus
    "The Diplomat": "https://thediplomat.com/feed/", # Asien-Pazifik Politik
    "Japan Times": "https://www.japantimes.co.jp/feed/topstories/",
    "The Hindu (National)": "https://www.thehindu.com/news/national/feeder/default.rss", # Indien
    "Times of India (World)": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms", # Indien, Weltnachrichten
    "The Australian (Politics)": "https://www.theaustralian.com.au/nation/politics/rss", # Ggf. hinter Paywall
    "Sydney Morning Herald (World)": "https://www.smh.com.au/world/rss.xml", # Australien

    # Mittlerer Osten
    "Haaretz": "https://www.haaretz.com/cmlink/1.628752", # Israel
    "Times of Israel": "https://www.timesofisrael.com/feed/", # Israel
    "Arab News": "https://www.arabnews.com/rss.xml", # Saudi-Arabien
    "The National UAE": "https://www.thenationalnews.com/arc/outboundfeeds/rss/?outputType=xml§ion=/&subsection=/world", # VAE

    # Afrika
    "BBC Africa": "http://feeds.bbci.co.uk/news/world/africa/rss.xml",
    "Mail & Guardian": "https://mg.co.za/feed/", # Südafrika
    "News24 Politics": "https://feeds.news24.com/articles/news24/politics/rss", # Südafrika
    "Daily Maverick": "https://www.dailymaverick.co.za/dmrss/", # Südafrika, allgemein mit Politikanteil

    # Lateinamerika
    "BBC Mundo": "https://www.bbc.com/mundo/temas/america_latina/index.xml", # Spanisch
    "El Universal (México)": "https://www.eluniversal.com.mx/rss.xml",
    "Folha de S.Paulo (Poder)": "https://feeds.folha.uol.com.br/poder/rss091.xml", # Brasilien, Politik
    "La Nación (Argentina - Política)": "https://www.lanacion.com.ar/politica/rss",
    "Reuters LatAm": "http://feeds.reuters.com/reuters/latinAmericaNews", # Englisch

    # Kanada
    "CBC Politics": "https://www.cbc.ca/cmlink/rss-politics",
    "Globe and Mail Politics": "https://www.theglobeandmail.com/politics/?service=rss",
    "CTV News Politics": "https://www.ctvnews.ca/rss/politics",
    "National Post": "https://nationalpost.com/category/news/politics/feed",

    # Internationale Organisationen
    "United Nations News": "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
    "European Council Newsroom": "https://www.consilium.europa.eu/en/press/press-releases/rss/",
    "NATO News": "https://www.nato.int/rss/press-releases.xml",
    "World Bank News": "https://www.worldbank.org/en/news/all.rss",
    "WHO News": "https://www.who.int/rss-feeds/news-english.xml", # Weltgesundheitsorganisation
    "WTO News": "https://www.wto.org/library/rss/news_e.xml", # Welthandelsorganisation
    "IMF News": "https://www.imf.org/external/rss/whatsnew.xml", # Internationaler Währungsfonds

    # Spezialisierte Politik-Portale & Think Tanks (International)
    "Foreign Affairs": "https://www.foreignaffairs.com/rss.xml",
    "Foreign Policy": "https://foreignpolicy.com/feed/",
    "Council on Foreign Relations (CFR)": "https://www.cfr.org/rss-feeds", # Bietet diverse Feeds an
    "Brookings Institution": "https://www.brookings.edu/feed/",
    "Carnegie Endowment for International Peace": "https://carnegieendowment.org/rss/full.xml",
    "Atlantic Council": "https://www.atlanticcouncil.org/feed/",
    "Chatham House": "https://www.chathamhouse.org/rss/news", # UK-basiert, internationaler Fokus
    "International Crisis Group": "https://www.crisisgroup.org/rss",

    # Google & Bing News (Politik) - als generische internationale Ergänzung
    "Google News International Politics": "https://news.google.com/rss/search?q=international+politics&hl=en&gl=US&ceid=US:en", # Englisch, global
    "Google News Politics (DE)": "https://news.google.com/rss/search?q=Politik&hl=de&gl=DE&ceid=DE:de",
    "Google News Politics (FR)": "https://news.google.com/rss/search?q=Politique&hl=fr&gl=FR&ceid=FR:fr",
    # "Bing News Politics": "https://www.bing.com/news/search?q=Politics&format=rss", # Bing RSS kann unzuverlässig sein

    # Darknet Quellen (TOR-Netzwerk erforderlich für das Abrufen der Feeds)
    # WICHTIGER HINWEIS:
    # 1. Technische Anpassung: Das Python-Skript (news.py), das diese Konfiguration verwendet,
    #    muss so modifiziert werden, dass es HTTP/HTTPS-Anfragen über das Tor-Netzwerk leiten kann
    #    (z.B. mittels Libraries wie 'requests' mit SOCKS-Proxy-Unterstützung via Tor).
    #    Dies ist eine über die reine Konfigurationsanpassung hinausgehende Code-Änderung.
    # 2. Stabilität und Verfügbarkeit: .onion Adressen sind oft nicht dauerhaft erreichbar
    #    und können sich ändern oder verschwinden.
    # 3. Inhaltliche Risiken: Inhalte aus dem Darknet können unzuverlässig, extremistisch, illegal
    #    oder anderweitig problematisch sein. Eine sorgfältige Prüfung und Filterung ist unerlässlich.
    # 4. Legalität: Das Zugreifen auf bestimmte Inhalte im Darknet kann rechtliche Konsequenzen haben.
    #    Stellen Sie sicher, dass Sie die Gesetze Ihrer Region einhalten.
    #
    # Die folgenden Einträge sind PLATZHALTER und müssen durch tatsächliche, funktionierende
    # und für Sie relevante .onion RSS-Feed URLs ersetzt werden, die Sie selbst recherchieren müssen.
    #
    # "Beispiel Darknet News DE (Platzhalter)": "http://beispielabcde12345.onion/rss-de.xml",
    # "Example Darknet News EN (Placeholder)": "http://examplexyz7890.onion/rss-en.xml",
    # "ProPublica (via Tor Mirror - falls RSS existiert)": "http://p53lf57qovyuvwsc6xnrppyply3vtqm7l6pcobkmyqsiofyeznfu5uqd.onion/rss" # Beispiel eines bekannten Dienstes mit .onion-Adresse; RSS-Feed-Existenz dort müsste geprüft werden.
}

# Politik-relevante Keywords für Filterung (bereits sehr international, erweitert)
IT_KEYWORDS_PREFILTER = [
    'politik', 'politics', 'government', 'regierung', 'bundestag', 'parliament',
    'election', 'wahl', 'vote', 'abstimmung', 'minister', 'chancellor', 'kanzler',
    'president', 'präsident', 'congress', 'senate', 'house', 'legislation',
    'gesetzentwurf', 'law', 'gesetz', 'policy', 'partei', 'party', 'coalition',
    'koalition', 'opposition', 'democracy', 'demokratie', 'republican', 'democrat',
    'conservative', 'liberal', 'social democrat', 'grüne', 'green party',
    'campaign', 'wahlkampf', 'candidate', 'kandidat', 'voter', 'wähler',
    'referendum', 'volksabstimmung', 'constitution', 'verfassung', 'supreme court',
    'bundesverfassungsgericht', 'diplomat', 'foreign policy', 'außenpolitik', 'international relations',
    'geopolitics', 'geopolitik', 'global affairs', 'world politics', 'international security',
    'trade war', 'handelskrieg', 'sanctions', 'sanktionen', 'treaty', 'vertrag',
    'nato', 'eu', 'european union', 'europäische union', 'un', 'united nations', 'vereinte nationen',
    'brexit', 'migration', 'immigration', 'einwanderung', 'refugee', 'flüchtling', 'asylum', 'asyl',
    'climate policy', 'klimapolitik', 'climate change', 'klimawandel', 'global warming',
    'tax reform', 'steuerreform', 'healthcare reform', 'gesundheitsreform',
    'infrastructure', 'infrastruktur', 'budget', 'haushalt', 'public finance',
    'debt ceiling', 'schuldenobergrenze', 'economic policy', 'wirtschaftspolitik', 'global economy',
    'cybersecurity', 'disinformation', 'propaganda', 'human rights', 'menschenrechte',
    'conflict', 'konflikt', 'war', 'krieg', 'peace', 'frieden', 'diplomacy', 'diplomatie',
    'terrorism', 'counter-terrorism', 'extremism', 'radicalization',
    'ukraine', 'russia', 'china', 'taiwan', 'iran', 'north korea', 'middle east', 'naher osten',
    'putin', 'xi jinping', 'zelensky', 'biden', 'scholz', 'macron', # Beispielhafte aktuelle Führungspersonen
    'kremlin', 'beijing', 'kyiv', 'kiev', 'moscow', 'tehran', 'pyongyang', 'washington', 'brussels', 'berlin',
    'crimea', 'donbas', 'donetsk', 'luhansk', 'annexation', 'territorial integrity', 'sovereignty', 'ceasefire',
    'war crimes', 'international law', 'völkerrecht', 'nuclear weapons', 'atomwaffen', 'non-proliferation',
    'deterrence', 'abschreckung', 'containment', 'eindämmung', 'cold war', 'kalter krieg',
    'sphere of influence', 'einflusssphäre', 'intelligence services', 'nachrichtendienste', 'espionage',
    # Keywords, die im Kontext von Darknet-Diskussionen relevant sein könnten (mit Vorsicht verwenden):
    'opsec', 'privacy', 'anonymity', 'surveillance', 'censorship', 'dark web', 'tor network',
    'hacktivism', 'information warfare', 'underground economy', 'freedom of information'
]

# Übersetzungswörterbuch für wichtige politische Begriffe (bereits sehr international, erweitert)
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
    'authoritarianism': 'Autoritarismus',
    'autocracy': 'Autokratie',
    'totalitarianism': 'Totalitarismus',
    'republican': 'Republikaner',
    'democrat': 'Demokrat',
    'conservative': 'Konservativ',
    'liberal': 'Liberal',
    'socialist': 'Sozialistisch',
    'communist': 'Kommunistisch',
    'nationalist': 'Nationalistisch',
    'populist': 'Populistisch',
    'far-right': 'Rechtsextrem',
    'far-left': 'Linksextrem',
    'campaign': 'Wahlkampf',
    'candidate': 'Kandidat',
    'voter': 'Wähler',
    'polling': 'Meinungsumfrage',
    'referendum': 'Referendum/Volksabstimmung',
    'constitution': 'Verfassung',
    'supreme court': 'Oberster Gerichtshof',
    'judicial system': 'Justizsystem',
    'foreign policy': 'Außenpolitik',
    'international relations': 'Internationale Beziehungen',
    'domestic policy': 'Innenpolitik',
    'geopolitics': 'Geopolitik',
    'sovereignty': 'Souveränität',
    'territorial integrity': 'Territoriale Integrität',
    'trade war': 'Handelskrieg',
    'sanctions': 'Sanktionen',
    'embargo': 'Embargo',
    'treaty': 'Vertrag',
    'alliance': 'Bündnis',
    'summit': 'Gipfeltreffen',
    'negotiation': 'Verhandlung',
    'diplomacy': 'Diplomatie',
    'ambassador': 'Botschafter',
    'consulate': 'Konsulat',
    'embassy': 'Botschaft',
    'immigration': 'Einwanderung',
    'emigration': 'Auswanderung',
    'border control': 'Grenzkontrolle',
    'refugee': 'Flüchtling',
    'asylum seeker': 'Asylsuchender',
    'humanitarian aid': 'Humanitäre Hilfe',
    'climate policy': 'Klimapolitik',
    'environmental policy': 'Umweltpolitik',
    'sustainable development': 'Nachhaltige Entwicklung',
    'energy policy': 'Energiepolitik',
    'tax reform': 'Steuerreform',
    'fiscal policy': 'Fiskalpolitik',
    'monetary policy': 'Geldpolitik',
    'central bank': 'Zentralbank',
    'healthcare reform': 'Gesundheitsreform',
    'public health': 'Öffentliche Gesundheit',
    'education policy': 'Bildungspolitik',
    'social welfare': 'Sozialhilfe',
    'social security': 'Sozialversicherung',
    'infrastructure': 'Infrastruktur',
    'budget': 'Haushalt',
    'national debt': 'Staatsverschuldung',
    'austerity': 'Sparpolitik',
    'economic policy': 'Wirtschaftspolitik',
    'globalization': 'Globalisierung',
    'protectionism': 'Protektionismus',
    'free trade': 'Freihandel',
    'cybersecurity policy': 'Cybersicherheitspolitik',
    'data privacy': 'Datenschutz',
    'surveillance': 'Überwachung',
    'censorship': 'Zensur',
    'disinformation campaign': 'Desinformationskampagne',
    'propaganda': 'Propaganda',
    'fake news': 'Falschnachrichten',
    'human rights violation': 'Menschenrechtsverletzung',
    'civil liberties': 'Bürgerrechte',
    'freedom of speech': 'Redefreiheit',
    'freedom of the press': 'Pressefreiheit',
    'activism': 'Aktivismus',
    'civil disobedience': 'Ziviler Ungehorsam',
    'armed conflict': 'Bewaffneter Konflikt',
    'civil war': 'Bürgerkrieg',
    'insurgency': 'Aufstand',
    'counter-insurgency': 'Aufstandsbekämpfung',
    'peacekeeping': 'Friedenssicherung',
    'peace agreement': 'Friedensabkommen',
    'ceasefire': 'Waffenstillstand',
    'terrorism': 'Terrorismus',
    'counter-terrorism': 'Terrorismusbekämpfung',
    'radicalization': 'Radikalisierung',
    'extremism': 'Extremismus',
    'intelligence agency': 'Nachrichtendienst',
    'espionage': 'Spionage',
    'coup d\'état': 'Staatsstreich',
    'political unrest': 'Politische Unruhen',
    'protest': 'Protest',
    'demonstration': 'Demonstration',
    'riot': 'Ausschreitung',
    'revolution': 'Revolution',
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
    'us-china relations': 'USA-China Beziehungen',
    'ukrainian government': 'Ukrainische Regierung',
    'donetsk': 'Donezk',
    'luhansk': 'Luhansk',
    'crimea': 'Krim',
    'annexation': 'Annexion',
    'minsk agreements': 'Minsker Abkommen',
    'donbas': 'Donbass',
    'international criminal court (icc)': 'Internationaler Strafgerichtshof (IStGH)',
    'international court of justice (icj)': 'Internationaler Gerichtshof (IGH)',
    'united nations security council (unsc)': 'UN-Sicherheitsrat',
    'united nations general assembly (unga)': 'UN-Generalversammlung',
    'european parliament': 'Europäisches Parlament',
    'european commission': 'Europäische Kommission',
    'european council': 'Europäischer Rat',
    # Begriffe, die im Kontext des Darknets relevant sein könnten:
    'darknet politics': 'Darknet-Politik',
    'online activism': 'Online-Aktivismus',
    'information control': 'Informationskontrolle',
    'digital resistance': 'Digitaler Widerstand',
    'whistleblowing': 'Whistleblowing',
    'encrypted communication': 'Verschlüsselte Kommunikation'
}