
import sys
import re
import unicodedata
import requests
from bs4 import BeautifulSoup


def normalize_greek(text):
    return unicodedata.normalize("NFC", text)

def get_bailly_entry(word):
    url = f"https://logeion.uchicago.edu/{word}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    bailly_header = soup.find("h3", string=lambda s: s and "Bailly 2024" in s)
    if not bailly_header:
        return None
    bailly_div = bailly_header.find_next("div")
    if not bailly_div:
        return None
    return bailly_div.get_text(separator="\n").strip()

def extract_greek_from_etym(bailly_text):
    greek_words = set()
    etym_match = re.search(r"Etym\.(.*?)(?:\n[A-Z]|$)", bailly_text, re.S)
    if not etym_match:
        return greek_words
    etym_text = etym_match.group(1)
    greek_pattern = r"[ἀ-῾Α-Ωα-ω]+"
    for w in re.findall(greek_pattern, etym_text):
        greek_words.add(normalize_greek(w))
    return greek_words

def get_wiktionary_etymology(word):
    url = f"https://en.wiktionary.org/wiki/{word}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    etym_text = ""
    in_ancient_greek = False
    in_etymology = False
    for tag in soup.find_all(["h2", "h3"]):
        if tag.name == "h2" and "Ancient Greek" in tag.get_text():
            in_ancient_greek = True
            continue
        if in_ancient_greek and tag.name == "h3" and "Etymology" in tag.get_text():
            in_etymology = True
            continue
        if in_ancient_greek and in_etymology:
            if tag.name in ["h2", "h3"]:
                break
            next_node = tag.find_next_sibling()
            if next_node:
                etym_text += next_node.get_text(separator="\n")
    return etym_text.strip() if etym_text else None

def append_to_file(text, filename="filebailly.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n\n")

visited = set()

def process_word(word):
    word = normalize_greek(word)
    if word in visited:
        return
    visited.add(word)

    print(f"\n=== PROCESSING {word} ===\n")

    bailly = get_bailly_entry(word)
    if bailly:
        print(f"=== BAILLY 2024 ENTRY FOR {word} ===\n{bailly}\n")
        append_to_file(f"=== BAILLY 2024 ENTRY FOR {word} ===\n{bailly}")
        greek_words = extract_greek_from_etym(bailly)
        for g in greek_words:
            process_word(g)

    wikietym = get_wiktionary_etymology(word)
    if wikietym:
        print(f"=== WIKTIONARY ETYMOLOGY FOR {word} ===\n{wikietym}\n")
        append_to_file(f"=== WIKTIONARY ETYMOLOGY FOR {word} ===\n{wikietym}")

###############################################
#  MAIN — READ WORDS FROM fileone.txt         #
###############################################

def main():
    try:
        with open("fileone.txt", "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ ERROR: fileone.txt not found.")
        sys.exit(1)

    print(f"\nLoaded {len(words)} Greek words from fileone.txt\n")

    for w in words:
        process_word(w)

if __name__ == "__main__":
    main()


import requests
from bs4 import BeautifulSoup
import re
import unicodedata

def normalize_greek(text):
    return unicodedata.normalize("NFC", text)

def getbaillyentry(word):
    url = f"https://logeion.uchicago.edu/{word}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    bailly_header = soup.find("h3", string=lambda s: s and "Bailly 2024" in s)
    if not bailly_header:
        return None
    baillydiv = baillyheader.find_next("div")
    if not bailly_div:
        return None
    return baillydiv.gettext(separator="\n").strip()

def extractgreekfrometym(baillytext):
    greek_words = set()
    etymmatch = re.search(r"Etym\.(.*?)(?:\n[A-Z]|$)", baillytext, re.S)
    if not etym_match:
        return greek_words
    etymtext = etymmatch.group(1)
    greek_pattern = r"[ἀ-῾Α-Ωα-ω]+"
    for w in re.findall(greekpattern, etymtext):
        greekwords.add(normalizegreek(w))
    return greek_words

def getwiktionaryetymology(word):
    url = f"https://en.wiktionary.org/wiki/{word}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    etym_text = ""
    inancientgreek = False
    in_etymology = False
    for tag in soup.find_all(["h2", "h3"]):
        if tag.name == "h2" and "Ancient Greek" in tag.get_text():
            inancientgreek = True
            continue
        if inancientgreek and tag.name == "h3" and "Etymology" in tag.get_text():
            in_etymology = True
            continue
        if inancientgreek and in_etymology:
            if tag.name in ["h2", "h3"]:
                break
            nextnode = tag.findnext_sibling()
            if next_node:
                etymtext += nextnode.get_text(separator="\n")
    return etymtext.strip() if etymtext else None

def appendtofile(text, filename="filebailly.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n\n")

visited = set()

def process_word(word):
    word = normalize_greek(word)
    if word in visited:
        return
    visited.add(word)
    print(f"Processing: {word}")
    bailly = getbaillyentry(word)
    if bailly:
        appendtofile(f"=== BAILLY 2024 ENTRY FOR {word} ===\n{bailly}")
        greekwords = extractgreekfrometym(bailly)
        for g in greek_words:
            process_word(g)
    wikietym = getwiktionaryetymology(word)
    if wikietym:
        appendtofile(f"=== WIKTIONARY ETYMOLOGY FOR {word} ===\n{wikietym}")

def main():
    words = input("Enter Greek words separated by spaces: ").strip().split()
    for w in words:
        process_word(w)

if name == "main":
    main()









1

Interea medium Aeneas
Mitten im Meer hielt 

iam classe tenebat
*schon Aineias indes mit der Flotte
*
certus iter fluctusque atros Aquilone secabat
*Sicher den Weg und schnitt mit dem Nord durch die dunkelen Fluten.
*
moenia respiciens, quae iam infelicis Elissae
*Hinter sich sah er die Stadt, durch der unglückselgen Elissa
*
conlucent flammis. quae tantum accenderit ignem
*Flammen erhellt. Zwar ist ihm der Grund des gewaltigen Feuers
*
5



causa latet; duri magno sed amore dolores
Dunkel; der heftige Schmerz ob des Bruchs so inniger Liebe

polluto, notumque furens quid femina possit,
*Und die Erfahrung jedoch, was alles ein rasendes Weib wagt,
*
triste per augurium Teucrorum pectora ducunt.
*Füllen der Teukrier Brust mit unheilkündender Ahnung.
*
ut pelagus tenuere rates nec iam amplius ulla
*Als auf die Höhe die Flotte gelangt und nirgend ein Land mehr
*
occurrit tellus, maria undique et undique caelum,
*Sichtbar bleibt, als alles umher nur Himmel und Meer ist,
*
10



olli caeruleus supra caput astitit imber
Hebt sich ein Regengewölk mit bläulichem Schein ihm zu Häupten,

noctem hiememque ferens et inhorruit unda tenebris.
*Schwanger mit Sturm und Nacht, und schwarz auf schaudert die Woge.
*
ipse gubernator puppi Palinurus ab alta:
*Selbst Palinurus, der Lenker des Steuers, ruft hoch vom Verdecke:
*
"heu quianam tanti cinxerunt aethera nimbi?
*"Weh! welch dichtes Gewölk umhüllt allseitig den Aither!
*
quidve, pater Neptune, paras?" sic deinde locutus
*Vater Neptun, was hast du im Sinn?" - So sprechend, befiehlt er,
*
15



colligere arma iubet validisque incumbere remis,
Alles zu rüsten im Schiff und sich fest auf die Ruder zu stemmen;

obliquatque sinus in ventum ac talia fatur:
*Stellt schräg gegen den Wind dann die Segel und redet die Worte:
*
"magnanime Aenea, non, si mihi Iuppiter auctor
*"Nicht wenn Iupiter selbst sich verbürgte, gedächt ich bei diesem
*
spondeat, hoc sperem Italiam contingere caelo.
*Himmel, erhabener Fürst, Italiens Strand zu erreichen.
*
mutati transversa fremunt et vespere ab atro
*Widrig dreht mit Gebraus sich der Wind; er steigt von dem dunklen
*
20



consurgunt venti, atque in nubem cogitur aër.
Abend herauf, und die Luft verdickt zu Nebelgewölk sich.

nec nos obniti contra nec tendere tantum
*Unsere Kraft reicht nicht, ihm entgegenzusteuern, noch hält sie
*
sufficimus. superat quoniam Fortuna, sequamur,
*Wider ihn aus; so folgen wir denn, vom Geschicke bewältigt;
*
quoque vocat vertamus iter. nec litora longe
*Wenden wir um, wohin es uns ruft. Des verbrüderten Eryx
*
fida reor fraterna Erycis portusque Sicanos,
*Sicherer Strand und Sikaniens Port kann, denk ich, nicht fern sein,
*
25



si modo rite memor servata remetior astra."
Täuscht das Gedächtnis mich nicht bei erneuter Betrachtung der Sterne."

tum pius Aeneas: "equidem sic poscere ventos
*Und Aineias darauf: "Längst merk ich, dass es die Winde
*
iamdudum et frustra cerno te tendere contra.
*Also fordern und du umsonst dich gegen sie anstrengst.
*
flecte viam velis. an sit mihi gratior ulla,
*Wende die Segel herum! Wie möchte' ein anderes Land ich
*
quove magis fessas optem dimittere navis,
*Lieber dazu mir ersehn, die ermüdeten Schiffe zu rasten,
*
30



quam quae Dardanium tellus mihi servat Acesten
Als das, welches den Dardaner mir, den Akestes, beherbergt

et patris Anchisae gremio complectitur ossa?"
*Und des Schoß das Gebein umhegt des Erzeugers Anchises!"
*
haec ubi dicta, petunt portus et vela secundi
*Sprach's und sie lenken zum Hafen den Kurs und der günstige Westwind
*
intendunt Zephyri; fertur cita gurgite classis,
*Schwellet die Segel; es fliegt auf eilenden Wogen die Flotte,
*
et tandem laeti notae advertuntur harenae.
*Und froh landen zuletzt sie am Sand des bekannten Gestades.
*
35



At procul ex celso miratus vertice montis
Fernher sieht Akestes vom ragenden Gipfel des Berges

adventum sociasque rates occurrit Acestes,
*Staunend der Freunde Geschwader sich nahn und eilt, sie zu grüßen,
*
horridus in iaculis et pelle Libystidis ursae,
*Wild umstarrt mit Geschoss und dem Fell der libystischen Bärin.
*
Troia Criniso conceptum flumine mater
*Vom Flussgotte Krimisos erzeugt, und von troischer Mutter
*
quem genuit. veterum non immemor ille parentum
*War er geboren, und gern noch dacht' er der früheren Eltern,
*
40



gratatur reduces et gaza laetus agresti
Wünschte den Wiedergekommenen Glück; mit ländlichem Reichtum

excipit, ac fessos opibus solatur amicis.
*Nahm er sie auf und erquickte sie froh mit freundlichen Gaben.
*
Postera cum primo stellas Oriente fugarat
*Als hellstrahlend der Tag beim ersten Erwachen die Sterne
*
clara dies, socios in coetum litore ab omni
*Wieder verscheucht, da ruft Aineias vom ganzen Gestade
*
advocat Aeneas tumulique ex aggere fatur:
*Alle Gefährten herbei und spricht von dem Hügel des Grabes:
*
45



"Dardanidae magni, genus alto a sanguine divum,
"Dardanos' großes Geschlecht, vom erhabenen Blute der Götter

annuus exactis completur mensibus orbis,
*Stammend, es füllt sich ein Jahr aufs neu in der Monate Kreislauf,
*
ex quo reliquias divinique ossa parentis
*Seit wir den sterblichen Rest, die Gebeine des göttlichen Vaters,
*
condidimus terra maestasque sacravimus aras;
*Hier in die Erde gesenkt und geweiht ihm Traueraltäre.
*
iamque dies, nisi fallor, adest, quem semper acerbum,
*Dies ist, irr ich mich nicht, der Tag, den ich ewig mit bittren
*
50



semper honoratum - sic di voluistis - habebo.
Schmerzen - so habt ihr's, Götter, gewollt - zu ehren gedenke.

hunc ego Gaetulis agerem si Syrtibus exsul,
*Sollt' ich ihn, landesverbannt, in Gätuliens Syrten verleben,
*
Argolicove mari deprensus et urbe Mycenae,
*Sollt' im argolischen Meer, in Mykenes Stadt er mich treffen,
*
annua vota tamen sollemnisque ordine pompas
*Würd' ich den festlichen Zug nach Brauch und das Jahresgelübde
*
exsequerer strueremque suis altaria donis.
*Dennoch begehn und die Gaben ihm weihn auf den hohen Altären.
*
55



nunc ultro ad cineres ipsius et ossa parentis
Jetzo sind wir beim Staub und bei den Gebeinen des Vaters

haud equidem sine mente, reor, sine numine divum
*Selbst anwesend und, wie mich bedünkt, nicht ohne der Götter
*
adsumus et portus delati intramus amicos.
*Willen und Macht und sind zum befreundeten Hafen verschlagen.
*
ergo agite et laetum cuncti celebremus honorem:
*Auf denn, und lasst insgesamt uns die festlichen Ehren begehen!
*
poscamus ventos, atque haec me sacra quotannis
*Flehn wir um Wind, und gestatt' er, dass einst ich jährlich die Opfer
*
60



urbe velit posita templis sibi ferre dicatis.
In der gegründeten Stadt in dem eigenen Tempel ihm bringe.

bina boum vobis Troia generatus Acestes
*Troias Sprössling, Akestes, gibt euch zwei Stiere für jedes
*
dat numero capita in navis; adhibete penatis
*Schiff zum Geschenk. Ihr ladet zum Mahl die Penaten der Heimat
*
et patrios epulis et quos colit hospes Acestes.
*Und mit ihnen vereint, die verehret der Gastfreund Akestes.
*
praeterea, si nona diem mortalibus almum
*Wenn den erquickenden Tag dann den Sterblichen wieder das neunte
*
65



Aurora extulerit radiisque retexerit orbem,
Frührot bringt und mit leuchtendem Strahl aufhellet den Erdkreis,

prima citae Teucris ponam certamina classis;
*Werd ich ein Schiffswettrennen zuerst ausrichten den Teukrern.
*
quique pedum cursu valet, et qui viribus audax
*Wer sich der Füße Behendigkeit rühmt, wer kühn sich durch Kraft weiß,
*
aut iaculo incedit melior levibusque sagittis,
*Wer auf den Speer sich besser versteht und die flüchtigen Pfeile,
*
seu crudo fidit pugnam committere caestu,
*Wer sich den Kampf zu bestehen getraut mit dem blutigen Cestus,
*
70



cuncti adsint meritaeque exspectent praemia palmae.
Finde sich jeder denn ein, nach Verdienst um die Palme zu werben.

ore favete omnes et cingite tempora ramis.
*Schweiget in Andacht jetzt und kränzt mit Zweigen die Schläfe."
*
Sic fatus velat materna tempora myrto.
*Sprach's und umhüllte das Haupt mit Myrten, dem Laube der Mutter;
*
hoc Helymus facit, hoc aevi maturus Acestes,
*Elymus tut, es tut der bejahrte Akestes dasselbe,
*
hoc puer Ascanius, sequitur quos cetera pubes.
*Auch Askanios, sein Kind, und die übrigen folgen dem Beispiel.
*
75



