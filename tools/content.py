# -*- coding: utf-8 -*-
"""Kvintána — content model.

PROVENANCE RULES — read before editing.

  SOURCE:  copied verbatim (or paraphrased without adding information) from
           kvintana.cz. Safe to publish as-is.
  WRITTEN: newly written for this site. Contains NO factual claim that isn't
           backed by a SOURCE string somewhere in this file — no dates, no
           coverage areas, no response times, no capacities, no prices.

Anything the source site does not state is simply absent here. If the club
wants it on the site, they have to supply it.
"""

SITE_URL = "https://kvintana.cz"

# Formspree endpoint for the inquiry form (public by design).
FORMSPREE = "https://formspree.io/f/mrenrwez"

SITE = {
    "name": "Kvintána",
    "tagline": "Spolek historického jezdectví",   # SOURCE (page titles)
    "person": "Viktor Fiala",                     # SOURCE (contact page)
    "phone": "+420 737 179 811",                  # SOURCE
    "phone_href": "+420737179811",
    "email": "jizda@centrum.cz",                  # SOURCE
    "address": ["Viktor Fiala", "Široký důl 5", "572 01 Polička"],  # SOURCE
    "gps": "49°44'46.5\"N 16°13'33.5\"E",         # SOURCE
    "lat": 49.746250,
    "lon": 16.225972,
    # Where "open the map" goes. The map image itself is rendered from OSM
    # tiles (see tools/build_map.py), so OSM attribution stays either way —
    # but the click-through goes to Google Maps, which is what people here
    # actually navigate with.
    "map_url": "https://www.google.com/maps/search/?api=1&query=49.746250%2C16.225972",
}

# --- Představení -------------------------------------------------------------
# `text` and `spec` are SOURCE. `teaser` is WRITTEN but only restates `text`.
# Shows the source gives no spec for simply have none — nothing is invented.

