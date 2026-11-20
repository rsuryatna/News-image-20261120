// News poster data — Friday 20 November 2026 (v2).
// The DATA literal below is strict JSON (double quotes, no trailing commas,
// no comments inside it) so build_poster.py can parse it directly.

export interface FeaturedStory {
  id: number;
  place: string;
  topic: string;
  stamp: string;
  headline: string;
  body: string;
  source: string;
  region: string;
  lat: number;
  lon: number;
  art: string;
}

export interface Brief {
  id: number;
  place: string;
  text: string;
  source: string;
  region: string;
}

export interface StatItem {
  value: string;
  label: string;
}

export interface RegionCount {
  name: string;
  count: number;
}

export interface PosterData {
  eyebrow: string;
  masthead: string;
  subhead: string;
  stats: StatItem[];
  regions: RegionCount[];
  featured: FeaturedStory[];
  briefs: Brief[];
  dateCheckTitle: string;
  dateCheck: string[];
  notYet: string;
  footerDisclaimer: string;
  footerSources: string;
  mapNote: string;
}

export const DATA: PosterData = {
  "eyebrow": "FRIDAY · 20 NOVEMBER 2026 · 36 STORIES",
  "masthead": "THE WORLD TODAY",
  "subhead": "One day of world news — every story happened, or was first reported, on Friday 20 November 2026.",
  "stats": [
    { "value": "300,000+", "label": "evacuated ahead of Cyclone Akvan" },
    { "value": "~30", "label": "ballistic missiles fired at Kyiv" },
    { "value": "−7%", "label": "Asia shares' worst week since 2020" },
    { "value": "2.3%", "label": "Japan Oct headline CPI" },
    { "value": "118", "label": "Phillips' historic century vs India" },
    { "value": "$97.17", "label": "Anthropic first close, +17%" }
  ],
  "regions": [
    { "name": "EUROPE", "count": 8 },
    { "name": "AMERICAS", "count": 6 },
    { "name": "ASIA-PACIFIC", "count": 10 },
    { "name": "MIDEAST", "count": 3 },
    { "name": "AFRICA", "count": 3 },
    { "name": "OCEANIA", "count": 5 },
    { "name": "WORLD / SPACE", "count": 1 }
  ],
  "featured": [
    {
      "id": 1,
      "place": "GOPALPUR, INDIA",
      "topic": "CYCLONE",
      "stamp": "02:30 UTC",
      "headline": "Cyclone Akvan makes landfall in eastern India",
      "body": "Severe storm crosses near Gopalpur; 300,000+ evacuated, 423 rescue teams deployed, winds 70–80 kmph gusting to 90. Schools shut.",
      "source": "IMD, Reuters",
      "region": "ASIA-PACIFIC",
      "lat": 19.3,
      "lon": 84.9,
      "art": "cyclone"
    },
    {
      "id": 2,
      "place": "KYIV, UKRAINE",
      "topic": "WAR",
      "stamp": "01:25 UTC",
      "headline": "Russia fires wave of ~30 ballistic missiles at Kyiv",
      "body": "Seven overnight waves hit energy and transport sites; 3 killed; 3 Dnipro bridges damaged; power cuts hit parts of the capital.",
      "source": "Kyiv Independent, Reuters",
      "region": "EUROPE",
      "lat": 50.4,
      "lon": 30.5,
      "art": "missiles"
    },
    {
      "id": 3,
      "place": "ANTALYA, TÜRKIYE",
      "topic": "CLIMATE",
      "stamp": "12:00 UTC*",
      "headline": "COP31 reaches its final day deadlocked",
      "body": "Closing draft omits fossil-fuel phase-out while $120bn adaptation finance stays unresolved; hosts push “35 by 35” clean-power goal.",
      "source": "UN News, Reuters",
      "region": "MIDEAST",
      "lat": 36.9,
      "lon": 30.7,
      "art": "climate"
    },
    {
      "id": 4,
      "place": "SEOUL / TOKYO",
      "topic": "MARKETS",
      "stamp": "TOKYO CLOSE · 06:00 UTC",
      "headline": "AI sell-off sinks Asia to worst week since 2020",
      "body": "Nikkei −4.9%, KOSPI −5.4%, Taiex −6.8%, Hang Seng −2%. Figures are intraday lows, not closes.",
      "source": "Reuters",
      "region": "ASIA-PACIFIC",
      "lat": 37.6,
      "lon": 127.0,
      "art": "candles"
    },
    {
      "id": 5,
      "place": "MERCURY",
      "topic": "SPACE",
      "stamp": "09:00 UTC*",
      "headline": "BepiColombo reaches Mercury after 8 years",
      "body": "ESA/JAXA probe ends 8-year trip; orbit insertion set for Saturday.",
      "source": "ESA, BBC",
      "region": "WORLD / SPACE",
      "lat": 49.9,
      "lon": 8.7,
      "art": "mercury"
    },
    {
      "id": 6,
      "place": "BRUSSELS",
      "topic": "EUROPE",
      "stamp": "11:00 UTC*",
      "headline": "Burnham holds first EU–UK reset summit",
      "body": "Costa & von der Leyen host UK PM; agri-food & carbon-market links eyed.",
      "source": "EU Council",
      "region": "EUROPE",
      "lat": 50.8,
      "lon": 4.4,
      "art": "flags"
    },
    {
      "id": 7,
      "place": "TOKYO",
      "topic": "ECONOMY",
      "stamp": "00:30 UTC*",
      "headline": "Japan inflation hits 2.3%; BoJ hike eyed",
      "body": "October headline CPI rises from 2.1%; core inflation was 2.2% as energy subsidies were cut.",
      "source": "Reuters",
      "region": "ASIA-PACIFIC",
      "lat": 35.7,
      "lon": 139.7,
      "art": "bars"
    },
    {
      "id": 8,
      "place": "BEIJING",
      "topic": "RATES",
      "stamp": "01:15 UTC",
      "headline": "China holds lending rates for 18th month",
      "body": "1-year LPR stays at 3.0%, 5-year at 3.5% as expected.",
      "source": "PBOC, Reuters",
      "region": "ASIA-PACIFIC",
      "lat": 39.9,
      "lon": 116.4,
      "art": "bank"
    },
    {
      "id": 9,
      "place": "WELLINGTON",
      "topic": "CRICKET",
      "stamp": "02:00 UTC*",
      "headline": "Phillips makes history with 118 vs India",
      "body": "First NZ batter with centuries in all 3 formats vs India in a year.",
      "source": "ICC, AP",
      "region": "OCEANIA",
      "lat": -41.3,
      "lon": 174.8,
      "art": "cricket"
    },
    {
      "id": 10,
      "place": "SAN SALVADOR",
      "topic": "POLITICS",
      "stamp": "15:00 UTC*",
      "headline": "Bukele registers for third-term bid",
      "body": "Files with electoral tribunal for Feb 2027 vote; rights groups object.",
      "source": "AP",
      "region": "AMERICAS",
      "lat": 13.7,
      "lon": -89.2,
      "art": "ballot"
    },
    {
      "id": 11,
      "place": "YENNE COAST",
      "topic": "MIGRATION",
      "stamp": "10:00 UTC*",
      "headline": "Migrant boat capsizes off Yenne; 4 dead",
      "body": "Dozens missing from ~50–100 aboard as Canary arrivals surge.",
      "source": "Al Jazeera",
      "region": "AFRICA",
      "lat": 14.7,
      "lon": -17.4,
      "art": "boat"
    },
    {
      "id": 12,
      "place": "ROME",
      "topic": "LABOUR",
      "stamp": "09:00 UTC*",
      "headline": "Italy's CGIL holds 24-hr general strike",
      "body": "Unions rally across ~100 squares against 2027 budget; transit hit.",
      "source": "CGIL, AFP",
      "region": "EUROPE",
      "lat": 41.9,
      "lon": 12.5,
      "art": "strike"
    },
    {
      "id": 13,
      "place": "BARCELONA",
      "topic": "HEALTH",
      "stamp": "09:00 UTC*",
      "headline": "Pancreatic cancer pill shrinks tumours 60.7%",
      "body": "Daraxonrasib + chemo beats chemo alone (23–42%) in early trial.",
      "source": "Reuters",
      "region": "EUROPE",
      "lat": 41.4,
      "lon": 2.2,
      "art": "pill"
    }
  ],
  "briefs": [
    { "id": 14, "place": "BRAZIL", "text": "Lula meets chief Raoni as Indigenous land is recognised", "source": "Al Jazeera", "region": "AMERICAS" },
    { "id": 15, "place": "SEOUL", "text": "Ruling party moves to impeach Chief Justice Cho Hee-dae", "source": "SBS", "region": "ASIA-PACIFIC" },
    { "id": 16, "place": "BOUGAINVILLE", "text": "Rio Tinto pledges $370m for Panguna mine legacy", "source": "Reuters", "region": "ASIA-PACIFIC" },
    { "id": 17, "place": "CANBERRA", "text": "CBO warns AUKUS sub sales could shrink US fleet", "source": "Reuters", "region": "OCEANIA" },
    { "id": 18, "place": "FLORIDA", "text": "St. Johns River hits record 18.3 ft; four counties shut schools", "source": "AP", "region": "AMERICAS" },
    { "id": 19, "place": "WELLINGTON", "text": "Henry Nicholls scores 175* in 216-run stand with Phillips", "source": "ICC", "region": "OCEANIA" },
    { "id": 20, "place": "TONGA", "text": "Pacific kingdom declares emergency as El Niño drought bites", "source": "RNZ", "region": "OCEANIA" },
    { "id": 21, "place": "WASHINGTON", "text": "Pentagon puts US war cost against Iran at $4.8bn", "source": "Reuters", "region": "AMERICAS" },
    { "id": 22, "place": "LONDON", "text": "UK & Norway fund £100m+ for two Ukrainian naval vessels", "source": "BBC", "region": "EUROPE" },
    { "id": 23, "place": "COPENHAGEN", "text": "Denmark's parliament approves Greenland defence bill", "source": "AFP", "region": "EUROPE" },
    { "id": 24, "place": "JAKARTA", "text": "Indonesia's parliament passes asset-forfeiture bill", "source": "Reuters", "region": "ASIA-PACIFIC" },
    { "id": 25, "place": "DOROGOBUZH, RUSSIA", "text": "[CLAIM] Drones hit chemical plant in Smolensk region; blast and fire reported", "source": "ASTRA", "region": "EUROPE" },
    { "id": 26, "place": "SENEGAL", "text": "President Faye enacts supplementary budget by decree", "source": "AFP", "region": "AFRICA" },
    { "id": 27, "place": "HORMUZ", "text": "Four attacks on vessels in 96 hours, maritime centre says", "source": "UKMTO", "region": "MIDEAST" },
    { "id": 28, "place": "NEW DELHI", "text": "Pakistan minister to lead delegation to SCO dialogue", "source": "The Hindu", "region": "ASIA-PACIFIC" },
    { "id": 29, "place": "QATAR", "text": "U17 World Cup: Australia stun Argentina 2-0", "source": "FIFA", "region": "MIDEAST" },
    { "id": 30, "place": "SOUTH AFRICA", "text": "Hamza spins Proteas to Test win; Bavuma sets record", "source": "ICC", "region": "AFRICA" },
    { "id": 31, "place": "TAIWAN", "text": "Short-sell curbs take effect; two Russian bombers tracked", "source": "Reuters", "region": "ASIA-PACIFIC" },
    { "id": 32, "place": "TURIN", "text": "Alcaraz–Cobolli & Medvedev–Tiafoe close ATP Finals groups", "source": "ATP", "region": "EUROPE" },
    { "id": 33, "place": "LOS ANGELES", "text": "GTA VI's first full day on sale; Metacritic 99", "source": "Sensor Tower", "region": "AMERICAS" },
    { "id": 34, "place": "NEW YORK", "text": "Anthropic ends first day up 17%, closing at $97.17", "source": "Reuters", "region": "AMERICAS" },
    { "id": 35, "place": "COX'S BAZAR", "text": "Rohingya camps weep and pray after ICJ ruling", "source": "Reuters", "region": "ASIA-PACIFIC" },
    { "id": 36, "place": "AUSTRALIA", "text": "Xi meets Albanese a day after APEC summit", "source": "AP", "region": "OCEANIA" }
  ],
  "dateCheckTitle": "DATE CHECK — First reported Thu 19 Nov, so NOT shown as Friday's news:",
  "dateCheck": [
    "Trump–Xi–Putin Shenzhen summit itself",
    "Anthropic's $83 IPO pricing & Nasdaq debut",
    "ICJ Myanmar Rohingya genocide verdict",
    "GTA VI midnight launch",
    "$190.4m Van Gogh sale (Wed 18 Nov evening)",
    "EU €45bn loan for Ukraine (18 Nov)",
    "US–Venezuela military deal",
    "Houthi strike on Riyadh PIF tower",
    "Kerch / Crimea Bridge strike (17 Nov)",
    "Senate 48–51 Iran war-powers vote",
    "Haiti army raid in Martissant (34 killed)"
  ],
  "notYet": "NOT YET — Sat 21 Nov: COP31 closing plenary · Las Vegas GP qualifying",
  "footerDisclaimer": "Every story here happened, or was first reported, on Friday 20 November 2026 in at least one time zone. Claims are attributed, not stated as fact.",
  "footerSources": "Sources: Reuters, AP, AFP, BBC, IMD, UN News, Al Jazeera, ICC, EU Council, PBOC. Original vector drawings.",
  "mapNote": "5 · Mercury — pin at ESOC, Darmstadt"
};