ille e concilio multis cum milibus ibat
Aus der Versammlung schritt zum Grab nun jener mit vielen

ad tumulum magna medius comitante caterva.
*Tausenden, mitten im Zug der ihn rings umgebenden Menge,
*
hic duo rite mero libans carchesia Baccho
*Goss nach Brauch auf die Erde daselbst zwei Becher des reinen
*
fundit humi, duo lacte novo, duo sanguine sacro,
*Bakchustrunks, zwei schäumender Milch, zwei heiligen Blutes,
*
purpureosque iacit flores ac talia fatur:
*Streute mit Purpurblumen das Grab und redete also:
*
80



"salve, sancte parens, iterum; salvete, recepti
"Sei mir von neuem gegrüßt, o heiliger Vater, du Asche,

nequiquam cineres animaeque umbraeque paternae.
*Die ich gerettet umsonst, du Schatten und Geist des Erzeugers;
*
non licuit finis Italos fataliaque arva
*Nicht Italien sollt' ich mit dir, die verheißenen Fluren,
*
nec tecum Ausonium, quicumque est, quaerere Thybrim."
*Nicht - wer immer es sei - den Thybris Ausoniens suchen."
*
dixerat haec, adytis cum lubricus anguis ab imis
*Also sprach er, da schlich aus den untersten Grüften, in sieben
*
85



septem ingens gyros, septena volumina traxit
Windungen schlüpfrig geballt, sich eine gewaltige Schlange,

amplexus placide tumulum lapsusque per aras,
*Schmiegte sich sanft um das Grab und umglitt die geweihten Altäre.
*
caeruleae cui terga notae maculosus et auro
*Bläulich war ihr der Rücken gefleckt, und die Schuppen umglühte
*
squamam incendebat fulgor, ceu nubibus arcus
*Golden ein schillernder Glanz, wie gegen die Sonn' in den Wolken
*
mille iacit varios adverso sole colores.
*Iris' Bogen erstrahlt mit tausend verschiedenen Farben.
*
90



obstipuit visu Aeneas. ille agmine longo
Staunen ergreift den Aineias; doch sie, in schlängelndem Zuge,

tandem inter pateras et levia pocula serpens
*Schlüpft an den Schalen herum und zwischen den funkelnden Bechern,
*
libavitque dapes rursusque innoxius imo
*Kostet vom heiligen Mahl und birgt unschädlich sich wieder
*
successit tumulo et depasta altaria liquit.
*Tief in der untersten Gruft und verlässt die benaschten Altäre.
*
hoc magis inceptos genitori instaurat honores,
*Um so froher erneut das begonnene Fest er dem Vater -
*
95



incertus geniumne loci famulumne parentis
Mocht' es ein Diener nun sein des Verstorbenen oder des Ortes

esse putet; caedit binas de more bidentis
*Schutzgeist -, schlachtet nach Brauch ein Paar zweijährige Lämmer,
*
totque sues, totidem nigrantis terga iuvencos,
*Schweine – die selbige Zahl - und zwei schwarzrückige Farren,
*
vinaque fundebat pateris animamque vocabat
*Bringt Trankopfer von Wein und ruft des erhabnen Anchises
*
Anchisae magni manisque Acheronte remissos.
*Geist herbei, die von Acherons Strom entlassenen Manen.
*
100



nec non et socii, quae cuique est copia, laeti
Froh auch weihn die Gefährten, was jeder vermag, an Geschenken;

dona ferunt, onerant aras mactantque iuvencos;
*Hoch auf werden Altäre getürmt und Stiere geschlachtet.
*
ordine aëna locant alii fusique per herbam
*Andere stellen die Kessel in Reihn, und, im Grase gelagert,
*
subiciunt veribus prunas et viscera torrent.
*Häufen sie Kohlen umher und rösten am Spieß das Gekröse.
*
Exspectata dies aderat nonamque serena
*Und nun kam der erwartete Tag. Schon führte das neunte
*
105



Auroram Phaethontis equi iam luce vehebant,
Frührot Phaethons Rosse herauf mit heiterem Lichte.

famaque finitimos et clari nomen Acestae
*Sämtliche Nachbarn lockt das Gerücht und Akestes' berühmter
*
excierat; laeto complerant litora coetu
*Name herbei; sie erfüllen den Strand in froher Versammlung,
*
visuri Aeneadas, pars et certare parati.
*Um die Troianer zu sehn, teils auch sich im Kampf zu versuchen.
*
munera principio ante oculos circoque locantur
*Erstlich stellt die Geschenke man aus inmitten der Rennbahn:
*
110



in medio, sacri tripodes viridesque coronae
Heilig Gerät, Dreifüße, die Kronen von Laub und die Palmen,

et palmae pretium victoribus, armaque et ostro
*Die zum Preis man den Siegern bestimmt, nebst Waffen und Kleidern,
*
perfusae vestes, argenti aurique talenta;
*Purpurgefärbt: ein Zentner an Gold und ein Zentner an Silber.
*
et tuba commissos medio canit aggere ludos.
*Und nun ruft von der Mitte des Walls zu den Spielen die Tuba.
*
Prima pares ineunt gravibus certamina remis
*Vier Fahrzeuge zuerst, gleich tüchtig, mit wuchtigen Rudern
*
115



quattuor ex omni delectae classe carinae.
Heben den Wettkampf an - aus sämtlichen Schiffen erlesen.

velocem Mnestheus agit acri remige Pristim,
*Mnestheus führet den hurtigen "Hai" mit gewandter Bemannung -
*
mox Italus Mnestheus, genus a quo nomine Memmi,
*Mnestheus, der Italer bald, von welchem die Memmier stammen;
*
ingentemque Gyas ingenti mole Chimaeram,
*Gyas den riesigen Bau des Schiffskolosses "Chimaira",
*
urbis opus, triplici pubes quam Dardana versu
*Die wie ein Stadtwall ragt; es treibt sie die Dardanermannschaft,
*
120



impellunt, terno consurgunt ordine remi;
Dreifach gereiht, da in drei Stockwerken die Ruder sich heben.

Sergestusque, domus tenet a quo Sergia nomen,
*Aber Sergestus, nach welchem noch heut sich der Sergier Haus nennt,
*
Centauro invehitur magna, Scyllaque Cloanthus
*Fährt auf dem großen "Kentaur", auf der bläulichen "Skylla" Kloanthus;
*
caerulea, genus unde tibi, Romane Cluenti.
*Von ihm leitet in Rom ihr Cluentier euer Geschlecht ab.
*
Est procul in pelago saxum spumantia contra
*Fern im Meer ist ein Fels genüber der schäumenden Küste,
*
125



litora, quod tumidis summersum tunditur olim
Der sonst untergetaucht von den schwellenden Wogen gepeitscht wird,

fluctibus, hiberni condunt ubi sidera Cauri;
*Wenn im Winter der Nord mit Gewölk umhüllt die Gestirne.
*
tranquillo silet immotaque attollitur unda
*Still bei ruhigem Meer und hoch aus dem glatten Gewässer
*
campus et apricis statio gratissima mergis.
*Hebt sich die Fläche, wo, gern sich sonnend, die Taucher verweilen.
*
hic viridem Aeneas frondenti ex ilice metam
*Vater Aineias steckt als Ziel für die Schiffer des Eichbaums
*
130



constituit signum nautis pater, unde reverti
Grün umlaubtes Gezweig hier aus, zum Zeichen, von wo sie

scirent et longos ubi circumflectere cursus.
*Wendeten und um den Fels in weiter Umkreisung sich schwängen.
*
tum loca sorte legunt ipsique in puppibus auro
*Und nun werden die Plätze verlost. Auf den Hinterverdecken
*
ductores longe effulgent ostroque decori;
*Und in Gold und Purpur geschmückt weit strahlend die Führer;
*
cetera populea velatur fronde iuventus
*Aber das übrige Volk, umkränzt mit dem Laube der Pappel,
*
135



nudatosque umeros oleo perfusa nitescit.
Glänzt, mit triefendem Öle gesalbt, um die nackenden Schultern.

considunt transtris, intentaque bracchia remis;
*Dann auf den Bänken gereiht und den Arm ausstreckend zum Ruder,
*
intenti exspectant signum, exsultantiaque haurit
*Harren sie auf das Signal voll Spannung. Ein pochendes Bangen
*
corda pavor pulsans laudumque arrecta cupido.
*Fesselt das hüpfende Herz und hochaufstrebender Ehrgeiz.
*
inde ubi clara dedit sonitum tuba, finibus omnes,
*Dann, wie schmetternd die Tuba ertönt, da - sonder Verzug - stürzt
*
140



haud mora, prosiluere suis; ferit aethera clamor
Jeder aus seinem Bezirk; es dröhnt seemännischer Wettruf

nauticus, adductis spumant freta versa lacertis.
*Laut durch die Luft, und die Flut schäumt auf vom Rucke der Arme.
*
infindunt pariter sulcos, totumque dehiscit
*Reihweis schneiden die Furchen sie ein, und durchwühlt von den Rudern,
*
convulsum remis rostrisque tridentibus aequor.
*Von dreizackigen Schnäbeln durchwühlt, gähnt rings das Gewässer.
*
non tam praecipites biiugo certamine campum
*So nicht stürzen, den Schranken entrafft, durch die Ebne die Wagen
*
145



corripuere ruuntque effusi carcere currus,
Sausend im Fluge dahin im Kampfe der Doppelgespanne;

nec sic immissis aurigae undantia lora
*So nicht schüttelt mit Macht die geschwungenen Zügel den raschen
*
concussere iugis pronique in verbera pendent.
*Rossen der Lenker ums Haupt und beugt sich zum Hieb mit dem Leib vor.
*
tum plausu fremituque virum studiisque faventum
*Und nun hallt von Geklatsch und Lärm und ermunterndem Zuruf
*
consonat omne nemus, vocemque inclusa volutant
*Alles Gewäld umher. Es wälzt sich der Schall an des Ufers
*
150



litora, pulsati colles clamore resultant.
Wandungen hin und donnert zurück von den dröhnenden Hügeln.

Effugit ante alios primisque elabitur undis
*Aber den andern enteilt und gleitet zuvor auf den Wogen
*
turbam inter fremitumque Gyas; quem deinde Cloanthus
*Gyas, vom lärmenden Schwärm umjauchzt; es folgt ihm Kloanthus,
*
consequitur, melior remis, sed pondere pinus
*Besser mit Rudern versehn; doch hemmt ihn der mächtigen Fichte
*
tarda tenet. post hos aequo discrimine Pristis
*Zögernde Last. Nach diesen, getrennt durch gleiche Entfernung,
*
155



Centaurusque locum tendunt superare priorem;
Suchen der "Hai" und "Kentaur" sich den Vorrang streitig zu machen;

et nunc Pristis habet, nunc victam praeterit ingens
*Und jetzt hat ihn der "Hai", jetzt rudert der große "Kentaur" ihm
*
Centaurus, nunc una ambae iunctisque feruntur
*Siegreich wieder vorbei, jetzt schweben sie nebeneinander
*
frontibus et longa sulcant vada salsa carina.
*Bug an Bug, weithin durchfurchen die Kiele die Salzflut.
*
iamque propinquabant scopulo metamque tenebant,
*Und schon waren dem Fels sie genaht und berührten das Ziel schon,
*
160



cum princeps medioque Gyas in gurgite victor
Als in der Mitte des Meers, siegreich als vorderster fahrend,

rectorem navis compellat voce Menoeten:
*Gyas den Steurer des Schiffs, Menoites, also bedeutet:
*
"quo tantum mihi dexter abis? huc derige cursum;
*"Wozu gehst du so weit rechts ab? Hier richte den Lauf her!
*
litus ama et laeva stringat sine palmula cautes;
*Halte den Strand; lass links am Geklipp hinstreifen das Ruder;
*
altum alii teneant." dixit; sed caeca Menoetes
*Such ein andrer die Höh!" Er sprach's, doch Menoites, vor blinden
*
165



saxa timens proram pelagi detorquet ad undas.
Riffen besorgt, dreht grade den Bug in die Wogen des Meeres.

"quo diversus abis?" iterum "pete saxa, Menoete!"
*Laut ruft Gyas aufs neu: "Wohin dort ab, o Menoites?
*
cum clamore Gyas revocabat, et ecce Cloanthum
*Richt auf die Klippen den Lauf!" - und sieh, er erblickt den Kloanthus
*
respicit instantem tergo et propiora tenentem.
*Hinter sich, der ihm den Rücken bedroht und den näheren Weg hält.
*
ille inter navemque Gyae scopulosque sonantis
*Jener, der zwischen des Gyas Schiff und den tosenden Felsen
*
170



radit iter laevum interior subitoque priorem
Links hinstreift in engerem Kreis, fährt jetzt an dem Sieger

praeterit et metis tenet aequora tuta relictis.
*Plötzlich vorbei und über das Ziel in das sichere Wasser.
*
tum vero exarsit iuveni dolor ossibus ingens
*Aber unendlicher Schmerz durchflammt die Gebeine des Jünglings,
*
nec lacrimis caruere genae, segnemque Menoeten
*Tränen besprühn ihm die Wangen sogar; er vergisst, was der Anstand,
*
oblitus decorisque sui sociumque salutis
*Was ihm das Heil der Gefährten gebietet: den trägen Menoites
*
175



in mare praecipitem puppi deturbat ab alta;
Stößt er ins Meer kopfüber vom ragenden Hinterverdecke.

ipse gubernaclo rector subit, ipse magister
*Als Schiffsmeister sodann setzt selber er sich an das Steuer,
*
hortaturque viros clavumque ad litora torquet.
*Muntert die Mannschaft auf und wendet das Ruder zum Strand hin.
*
at gravis ut fundo vix tandem redditus imo est
*Aber Menoites, bejahrt und schwer durch die triefenden Kleider,
*
iam senior madidaque fluens in veste Menoetes
*Wie er mit Not zuletzt aus der untersten Tiefe herauftaucht,
*
180



summa petit scopuli siccaque in rupe resedit.
Klimmt auf die Höhe des Riffs und setzt auf den trockenen Fels sich.

illum et labentem Teucri et risere natantem
*Hatten die Teukrer gelacht, wie er fiel, und gelacht, wie er fortschwamm,
*
et salsos rident revomentem pectore fluctus.
*Lachen sie jetzt, wie tief aus der Brust er die salzige Flut speit.
*
Hic laeta extremis spes est accensa duobus,
*Fröhliche Hoffnung strahlt nun beiden, Sergestus und Mnestheus
*
Sergesto Mnestheique, Gyan superare morantem.
*(Welche die letzten bis jetzt), zu besiegen den zögernden Gyas.
*
185



Sergestus capit ante locum scopuloque propinquat,
Und Sergestus eilt vor und nähert bereits sich der Klippe,