SHOWS = [
    {
        "slug": "ohen-a-kun",
        "name": "Oheň a kůň",
        "kicker": "Ohnivá show",
        "text": "V divočině dva zdánlivě nesmiřitelní protivníci, ovšem s pomocí "
                "člověka se z nich mohou stát i partneři. Čeká vás ohnivá podívaná, "
                "na kterou jen tak nezapomenete!",
        "teaser": "Kůň, jezdec a plameny. Podívaná, na kterou jen tak nezapomenete.",
        "cast": "Jezdec + kůň, dva pěší pomocníci",
        "length": "15 minut",
        "cover": "g1-4",
        "hero": "g1-3",
        "photos": ["g1-3", "g1-4", "g1-2", "g1-5"],
    },
    {
        "slug": "partie-krasneho-dragouna",
        "name": "Partie krásného dragouna",
        "kicker": "Rakousko-Uhersko",
        "text": "V rytmu vídeňského valčíku se zvolna blíží Velká válka, která "
                "definitivně odvane dobu galantních mužů v nádherných uniformách "
                "na ztepilých koních, kdykoliv připravených vyrazit tryskem do útoku "
                "s blýskavými šavlemi napřaženými ke smrtelným úderům nebo padnout "
                "za císaře pána a jeho rodinu. Zatím je však ještě mír, tak vyrazme "
                "na nedalekou jízdárnu pokochat se jezdeckým uměním chlapíků "
                "v rudých rajtkách a blankytně modrých blůzách.",
        "teaser": "Poslední mír před Velkou válkou, šavle a modré blůzy.",
        "cast": "2 koně + 2 jezdci",
        "length": "cca 30 minut",
        "cover": "g2-6",
        "hero": "g2-6",
        "photos": ["g2-6", "g2-7", "g2-8", "g2-9", "g2-10", "g2-11", "g2-12"],
    },
    {
        "slug": "vivat-maria-theresia",
        "name": "Vivat Maria Theresia",
        "kicker": "Války slezské",
        "text": "Vydejte se na toulky po bitevních polích válek slezských. "
                "Zaposlouchejte se do poutavého vyprávění vysloužilého kyrysníka "
                "Jeho výsosti Marie Terezie, do řinčení jeho těžkého jezdeckého "
                "palaše a dusotu vojenského oře a dávejte dobrý pozor. Možná budete "
                "naverbováni do jeho jezdeckého pluku a pak se teprve začnou dít věci!",
        "teaser": "Vysloužilý kyrysník verbuje diváky do svého pluku.",
        "cast": "2 koně + 2 jezdci",
        "length": "cca 30 minut",
        "cover": "g3-47",
        "hero": "g3-48",
        "photos": ["g3-47", "g3-48", "g3-46", "g3-49", "g3-50", "g3-51", "g3-52"],
    },
    {
        "slug": "rytirske-turnaje",
        "name": "Rytířské turnaje",
        "kicker": "Středověk",
        "text": "Vdechněte závan dávných časů, dob, kdy se nechodilo na fotbal "
                "a kdy vás vaši páni uměli nejen obrat o desátky, ale také vás "
                "obstojně pobavit či ochránit vlastním mečem. Zde nehledejte okázalou "
                "a unylou zábavu, slečinky na načančaných koních. Půjde do tuhého. "
                "Potečou tu hektolitry koňského a chlapského potu, kolem hlav vám "
                "budou létat třísky ze zlámaných dřevců a kusy pomačkaných zbrojí, "
                "ale i tak si užijete obrovskou porci nefalšované středověké zábavy.",
        "teaser": "Zlámané dřevce, pomačkané zbroje. Půjde do tuhého.",
        "cast": "",      # source gives no obsazení for this show
        "length": "",    # source gives no délka for this show
        "cover": "g0-45",
        "hero": "g4-68",
        "photos": ["g0-45", "g4-42", "g4-68", "g4-35", "g4-43", "g4-69", "g4-70",
                    "g4-71", "g4-44", "g4-36", "g4-37", "g4-38", "g4-39", "g4-40", "g4-41"],
    },
    {
        "slug": "rytir-sysel-z-holohlav",
        "name": "Rytíř Sysel z Holohlav",
        "kicker": "Komediální",
        "text": "Starý turnajový bijec k vám zavítá na své věrné kobylce a doprovodí "
                "ho jeho krásná paní, se kterou je rytíř čas od času takzvaně na nože. "
                "Možná se stanete svědky toho, jakým způsobem naši dávní předkové "
                "řešili manželské spory. Jistě přijde řeč na meče, kopí či dřevce, "
                "tak se hezky usaďte a můžete se vsadit, kdo že to nosí u Syslů "
                "z Holohlav kroužkové kalhoty.",
        "teaser": "Manželská rozepře řešená mečem, kopím a dřevcem.",
        "cast": "2 koně + 2 jezdci",
        "length": "cca 30 minut",
        "cover": "g5-30",
        "hero": "g5-31",
        "photos": ["g5-30", "g5-31", "g5-32", "g5-27", "g5-28", "g5-29", "g5-33", "g5-34"],
    },
    {
        "slug": "pruvody-stafaze-bitvy",
        "name": "Průvody, stafáže, bitvy",
        "kicker": "Doplněk akce",
        "text": "Vsaďte na koně, kteří prošli našima rukama. Na koně, kteří znají "
                "salvy z mušket, kanonů i obyčejnou lidskou tlačenici.",
        "teaser": "Koně, kteří znají salvy z mušket, kanonů i lidskou tlačenici.",
        "cast": "",
        "length": "",
        "cover": "g7-15",
        "hero": "g7-14",
        "photos": ["g7-15", "g7-14", "g7-13", "g7-16", "g7-17"],
    },
]

# --- Nabídka ------------------------------------------------------------------

OFFERS = [
    {"slug": "predstaveni", "url": "/predstaveni/", "name": "Představení",
     "teaser": "Šest programů pro hrady, města a vesnice.", "cover": "g1-4"},
    {"slug": "putovani", "url": "/putovani/", "name": "Putování",
     "teaser": "Putování krajem po stopách dávných kupeckých karavan.", "cover": "g6-18"},
    {"slug": "vyjizdky", "url": "/vyjizdky/", "name": "Vyjížďky",
     "teaser": "Do sedla pod vedením zkušeného instruktora.", "cover": "g6-23"},
    {"slug": "jezdecke-kurzy", "url": "/jezdecke-kurzy/", "name": "Jezdecké kurzy",
     "teaser": "Vícedenní výcvikové pobyty pro školky, školy i firmy.", "cover": "g6-26"},
    {"slug": "skolni-vylety", "url": "/skolni-vylety/", "name": "Školní výlety",
     "teaser": "Program pro školy a školky.", "cover": "g21-67"},
    {"slug": "filmy", "url": "/filmy/", "name": "Filmy",
     "teaser": "Koně a jezdci do kaskadérských i komparsových rolí.", "cover": "g16-54"},
    {"slug": "preprava-koni", "url": "/preprava-koni/", "name": "Přeprava koní",
     "teaser": "Vozy a přívěsy — pro vás i k zapůjčení.", "cover": "g5-27"},
]

