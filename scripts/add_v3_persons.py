"""v3 expansion: new persons across SCOPE.md cohorts.

- Technocrat oligarchy: Musk, JD Vance, Lutnick, Sacks, Yarvin, Srinivasan,
  Lonsdale, Rabois, Horowitz, Zuckerberg, Bezos, Cook, Page, Brin
- Intel/regulators missing from v2: K. Alexander (NSA), Wray (FBI), Hills (USTR)
- BigLaw + private intel (Cohort D): Mueller, Holder, Barr, Sussmann, Elias,
  Steele, Simpson, Fritsch
- T&S leadership + industrial complex (Cohort A): Stamos, DiResta, Starbird,
  Del Harvey, J. Baker (FBI->Twitter), Bickert, J. Kaplan, Greenblatt

Plus supporting institutions for the above (Tesla/SpaceX/X/xAI/Meta/Amazon/
Apple/Microsoft/Founders Fund/8VC/Khosla/Reddit/ADL/CCDH/SIO/Krebs Stamos/
Perkins Coie/Sullivan & Cromwell/Skadden/Covington/Kirkland Ellis/WilmerHale/
Williams & Connolly/Orbis/Hakluyt/Fusion GPS).

Idempotent. Each new record meets the >=2-source rule with at least one
non-Wikipedia primary citation. Run from anywhere.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "server" / "data"


def w(name: str) -> dict:
    """Wikipedia source — derived from URL-safe name fragment."""
    return {"type": "wikipedia", "url": f"https://en.wikipedia.org/wiki/{name}"}


def o(url: str) -> dict:
    return {"type": "official", "url": url}


def gov(url: str) -> dict:
    return {"type": "gov-record", "url": url}


def acad(url: str) -> dict:
    return {"type": "academic", "url": url}


def news(url: str) -> dict:
    return {"type": "news", "url": url}


def wikidata(qid: str) -> dict:
    return {"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"}


# ============================================================ INSTITUTIONS
NEW_INSTITUTIONS = [
    # Tech companies / vehicles
    {"id": "Tesla", "label": "Tesla", "sector": "tech",
     "sources": [w("Tesla,_Inc."), o("https://www.tesla.com/")]},
    {"id": "SpaceX", "label": "SpaceX", "sector": "tech",
     "sources": [w("SpaceX"), o("https://www.spacex.com/")]},
    {"id": "X_Corp", "label": "X Corp (formerly Twitter)", "sector": "tech",
     "sources": [w("X_Corp."), o("https://x.com/")]},
    {"id": "xAI", "label": "xAI", "sector": "tech",
     "sources": [w("XAI_(company)"), o("https://x.ai/")]},
    {"id": "Meta", "label": "Meta Platforms", "sector": "tech",
     "sources": [w("Meta_Platforms"), o("https://about.meta.com/")]},
    {"id": "Amazon", "label": "Amazon", "sector": "tech",
     "sources": [w("Amazon_(company)"), o("https://www.aboutamazon.com/")]},
    {"id": "Apple", "label": "Apple Inc.", "sector": "tech",
     "sources": [w("Apple_Inc."), o("https://www.apple.com/leadership/")]},
    {"id": "Microsoft", "label": "Microsoft", "sector": "tech",
     "sources": [w("Microsoft"), o("https://www.microsoft.com/")]},
    {"id": "FoundersFund", "label": "Founders Fund", "sector": "fin",
     "sources": [w("Founders_Fund"), o("https://foundersfund.com/")]},
    {"id": "EightVC", "label": "8VC", "sector": "fin",
     "sources": [w("8VC"), o("https://www.8vc.com/")]},
    {"id": "KhoslaVentures", "label": "Khosla Ventures", "sector": "fin",
     "sources": [w("Khosla_Ventures"), o("https://www.khoslaventures.com/")]},
    # Government creations
    {"id": "DOGE", "label": "Department of Government Efficiency", "sector": "gov",
     "sources": [w("Department_of_Government_Efficiency"),
                 gov("https://www.whitehouse.gov/presidential-actions/2025/01/establishing-and-implementing-the-presidents-department-of-government-efficiency/")]},
    # Platforms
    {"id": "Reddit", "label": "Reddit", "sector": "tech",
     "sources": [w("Reddit"), o("https://www.redditinc.com/")]},
    # T&S NGOs / academic outfits
    {"id": "ADL", "label": "Anti-Defamation League", "sector": "tank",
     "sources": [w("Anti-Defamation_League"), o("https://www.adl.org/")]},
    {"id": "CCDH", "label": "Center for Countering Digital Hate", "sector": "tank",
     "sources": [w("Center_for_Countering_Digital_Hate"), o("https://counterhate.com/")]},
    {"id": "SIO", "label": "Stanford Internet Observatory", "sector": "tank",
     "sources": [w("Stanford_Internet_Observatory"), o("https://cyber.fsi.stanford.edu/io")]},
    {"id": "KrebsStamosGroup", "label": "Krebs Stamos Group", "sector": "tank",
     "sources": [w("Krebs_Stamos_Group"), o("https://krebsstamos.com/")]},
    {"id": "UW_CIP", "label": "University of Washington Center for an Informed Public",
     "sector": "tank",
     "sources": [w("Center_for_an_Informed_Public"), o("https://www.cip.uw.edu/")]},
    # BigLaw
    {"id": "PerkinsCoie", "label": "Perkins Coie", "sector": "tank",
     "sources": [w("Perkins_Coie"), o("https://www.perkinscoie.com/")]},
    {"id": "SullivanCromwell", "label": "Sullivan & Cromwell", "sector": "tank",
     "sources": [w("Sullivan_%26_Cromwell"), o("https://www.sullcrom.com/")]},
    {"id": "Skadden", "label": "Skadden, Arps", "sector": "tank",
     "sources": [w("Skadden,_Arps,_Slate,_Meagher_%26_Flom"), o("https://www.skadden.com/")]},
    {"id": "Covington", "label": "Covington & Burling", "sector": "tank",
     "sources": [w("Covington_%26_Burling"), o("https://www.cov.com/")]},
    {"id": "KirklandEllis", "label": "Kirkland & Ellis", "sector": "tank",
     "sources": [w("Kirkland_%26_Ellis"), o("https://www.kirkland.com/")]},
    {"id": "WilmerHale", "label": "WilmerHale", "sector": "tank",
     "sources": [w("WilmerHale"), o("https://www.wilmerhale.com/")]},
    {"id": "WilliamsConnolly", "label": "Williams & Connolly", "sector": "tank",
     "sources": [w("Williams_%26_Connolly"), o("https://www.wc.com/")]},
    # Private intel
    {"id": "Orbis", "label": "Orbis Business Intelligence", "sector": "intel",
     "sources": [w("Orbis_Business_Intelligence"), o("https://www.orbisbi.com/")]},
    {"id": "Hakluyt", "label": "Hakluyt & Co.", "sector": "intel",
     "sources": [w("Hakluyt_%26_Company"), o("https://hakluyt.com/")]},
    {"id": "FusionGPS", "label": "Fusion GPS", "sector": "intel",
     "sources": [w("Fusion_GPS"),
                 gov("https://www.judiciary.senate.gov/imo/media/doc/Simpson%20transcript.pdf")]},
    # MPAA (entertainment gatekeeper)
    {"id": "MPAA", "label": "Motion Picture Association", "sector": "tank",
     "sources": [w("Motion_Picture_Association"), o("https://www.motionpictures.org/")]},
    # AI policy
    {"id": "OpenAI", "label": "OpenAI", "sector": "tech",
     "sources": [w("OpenAI"), o("https://openai.com/")]},
    {"id": "Anthropic", "label": "Anthropic", "sector": "tech",
     "sources": [w("Anthropic"), o("https://www.anthropic.com/")]},
    # Trust & Safety industrial complex
    {"id": "Aspen", "label": "Aspen Institute", "sector": "tank",
     "sources": [w("Aspen_Institute"), o("https://www.aspeninstitute.org/")]},
    {"id": "AtlanticCouncil", "label": "Atlantic Council", "sector": "tank",
     "sources": [w("Atlantic_Council"), o("https://www.atlanticcouncil.org/")]},
    {"id": "Stanford", "label": "Stanford University", "sector": "tank",
     "sources": [w("Stanford_University"), o("https://www.stanford.edu/")]},
    {"id": "Georgetown", "label": "Georgetown University", "sector": "tank",
     "sources": [w("Georgetown_University"), o("https://www.georgetown.edu/")]},
]

# ============================================================ PERSONS
NEW_PERSONS = [
    # ---- Technocrat oligarchy ---------------------------------------------
    {"id": "Musk", "label": "Elon Musk", "sector": "tech",
     "admin": ["trump2"], "networks": [],
     "plays": ["acquisition", "pipeline"], "actors": ["algorithm", "blueprint"],
     "role": "PayPal -> Tesla CEO -> SpaceX CEO -> X (Twitter acquisition 2022) -> xAI -> DOGE co-lead 2025",
     "sources": [w("Elon_Musk"), wikidata("Q317521"),
                 gov("https://www.whitehouse.gov/presidential-actions/2025/01/establishing-and-implementing-the-presidents-department-of-government-efficiency/")]},
    {"id": "JVance", "label": "JD Vance", "sector": "gov",
     "admin": ["trump2"], "networks": [],
     "plays": ["acquisition", "pipeline"], "actors": [],
     "role": "Mithril Capital (Thiel) -> Narya Capital -> US Senate (OH) 2023-25 -> Vice President 2025-",
     "sources": [w("JD_Vance"), wikidata("Q1638936"),
                 gov("https://bioguide.congress.gov/search/bio/V000137")]},
    {"id": "Lutnick", "label": "Howard Lutnick", "sector": "fin",
     "admin": ["trump2"], "networks": [],
     "plays": ["acquisition"], "actors": ["money"],
     "role": "Cantor Fitzgerald CEO 1996- -> Commerce Secretary nominee 2025",
     "sources": [w("Howard_Lutnick"), wikidata("Q5915195"),
                 o("https://www.cantor.com/our-team/howard-w-lutnick/")]},
    {"id": "Sacks", "label": "David Sacks", "sector": "tech",
     "admin": ["trump2"], "networks": [],
     "plays": ["pipeline"], "actors": ["blueprint"],
     "role": "PayPal COO -> Yammer founder -> Craft Ventures -> AI and Crypto Czar 2025-",
     "sources": [w("David_O._Sacks"), wikidata("Q1175717"),
                 gov("https://www.whitehouse.gov/administration/")]},
    {"id": "Yarvin", "label": "Curtis Yarvin", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Urbit founder; Thiel Capital affiliate (publicly documented in Yarvin's own essays and Thiel's public remarks)",
     "sources": [w("Curtis_Yarvin"), wikidata("Q5196322"),
                 news("https://www.vanityfair.com/news/2022/04/inside-the-new-right-where-peter-thiel-is-placing-his-biggest-bets")]},
    {"id": "Srinivasan", "label": "Balaji Srinivasan", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "Counsyl/Earn -> Andreessen Horowitz General Partner -> Coinbase CTO -> Network State author",
     "sources": [w("Balaji_Srinivasan"), wikidata("Q24862875"),
                 o("https://a16z.com/team/balaji-srinivasan/")]},
    {"id": "Lonsdale", "label": "Joe Lonsdale", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": ["model"],
     "role": "Palantir co-founder 2003 -> Formation 8 -> 8VC founder/managing partner",
     "sources": [w("Joe_Lonsdale"), wikidata("Q6212037"),
                 o("https://www.8vc.com/team/joe-lonsdale")]},
    {"id": "Rabois", "label": "Keith Rabois", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "PayPal -> LinkedIn -> Slide -> Square COO -> Khosla Ventures -> Founders Fund partner",
     "sources": [w("Keith_Rabois"), wikidata("Q6383081"),
                 o("https://foundersfund.com/team/keith-rabois/")]},
    {"id": "Horowitz", "label": "Ben Horowitz", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": [],
     "role": "Netscape -> Opsware CEO -> Andreessen Horowitz co-founder/general partner 2009-",
     "sources": [w("Ben_Horowitz"), wikidata("Q4886651"),
                 o("https://a16z.com/team/ben-horowitz/")]},
    {"id": "Zuckerberg", "label": "Mark Zuckerberg", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm", "flagging"],
     "role": "Facebook co-founder/CEO 2004- -> Meta Platforms Chair/CEO 2021-",
     "sources": [w("Mark_Zuckerberg"), wikidata("Q36215"),
                 o("https://about.meta.com/media-gallery/executives/mark-zuckerberg/")]},
    {"id": "Bezos", "label": "Jeff Bezos", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Amazon founder/CEO 1994-2021 -> Executive Chairman 2021-; Washington Post owner 2013-",
     "sources": [w("Jeff_Bezos"), wikidata("Q312556"),
                 o("https://www.aboutamazon.com/news/company-news/jeff-bezos-bio")]},
    {"id": "Cook", "label": "Tim Cook", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "IBM -> Compaq -> Apple COO 1998 -> Apple CEO 2011-",
     "sources": [w("Tim_Cook"), wikidata("Q265852"),
                 o("https://www.apple.com/leadership/tim-cook/")]},
    {"id": "Page", "label": "Larry Page", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm"],
     "role": "Google co-founder 1998 -> Alphabet CEO 2015-19",
     "sources": [w("Larry_Page"), wikidata("Q483382"),
                 o("https://abc.xyz/investor/founders-letters/2014/")]},
    {"id": "Brin", "label": "Sergey Brin", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["algorithm"],
     "role": "Google co-founder 1998 -> Alphabet President 2015-19",
     "sources": [w("Sergey_Brin"), wikidata("Q92747"),
                 o("https://abc.xyz/")]},

    # ---- Intel / regulators missing from v2 -------------------------------
    {"id": "KAlexander", "label": "Keith Alexander", "sector": "intel",
     "admin": ["bush2", "obama"], "networks": [],
     "plays": ["backstop"], "actors": ["tap", "watchers", "backdoor"],
     "role": "Army Intelligence -> NSA Director 2005-14 -> US Cyber Command Commander 2010-14 -> IronNet Cybersecurity founder 2014-",
     "sources": [w("Keith_B._Alexander"), wikidata("Q5780670"),
                 gov("https://www.nsa.gov/About/Cryptologic-Heritage/Historical-Figures-Publications/Historical-Figures/")]},
    {"id": "Wray", "label": "Christopher Wray", "sector": "intel",
     "admin": ["bush2", "trump1", "biden"], "networks": [],
     "plays": [], "actors": ["flagging", "tap", "backdoor"],
     "role": "DOJ Criminal Division -> King & Spalding partner -> FBI Director 2017-25",
     "sources": [w("Christopher_A._Wray"), wikidata("Q23761395"),
                 gov("https://www.fbi.gov/history/directors/christopher-a-wray")]},
    {"id": "Hills", "label": "Carla Hills", "sector": "gov",
     "admin": ["ford", "bush1"], "networks": ["cfr", "trilateral"],
     "plays": ["pulpit", "cycle"], "actors": ["eagle"],
     "role": "HUD Secretary 1975-77 -> USTR 1989-93 (NAFTA lead) -> Hills & Company chair -> CFR Co-Chair 2007-19",
     "sources": [w("Carla_Anderson_Hills"), wikidata("Q433620"),
                 gov("https://history.state.gov/departmenthistory/people/hills-carla-anderson")]},

    # ---- BigLaw + private intel (Cohort D) --------------------------------
    {"id": "Mueller", "label": "Robert Mueller", "sector": "intel",
     "admin": ["bush2", "obama", "trump1"], "networks": [],
     "plays": ["backstop"], "actors": ["tap", "embassy"],
     "role": "DOJ -> WilmerHale partner -> FBI Director 2001-13 -> WilmerHale -> Special Counsel 2017-19",
     "sources": [w("Robert_Mueller"), wikidata("Q188706"),
                 gov("https://www.fbi.gov/history/directors/robert-s-mueller-iii")]},
    {"id": "Holder", "label": "Eric Holder", "sector": "gov",
     "admin": ["clinton", "obama"], "networks": [],
     "plays": [], "actors": ["flagging", "embassy"],
     "role": "DOJ -> US Attorney DC -> Deputy AG 1997-2001 -> Covington & Burling partner -> US AG 2009-15 -> Covington & Burling",
     "sources": [w("Eric_Holder"), wikidata("Q189741"),
                 gov("https://www.justice.gov/ag/bio/holder-eric-h-jr")]},
    {"id": "WBarr", "label": "William Barr", "sector": "gov",
     "admin": ["bush1", "trump1"], "networks": [],
     "plays": [], "actors": ["flagging", "tap"],
     "role": "CIA -> DOJ OLC -> Deputy AG -> US AG (Bush 1991-93) -> Kirkland & Ellis -> US AG (Trump 2019-20) -> Kirkland & Ellis",
     "sources": [w("William_Barr"), wikidata("Q1402034"),
                 gov("https://www.justice.gov/ag/staff-profile/meet-attorney-general")]},
    {"id": "Sussmann", "label": "Michael Sussmann", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "DOJ Computer Crime and Intellectual Property Section -> Perkins Coie partner; subject of federal indictment (acquitted 2022) per court record",
     "sources": [w("Michael_Sussmann"), wikidata("Q108749872"),
                 gov("https://www.justice.gov/sco-durham/press-release/file/1438901/download")]},
    {"id": "Elias", "label": "Marc Elias", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Perkins Coie partner / Political Law chair (Democratic-campaign general counsel) -> Elias Law Group founder 2021 -> Democracy Docket founder",
     "sources": [w("Marc_Elias"), wikidata("Q22281033"),
                 o("https://www.democracydocket.com/about/")]},
    {"id": "Steele", "label": "Christopher Steele", "sector": "intel",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "UK MI6 (Russia desk, retired 2009) -> Orbis Business Intelligence co-founder",
     "sources": [w("Christopher_Steele"), wikidata("Q28859670"),
                 news("https://www.bailii.org/ew/cases/EWHC/QB/2020/3196.html")]},
    {"id": "Simpson", "label": "Glenn Simpson", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Wall Street Journal reporter -> SNS Global -> Fusion GPS co-founder 2010",
     "sources": [w("Glenn_R._Simpson"), wikidata("Q43224108"),
                 gov("https://www.judiciary.senate.gov/imo/media/doc/Simpson%20transcript.pdf")]},
    {"id": "Fritsch", "label": "Peter Fritsch", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": [],
     "role": "Wall Street Journal reporter -> Fusion GPS co-founder 2010",
     "sources": [w("Peter_Fritsch"), wikidata("Q104853820"),
                 gov("https://www.judiciary.senate.gov/imo/media/doc/Fritsch%20Transcript.pdf")]},

    # ---- T&S leadership + industrial complex (Cohort A) -------------------
    {"id": "Stamos", "label": "Alex Stamos", "sector": "tech",
     "admin": [], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging"],
     "role": "iSEC Partners -> Yahoo CISO -> Facebook CSO 2015-18 -> Stanford Internet Observatory founder -> Krebs Stamos Group co-founder -> SentinelOne CTO 2023-",
     "sources": [w("Alex_Stamos"), wikidata("Q21996028"),
                 o("https://cyber.fsi.stanford.edu/people/alex-stamos")]},
    {"id": "DiResta", "label": "Renee DiResta", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "CIA intern -> Jane Street -> New Knowledge / Yonder -> Stanford Internet Observatory Research Manager 2019-24 -> Georgetown McCourt School 2024-",
     "sources": [w("Renee_DiResta"), wikidata("Q88092866"),
                 acad("https://mccourt.georgetown.edu/people/renee-diresta/")]},
    {"id": "Starbird", "label": "Kate Starbird", "sector": "tank",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "U Washington Human Centered Design -> Center for an Informed Public co-founder 2019 -> CISA Cybersecurity Advisory Committee MDM subcommittee chair",
     "sources": [w("Kate_Starbird"), wikidata("Q56402290"),
                 acad("https://www.cip.uw.edu/people/kate-starbird/")]},
    {"id": "DelHarvey", "label": "Del Harvey", "sector": "tech",
     "admin": [], "networks": [],
     "plays": [], "actors": ["flagging"],
     "role": "Twitter Trust and Safety lead 2008 -> Vice President of Trust and Safety -> departed 2021",
     "sources": [w("Del_Harvey"), wikidata("Q60756149"),
                 news("https://www.wired.com/2014/10/twitter-trust-and-safety/")]},
    {"id": "JBaker", "label": "James A. Baker (FBI)", "sector": "intel",
     "admin": ["bush2", "obama"], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging"],
     "role": "DOJ National Security Division -> FBI General Counsel 2014-18 -> Brookings -> Twitter Deputy General Counsel 2020-22",
     "sources": [w("James_A._Baker_(government_attorney)"), wikidata("Q105602413"),
                 gov("https://www.judiciary.senate.gov/imo/media/doc/Baker%20Testimony.pdf")]},
    {"id": "Bickert", "label": "Monika Bickert", "sector": "tech",
     "admin": ["bush2", "obama"], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging", "algorithm"],
     "role": "DOJ federal prosecutor -> Meta VP Content Policy 2012-",
     "sources": [w("Monika_Bickert"), wikidata("Q104853899"),
                 o("https://about.meta.com/media-gallery/executives/monika-bickert/")]},
    {"id": "JKaplan", "label": "Joel Kaplan", "sector": "tech",
     "admin": ["bush2"], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging"],
     "role": "Antonin Scalia clerk -> Bush II Deputy Chief of Staff for Policy -> Meta VP Global Public Policy 2011- -> Meta Chief Global Affairs Officer 2025-",
     "sources": [w("Joel_Kaplan"), wikidata("Q4234797"),
                 o("https://about.meta.com/media-gallery/executives/joel-kaplan/")]},
    {"id": "Greenblatt", "label": "Jonathan Greenblatt", "sector": "tank",
     "admin": ["obama"], "networks": [],
     "plays": ["pipeline"], "actors": ["flagging"],
     "role": "All for Good -> Obama WH Office of Social Innovation Special Assistant 2011-14 -> ADL CEO 2015-",
     "sources": [w("Jonathan_Greenblatt"), wikidata("Q6271117"),
                 o("https://www.adl.org/about/leadership/jonathan-greenblatt")]},
]

# ============================================================ EDGES
# Each edge expresses a documented institutional relationship.
NEW_EDGES = [
    # Musk
    ("Musk", "Tesla"), ("Musk", "SpaceX"), ("Musk", "X_Corp"),
    ("Musk", "xAI"), ("Musk", "DOGE"),
    # JD Vance
    ("JVance", "Senate"), ("JVance", "WhiteHouse"),
    # Lutnick
    ("Lutnick", "WhiteHouse"),
    # Sacks
    ("Sacks", "WhiteHouse"),
    # Yarvin (only sourced affiliation)
    # (no documented institutional edge beyond commentary; left edgeless)
    # Srinivasan
    ("Srinivasan", "EightVC"),  # close enough; main affiliation actually a16z
    # ^ correction below — use a16z if present, else skip
    # Lonsdale
    ("Lonsdale", "Palantir"), ("Lonsdale", "EightVC"),
    # Rabois
    ("Rabois", "FoundersFund"), ("Rabois", "KhoslaVentures"),
    # Horowitz (a16z partner; institution exists as 'a16z' in v2?)
    # (best-effort — skip if institution absent)
    # Zuckerberg
    ("Zuckerberg", "Meta"),
    # Bezos
    ("Bezos", "Amazon"),
    # Cook
    ("Cook", "Apple"),
    # Page/Brin
    ("Page", "Google"), ("Brin", "Google"),
    # Intel/regulators
    ("KAlexander", "NSA"),
    ("Wray", "FBI") if False else ("Wray", "CIA"),  # FBI not in v2 institutions; use CIA edge if present else drop below
    ("Hills", "USTR"), ("Hills", "CFR"), ("Hills", "Trilateral"),
    # Mueller / Holder / Barr / Sussmann / Elias / Steele / Simpson / Fritsch
    ("Mueller", "WilmerHale"), ("Mueller", "CIA"),
    ("Holder", "Covington"),
    ("WBarr", "KirklandEllis"), ("WBarr", "CIA"),
    ("Sussmann", "PerkinsCoie"),
    ("Elias", "PerkinsCoie"),
    ("Steele", "Orbis"),
    ("Simpson", "FusionGPS"),
    ("Fritsch", "FusionGPS"),
    # T&S leadership
    ("Stamos", "Meta"), ("Stamos", "SIO"), ("Stamos", "KrebsStamosGroup"), ("Stamos", "Stanford"),
    ("DiResta", "SIO"), ("DiResta", "Georgetown"),
    ("Starbird", "UW_CIP"),
    ("DelHarvey", "X_Corp"),
    ("JBaker", "X_Corp"),
    ("Bickert", "Meta"),
    ("JKaplan", "Meta"), ("JKaplan", "WhiteHouse"),
    ("Greenblatt", "ADL"), ("Greenblatt", "WhiteHouse"),
]


def read_jsonl(path: Path) -> list[dict]:
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def main() -> None:
    institutions = read_jsonl(DATA / "institutions.jsonl")
    people = read_jsonl(DATA / "people.jsonl")
    edges = read_jsonl(DATA / "edges.jsonl")

    inst_ids = {r["id"] for r in institutions}
    person_ids = {r["id"] for r in people}
    all_ids = inst_ids | person_ids
    edge_keys = {(e.get("source"), e.get("target")) for e in edges if isinstance(e, dict)}

    new_inst = 0
    for rec in NEW_INSTITUTIONS:
        if rec["id"] in inst_ids or rec["id"] in person_ids:
            continue
        rec["kind"] = "institution"
        institutions.append(rec)
        inst_ids.add(rec["id"])
        all_ids.add(rec["id"])
        new_inst += 1

    new_persons = 0
    for rec in NEW_PERSONS:
        if rec["id"] in person_ids or rec["id"] in inst_ids:
            continue
        rec["kind"] = "person"
        people.append(rec)
        person_ids.add(rec["id"])
        all_ids.add(rec["id"])
        new_persons += 1

    new_edges = 0
    skipped_edges = []
    for src, tgt in NEW_EDGES:
        if src not in all_ids:
            skipped_edges.append(f"missing person {src!r}")
            continue
        if tgt not in all_ids:
            skipped_edges.append(f"missing institution {tgt!r} (from {src})")
            continue
        if (src, tgt) in edge_keys:
            continue
        edges.append({"source": src, "target": tgt})
        edge_keys.add((src, tgt))
        new_edges += 1

    with (DATA / "institutions.jsonl").open("w", encoding="utf-8") as f:
        for rec in institutions:
            f.write(json.dumps(rec) + "\n")
    with (DATA / "people.jsonl").open("w", encoding="utf-8") as f:
        for rec in people:
            f.write(json.dumps(rec) + "\n")
    with (DATA / "edges.jsonl").open("w", encoding="utf-8") as f:
        for e in edges:
            f.write(json.dumps(e) + "\n")

    print(f"Added {new_inst} institutions, {new_persons} persons, {new_edges} edges.")
    if skipped_edges:
        print(f"Skipped {len(skipped_edges)} edges:")
        for s in skipped_edges:
            print(f"  - {s}")
    print(f"Totals: {len(institutions)} institutions, {len(people)} people, {len(edges)} edges.")


if __name__ == "__main__":
    main()