nec tota tamen ille prior praeeunte carina;
*Doch nicht ganz voran mit der völligen Länge des Kieles,
*
parte prior, partim rostro premit aemula Pristis.
*Teilweis nur, da die Spitze des "Hais" wetteifernd sich anlegt.
*
at media socios incedens nave per ipsos
*Aber die Mitte des Schiffs und die Reihn der Genossen durchschreitet
*
hortatur Mnestheus: "nunc, nunc insurgite remis,
*Mnestheus nun und mahnt: "Jetzt stemmt euch, jetzt auf die Ruder,
*
190



Hectorei socii, Troiae quos sorte suprema
Hektors befreundete Schar, die bei Troias letztem Geschicke

delegi comites; nunc illas promite viris,
*Ich zu Gefährten erwählt; jetzt zeigt von neuem die Kräfte,
*
nunc animos, quibus in Gaetulis Syrtibus usi
*Jetzo den Mut, den ihr einst in Gätuliens Syrten erprobt habt,
*
Ionioque mari Maleaeque sequacibus undis.
*In dem Ionischen Meer und Maleas Wogengedränge.
*
non iam prima peto Mnestheus neque vincere certo
*Streb' ich doch nicht nach dem Sieg, noch verlang' ich den ersten der Preise -
*
195



- quamquam o! - sed superent quibus hoc, Neptune, dedisti -;
Wenn schon - ha! - doch trag ihn davon, wem Neptun ihn verliehen!

extremos pudeat rediisse: hoc vincite, cives,
*Schämt euch nur als die letzten zurückzukehren; den einen
*
et prohibete nefas." olli certamine summo
*Sieg, Mitbürger, erkämpft und verhindert die Schmach l" Und sie werfen
*
procumbunt: vastis tremit ictibus aerea puppis
*Heiß wetteifernd sich vor, dass von heftigen Schlägen der ehrne
*
subtrahiturque solum, tum creber anhelitus artus
*Schiffsbauch dröhnt, dass der Grund fortfliegt, und Ächzen die Glieder
*
200



aridaque ora quatit, sudor fluit undique rivis.
Schütternd durchzuckt und den dörrenden Mund, dass in Bächen der Schweiß fließt.

attulit ipse viris optatum casus honorem:
*Zufall brachte den Sieg zuletzt, den die Männer ersehnten.
*
namque furens animi dum proram ad saxa suburget
*Denn da rasenden Muts an die Felsen Sergestus den Vorbug
*
interior spatioque subit Sergestus iniquo,
*Drängt und im inneren Kreis den gefährlichsten Raum sich zum Weg nimmt,
*
infelix saxis in procurrentibus haesit.
*Fährt unglücklich er fest auf den Felsausläufen der Klippe.
*
205



concussae cautes et acuto in murice remi
Heftig schüttert das Riff, es zerkracht auf der scharfen Koralle

obnixi crepuere inlisaque prora pependit.
*Ruder an Ruder im Stoß; leck sitzt auf dem Grunde der Schiffsbug.
*
consurgunt nautae et magno clamore morantur
*Sämtliches Volk springt auf mit fruchtlos tobendem Lärmen;
*
ferratasque trudes et acuta cuspide contos
*Stangen, mit Spitzen bewehrt, und eisenbeschlagene Piken
*
expediunt fractosque legunt in gurgite remos.
*Holen sie vor und sammeln im Meer die zerbrochenen Ruder.
*
210



at laetus Mnestheus successuque acrior ipso
Mnestheus, froh des Erfolgs und mutiger, fleht zu den Winden

agmine remorum celeri ventisque vocatis
*Jetzo empor und eilt mit beschleunigtem Schlage der Ruder
*
prona petit maria et pelago decurrit aperto.
*Fort zur ebenen See und läuft in das offene Meer ein.
*
qualis spelunca subito commota columba,
*So wie plötzlich verscheucht aus verborgener Höhle die Taube,
*
cui domus et dulces latebroso in pumice nidi,
*Die ihr Haus und freundliches Nest im durchlöcherten Tuff baut,
*
215



fertur in arva volans plausumque exterrita pennis
Fort auf die Felder sich schwingt und erschreckt ihr Dach mit gewaltig

dat tecto ingentem, mox aëre lapsa quieto
*Klatschendem Fittich umkreist, doch bald der beruhigten Lüfte
*
radit iter liquidum celeris neque commovet alas:
*Flüssige Bahn durchschwebt, still gleitend auf flüchtigen Schwingen:
*
sic Mnestheus, sic ipsa fuga secat ultima Pristis
*So durchschneidet das äußerste Meer in fliegender Eile
*
aequora, sic illam fert impetus ipse volantem.
*Mnestheus jetzt mit dem "Hai", so treibt im Flug ihn der Anlauf.
*
220



et primum in scopulo luctantem deserit alto
Hinter sich lässt er Sergestus zuerst, der im hohen Geklipp noch

Sergestum brevibusque vadis frustraque vocantem
*Und auf der Bank Untiefen sich müht und, vergeblich um Hilfe
*
auxilia et fractis discentem currere remis.
*Rufend, den Lauf zu erneuern versucht mit zerbrochenen Rudern.
*
inde Gyan ipsamque ingenti mole Chimaeram
*Dann holt Gyas sogar er ein und seiner "Chimaira"
*
consequitur; cedit, quoniam spoliata magistro est.
*Riesigen Bau; sie weicht, da der richtige Lenker ihr fehlte.
*
225



solus iamque ipso superest in fine Cloanthus,
Und schon dicht am Ziel ist allein Kloanthus noch übrig.

quem petit et summis adnixus viribus urget.
*Auf ihn steuert er jetzt mit Macht, mit der äußersten Kraft los.
*
Tum vero ingeminat clamor cunctique sequentem
*Doppelt erhebt sich der Lärm; man spornt mit eifrigem Zuruf
*
instigant studiis, resonatque fragoribus aether.
*Rings den Verfolgenden an; es hallt vom Getöse der Aither.
*
hi proprium decus et partum indignantur honorem
*Jenen empört es das Herz, den erworbenen Sieg und die Ehre
*
230



ni teneant, vitamque volunt pro laude pacisci;
Aufzugeben; sie wollen den Ruhm mit dem Leben erkaufen.

hos successus alit: possunt, quia posse videntur.
*Diese, belebt vom Erfolg, sind stark, weil stark sie erscheinen.
*
et fors aequatis cepissent praemia rostris,
*Möglich, dass beide zugleich sich des Wettlaufs Preis noch errängen,
*
ni palmas ponto tendens utrasque Cloanthus
*Hätte Kloanthus nicht, zum Meer ausbreitend die Arme,
*
fudissetque preces divosque in vota vocasset:
*So der Unsterblichen Schar mit Gebet und Gelübden gerufen:
*
235



"di, quibus imperium est pelagi, quorum aequora curro,
"Götter, Beherrscher des Meers, euch, deren Gebiet ich durchfahre,

vobis laetus ego hoc candentem in litore taurum
*Will ich den glänzendsten Stier vor euren Altar am Gestade
*
constituam ante aras voti reus, extaque salsos
*Froh hinstellen als schuldigen Dank; ich will das Gekröse
*
proiciam in fluctus et vina liquentia fundam."
*Streun in die salzige Flut und Wein ausgießen zur Spende."
*
dixit, eumque imis sub fluctibus audiit omnis
*Sprach's, und tief bis zur untersten Flut hin hörten ihn alle
*
240



Nereidum Phorcique chorus Panopeaque virgo,
Nereustöchter, des Phorkys' Chor, Panopea, die Jungfrau;

et pater ipse manu magna Portunus euntem
*Vater Portunus selbst, er schob mit gewaltiger Hand ihn
*
impulit: illa Noto citius volucrique sagitta
*Vorwärts; schneller entflieht der geflügelte Pfeil und der Süd nicht,
*
ad terram fugit et portu se condidit alto.
*Als er zum Land hinflog und sich barg im umragenden Hafen.
*
tum satus Anchisa cunctis ex more vocatis
*Aber Anchises' Sohn, nach Gebrauch erst alle versammelnd,
*
245



victorem magna praeconis voce Cloanthum
Gibt durch des Herolds mächtigen Ruf den Kloanthus als Sieger

declarat viridique advelat tempora lauro,
*Jetzo kund, umhüllt ihm die Schläfe mit grünendem Lorbeer,
*
muneraque in navis ternos optare iuvencos
*Lässt ein jegliches Schiff zum Geschenk drei Farren sich wählen
*
vinaque et argenti magnum dat ferre talentum.
*Und gibt Wein und Silber, ein volles Talent für ein jedes,
*
ipsis praecipuos ductoribus addit honores:
*Aber den Führern verehrt er zudem noch besondere Gaben.
*
250



victori chlamydem auratam, quam plurima circum
Erstlich ein goldnes Gewand für den Sieger; maiandrisch gekrümmt lief

purpura maeandro duplici Meliboea cucurrit,
*Breit ringsum ein doppelter Streif meliboiischen Purpurs.
*
intextusque puer frondosa regius Ida
*Drin ist der fürstliche Knabe gewirkt, der auf waldigem Ida
*
velocis iaculo cervos cursuque fatigat
*Flüchtige Hirsche verfolgt und im Lauf abhetzt mit dem Wurfspieß,
*
acer, anhelanti similis, quem praepes ab Ida
*Eifrig - man sieht, wie er keucht - ihn entrafft in den Aither vom Ida
*
255



sublimem pedibus rapuit Iovis armiger uncis;
Zeus' Blitzträger, der stürmische Aar, mit kralligen Klauen.

longaevi palmas nequiquam ad sidera tendunt
*Fruchtlos strecken die Händ' empor zu den Sternen die greisen
*
custodes, saevitque canum latratus in auras.
*Hüter; es rast in die Luft das Gebell der erbitterten Meute.
*
at qui deinde locum tenuit virtute secundum,
*Ihm, der durch Mut und Geschick sodann als Zweiter zum Ziel kam,
*
levibus huic hamis consertam auroque trilicem
*Gab er den Panzer zum Preis, den, aus dreidrähtigen blanken
*
260



loricam, quam Demoleo detraxerat ipse
Maschen von Golde gewirkt, er einst dem Demoleos siegreich

victor apud rapidum Simoenta sub Ilio alto,
*Selbst abzog vor Ilions Wall an des Simois Wirbeln.
*
donat habere, viro decus et tutamen in armis.
*Diesen verehrt' er dem Mann als Zier und Schutz in der Feldschlacht.
*
vix illam famuli Phegeus Sagarisque ferebant
*Kaum dass untergestemmt mit den Schultern das wuchtige Netzwerk
*
multiplicem conixi umeris; indutus at olim
*Phegeus und Sagaris jetzt fortschleppten, die Knechte, das laufend
*
265



Demoleos cursu palantis Troas agebat.
Einst Demoleos trug, wenn die flüchtigen Troer er jagte.

tertia dona facit geminos ex aere lebetas
*Ferner bestimmt' er zum dritten Geschenk drei eherne Kessel;
*
cymbiaque argento perfecta atque aspera signis.
*Schalen, durchaus von Silber, dazu mit erhabenem Bildwerk.
*
iamque adeo donati omnes opibusque superbi
*Und schon gingen sie, sämtlich beschenkt und stolz auf die Schätze,
*
puniceis ibant evincti tempora taenis,
*Festlich die Schläfe bekränzt mit purpurfarbenen Binden,
*
270



cum saevo e scopulo multa vix arte revulsus
Als mit allerlei Kunst Sergestus sich kaum von dem grausen

amissis remis atque ordine debilis uno
*Fels losriss und, der Ruder beraubt, arg schwankend, an einem
*
inrisam sine honore ratem Sergestus agebat.
*Borde gelähmt, hertrieb auf entehrtem, verspottetem Fahrzeug.
*
qualis saepe viae deprensus in aggere serpens,
*So wie die Schlange gequetscht auf dem Damme des Wegs, wenn das ehrne
*
aerea quem obliquum rota transiit aut gravis ictu
*Rad quer über den Leib ihr fortging oder des Wandrers
*
275



seminecem liquit saxo lacerumque viator;
Heftiger Schlag halbtot und verstümmelt sie auf dem Gestein ließ;

nequiquam longos fugiens dat corpore tortus
*Fruchtlos dreht sie den Leib im Fliehn und windet und dehnt sich;
*
parte ferox ardensque oculis et sibila colla
*Wild ist ihr vorderer Teil; mit glühenden Augen erhebt sie
*
arduus attollens; pars vulnere clauda retentat
*Hoch noch den zischenden Schlund; doch der Schweif hält, lahm durch die Wunde,
*
nexantem nodis seque in sua membra plicantem:
*Immer sie auf, wie die Knoten sie schürzt und den Leib um sich selbst rollt:
*
280



tali remigio navis se tarda movebat;
Also rückte das Schiff träg vor mit dem Rudergeräte;

vela facit tamen et velis subit ostia plenis.
*Aber es segelt und läuft in die Bucht mit blähendem Bausch ein.
*
Sergestum Aeneas promisso munere donat
*Und Aineias verehrt dem Sergestus verheißene Gabe,
*
servatam ob navem laetus sociosque reductos.
*Froh des erhaltenen Schiffs und der wiedergebrachten Gefährten.
*
olli serva datur operum haud ignara Minervae,
*Pholoe wird ihm, die Magd, zuteil, wohl kundig in Pallas'
*
285



Cressa genus, Pholoe, geminique sub ubere nati.
Werken, von kretischem Stamm, mit Zwillingssöhnen am Busen.

Hoc pius Aeneas misso certamine tendit
*Dies war das Ende des Kampfs. Jetzt wandte der fromme Aineias
*
gramineum in campum, quem collibus undique curvis
*Sich zu dem rasigen Grund, den ein Kreis von bewaldeten Hügeln
*
cingebant silvae, mediaque in valle theatri
*Rings einschloss; in dem Tal, von den Halden umhegt, war die Rennbahn.
*
circus erat; quo se multis cum milibus heros
*Dorthin ging zur Versammlung der Held in Begleitung von vielen
*
290



consessu medium tulit exstructoque resedit.
Tausenden, trat in den Kreis, nahm Platz auf erhabenem Thronsitz.

hic, qui forte velint rapido contendere cursu,
*Hierhin lädt er ein, wer immer zum stürmischen Wettlauf
*
invitat pretiis animos, et praemia ponit.
*Neigung verspürt, und reizt durch Gewinn und Preise den Mut an.
*
undique conveniunt Teucri mixtique Sicani,
*Ringsher kommen die Teukrer herbei, vermischt mit Sikanern;
*
Nisus et Euryalus primi,
*Nisus nahet zuerst und Euryalus.
*
295



Euryalus forma insignis viridique iuventa,
Wie Euryalus selbst durch Gestalt und blühende Jugend,

Nisus amore pio pueri; quos deinde secutus
*So tat Nisus durch züchtige Glut sich hervor für den Knaben.
*
regius egregia Priami de stirpe Diores;
*Dann folgt, Priamos' Königsgeschlecht entsprossen, Diores;
*
hunc Salius simul et Patron, quorum alter Acarnan,
*Patron und Salius dann, akarnanischen Stammes der eine,
*
alter ab Arcadio Tegeaeae sanguine gentis;
*Dieser arkadischen Bluts, tegeäischen Ahnen entsprossen.
*
300