# --- Filmografie — SOURCE, order preserved -----------------------------------
# "Mohli jste nás vidět v těchto filmech:"

FILMS = [
    {"title": "Strážce duší", "photos": ["g8-63", "g8-65"]},
    {"title": "Svatba na bitevním poli", "photos": ["g9-62"]},
    {"title": "My Giant", "photos": []},
    {"title": "Něvskij", "photos": []},
    {"title": "Dvanáct měsíčků", "photos": []},
    {"title": "Tři srdce", "photos": ["g13-61"]},
    {"title": "Ztracený princ", "photos": []},
    {"title": "Tajemství lesní země", "photos": ["g15-56", "g15-57", "g15-58", "g15-59", "g15-60"]},
    {"title": "Cyril a Metoděj", "photos": ["g16-53", "g16-54", "g16-55"]},
]

# --- Koně — SOURCE (Vyjížďky page) -------------------------------------------

HORSES = ["Šeila", "Lady Lucky", "Rainy", "Pretty Woman", "Amanda"]

# --- Fotogalerie — album names are SOURCE ------------------------------------

ALBUMS = [
    {"slug": "ohen-a-kun", "name": "Oheň a kůň", "cat": "predstaveni",
     "photos": ["g1-3", "g1-4", "g1-2", "g1-5"]},
    {"slug": "partie-krasneho-dragouna", "name": "Partie krásného dragouna", "cat": "predstaveni",
     "photos": ["g2-6", "g2-7", "g2-8", "g2-9", "g2-10", "g2-11", "g2-12"]},
    {"slug": "vivat-maria-theresia", "name": "Vivat Maria Theresia", "cat": "predstaveni",
     "photos": ["g3-47", "g3-48", "g3-46", "g3-49", "g3-50", "g3-51", "g3-52"]},
    {"slug": "rytirske-turnaje", "name": "Rytířské turnaje", "cat": "predstaveni",
     "photos": ["g0-45", "g4-42", "g4-68", "g4-35", "g4-43", "g4-69", "g4-70", "g4-71",
                 "g4-44", "g4-36", "g4-37", "g4-38", "g4-39", "g4-40", "g4-41"]},
    {"slug": "rytir-sysel-z-holohlav", "name": "Rytíř Sysel z Holohlav", "cat": "predstaveni",
     "photos": ["g5-30", "g5-31", "g5-32", "g5-27", "g5-28", "g5-29", "g5-33", "g5-34"]},
    {"slug": "pruvody-stafaze-bitvy", "name": "Průvody, stafáže, bitvy", "cat": "predstaveni",
     "photos": ["g7-15", "g7-14", "g7-13", "g7-16", "g7-17"]},
    {"slug": "putovani", "name": "Fotografie z putování", "cat": "krajina",
     "photos": ["g6-18", "g6-23", "g6-22", "g6-21", "g6-20", "g6-19", "g6-24", "g6-25", "g6-26"]},
    {"slug": "skolni-vylety", "name": "Foto — školní výlety", "cat": "krajina",
     "photos": ["g21-66", "g21-67"]},
    {"slug": "strazce-dusi", "name": "Strážce duší", "cat": "film",
     "photos": ["g8-63", "g8-65"]},
    {"slug": "svatba-na-bitevnim-poli", "name": "Svatba na bitevním poli", "cat": "film",
     "photos": ["g9-62"]},
    {"slug": "tri-srdce", "name": "Tři srdce", "cat": "film",
     "photos": ["g13-61"]},
    {"slug": "tajemstvi-lesni-zeme", "name": "Tajemství lesní země", "cat": "film",
     "photos": ["g15-56", "g15-57", "g15-58", "g15-59", "g15-60"]},
    {"slug": "cyril-a-metodej", "name": "Cyril a Metoděj", "cat": "film",
     "photos": ["g16-53", "g16-54", "g16-55"]},
]

