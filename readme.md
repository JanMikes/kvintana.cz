# Kvintána — nový web (prototyp)

Statický prototyp prezentačního webu pro **Kvintánu, spolek historického jezdectví**
(náhrada za současný kvintana.cz).

Bez backendu — 19 hotových HTML stránek, které se dají otevřít přímo v prohlížeči.

```
open index.html
```

Formulář poptávky a filtr galerie fungují na klientovi; formulář zatím nikam neodesílá.

---

## Struktura

```
index.html                       Domů
o-nas.html                       O nás
nabidka.html                     Nabídka (rozcestník 7 služeb)
predstaveni.html                 Přehled šesti představení
predstaveni/<slug>.html          Detail představení (6×)
putovani.html                    ┐
vyjizdky.html                    │
jezdecke-kurzy.html              │ zbývajících 6 služeb
skolni-vylety.html               │
filmy.html                       │
preprava-koni.html               ┘
fotogalerie.html                 13 alb + lightbox
kontakt.html                     Kontakt + poptávkový formulář + mapa
spoluprace.html                  Partneři

assets/css/site.css              Design systém (jediný stylesheet)
assets/js/site.js                Chování — bez závislostí
assets/img/                      Nagradované fotky, WebP ve 4 šířkách + JPG fallback

tools/content.py                 Veškerý obsah na jednom místě
tools/build.py                   Generátor → vypíše .html do rootu
tools/build_images.sh            Pipeline pro fotky
tools/build_map.py               Statická mapa z OSM dlaždic
```

### Přegenerování

```bash
python3 tools/build.py          # HTML (bez závislostí)
sh tools/build_images.sh        # fotky, vyžaduje ImageMagick 7
python3 tools/build_map.py      # mapa, vyžaduje síť + ImageMagick
```

HTML soubory v rootu jsou výsledek — dají se předat komukoliv i bez generátoru.
Generátor existuje proto, aby se hlavička, patička a navigace daly měnit na jednom
místě místo ve dvaceti souborech.

---

## Design — „Ember & Night"

| Token | Hodnota | Použití |
|---|---|---|
| `--night` | `#14100e` | podklad |
| `--night-raise` | `#1c1714` | odsazené sekce |
| `--ember` / `--ember-hot` | `#c2461e` / `#e86a32` | akcent, tlačítka |
| `--brass` | `#a8823c` | historizující detaily, střídmě |
| `--bone` | `#ede3d4` | text |