tum duo Trinacrii iuvenes, Helymus Panopesque
Elymus folgt und Panopes dann, Trinakrier beide,

adsueti silvis, comites senioris Acestae;
*Früh an die Wälder gewöhnt, des bejahrten Akestes Gefährten,
*
multi praeterea, quos fama obscura recondit.
*Und noch viele danach, die mit Dunkel verhüllet die Sage.
*
Aeneas quibus in mediis sic deinde locutus:
*Drauf in der Mitte der Schar sprach also Vater Aineias:
*
"accipite haec animis laetasque advertite mentes.
*"Nehmt dies auf in den Geist und merkt es mit frohem Gemüte:
*
305



nemo ex hoc numero mihi non donatus abibit.
Niemand hier aus der Schar wird leer an Gaben davongehn.

Cnosia bina dabo levato lucida ferro
*Jeder erhält von glänzendem Stahl zwei gnosische Pfeile,
*
spicula caelatamque argento ferre bipennem;
*Jeder ein Beil zum Geschenk mit erhabener Silberverzierung,
*
omnibus hic erit unus honos. tres praemia primi
*Dieses Geschenk ist für sämtliche gleich; doch gewinnen die ersten
*
accipient flavaque caput nectentur oliva.
*Drei noch Preise und kränzen ihr Haupt mit falben Oliven.
*
310



primus equum phaleris insignem victor habeto;
Ihm, der als erster sich zeigt, ist ein Ross mit prächtigem Zaumwerk,

alter Amazoniam pharetram plenamque sagittis
*Ein amazonischer Köcher mit Thrakergeschoss ist dem zweiten
*
Threiciis, lato quam circum amplectitur auro
*Sieger bestimmt, dazu ein breit umliegender goldner
*
balteus et tereti subnectit fibula gemma;
*Gürtel: aus Edelgestein ist das rundliche Schloss, das ihn zuhakt.
*
tertius Argolica hac galea contentus abito."
*Dieser argolische Helm sei genügender Lohn für den Dritten."
*
315



Haec ubi dicta, locum capiunt signoque repente
So Aineias. Sie stellen sich auf. Als das Zeichen gegeben,

corripiunt spatia audito limenque relinquunt,
*Stürzen die Bahn sie plötzlich hinan und verlassen die Schranken,
*
effusi nimbo similes. simul ultima signant,
*Wie Platzregen vom Himmel sich gießt, und fassen das Ziel scharf.
*
primus abit longeque ante omnia corpora Nisus
*Gleich aus der übrigen Schar hervor weithin durch die Bahn schießt
*
emicat et ventis et fulminis ocior alis;
*Nisus, behenderen Flugs als die Winde und Schwingen des Blitzes.
*
320



proximus huic, longo sed proximus intervallo,
Nächst ihm, aber doch nur in beträchtlichem Abstand nächst ihm,

insequitur Salius; spatio post deinde relicto
*Zeigt sich Salius; wieder ein Raum, dann folgt als der dritte
*
tertius Euryalus;
*Läufer Euryalus ihm.
*
Euryalumque Helymus sequitur; quo deinde sub ipso
*Nach Euryalus gleich kommt Elymus. Siehe, da fliegt schon,
*
ecce volat calcemque terit iam calce Diores
*Ferse an Ferse gedrängt und über die Schultern ihm ragend,
*
325



incumbens umero, spatia et si plura supersint
Hurtig Diores heran; wenn weiter sich dehnte die Rennbahn,

transeat elapsus prior ambiguumque relinquat.
*Käm' er vielleicht noch zuvor, wo nicht, gleichzeitig zum Ziele.
*
iamque fere spatio extremo fessique sub ipsam
*Und schon hatten erschöpft auf der äußersten Bahn sie dem Ende
*
finem adventabant, levi cum sanguine Nisus
*Fast sich genaht, da glitt unglücklich in schlüpfrigem Blute
*
labitur infelix, caesis ut forte iuvencis
*Nisus aus, weil just von geschlachteten Rindern der grüne
*
330



fusus humum viridisque super madefecerat herbas.
Rasen noch feucht und unter dem Gras auch der Boden durchnässt war.

hic iuvenis iam victor ovans vestigia presso
*Hier hielt, jubelnd bereits im Sieg, die schwankenden Schritte
*
haud tenuit titubata solo, sed pronus in ipso
*Nicht am Boden der Jüngling fest; vornüber geneigt stürzt
*
concidit immundoque fimo sacroque cruore.
*Grad in das heilige Blut er hin und den schmutzigen Unrat.
*
non tamen Euryali, non ille oblitus amorum:
*Doch des Euryalus nicht noch der Liebe zum Jüngling vergessend,
*
335



nam sese opposuit Salio per lubrica surgens;
Stellt er dem Salius sich, aus dem Schlamm aufstehend, entgegen,

ille autem spissa iacuit revolutus harena,
*So dass jener im klumpenden Sand hinstürzend sich wälzte.
*
emicat Euryalus et munere victor amici
*Und Euryalus schießt, durch den Freund zum Sieg und zum ersten
*
prima tenet, plausuque volat fremituque secundo.
*Platze verholfen, voran bei Geklatsch und ermunterndem Zuruf.
*
post Helymus subit et nunc tertia palma Diores.
*Elymus folgt ihm zunächst und als dritter Gekrönter Diores.
*
340



hic totum caveae consessum ingentis et ora
Doch nun füllt ringsum der Versammlung gewaltige Räume

prima patrum magnis Salius clamoribus implet,
*Salius laut mit Geschrei und die vordersten Reihen der Väter;
*
ereptumque dolo reddi sibi poscit honorem.
*Eifrig verlangt er das Ehrengeschenk, das durch List ihm entrissen.
*
tutatur favor Euryalum lacrimaeque decorae,
*Doch den Euryalus schützet die Gunst und des Weinenden Anmut
*
gratior et pulchro veniens in corpore virtus.
*Und die in schöner Gestalt einnehmender wirkende Leistung.
*
345



adiuvat et magna proclamat voce Diores,
Auch Diores stehet ihm bei mit gewaltiger Stimme,

qui subiit palmae frustraque ad praemia venit
*Der in den Sieg nachrückt und vergeblich jetzt zu dem letzten
*
ultima, si primi Salio reddentur honores.
*Preis antritt, wenn Salius noch als erster gekrönt wird.
*
tum pater Aeneas "vestra" inquit "munera vobis
*Vater Aineias sprach: "Es bleiben euch, Jünglinge, eure
*
certa manent, pueri et palmam movet ordine nemo;
*Gaben gewiss, und niemand rückt an der Folge der Palmen.
*
350



me liceat casus miserari insontis amici."
Mir sei Erbarmen erlaubt, wenn ein Freund unschuldig zu Fall kam."

sic fatus tergum Gaetuli immane leonis
*Sprach's, und das riesige Fell von einem gätulischen Löwen
*
dat Salio villis onerosum atque unguibus aureis.
*Gab er dem Salius, schwer von Zotten und goldenen Klauen.
*
hic Nisus "si tanta" inquit "sunt praemia victis,
*Nisus darauf: "Wird solch ein Preis zuteil den Besiegten,
*
et te lapsorum miseret, quae munera Niso
*Und tun so die Gefallnen dir leid, mit welchem Geschenke
*
355



digna dabis, primam merui qui laude coronam
Ehrst du den Nisus, der heut sich den ersten der Kränze verdiente,

ni me, quae Salium, fortuna inimica tulisset?"
*Hätt' ihn dasselbe Geschick nicht ereilt, das den Salius fällte?"
*
et simul his dictis faciem ostentabat et udo
*Also sprach er und zeigte dabei sein Gesicht und die Glieder,
*
turpia membra fimo. risit pater optimus olli
*Schmutzig von triefendem Mist. Es lachte der gütige Vater,
*
et clipeum efferri iussit, Didymaonis artes,
*Und er befahl einen Schild, ein Werk Didymaons, zu holen,
*
360



Neptuni sacro Danais de poste refixum.
Den er den Griechen geraubt von Neptunus' heiligen Pfosten.

hoc iuvenem egregium praestanti munere donat.
*Mit dem reichen Geschenk erfreut er den trefflichen Jüngling.
*
Post, ubi confecti cursus et dona peregit,
*Da nun beendet der Lauf und er alle Geschenke verteilt hat,
*
"nunc, si cui virtus animusque in pectore praesens,
*Ruft er: "Wohlan, wem Mut und Kraft jetzt wohnt in dem Busen,
*
adsit et evinctis attollat bracchia palmis":
*Tret er her und erheb er den Arm mit umwundenen Händen."
*
365



sic ait, et geminum pugnae proponit honorem,
Spricht's und setzt für den Kampf ein doppeltes Ehrengeschenk aus,

victori velatum auro vittisque iuvencum,
*Stattlich mit Binden und Gold umkränzt, ein Rind für den Sieger,
*
ensem atque insignem galeam solacia victo.
*Und ein vortreffliches Schwert nebst Helm als Trost dem Besiegten.
*
nec mora; continuo vastis cum viribus effert
*Ohne Verzug zeigt seine Gestalt voll riesiger Stärke
*
ora Dares magnoque virum se murmure tollit,
*Dares und reckt sich empor mit lautem Gemurmel der Männer.
*
370



solus qui Paridem solitus contendere contra,
Denn er pflegte allein sich im Kampf mit Paris zu messen,

idemque ad tumulum quo maximus occubat Hector
*Er auch schlug an dem Grab, wo Hektor, der Herrliche, ruhet,
*
victorem Buten immani corpore, qui se
*Butes zu Boden, der, siegreich stets und gewaltigen Wuchses,
*
Bebrycia veniens Amyci de gente ferebat,
*Aus Bebrykergeschlecht von Amykos' Stamme sich herschrieb -
*
perculit et fulva moribundum extendit harena.
*Schlug ihn und streckt' als Sterbenden ihn in den gelblichen Sand hin.
*
375



talis prima Dares caput altum in proelia tollit,
So hob Dares sein Haupt hoch auf zum Beginne des Kampfes,

ostenditque umeros latos alternaque iactat
*Zeigte den Nacken, so breit wie er war, und reckte die Arme
*
bracchia protendens et verberat ictibus auras.
*Wechselnd empor und zerteilte die Luft mit gewaltigen Hieben.
*
quaeritur huic alius; nec quisquam ex agmine tanto
*Wer ist der Gegner für ihn? Kein einziger wagt aus dem ganzen
*
audet adire virum manibusque inducere caestus.
*Schwarme dem Mann sich zu nahn und die Faust mit Riemen zu gürten.
*
380



ergo alacris cunctosque putans excedere palma
Fröhlichen Sinnes darum, dass sich alle der Palme bescheiden,

Aeneae stetit ante pedes, nec plura moratus
*Tritt zu Aineias' Füßen er hin, und ohne zu zaudern,
*
tum laeva taurum cornu tenet atque ita fatur:
*Fasst mit der Linken den Stier er beim Hörn und redet die Worte:
*
"nate dea, si nemo audet se credere pugnae,
*"Göttingeborner, wenn keiner es wagt, sich dem Kampf zu vertrauen,
*
quae finis standi? quo me decet usque teneri?
*Wozu stehen wir hier? Wie lange denn soll ich noch warten?
*
385



ducere dona iube." cuncti simul ore fremebant
Lass mit dem Preis mich ziehn." Und Beifall murmelten alle

Dardanidae reddique viro promissa iubebant.
*Troer und hießen dem Mann einhändigen, was ihm versprochen.
*
Hic gravis Entellum dictis castigat Acestes,
*Doch ernst rügt den Entellos jetzt mit Worten Akestes,
*
proximus ut viridante toro consederat herbae:
*Der ihm grade zunächst dasaß auf grünendem Rasen:
*
"Entelle, heroum quondam fortissime frustra,
*"O Entellos, du galtest umsonst als der tapferste Held einst.
*
390



tantane tam patiens nullo certamine tolli
Kannst du geduldig es sehn, dass ohne Gefecht man so große

dona sines? ubi nunc nobis deus ille, magister
*Gaben entführt? Wo bleibt uns der göttliche Lehrer und Meister
*
nequiquam memoratus, Eryx? ubi fama per omnem
*Eryx, den du vergebens nun rühmst? Wo der Ruf durch das ganze
*
Trinacriam et spolia illa tuis pendentia tectis?"
*Sikulerland? Wo der Spolien Zier, die im Hause dir hangen?"
*
ille sub haec: "non laudis amor nec gloria cessit
*Jener darauf: "Mein Ehrgeiz ist und die Liebe zum Ruhme
*
395



pulsa metu; sed enim gelidus tardante senecta
Nicht durch Feigheit verscheucht; doch kalt von lähmendem Alter

sanguis hebet, frigentque effetae in corpore vires.
*Starrt mir das Blut, und die Kraft ward stumpf im frostigen Körper.
*
si mihi quae quondam fuerat quaque improbus iste
*Stände die Jugend mir noch, auf die der verwegene Prahler
*
exsultat fidens, si nunc foret illa iuventas,
*Pochend vertraut, zu Gebot, wie sie einst auch mir zu Gebot stand,
*
haud equidem pretio inductus pulchroque iuvenco
*Ja, ich wäre gekommen, doch nicht durch den Preis und den schönen
*
400



venissem, nec dona moror." sic deinde locutus
Farren gelockt. Mich rührt kein Geschenk." Da er also gesprochen,

in medium geminos immani pondere caestus
*Warf er die zwei Schlagriemen von furchtbarer Wucht in des Kreises
*
proiecit, quibus acer Eryx in proelia suetus
*Mitte, mit denen vordem zum Kampfe der mutige Eryx
*
ferre manum duroque intendere bracchia tergo.
*Ging und Hand und Arm mit den starrenden Fellen umschnürte.
*
obstipuere animi: tantorum ingentia septem
*Staunen ergriff sie im Geist, so riesig waren die sieben
*
405



terga boum plumbo insuto ferroque rigebant.
Stierhautlagen und strotzten mit Blei durchnäht und mit Eisen;

ante omnis stupet ipse Dares longeque recusat,
*Dares selbst stutzt mehr als die andern und weigert sich ernstlich.
*
magnanimusque Anchisiades et pondus et ipsa
*Staunend bewegst auch du, hochherziger Anchisiade,
*
huc illuc vinclorum immensa volumina versat.
*Hin und wieder die Last und der Bänder unendliche Knäuel.
*
tum senior talis referebat pectore voces:
*Und es eröffnet der Greis sein Herz mit folgenden Worten:
*
410



"quid, si quis caestus ipsius et Herculis arma
"Wie wenn einer die Wehr und den Riemen des Herkules selber

vidisset tristemque hoc ipso in litore pugnam?
*Hätte gesehn und den schrecklichen Kampf an diesem Gestade?
*
haec germanus Eryx quondam tuus arma gerebat
*Dies ist die Wehr, die Eryx einst, dein Bruder, geführt hat.
*
- sanguine cernis adhuc sparsoque infecta cerebro -,
*Jetzt noch siehst du mit Blut sie befleckt und verspritztem Gehirne.
*
his magnum Alciden contra stetit, his ego suetus,
*Hiermit stand er im Kampf dem erhabnen Alkiden; ich führte
*
415