GALLERY_CATS = [
    ("all", "Vše"),
    ("predstaveni", "Představení"),
    ("film", "Film"),
    ("krajina", "Krajina a lidé"),
]

# --- Spolupráce — SOURCE ------------------------------------------------------

PARTNERS = [
    {"name": "Vojtěch Flídr Art-Photography",
     "url": "https://www.facebook.com/VojtechFlidrArtPhotography/",
     "host": "facebook.com",
     "note": "Nejšikovnější fotograf v celém širém okolí, velmi milý, usměvavý "
             "a výsledky stojí za to!"},
    {"name": "Hrad Starý Jičín", "url": "http://www.hradstaryjicin.cz",
     "host": "hradstaryjicin.cz", "note": ""},
    {"name": "Viking Agency", "url": "http://www.vikingagency.cz",
     "host": "vikingagency.cz", "note": ""},
    {"name": "Cirkus Trochu Jinak", "url": "http://www.cirkusjinak.cz",
     "host": "cirkusjinak.cz", "note": ""},
    {"name": "Studio Bez Kliky", "url": "http://www.bezkliky.eu/studio/",
     "host": "bezkliky.eu", "note": ""},
    {"name": "GRYFF", "url": "http://www.gryff.cz",
     "host": "gryff.cz", "note": ""},
]

# --- Čísla na homepage --------------------------------------------------------
# Every one of these is countable from the source site. Nothing else goes here.

FACTS = [
    ("06", "představení"),   # 6 shows listed under Nabídka → Představení
    ("09", "filmů"),         # 9 titles on the Filmy page
    ("05", "koní"),          # Šeila, Lady Lucky, Rainy, Pretty Woman, Amanda
    ("13", "fotogalerií"),   # 13 albums in Fotogalerie
]


# --- Redirects from the old Nette URLs ---------------------------------------
# GitHub Pages cannot issue 301s, so tools/build.py renders each of these as a
# stub page carrying <link rel="canonical"> + an instant meta refresh.
# Sources are the paths the old site actually exposed (verified against the live
# site before the migration).

_SHOW_BY_OLD_ID = {
    1: "ohen-a-kun", 2: "partie-krasneho-dragouna", 3: "vivat-maria-theresia",
    4: "rytirske-turnaje", 5: "rytir-sysel-z-holohlav", 7: "pruvody-stafaze-bitvy",
}

# old gallery id -> new album slug (see ALBUMS); anchors into /fotogalerie/
_ALBUM_BY_OLD_ID = {
    1: "ohen-a-kun", 2: "partie-krasneho-dragouna", 3: "vivat-maria-theresia",
    4: "rytirske-turnaje", 5: "rytir-sysel-z-holohlav", 6: "putovani",
    7: "pruvody-stafaze-bitvy", 8: "strazce-dusi", 9: "svatba-na-bitevnim-poli",
    13: "tri-srdce", 15: "tajemstvi-lesni-zeme", 16: "cyril-a-metodej",
    21: "skolni-vylety",
}

REDIRECTS = {}

# /nabidka/detail/1..7 -> the seven offer pages, in the old menu order
for _i, _o in enumerate(OFFERS, 1):
    REDIRECTS["nabidka/detail/%d" % _i] = _o["url"]

# /nabidka/detail-predstaveni/N -> show pages, or /filmy/ for the film galleries
for _i, _slug in _SHOW_BY_OLD_ID.items():
    REDIRECTS["nabidka/detail-predstaveni/%d" % _i] = "/predstaveni/%s/" % _slug
for _i in (8, 9, 13, 15, 16):
    REDIRECTS["nabidka/detail-predstaveni/%d" % _i] = "/filmy/"

# /fotogalerie/detail/N -> the album's anchor on the gallery page
for _i, _slug in _ALBUM_BY_OLD_ID.items():
    REDIRECTS["fotogalerie/detail/%d" % _i] = "/fotogalerie/#%s" % _slug

# the calendar page was removed outright
REDIRECTS["kalendar-akci"] = "/"