**Písmo** — [Fraunces](https://fonts.google.com/specimen/Fraunces) (variabilní,
osy `SOFT` a `WONK` dávají textu lehce archaický charakter) na nadpisy,
[Instrument Sans](https://fonts.google.com/specimen/Instrument+Sans) na text.
Obojí z Google Fonts, plná podpora české diakritiky.

**Proč tmavá:** nejsilnější fotky spolku jsou noční snímky ohnivé show. Tmavý
podklad je nechá svítit a zároveň sjednotí zbytek archivu, který je fotograficky
hodně nesourodý. Pomáhá tomu i jemné zrno přes celou stránku a společný teplý
grade všech fotek.

### Prvky, které web drží pohromadě

- **Číslovaný index nabídky** — služby jako redakční seznam s náhledem
  u každé položky (bez hoveru, funguje stejně na dotyku).
- **Posunutá mřížka karet** — prostřední sloupec je záměrně níž.
- **Iniciála** v úvodním odstavci dlouhých textů.
- **Dvojportrét** Viktora a Terezy v sekci O nás na homepage — dvě fotky
  ze stejného focení, druhá záměrně posunutá níž.
- **Zrno + teplý grade** na všech fotkách.
- **Běžící pás filmografie** na homepage.
- **Mapa** vyrenderovaná z OSM dlaždic a nagradovaná do palety — žádný cizí
  iframe, žádné requesty třetích stran za běhu. Kliknutí vede do Google Map
  (adresa je v `SITE["map_url"]`).

---

## Obsah — co je odkud

`tools/content.py` má na začátku pravidla provenience a každý údaj je označený:

- **SOURCE** — doslova (nebo bez přidání informace) z kvintana.cz.
- **WRITTEN** — nově napsané pro tenhle web. Neobsahuje **žádné** tvrzení,
  které by nestálo na nějakém SOURCE řetězci: žádné roky, žádný dosah
  působnosti, žádné doby odezvy, kapacity ani ceny.

Co stávající web neuvádí, tady prostě není. Konkrétně jsem odstranil dřívější
verze textů, které si vymýšlely: vhodnou denní dobu u představení, „působnost
celá ČR", „odpovídáme do dvou dnů", autorství fotografií, počty dětí a věkové
skupiny u školních výletů a rok založení spolku.

### Co je potřeba doplnit před spuštěním

- **Kalendář akcí je pryč.** Na požádání smazán — spolek si ho nedokáže udržovat
  aktuální a prázdný nebo zastaralý kalendář působí hůř než žádný.
- **Rozpor v adrese:** kontakt uvádí *Široký důl 5, Polička*, ale text
  u vyjížděk zve *do Lučic* a putování popisuje Hostýnské vrchy a Moravskou
  bránu. Obojí je na webu zobrazené tak, jak je dnes — je potřeba ujasnit,
  kde spolek reálně sídlí a odkud vyjíždí.
- **Čísla na homepage** (6 představení, 9 filmů, 5 koní, 13 fotogalerií) jsou
  spočítaná z obsahu stávajícího webu. Rok založení ani „X let zkušeností"
  nikde není — spolek není ani ve veřejném spolkovém rejstříku, takže to
  nemám z čeho ověřit. Pokud to na web chcete, musíte dodat údaj vy.
- **Fotky Viktora a Terezy** — identifikoval je klient (`g3-51` a `g3-52`,
  původně `img/gallery/3/51.jpg` a `52.jpg`). Jsou to jediné dvě fotky
  na webu, u kterých je někdo jmenovitě označený. Stejný dvojportrét se dá
  snadno použít i na stránce O nás — teď tam je detail zbroje.
- **Autorská práva k fotkám** — stávající web neuvádí, kdo fotky pořídil.
  Popisky proto žádného autora neuvádějí. Vojtěch Flídr je zmíněný jen tam,
  kde ho zmiňuje i současný web, tedy na stránce Spolupráce.
- **Fotky** — použitý je celý dostupný archiv (68 snímků). Kvalita je smíšená.
  Hlavní fotka na homepage je teď nejostřejší snímek v archivu (rytířský
  turnaj pod hradbami, 4688 px); ohnivá show je bohužel jen v 800 px, takže
  se používá tam, kde se zobrazuje menší. AI upscale by detail nedodal —
  nové focení ano.

## Technicky

- Žádný build step pro frontend, žádné závislosti v prohlížeči.
- Fotky: WebP v šířkách 400/800/1200/2000 (nikdy se needituje nahoru přes originál)
  + JPG fallback, `srcset` + `sizes`, `loading="lazy"` mimo hero.
- Stránka je čitelná i s vypnutým JavaScriptem — animace odhalování se aktivují
  až podle třídy `js` na `<html>`.
- Respektuje `prefers-reduced-motion`.
- Lightbox: klávesnice (šipky, Esc), swipe na mobilu, návrat fokusu.
- Hlavička je vždy prosklená (blur + tmavý podklad), aby navigace držela
  kontrast nad jakoukoliv fotkou.
- Mapa je statický obrázek, ne iframe — bez cizích requestů a cookies.
  Podklad je z OpenStreetMap (atribuce je proto povinná a je pod mapou),
  ale odkaz „Otevřít" míří do Google Map.
- Celkem ~31 MB fotek; při nasazení stojí za zvážení, jestli jsou potřeba
  varianty 2000 px u všech alb.