dum melior viris sanguis dabat, aemula necdum
Selbst sie, da besseres Blut mir noch Kraft lieh, da mir die Schläfe

temporibus geminis canebat sparsa senectus.
*Neidisches Alter noch nicht mit bleichenden Haaren bestreute.
*
sed si nostra Dares haec Troius arma recusat
*Doch wenn unsere Wehr vom troischen Dares verschmäht wird,
*
idque pio sedet Aeneae, probat auctor Acestes,
*Wenn es der fromme Aineias verlangt und Akestes es billigt,
*
aequemus pugnas. Erycis tibi terga remitto
*Machen den Kampf wir gleich; ich entsage der Häute des Eryx
*
420



- solve metus -, et tu Troianos exue caestus."
- Lass von der Furcht! - und du, tu ab den troianischen Riemen."

haec fatus duplicem ex umeris reiecit amictum
*Also sprach er und warf von den Schultern den doppelten Mantel,
*
et magnos membrorum artus, magna ossa lacertosque
*Zeigte der Glieder gewaltigen Bau und Knochen und Arme
*
exuit atque ingens media consistit harena.
*Nackt, und aufrecht stand er, ein Ries', inmitten der Kampfbahn.
*
tum satus Anchisa caestus pater extulit aequos
*Doch nun holt des Anchises Sohn gleichmäßige Riemen
*
425



et paribus palmas amborum innexuit armis.
Und jedwedem umschnürt mit entsprechender Wehr er die Arme.

constitit in digitos extemplo arrectus uterque
*Fest stehn beide sogleich und gestreckt, auf die Zehen erhoben,
*
bracchiaque ad superas interritus extulit auras.
*Holen sie furchtlos hoch in die Luft mit den Armen zum Hieb aus
*
abduxere retro longe capita ardua ab ictu
*Ziehen das ragende Haupt vor dem Schlag zurück und vermischen
*
immiscentque manus manibus pugnamque lacessunt,
*Gegnerisch Faust mit Faust und reizen sich neckend zum Kampfe.
*
430



ille pedum melior motu fretusque iuventa,
Jener gewandter zu Fuß und kühn in der Jugend Bewusstsein,

hic membris et mole ualens; sed tarda trementi
*Dieser durch massigen Wuchs im Vorteil; aber es wankt ihm
*
genua labant, vastos quatit aeger anhelitus artus.
*Zitternd das Knie, und er ächzt schwer auf, dass der riesige Leib bebt.
*
multa viri nequiquam inter se vulnera iactant,
*Fruchtlos schleudern die Männer zuerst aufeinander die Streiche,
*
multa cavo lateri ingeminant et pectore vastos
*Treffen mit hämmerndem Schlag das Gewölbe der Rippen; die Brust hallt
*
435



dant sonitus, erratque auris et tempora circum
Donnernd zurück; es schwirret die Faust um Ohren und Schläfe

crebra manus, duro crepitant sub vulnere malae.
*Hin und her; manch heftiger Hieb kracht gegen die Backen.
*
stat gravis Entellus nisuque immotus eodem
*Schwer und fest hält stets auf dem selbigen Platz sich Entellos,
*
corpore tela modo atque oculis vigilantibus exit.
*Nur ausweichend dem Schlag mit dem Leib und den wachsamen Augen.
*
ille, velut celsam oppugnat qui molibus urbem
*Doch dem Belagerer gleich, der den hochaufragenden Stadtwall
*
440



aut montana sedet circum castella sub armis,
Oder ein Bergschloss rings umstellt mit bewaffneten Scharen,

nunc hos, nunc illos aditus, omnemque pererrat
*Sucht sich den Zugang hier und dort rings irrenden Blickes
*
arte locum et variis adsultibus inritus urget.
*Jener mit List und bestürmt ihn umsonst von verschiedenen Seiten.
*
ostendit dextram insurgens Entellus et alte
*Und nun hebt sich Entellos und holt hoch aus mit geschwungner
*
extulit, ille ictum venientem a vertice velox
*Rechten; doch jener, der schnell den vom Scheitel ihm drohenden Hieb sieht,
*
445



praevidit celerique elapsus corpore cessit;
Gleitet zur Seite behend und entgeht ihm mit hurtigem Leibe.

Entellus viris in ventum effudit et ultro
*Und in den Wind ausschüttet die Kraft Entellos; er selber
*
ipse gravis graviterque ad terram pondere vasto
*Stürzt, so schwer wie er war, schwer hin auf den Grund mit des Leibes
*
concidit, ut quondam cava concidit aut Erymantho
*Wuchtiger Last, wie entwurzelt und hohl die gewaltige Fichte
*
aut Ida in magna radicibus eruta pinus.
*Auf Erymanthos' Höhn und Idas Waldungen hinstürzt.
*
450



consurgunt studiis Teucri et Trinacria pubes;
Eifrig erheben die Teukrier sich und Trinakriens Jugend;

it clamor caelo primusque accurrit Acestes
*Lärm steigt auf zum Gewölk; gleich eilt Akestes zum Beistand,
*
aequaevumque ab humo miserans attollit amicum.
*Und teilnehmend erhebt er den Freund und Altersgenossen.
*
at non tardatus casu neque territus heros
*Aber der Held, nicht erschreckt noch träger gemacht durch den Unfall,
*
acrior ad pugnam redit ac vim suscitat ira;
*Kehrt nur kühner zurück zum Kampf; Zorn weckt' ihm die Kräfte;
*
455



tum pudor incendit viris et conscia virtus,
Scham auch schüret die Kraft und des eigenen Wertes Bewusstsein.

praecipitemque Daren ardens agit aequore toto
*Hitzig verfolgt um die Bahn er den schleunig entfliehenden Dares,
*
nunc dextra ingeminans ictus, nunc ille sinistra.
*Hieb auf Hieb trifft wechselnd er ihn mit der Rechten und Linken,
*
nec mora nec requies: quam multa grandine nimbi
*Lässt ihm nicht Ruhe noch Rast. Wie Hagel herab auf die Dächer
*
culminibus crepitant, sic densis ictibus heros
*Rasselt aus Wettergewölk, so rastlos hämmert mit beiden
*
460



creber utraque manu pulsat versatque Dareta.
Fäusten und tummelt der Held mit schwirrenden Streichen den Dares.

Tum pater Aeneas procedere longius iras
*Nicht ließ weiter den Zorn vorschreiten der Vater Aineias
*
et saevire animis Entellum haud passus acerbis,
*Und den Entellos nicht fort noch toben erbitterten Mutes,
*
sed finem imposuit pugnae fessumque Dareta
*Sondern er macht' ein Ende dem Kampfund entriss den erschöpften
*
eripuit mulcens dictis ac talia fatur:
*Dares ihm mit freundlichem Wort und redete also:
*
465



"infelix, quae tanta animum dementia cepit?
"Was für ein blendender Wahn, Unseliger, hat dich ergriffen?

non viris alias conversaque numina sentis?
*Merkst du denn nicht die verwandelte Kraft und der Götter Entfremdung?
*
cede deo." dixitque et proelia voce diremit.
*Weiche dem Gott!" Er sprach's und trennte den Kampf mit dem Worte.
*
ast illum fidi aequales genua aegra trahentem
*Doch ihn führte die Schar der vertrauten Genossen, die matten
*
iactantemque utroque caput crassumque cruorem
*Knie hinschleppend, mit wankendem Haupt und geronnene Massen
*
470



ore eiectantem mixtosque in sanguine dentes
Blut ausspeiend und zwischen dem Blut zerschmetterte Zähne,

ducunt ad navis; galeamque ensemque vocati
*Hin zu den Schiffen. Den Helm und das Schwert, wozu man sie aufrief,
*
accipiunt, palmam Entello taurumque relinquunt.
*Nahmen sie an; es verblieb dem Entellos der Stier und die Palme.
*
hic victor superans animis tauroque superbus
*Der rief, stolz auf den Stier im Gefühle des Siegs sich erhebend:
*
"nate dea, vosque haec" inquit "cognoscite, Teucri,
*"Merk es, o Venus' Sohn, und merkt es, ihr anderen Teukrer,
*
475



et mihi quae fuerint iuvenali in corpore vires
Was für Kräfte vordem mein Jünglingskörper besessen,

et qua servetis revocatum a morte Dareta."
*Was für ein Tod es war, von dem ihr Dares errettet."
*
dixit, et adversi contra stetit ora iuvenci
*Sprach's, und entgegengewandt dem Gesichte des Stiers, der als Kampfpreis
*
qui donum astabat pugnae, durosque reducta
*Dastand, stellt' er sich hin. Zurück dann zog er die Rechte,
*
libravit dextra media inter cornua caestus
*Hob sich empor und schwang recht zwischen die Hörner den harten
*
480



arduus, effractoque inlisit in ossa cerebro:
Riemen und schlug ins Gehirn hinein den zerschmetterten Schädel,

sternitur exanimisque tremens procumbit humi bos.
*Dass hinstürzend sich tot am Boden der zuckende Stier streckt;
*
ille super talis effundit pectore voces:
*Und es ergoss dazu sich sein Herz in folgenden Worten:
*
"hanc tibi, Eryx, meliorem animam pro morte Daretis
*"Nimm für Dares' Tod dies Leben als bessres Geschenk an,
*
persolvo; hic victor caestus artemque repono."
*Eryx; Riemen und Kunst leg hier ich nieder als Sieger."
*
485



Protinus Aeneas celeri certare sagitta
Und nun fordert Aineias auf, wem immer mit raschen

invitat qui forte velint et praemia dicit,
*Pfeilen den Kampf zu versuchen beliebt, und ordnet die Preise.
*
ingentique manu malum de nave Seresti
*Dann mit gewaltiger Hand stellt selbst er den Mast von Serestus'
*
erigit et volucrem traiecto in fune columbam,
*Schiff auf und knüpft hoch an das Tau, das oben hindurchgeht,
*
quo tendant ferrum, malo suspendit ab alto.
*Eine geflügelte Taub' als Ziel für das Eisen der Schützen.
*
490



convenere viri deiectamque aerea sortem
Und schon sammeln sie sich; auf dem Boden des ehernen Helmes

accepit galea, et primus clamore secundo
*Liegen die Lose bereit. Mit Beifallsruf als das erste
*
Hyrtacidae ante omnis exit locus Hippocoontis;
*Kommt Hippokoons Zeichen heraus, des Hyrtakossohnes.
*
quem modo navali Mnestheus certamine victor
*Mnestheus folgte darauf, der im Schiffswettrennen soeben
*
consequitur, viridi Mnestheus evinctus oliva.
*Siegte, das Haar noch bekränzt mit des Ölbaums grünenden Zweigen.
*
495



tertius Eurytion, tuus, o clarissime, frater,

Pandare, qui quondam iussus confundere foedus
*Du, Eurytion kommst als der dritte, der Bruder des großen
*
in medios telum torsisti primus Achivos.
*Pandaros, der auf Pallas' Geheiß, den Vertrag zu vernichten,
*
extremus galeaque ima subsedit Acestes,
*In die argivischen Reihen zuerst absandte den Pfeilschuss.
*
ausus et ipse manu iuvenum temptare laborem.
*Tief auf dem Boden des Helms kam endlich als letzter Akestes,
*
*Der noch selbst es gewagt, sich im Jünglingswerk zu versuchen.
*
500



tum validis flexos incurvant viribus arcus
Und nun spannen mit rüstiger Kraft sie die Krümmung des Bogens,

pro se quisque viri et depromunt tela pharetris,
*Jeder der Männer für sich, und ziehen den Pfeil aus dem Köcher.
*
primaque per caelum nervo stridente sagitta
*Aber zuerst durchschnitt von schwirrender Sehne des jungen
*
Hyrtacidae iuvenis volucris diverberat auras,
*Hyrtakossohnes Geschoss die geflügelten Lüfte des Himmels.
*
et venit adversique infigitur arbore mali.
*Grad auf den Mast zu flog es und bohrte sich fest in den Stamm ein.
*
505



intremuit malus micuitque exterrita pennis
Schütternd erbebte der Mast, dass der Vogel erschrocken und angstvoll

ales, et ingenti sonuerunt omnia plausu.
*Flatterte und rings alles erscholl von gewaltigem Klatschen.
*
post acer Mnestheus adducto constitit arcu
*Mnestheus stellte sich drauf kühn hin mit gezogenem Bogen,
*
alta petens, pariterque oculos telumque tetendit.
*Zielte hinauf und richtete scharf nach dem Auge die Waffe.
*
ast ipsam miserandus avem contingere ferro
*Doch nicht reichte dem Armen die Kraft, dass er selber die Taube
*
510



non valuit; nodos et vincula linea rupit
Traf mit dem Stahl: er zerschnitt nur die Knoten des leinenen Bandes,

quis innexa pedem malo pendebat ab alto;
*Das, um die Füße geschürzt, sie fest an dem ragenden Mast hielt.
*
illa Notos atque atra volans in nubila fugit.
*Sie nun schwang sich zur Flucht in die Winde und schwarzes Gewölk auf.
*
tum rapidus, iamdudum arcu contenta parato
*Da rief eilig, der längst in Bereitschaft schon auf gespanntem
*
tela tenens, fratrem Eurytion in vota vocavit,
*Bogen gehalten den Pfeil, Eurytion, flehend zum Bruder,
*
515



iam vacuo laetam caelo speculatus et alis
Zielte zur Taube hinauf, die mit klatschenden Flügeln am weiten

plaudentem nigra figit sub nube columbam.
*Himmel sich fröhlich schwang, und durchbohrt' im schwarzen Gewölk sie.
*
decidit exanimis vitamque reliquit in astris
*Tot hin stürzt sie; sie lässt in des Aithers Gestirnen ihr Leben
*
aetheriis fixamque refert delapsa sagittam.
*Und bringt fallend den Pfeil zurück, von dem sie durchbohrt ward.
*
Amissa solus palma superabat Acestes,
*So blieb einzig, der Palme beraubt, Akestes noch übrig,
*
520



qui tamen aërias telum contendit in auras
Der gleichwohl sein Geschoss in die Lüfte des Aithers entsendet,

ostentans artemque pater arcumque sonantem.
*Dass er, der Alte, die Kunst und den klingenden Bogen bewähre.
*
hic oculis subitum obicitur magnoque futurum
*Da, urplötzlich, erscheint von großer Bedeutung ein Wunder
*
augurio monstrum; docuit post exitus ingens
*Jeglichem Blick, durch gewaltgen Erfolg nachträglich enträtselt,
*
seraque terrifici cecinerunt omina vates.
*Spät als Omen erklärt durch schreckenverkündende Seher.
*
525



namque volans liquidis in nubibus arsit harundo
Denn durch das helle Gewölk hinfliegend, entzündet der Schaft sich,

signavitque viam flammis tenuisque recessit
*Zeichnet mit Flammen den Weg und löst in die flüchtigen Lüfte
*
consumpta in ventos, caelo ceu saepe refixa
*Fernhin schwindend sich auf; wie oft, vom Himmel gerissen,
*
transcurrunt crinemque volantia sidera ducunt.
*Sterne den Raum durchziehn und den Schweif hinschleppen im Fluge.
*
attonitis haesere animis superosque precati
*Stutzend im Geist wie vom Donner gerührt, flehn hoch zu den Göttern
*
530



Trinacrii Teucrique viri, nec maximus omen
Teukrier und Trinakrier jetzt. Aineias, der Große,

abnuit Aeneas, sed laetum amplexus Acesten
*Weist nicht das Zeichen zurück; er umarmt den erfreuten Akestes,
*
muneribus cumulat magnis ac talia fatur:
*Gibt manch großes Geschenk ihm zum Lohn und redet die Worte:
*
"sume, pater, nam te voluit rex magnus Olympi
*"Nimm, o Vater; es spricht durch dies Wahrzeichen der große
*
talibus auspiciis exsortem ducere honores.
*Fürst des Olymp dir außer der Reihe den ehrenden Preis zu;
*
535



ipsius Anchisae longaevi hoc munus habebis,
Drum als Gabe bestimm' ich dir hier des bejahrten Anchises

cratera impressum signis, quem Thracius olim
*Eigenen Mischkrug, rings umprägt mit Bildern; der Thraker
*
Anchisae genitori in magno munere Cisseus
*Kisseus gab ihn als großes Geschenk einst meinem Erzeuger
*
ferre sui dederat monimentum et pignus amoris."
*Mit auf den Weg zum Pfand und Erinnrungszeichen der Liebe."
*
sic fatus cingit viridanti tempora lauro
*Also sprach er und kränzt' ihm das Haupt mit grünendem Lorbeer,
*
540



et primum ante omnis victorem appellat Acesten.
Und als Sieger erklärt er vor allen zuerst den Akestes.

nec bonus Eurytion praelato invidit honori,
*Auch missgönnt ihm Eurytion nicht, der Gute, den Vorzug,
*
quamvis solus avem caelo deiecit ab alto.
*Der allein doch den Vogel gefällt aus der Höhe des Himmels.
*
proximus ingreditur donis qui vincula rupit,
*Nächst ihm schreitet mit Gaben einher, der die Fessel durchschossen;
*
extremus volucri qui fixit harundine malum.
*Er, der den Mastbaum traf mit geflügeltem Schaft - als der letzte.
*
545



At pater Aeneas nondum certamine misso
Doch nun, eh er das Kampfspiel schließt, ruft Vater Aineias

custodem ad sese comitemque impubis Iuli
*Aipytos' Sohn zu sich, den zum Leiter des jungen Iulus
*
Epytiden vocat, et fidam sic fatur ad aurem:
*Er und Gefährten bestellt, und spricht zum Ohr des Getreuen:
*
"vade age et Ascanio, si iam puerile paratum
*"Auf und sage Askanios, wenn das Geschwader der Knaben
*
agmen habet secum cursusque instruxit equorum,
*Schon in Bereitschaft er hält, wenn schon er gerüstet den Wettlauf,
*
550



ducat avo turmas et sese ostendat in armis
Soll er dem Ahn herführen die Schar und sich in den Waffen

dic" ait. ipse omnem longo decedere circo
*Zeigen." Er sprach es und hieß das sich drängende Volk aus der langen
*
infusum populum et campos iubet esse patentis.
*Rennbahn weichen und rings das Gefild und die Ebene räumen.
*
incedunt pueri pariterque ante ora parentum
*Und vor der Eltern Gesicht ziehn jetzt gleichmäßig die Knaben
*
frenatis lucent in equis, quos omnis euntis
*Glänzend zu Ross einher; sie schwenken die Zügel, und jubelnd
*
555



Trinacriae mirata fremit Troiaeque iuventus.
Staunt die trinakrische Jugend sie an und die Jugend der Troer.

omnibus in morem tonsa coma pressa corona;
*Sämtlich tragen im Haar nach Brauch sie geschorene Kränze
*
cornea bina ferunt praefixa hastilia ferro,
*Und mit eiserner Spitze je zwei kornellene Speere,
*
pars levis umero pharetras; it pectore summo
*Blitzende Köcher ein Teil auf der Schulter, und über der Brust läuft
*
flexilis obtorti per collum circulus auri.
*Rings um den Hals ein biegsamer Reif von gewundenem Golde.
*
560



tres equitum numero turmae ternique vagantur
In drei Rotten geteilt sind die Reiter; vor jedem Geschwader

ductores; pueri bis seni quemque secuti
*Tummelt ein Hauptmann sich. Zu zweimal sechsen ihm folgend,
*
agmine partito fulgent paribusque magistris.
*Schimmert die Schar gleichmäßig verteilt, gleichmäßig geleitet.
*
una acies iuvenum, ducit quam parvus ovantem
*Dort ist der Jünglingszug, der mit Lust den Befehlen des kleinen
*
nomen avi referens Priamus, tua clara, Polite,
*Priamos folgt, dem Erben des Ahnherrennamens, Polites'
*
565



progenies, auctura Italos; quem Thracius albis
Edelem Spross, der das Italervolk zu mehren bestimmt ist.

portat equus bicolor maculis, vestigia primi
*Weiß ist sein Renner gefleckt, ein Thrakier, weiß um des Hufes
*
alba pedis frontemque ostentans arduus albam.
*Vordersten Rand und weiß an der Stirn, die stolz er emporwirft.
*
alter Atys, genus unde Atii duxere Latini,
*Atys alsdann, von dem die latinischen Atier stammen,
*
parvus Atys pueroque puer dilectus Iulo.
*Atys, noch selbst ein Knab' und geliebt vom Knaben Iulus.
*
570



extremus formaque ante omnis pulcher Iulus
Aber zuletzt, an Gestalt vor allen der schönste, Iulus

Sidonio est invectus equo, quem candida Dido
*Ritt auf sidonischem Ross, dem Geschenke der glänzenden Dido,
*
esse sui dederat monimentum et pignus amoris.
*Das sie zum Pfand ihm verehrt und Erinnrungszeichen der Liebe.
*
cetera Trinacriis pubes senioris Acestae
*Aber die übrige Schar ritt Sikulerpferde, die ihnen
*
fertur equis.
*Vater Akestes geliehn.
*
575



excipiunt plausu pavidos gaudentque tuentes
Beifallsklatschen empfängt die Erregten; die Dardaner freun sich

Dardanidae, veterumque agnoscunt ora parentum.
*Herzlich der Schau; sie erkennen das Bild der bejahrteren Eltern.
*
postquam omnem laeti consessum oculosque suorum
*Als an der Ihrigen Blicken vorbei um die ganze Versammlung
*
lustravere in equis, signum clamore paratis
*Rings sie geritten, da gibt durch Ruf das erwartete Zeichen
*
Epytides longe dedit insonuitque flagello.
*Aipytos' Sohn weithin und klatscht zugleich mit der Peitsche.
*
580



olli discurrere pares atque agmina terni
Und nun trennen sie sich gleichmäßig und ziehen die Rotten

diductis solvere choris, rursusque vocati
*Dreifach geteilt auseinander, dann schwenken sie um auf ein Zeichen,
*
convertere vias infestaque tela tulere.
*Jagen zurück auf dem Weg und erheben die Waffen zum Kampfe,
*
inde alios ineunt cursus aliosque recursus
*Ändern von neuem den Lauf und nehmen von neuem den Rücklauf,
*
adversi spatiis, alternosque orbibus orbis
*Gegeneinander gewandt auf der Bahn, umschlingen sich wechselnd
*
585



impediunt pugnaeque cient simulacra sub armis;
Kreis um Kreis und stellen ein Kampfbild dar mit den Waffen:

et nunc terga fuga nudant, nunc spicula vertunt
*Jetzo den Rücken gewandt zur Flucht, jetzt feindlich die Speere
*
infensi, facta pariter nunc pace feruntur.
*Richtend und jetzo vereint hinreitend in friedlichem Zuge.
*
ut quondam Creta fertur Labyrinthus in alta
*So wie vom Labyrinth man erzählt in Kretas Gebirgen,
*
parietibus textum caecis iter ancipitemque
*Dass es die Wege verbaut durch ein Mauergeweb und in tausend
*
590



mille viis habuisse dolum, qua signa sequendi
Pfade geteilt Irrgänge gehabt, wo jegliches Merkmal,

frangeret indeprensus et inremeabilis error;
*Durch Blendwerke verwirrt, unentdeckbar machte den Rückweg:
*
haud alio Teucrum nati vestigia cursu
*Also verwickeln die Spur im Lauf die troianischen Knaben,
*
impediunt texuntque fugas et proelia ludo,
*Weben die Flucht und den Kampf durcheinander im Spiel, den Delphinen
*
delphinum similes qui per maria umida nando
*Ähnlich, die schwimmend im wogenden Nass die karpathische Meerflut
*
595



Carpathium Libycumque secant.
Oder die libysche See mit schäkernden Spielen durchschneiden.

hunc morem cursus atque haec certamina primus
*Dies ist des Spieles Gebrauch und des Kampfs, den Askanios, da er
*
Ascanius, Longam muris cum cingeret Albam,
*Alba Longa mit Mauern umzog, dorthin als der erste
*
rettulit et priscos docuit celebrare Latinos,
*Trug und in selbiger Art zu feiern die alten Latiner
*
quo puer ipse modo, secum quo Troia pubes;
*Lehrte, wie einst er als Knab' ihn geübt mit der troischen Jugend.
*
600



Albani docuere suos; hinc maxima porro
Weiter dann wurd' er in Alba gelehrt; es empfing ihn das große

accepit Roma et patrium servavit honorem;
*Rom von dort und bewahrt ihn als ehrendes Erbe der Ahnherrn.
*
Troiaque nunc pueri, Troianum dicitur agmen.
*Troia nennt man das Spiel, Troianergeschwader die Knaben;
*
hac celebrata tenus sancto certamina patri.
*Heut noch feiert den Kampf man zu Ehren des heiligen Vaters.
*
Hinc primum Fortuna fidem mutata novavit.
*Und hier wandte zuerst treulos Fortuna die Bahnen.
*
605



dum variis tumulo referunt sollemnia ludis,
Als an dem Grab man die Feier begeht mit mancherlei Spielen,

Irim de caelo misit Saturnia Iuno
*Schickt die saturnische Iuno vom Himmel herab zu der Troer
*
Iliacam ad classem ventosque aspirat eunti,
*Flotte die Iris und leiht zum Flug ihr günstige Winde,
*
multa movens necdum antiquum saturata dolorem.
*Vieles erwägend, da noch ihr früherer Groll nicht gesättigt.
*
illa viam celerans per mille coloribus arcum
*Aber die Jungfrau schwingt auf tausendfach schillerndem Bogen
*
610



nulli visa cito decurrit tramite virgo.
Rasch sich hinab, von keinem gesehn auf dem flüchtigen Pfade;

conspicit ingentem concursum et litora lustrat
*Sieht den gewaltigen Auflauf hier, umschwebt die Gestade,
*
desertosque videt portus classemque relictam.
*Siehet den Hafen von Menschen geräumt und die Flotte verlassen.
*
at procul in sola secretae Troades acta
*Aber entfernt und allein am einsamen Strande beweinten
*
amissum Anchisen flebant, cunctaeque profundum
*Troias Fraun des Anchises Tod und blickten mit Tränen
*
615



pontum aspectabant flentes. heu tot vada fessis
Alle hinaus in die Tiefe der See: "Ach, dass den Erschöpften

et tantum superesse maris, vox omnibus una;
*So viel Fluten noch drohen und Meere!" so riefen sie alle,
*
urbem orant, taedet pelagi perferre laborem.
*Sehnsuchtsvoll nach der Stadt und satt der Beschwerden der Meerfahrt.
*
ergo inter medias sese haud ignara nocendi
*Nicht unkundig in schädlichem Tun, wirft recht in des Haufens
*
conicit et faciemque deae vestemque reponit;
*Mitte sie sich; doch legt sie die göttliche Tracht und Gestalt ab;
*
620



fit Beroe, Tmarii coniunx longaeva Dorycli,
Beroe wird sie, Doryklos', des Tmariers, greise Gemahlin,

cui genus et quondam nomen natique fuissent,
*Die mit Geschlecht vordem und Reichtum und Kindern gesegnet;
*
ac sic Dardanidum mediam se matribus infert.
*Also tritt sie hinein in den Kreis der dardanischen Mütter:
*
"o miserae, quas non manus" inquit "Achaica bello
*"Unglückselige ihr, die die Hand der Achaier im Kriege
*
traxerit ad letum patriae sub moenibus! o gens
*Nicht zum Tode geschleppt vor der Heimat Mauern! o armes
*
625



infelix, cui te exitio Fortuna reservat?
Volk, zu welcherlei Los will dich aufsparen das Schicksal?

septima post Troiae excidium iam vertitur aestas,
*Dies ist der siebente Sommer bereits nach Troias Zerstörung,
*
cum freta, cum terras omnis, tot inhospita saxa
*Seit wir Länder und Meer, so viel ungastliche Klippen,
*
sideraque emensae ferimur, dum per mare magnum
*Alle Gestirne durchmessen und weit durch die See wir verfolgen
*
Italiam sequimur fugientem et volvimur undis.
*Fliehendes Italerland, von rollenden Wogen geschaukelt.
*
630



hic Erycis fines fraterni atque hospes Acestes:
Hier ist des Eryx brüderlich Reich und Akestes, der Gastfreund.

quis prohibet muros iacere et dare civibus urbem?
*Weshalb gönnen wir hier nicht Stadt und Mauern den Bürgern?
*
o patria et rapti nequiquam ex hoste penates,
*Väterlich Land, ihr umsonst den Feinden entrissne Penaten,
*
nullane iam Troiae dicentur moenia? nusquam
*Spricht kein Mund hinfort von troianischen Mauern? und werd ich
*
Hectoreos amnis, Xanthum et Simoenta, videbo?
*Nirgend den Xanthos schaun und Simois, Hektors Gewässer?
*
635



quin agite et mecum infaustas exurite puppis.
Auf vielmehr und verbrennt mit mir die entsetzlichen Schiffe!

nam mihi Cassandrae per somnum vatis imago
*Denn mir träumte die Nacht, wie das Bild der Prophetin Kassandra
*
ardentis dare visa faces: "hic quaerite Troiam;
*Brennende Fackeln mir gab und sprach: ,Hier suchet euch Troia;
*
hic domus est" inquit "vobis." iam tempus agi res,
*Hier ist das Haus für euch.' Drum jetzt ist Zeit, dass wir handeln.
*
nec tantis mora prodigiis. en quattuor arae
*Solch ein Wunder verbietet Verzug. Hier sehet Neptunus'
*
640



Neptuno; deus ipse faces animumque ministrat."
Vier Altäre; der Gott leiht selbst uns den Mut und die Fackeln."

haec memorans prima infensum vi corripit ignem
*Sprach's und griff mit Gewalt zuerst nach dem feindlichen Feuer,
*
sublataque procul dextra conixa coruscat
*Holt weit aus und hoch mit der Rechten und schwingt es und wirft es.
*
et iacit. arrectae mentes stupefactaque corda
*Und wie staunenden Sinns und betäubt im Herzen die Frauen
*
Iliadum. hic una e multis, quae maxima natu,
*Ilions stehn, ruft eine der Schar, die bejahrteste, Pyrgo,
*
645



Pyrgo, tot Priami natorum regia nutrix:
Fürstliche Amme vordem bei vielen von Priamos' Kindern:

"non Beroe vobis, non haec Rhoeteia, matres,
*"Dies ist Beroe nicht, ihr Fraun, nicht Doryklos' Gattin
*
est Dorycli coniunx; divini signa decoris
*Ist, die Rhoiteierin, dies; o merkt auf der göttlichen Anmut
*
ardentisque notate oculos, qui spiritus illi,
*Zeichen, den flammenden Blick; wie kühn sie erscheint, wie die Mienen
*
qui vultus vocisque sonus vel gressus eunti.
*Strahlen, wie kräftig ihr Ton! Wie hebt sie beim Gehen die Schritte!
*
650



ipsa egomet dudum Beroen digressa reliqui
Selber verließ ich Beroen erst vor kurzem, die krank lag

aegram, indignantem tali quod sola careret
*Und die sehr es verdross, dass, allein abwesend bei solchem
*
munere nec meritos Anchisae inferret honores."
*Fest, sie die ehrenden Weihn dem Anchises müsse versagen."
*
haec effata.
*Also sprach sie.
*
at matres primo ancipites oculisque malignis
*Anfangs schwankten die Fraun und sahn mit zürnenden Blicken,
*
655



ambiguae spectare rates miserum inter amorem
Aber geteilten Gemüts nach den Schiffen, da hier der geliebte

praesentis terrae fatisque vocantia regna,
*Boden die Armen und dort das vom Schicksal verheißene Reich
*
cum dea se paribus per caelum sustulit alis
*lockt: Als durch die Luft sich die Göttin auf gleichhin schwebenden Flügeln
*
ingentemque fuga secuit sub nubibus arcum.
*Hob und weit durch die Luft das Gewölk durchschnitt mit dem Bogen.
*
tum vero attonitae monstris actaeque furore
*Da, durch das Wunder betäubt, von des Wahnsinns Stachel getrieben,
*
660



conclamant, rapiuntque focis penetralibus ignem,
Schreien sie auf und reißen den Brand von den häuslichen Herden,

pars spoliant aras, frondem ac virgulta facesque
*Plündern der Götter Altar, Laubwerk und Reisig und Fackeln
*
coniciunt. furit immissis Volcanus habenis
*Werfen sie drein; Vulkan lässt locker die Zügel, und rasend
*
transtra per et remos et pictas abiete puppis.
*Stürzt er durch Ruder, Gebälk und die tannenen bunten Verdecke.
*
Nuntius Anchisae ad tumulum cuneosque theatri
*Und Eumelos bringt dem Aineias zum Grab und des Schauspiels
*
665



incensas perfert navis Eumelus, et ipsi
Sitzen die Kunde sofort von den brennenden Schiffen; sie selber

respiciunt atram in nimbo volitare favillam.
*Sehn schon hinter sich schwarz im Gewölk aufwirbeln die Asche.
*
primus et Ascanius, cursus ut laetus equestris
*Und Askanios jagt, wie eben er froh noch den Rosslauf
*
ducebat, sic acer equo turbata petivit
*Leitet, als erster zu Ross kühn allen voran zum verwirrten
*
castra, nec exanimes possunt retinere magistri.
*Lager hinab; es halten ihn nicht die erschrockenen Führer.
*
670



"quis furor iste novus? quo nunc, quo tenditis" inquit
"Was für seltsame Wut ist das? Was wollt, was beginnt ihr,

"heu miserae cives? non hostem inimicaque castra
*Unglückselige Fraun? Nicht den Feind und der Danaer Lager
*
Argivum, vestras spes uritis. en, ego vester
*Äschert ihr ein, ihr verbrennt die eigenen Hoffnungen; seht hier
*
Ascanius!" - galeam ante pedes proiecit inanem,
*Euren Askanios!" Und hin wirft er zu ihren Füßen
*
qua ludo indutus belli simulacra ciebat.
*Leer seinen Helm, in dem er das Kriegsspiel eben noch lenkte.
*
675



accelerat simul Aeneas, simul agmina Teucrum.
Jetzt eilt auch Aineias herbei mit den Scharen der Teukrer.

ast illae diversa metu per litora passim
*Aber die Weiber entfliehn, ringshin sich zerstreuend am Ufer,
*
diffugiunt, silvasque et sicubi concava furtim
*Suchen den Wald zum Schutz und hohles Geklüft zum Versteck auf.
*
saxa petunt; piget incepti lucisque, suosque
*Denn schon reut sie die Tat, und sie schämen des Lichts sich, erkennen
*
mutatae agnoscunt excussaque pectore Iuno est.
*Wieder verändert die Ihren, der Brust ist Iuno entschüttelt.
*
680



Sed non idcirco flamma atque incendia viris
Aber es bändigt darum der verheerende Brand und die Flamme

indomitas posuere; udo sub robore vivit
*Nicht die entfesselte Kraft. Es lebt in dem feuchten Gebälk noch,
*
stuppa vomens tardum fumum, lentusque carinas
*Langsamen Rauch aufwirbelnd, das Werg; träg schwelender Dampf frisst
*
est vapor et toto descendit corpore pestis,
*Tief in den Kiel, und es senkt in den Rumpf ringsum sich das Unheil.
*
nec vires heroum infusaque flumina prosunt.
*Hier hilft weder der Helden Gewalt noch Ströme von Wasser.
*
685



tum pius Aeneas umeris abscindere vestem
Und nun reißt das Gewand von den Schultern der fromme Aineias,

auxilioque vocare deos et tendere palmas:
*Fleht zu den Göttern empor und streckt gen Himmel die Arme:
*
"Iuppiter omnipotens, si nondum exosus ad unum
*"Oh, allmächtiger Zeus, ist nicht gleichmäßig dir jeder
*
Troianos, si quid pietas antiqua labores
*Troer verhasst und gedenkt in Huld wie vor alters die Vorsicht
*
respicit humanos, da flammam evadere classi
*Menschlicher Mühn, so gib, dass das Feuer den Schiffen entweiche,
*
690



nunc, pater, et tenuis Teucrum res eripe leto.
Vater; entreiß dem Verderben die dürftige Habe der Teukrer,

vel tu, quod superest, infesto fulmine morti,
*Oder versenk auch mich, sofern ich's verdient, mit des Blitzes
*
si mereor, demitte tuaque hic obrue dextra."
*Feindlichem Strahl in den Tod und zerschmettre mich hier mit der Rechten."
*
vix haec ediderat cum effusis imbribus atra
*Kaum dass also er sprach, so rast mit Strömen von Regen
*
tempestas sine more furit tonitruque tremescunt
*Schwarz ein Gewitter daher, und die Felder, die Höhen des Landes
*
695



ardua terrarum et campi; ruit aethere toto
Beben von Donnergeroll. Es stürzt wild stäubend vom ganzen

turbidus imber aqua densisque nigerrimus Austris,
*Aither der Regen herab, tief schwarz vom peitschenden Südwind.
*
implenturque super puppes, semusta madescunt
*Rasch füllt jedes Verdeck sich an, das verkohlte Gebälk trieft,
*
robora, restinctus donec vapor omnis et omnes
*Dass allmählich der Qualm auslischt und sämtliche Schiffe
*
quattuor amissis servatae a peste carinae.
*Bis auf vier, die verbrannt, von dem grausen Verderben bewahrt sind.
*
700



At pater Aeneas casu concussus acerbo
Doch Aineias, aufs tiefste bewegt von dem bitteren Unfall,

nunc huc ingentis, nunc illuc pectore curas
*Wird hierhin und dort in der Brust von unendlichen Sorgen
*
mutabat versans, Siculisne resideret arvis
*Wechselnd durchwogt, ob zum Sitz er, der göttlichen Schickung vergessend,
*
oblitus fatorum, Italasne capesseret oras.
*Wähle die Sikulerflur, ob zum Italerstrand er sich wende.
*
tum senior Nautes, unum Tritonia Pallas
*Nautes, der Alte, darauf, den allein die tritonische Pallas
*
705



quem docuit multaque insignem reddidit arte -
Sich zum Schüler erkor, den sie vielfach schmückte mit Künsten,

haec responsa dabat, vel quae portenderet ira
*Gab ihm diesen Bescheid, was der Götter gewaltiges Zürnen
*
magna deum vel quae fatorum posceret ordo;
*Ihm weissag und was der Verhängnisse Ordnung gebiete.
*
isque his Aenean solatus vocibus infit:
*Und mit tröstendem Wort hebt also er an zu Aineias:
*
"nate dea, quo fata trahunt retrahuntque sequamur;
*"Göttingeborner, wohin uns das Schicksal zieht und zurückzieht,
*
710



quidquid erit, superanda omnis fortuna ferendo est.
Folgen wir ihm; durch Geduld ist jedes Geschick zu besiegen.

est tibi Dardanius divinae stirpis Acestes:
*Hast du den Dardaner doch von göttlichem Stamm, den Akestes:
*
hunc cape consiliis socium et coniunge volentem,
*Ihn nimm an zum Genossen im Rat; gern wird er dir beistehn.
*
huic trade amissis superant qui navibus et quos
*Tritt ihm die Mannschaft ab der verlorenen Schiffe und jeden,
*
pertaesum magni incepti rerumque tuarum est.
*Der mit Verdruss dir folgt und deinem erhabenen Planen;
*
715



longaevosque senes ac fessas aequore matres
Greise, von Alter gebeugt, und Mütter, erschöpft von der Seefahrt,

et quidquid tecum invalidum metuensque pericli est
*Und wer kraftlos sonst und wer vor Gefahren sich fürchtet,
*
delige, et his habeant terris sine moenia fessi;
*Lies sie aus, lass hier die Ermüdeten Mauern erbauen,
*
urbem appellabunt permisso nomine Acestam."
*Lass sie Acesta die Stadt mit deiner Erlaubnis benennen!"
*
Talibus incensus dictis senioris amici
*Durch dies Wort des bejahrteren Freunds noch tiefer ergriffen,
*
720



tum vero in curas animo diducitur omnis;
Wird von Sorgen sein Geist nach jeglicher Richtung getrieben.

et Nox atra polum bigis subvecta tenebat.
*Schon zog schwarz mit dem Doppelgespann am Pole die Nacht hin,
*
visa dehinc caelo facies delapsa parentis
*Als, vom Himmel herab sich senkend, des Vaters Anchises
*
Anchisae subito talis effundere voces:
*Schatten ihm plötzlich erschien und mit folgenden Worten ihn ansprach:
*
"nate, mihi vita quondam, dum vita manebat,
*"Sohn, der du teurer mir warst als mein Leben, solange mein Leben
*
725



care magis, nate Iliacis exercite fatis,
Dauerte; Sohn, der du Troias Geschick mühselig durchkämpft hast,

imperio Iovis huc venio, qui classibus ignem
*Iovis Geheiß schickt mich hierher, der vom Brande die Flotte
*
depulit, et caelo tandem miseratus ab alto est.
*Rettete, der von den himmlischen Höhn sich endlich erbarmt hat.
*
consiliis pare quae nunc pulcherrima Nautes
*Hör auf den trefflichen Rat, den jetzt dir Nautes, der Alte,
*
dat senior; lectos iuvenes, fortissima corda,
*Gibt. Die erlesenste Jugend allein, die tapfersten Herzen
*
730



defer in Italiam. gens dura atque aspera cultu
Führ in das Italerland. Hart ist und rauh von Gewöhnung

debellanda tibi Latio est. Ditis tamen ante
*Latiums Volk, das dort du bewältigen musst; doch zuvörderst
*
infernas accede domos et Averna per alta
*Steige zu Plutos Wohnung hinab; durch den tiefen Avernus
*
congressus pete, nate, meos. non me impia namque
*Suche mich auf, o Sohn; nicht hält bei den grausigen Schatten
*
Tartara habent, tristes umbrae, sed amoena piorum
*Tartarus' Nacht mich gebannt, die verruchte; bei heiteren Scharen
*
735



concilia Elysiumque colo. huc casta Sibylla
Weil in Elysium ich; mit reichlichem Blute von schwarzen

nigrarum multo pecudum te sanguine ducet.
*Opfern gesühnt, führt dorthin dich Sibylla, die keusche.
*
tum genus omne tuum et quae dentur moenia disces.
*Dann wird all dein Geschlecht und die künftige Stadt dir geweissagt.
*
iamque vale; torquet medios Nox umida cursus
*Jetzt leb wohl; feucht rollt inmitten des Weges die Nacht schon,
*
et me saevus equis Oriens adflavit anhelis."
*Und grimm weht mich der Aufgang an mit keuchenden Rossen."
*
740



dixerat et tenuis fugit ceu fumus in auras.
Sprach's und verschwand, wie Rauch in die flüchtigen Lüfte sich auflöst.

Aeneas "quo deinde ruis? quo proripis?" inquit,
*Aber Aineias: "Wohin? Wohin entraffst du so jäh dich?
*
"quem fugis? aut quis te nostris complexibus arcet?"
*Wen doch fliehst du? Wer hält dich zurück von meiner Umarmung?"
*
haec memorans cinerem et sopitos suscitat ignis,
*Also ruft er und schürt die entschlummerte Glut aus der Asche,
*
Pergameumque Larem et canae penetralia Vestae
*Und den pergamischen Lar und die heilige Stätte der greisen
*
745



farre pio et plena supplex veneratur acerra.
Vesta verehrt andächtig und fromm er mit Korn und mit Weihrauch.

Extemplo socios primumque accersit Acesten
*Gleich dann ruft die Gefährten er her und zuerst den Akestes,
*
et Iovis imperium et cari praecepta parentis
*Sagt, was Zeus ihm befahl, was sein teurer Erzeuger ihm vorschrieb
*
edocet et quae nunc animo sententia constet.
*Und bei welchem Entschluss er jetzt im Herzen beharre,
*
haud mora consiliis, nec iussa recusat Acestes:
*Nimmt auch nicht zur Beratung sich Zeit, und Akestes gehorcht ihm.
*
750



transcribunt urbi matres populumque volentem
Und nun zeichnen die Mütter sie auf für die Stadt und vom Volke,

deponunt, animos nil magnae laudis egentis.
*Wer sonst will: kein Herz, das viel nach besonderem Ruhm geizt.
*
ipsi transtra novant flammisque ambesa reponunt
*Bessern die Bänke der Ruderer aus und ersetzen der Schiffe
*
robora navigiis, aptant remosque rudentisque,
*Flammenzerfressnes Gebälk und versehn sie mit Rudern und Tauen.
*
exigui numero, sed bello vivida virtus.
*Klein an Zahl ist die Schar, doch belebt von kriegrischem Mute.
*
755



interea Aeneas urbem designat aratro
Doch Aineias umfurcht mit dem Pflug inzwischen den Stadtraum,

sortiturque domos; hoc Ilium et haec loca Troiam
*Zieht um die Häuser das Los, und "Ilion" lässt er die Stätte
*
esse iubet. gaudet regno Troianus Acestes
*Nennen und "Troia". Es freut sich des Reichs der Troianer Akestes,
*
indicitque forum et patribus dat iura vocatis.
*Ruft zu Markte das Volk, wählt Ratsherrn, gibt die Gesetze.
*
tum vicina astris Erycino in vertice sedes
*Dann wird nah den Gestirnen ein Sitz der idalischen Venus
*
760



fundatur Veneri Idaliae, tumuloque sacerdos
Hoch auf Eryx' Gipfel geweiht, und ein heiliger Hain wird

ac lucus late sacer additus Anchiseo.
*Weit umhegt und ein Priester bestimmt für Anchises' Grabmal.
*
Iamque dies epulata novem gens omnis, et aris
*Schon hat das Volk neun Tage geschmaust und der Götter Altäre
*
factus honos: placidi straverunt aequora venti
*Festlich geehrt, und das Meer ist von friedlichen Winden geglättet.
*
creber et aspirans rursus vocat Auster in altum.
*Günstig und frisch weht wieder der Süd und ruft auf die Höhe.
*
765



exoritur procurva ingens per litora fletus;
Längs dem gebogenen Strand nun erhebt sich unendlicher Jammer;

complexi inter se noctemque diemque morantur.
*Tag und Nacht durch weilt man daselbst in heißer Umarmung.
*
ipsae iam matres, ipsi, quibus aspera quondam
*Selber die Mütter und sie, die sonst mit Grausen das rauhe
*
visa maris facies et non tolerabile numen,
*Meer ansahn, die schon unerträglich dünkte der Name,
*
ire volunt omnemque fugae perferre laborem.
*Wollen nun ziehn und die Fahrt mit allen Beschwerden erdulden;
*
770



quos bonus Aeneas dictis solatur amicis
Da denn mit freundlichem Wort sie der gute Aineias ermuntert,

et consanguineo lacrimans commendat Acestae.
*Und, selbst weinend, dem Schutz sie empfiehlt des verwandten Akestes.
*
tris Eryci vitulos et Tempestatibus agnam
*Und nun lässt er den Stürmen ein Lamm, drei Kälber dem Eryx
*
caedere deinde iubet solvique ex ordine funem.
*Opfern und Reih bei Reih vom Strand abwinden die Taue.
*
ipse caput tonsae foliis evinctus olivae
*Selber das Haupt umkränzt mit geschorenem Laube des Ölzweigs,
*
775



stans procul in prora pateram tenet, extaque salsos
Steht er fern auf dem Bug und gießt aus erhobener Schale

proicit in fluctus ac vina liquentia fundit.
*Lauteren Wein in die salzige Flut und streuet Gekröse.
*
prosequitur surgens a puppi ventus euntis.
*Günstiger Wind springt auf und weht vom Spiegel dem Schiff nach.
*
certatim socii feriunt mare et aequora verrunt;
*Eifrig durchfegen die Flut und peitschen das Meer die Genossen.
*
At Venus interea Neptunum exercita curis
*Venus redet indes, von Sorgen gequält, zu Neptunus
*
780



adloquitur talisque effundit pectore questus:
Also und schüttet ihr Herz ihm aus in folgenden Klagen:

"Iunonis gravis ira neque exsaturabile pectus
*"Iunos grimmiger Zorn und nimmer ersättliche Rachsucht
*
cogunt me, Neptune, preces descendere in omnis;
*Zwingt mich, Neptun, mich herabzulassen zu jeglicher Bitte,
*
quam nec longa dies pietas nec mitigat ulla,
*Da nicht Dauer der Zeit noch Frömmigkeit je sie besänftigt,
*
nec Iovis imperio fatisque infracta quiescit.
*Nimmer sie ruht, nicht gebeugt durch Iovis Geheiß und Verhängnis.
*
785



non media de gente Phrygum exedisse nefandis
Und nicht genug, dass die Stadt aus der Mitte des phrygischen Volkes

urbem odiis satis est nec poenam traxe per omnem
*Durch den verderblichen Hass sie vertilgt und aufs höchste
*
reliquias Troiae: cineres atque ossa peremptae
*gepeinigt: Troias Rest, das Gebein und die Asche der Toten verfolgt sie.
*
insequitur. causas tanti sciat illa furoris.
*Was zu der grausamen Wut sie treibt, mag selber sie wissen;
*
ipse mihi nuper Libycis tu testis in undis
*Doch du kannst es bezeugen, wie jüngst urplötzlich den argen
*
790



quam molem subito excierit: maria omnia caelo
Lärm in der libyschen Flut sie erregt, wie Himmel und Meer sie

miscuit Aeoliis nequiquam freta procellis,
*Mengte zusammen, umsonst auf Aiolos' Stürme vertrauend;
*
in regnis hoc ausa tuis.
*Dies hat in deinem Gebiet sie gewagt.
*
per scelus ecce etiam Troianis matribus actis
*Sieh, wie die troischen Fraun zum Verbrechen sie eben gestachelt,
*
exussit foede puppis et classe subegit
*Schändlich die Schiffe verbrannt und Aineias' Genossen im fremden
*
795



amissa socios ignotae linquere terrae.
Land durch der Flotte Verlust zurückzubleiben genötigt.

quod superest, oro, liceat dare tuta per undas
*Doch für die übrige Fahrt lass du, ich flehe, mit sichern
*
vela tibi, liceat Laurentem attingere Thybrim,
*Segeln die Flut sie durchziehn und Laurentums Thybris erreichen,
*
si concessa peto, si dant ea moenia Parcae."
*Ist mir gestattet der Wunsch und verleihn dort Mauern die Parzen."
*
Tum Saturnius haec domitor maris edidit alti:
*Drauf antwortete so der saturnische Herrscher der Tiefe:
*
800



"fas omne est, Cytherea, meis te fidere regnis,
"Völlig mit Recht, Cytherea, vertraust du meinem Gebiet dich,

unde genus ducis. merui quoque; saepe furores
*Welchem du selber entstammst; auch hab ich's verdient, da den Ingrimm
*
compressi et rabiem tantam caelique marisque.
*Oft und die rasende Wut von Himmel und Meer ich gebändigt.
*
nec minor in terris, Xanthum Simoentaque testor,
*Auch auf dem Lande, wie Simois mir und Xanthos bezeugen,
*
Aeneae mihi cura tui. cum Troia Achilles
*Hab ich für deinen Aineias gesorgt. Als Achill, der Troianer
*
805



exanimata sequens impingeret agmina muris,
Keuchendem Heer nachsetzend, es hart auf die Mauern zurückwarf,

milia multa daret leto, gemerentque repleti
*Als er zu Tausenden dort sie mordete, seufzend die vollen
*
amnes nec reperire viam atque evolvere posset
*Ströme nicht fanden den Weg und Xanthos' Wirbel das Meer nicht
*
in mare se Xanthus, Pelidae tunc ego forti
*Konnten erreichen - da riss den Aineias, der sich mit Peleus'
*
congressum Aenean nec dis nec viribus aequis
*Tapferem Sohn, ungleich an Kraft und göttlichem Schutz, maß,
*
810



nube cava rapui, cuperem cum vertere ab imo
Ich aus der Schlacht im Gewölk, wiewohl des verrätrischen Troia

structa meis manibus periurae moenia Troiae.
*Mauern, die selbst ich erbaut, aus dem Grund zu schleudern ich wünschte.
*
nunc quoque mens eadem perstat mihi; pelle timores.
*Und noch jetzt ist mein Sinn derselbe; verscheuche die Furcht drum!
*
tutus, quos optas, portus accedet Averni.
*Sicher gelangt er zum Port, den du wünschest; nur einen Genossen
*
unus erit tantum amissum quem gurgite quaeres;
*Wird er verlieren; du magst in Avernus' Strudel ihn suchen.
*
815



unum pro multis dabitur caput."
Nur ein Haupt wird büßen für sämtliche."

his ubi laeta deae permulsit pectora dictis,
*Als so redend der Göttin Brust er erfreut und besänftigt,
*
iungit equos auro genitor, spumantiaque addit
*Schirret die Rosse mit Gold der Erzeuger; mit schäumenden Zügeln
*
frena feris manibusque omnis effundit habenas.
*Zäumt er sie auf und lässt aus der Hand lang schießen die Leinen.
*
caeruleo per summa levis volat aequora curru;
*Leicht fliegt hin auf der obersten Flut sein bläulicher Wagen -
*
820



subsidunt undae tumidumque sub axe tonanti
Still sinkt nieder die Wog', und unter der donnernden Achse

sternitur aequor aquis, fugiunt vasto aethere nimbi.
*Glättet der Schwall sich des Meers; das Gewölk fliegt weit aus dem Aither.
*
tum variae comitum facies, immania cete,
*Sieh, da nahet das bunte Geleit: Meerwunder und Riesen,
*
et senior Glauci chorus Inousque Palaemon
*Glaukos' greises Gefolg und Inos Sohn, Melikertes,
*
Tritonesque citi Phorcique exercitus omnis;
*Phorkys' sämtliches Heer und die hurtige Schar, die Tritonen;
*
825



laeva tenet Thetis et Melite Panopeaque virgo,
Links zieht Thetis und Melite auf, Panopea, die Jungfrau,

Nisaee Spioque Thaliaque Cymodoceque.
*Spio und Nisaia, Kymodoke dann und Thalia.
*
Hic patris Aeneae suspensam blanda vicissim
*Schmeichelnde Lust nun zieht von neuem dem Vater Aineias
*
gaudia pertemptant mentem; iubet ocius omnis
*Durch das besorgte Gemüt. Er befiehlt, gleich sämtliche Masten
*
attolli malos, intendi bracchia velis.
*Aufzurichten und rings an den Rahn zu entrollen die Segel.
*
830



una omnes fecere pedem pariterque sinistros,
Alle zugleich ziehn straff nun die Schoten; sie brassen die Segel

nunc dextros solvere sinus; una ardua torquent
*Alle zugleich, jetzt links, jetzt rechts, gleichmäßig die Hörner
*
cornua detorquentque; ferunt sua flamina classem.
*Toppend und vierend; es fliegt dahin vor dem Winde die Flotte.
*
princeps ante omnis densum Palinurus agebat
*Allen voran auf der Bahn als Führer des dichten Geschwaders
*
agmen; ad hunc alii cursum contendere iussi.
*Zieht Palinurus; es sollen nach ihm sich die übrigen richten.
*
835



iamque fere mediam caeli Nox umida metam
Und schon hatte die tauige Nacht beinahe des Himmels

contigerat, placida laxabant membra quiete
*Mitte berührt; und, unter die Ruder gestreckt, auf den harten
*
sub remis fusi per dura sedilia nautae,
*Bänken erquickten den Leib durch behagliche Ruhe die Schiffer,
*
cum levis aetheriis delapsus Somnus ab astris
*Als sich der flüchtige Schlaf, von des Aithers Gestirnen entgleitend,
*
aëra dimovit tenebrosum et dispulit umbras,
*Bahnte den Weg durch die dunkele Luft und die Schatten zerstreute,
*
840



te, Palinure, petens, tibi somnia tristia portans
Dir, Palinurus, zu nahn, dir traurige Träume zu bringen,

insonti; puppique deus consedit in alta
*Dir, der nichts du verbrachst. Und es setzt sich der Gott auf den hohen
*
Phorbanti similis funditque has ore loquelas:
*Spiegel in Phorbas' Gestalt und ergießt sich in folgende Worte:
*
"Iaside Palinure, ferunt ipsa aequora classem,
*"Iasus' Sohn, Palinurus, das Meer führt selber die Flotte
*
aequatae spirant aurae, datur hora quieti.
*Mit gleichmäßigem Hauch und gönnt dir, ein Stündchen zu ruhen.
*
845



pone caput fessosque oculos furare labori.
Lege das Haupt und entzieh die ermüdeten Augen der Arbeit;

ipse ego paulisper pro te tua munera inibo."
*Lass inzwischen mich selbst dein Geschäft ein Weilchen vertreten."
*
cui vix attollens Palinurus lumina fatur:
*Kaum noch hebend den Blick, antwortet ihm so Palinurus:
*
"mene salis placidi vultum fluctusque quietos
*"Heißt du die ruhige Flut und des Meers friedfertiges Antlitz
*
ignorare iubes? mene huic confidere monstro?
*Mich misskennen? Ich soll noch baun auf die Tücke des Untiers?
*
850



Aenean credam - quid enim? - fallacibus auris
Was? Ich soll den Aineias den trügrischen Winden vertrauen?

et caeli totiens deceptus fraude sereni?"
*Ich, so häufig getäuscht durch die Bosheit des heiteren Himmels?"
*
talia dicta dabat, clavumque adfixus et haerens
*Also sprach er und ließ, sich fest anklammernd, das Steuer
*
nusquam amittebat oculosque sub astra tenebat.
*Nie aus der Hand und hielt zu den Sternen die Augen erhoben.
*
ecce deus ramum Lethaeo rore madentem
*Siehe, da schüttelt der Gott ein Reis, von lethäischem Taue
*
855



vique soporatum Stygia super utraque quassat
Triefend, durch stygische Kraft mit Schlummer geschwängert, um beide

tempora, cunctantique natantia lumina solvit.
*Schläfen, es senken sofort sich des Zaudernden schwimmende
*
vix primos inopina quies laxaverat artus,
*Blicke. Kaum dass der plötzliche Schlaf ihm die Spannkraft löste der Glieder,
*
et super incumbens cum puppis parte revulsa
*Als er sich über ihn legt und mit brechenden Stücken des Spiegels
*
cumque gubernaclo liquidas proiecit in undas
*Und mit dem Steuer ihn selbst hinab in die flutenden Wogen
*
860



praecipitem ac socios nequiquam saepe vocantem;
Köpflings stürzt, wo er laut, doch umsonst zurief den Genossen;

ipse volans tenuis se sustulit ales ad auras.
*Doch hoch schwang der geflügelte Gott in die flüchtige Luft sich
*
currit iter tutum non setius aequore classis
*Gleichwohl zieht durch das Meer in sicheren Bahnen die Flotte,
*
promissisque patris Neptuni interrita fertur.
*Sonder Gefahr und Schreck, wie Vater Neptun es verheißen.
*
iamque adeo scopulos Sirenum advecta subibat,
*Und schon nahte sie sich auf der Fahrt dem Geklipp der Sirenen
*
865



difficilis quondam multorumque ossibus albos;
- Einst ein schwieriger Strand und bleich von vielen Gebeinen;

tum rauca adsiduo longe sale saxa sonabant,
*Auch scholl rauh weithin von beständiger Brandung das Felsriff-:
*
cum pater amisso fluitantem errare magistro
*Als Aineias bemerkt, dass das Schiff unsicheren Laufes
*
sensit, et ipse ratem nocturnis rexit in undis
*Schwanke, des Führers beraubt, und es selbst durch die nächtliche Flut lenkt,
*
multa gemens casuque animum concussus amici:
*Oft aufseufzend, aufs tiefste bewegt durch den Tod des Genossen:
*
870






"o nimium caelo et pelago confise sereno,
"Ach, der dem heiteren Meer und Himmel zu sehr du vertrautest,

nudus in ignota, Palinure, iacebis harena."
*Nackt nun wirst, Palinurus, auf fremdem Gestade du liegen.
*
