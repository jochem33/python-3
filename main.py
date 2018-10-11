import os

EXTENSIE = '.wrd'
MAX_WOORDLENGTE = 20
SCHEIDER = '='
SCHERMBREEDTE = 80
HALVESCHERMBREEDTE = SCHERMBREEDTE / 2
SCHERMHOOGTE = 15
menuregels = 0

# tekens voor UI
ZIJKANT = "|"
ONDERKANT = "="
BOVENKANT = "="

# acties:
NIEUWE_LIJST = 'n'
OVERHOREN = 'o'
WIJZIGEN = "e"
STOPPEN = 'q'

# acties in edit menu
REGELSVERWIJDEREN = "d"
FILEVERWIJDEREN = "del"
REGELSTOEVOEGEN = "a"

RECENTELIJSTENFILENAAM = "recentelijsten.lists"


def readfile(path):
    with open(path) as file:
        filelines = file.read().split("\n")

    return filelines


def writefile(path, lines, writeoradd):
    file = open(path, writeoradd)

    for line in lines:
        file.write(line)
        file.write("\n")

    file.close()


def initialiseerrecente_lijsten():
    recentelijsten = []

    try:
        recentelijsten = readfile(RECENTELIJSTENFILENAAM)
    except FileNotFoundError:
        pass

    return recentelijsten


def printbody():
    menuregel("Welkom bij Jochem's overhoor programma!")
    menuregel("Type een van de volgende letters om de bijstaande actie uit te voeren:")
    menuregel("Nieuwe lijst: " + NIEUWE_LIJST)
    menuregel("Overhoren: " + OVERHOREN)
    menuregel("Wijzigen: " + WIJZIGEN)
    menuregel("Stoppen (Kan altijd gebruikt worden): " + STOPPEN)


def leesinvoer():
    clear()
    printheader()
    printbody()
    printfooter()
    gekozenactie = input("Kies actie: ")
    clear()
    return gekozenactie


def main():
    recentelijsten = initialiseerrecente_lijsten()
    gekozenactie = leesinvoer()
    mainfunctiesdict = {"n":nieuwelijst, "o":overhoor, "e":wijzigen}

    while gekozenactie != STOPPEN:
        try:
            mainfunctiesdict[gekozenactie](recentelijsten)
        except KeyError:
            alert("Sorry, we hebben je niet helemaal begrepen, probeer het nog een keer: ")

        gekozenactie = leesinvoer()


def printnieuwelijstinstructies():
    printheader()
    menuregel("type woorden gescheiden door \"=\".")
    menuregel("Voorbeeld: \"to walk=lopen\"")
    printfooter()


def nieuwelijst(recentelijsten):
    printnieuwelijstinstructies()

    woordenlijst = woordenvoornieuwelijsttypen()

    savefile(woordenlijst)


def woordenvoornieuwelijsttypen():
    woordenlijst = {}
    nogsplitten = input()
    while nogsplitten not in ["", "q"]:
        try:
            woord1, woord2 = nogsplitten.split(SCHEIDER)
            woordenlijst[woord1] = woord2
        except ValueError:
            print("Je hebt iets niet goed opgegeven!")
        nogsplitten = input()

    clear()
    return woordenlijst


def savefile(woordenlijst):
    printheader()
    menuregel("Onder welke naam wil je de lijst opslaan?")
    menuregel("Type \"NEE\" om de lijst niet op te slaan ")
    printfooter()

    filename = input("naam: ")

    if filename == "NEE":
        alert("Je file word niet opgeslagen!")
    else:
        filename = filename + EXTENSIE
        lines = []

        for key in woordenlijst:
            lines.append(key + "=" + woordenlijst[key])

        writefile(filename, lines, "w")

        alert("Je nieuwe lijst is opgeslagen als " + filename)


def zetoverhoorfileindict(gekozenfile):
    bestandsdata = readfile(gekozenfile)

    overhoordict = {}
    for item in bestandsdata:
        if not item == "":
            woord1, woord2 = item.split("=")
            overhoordict[woord1] = woord2

    return overhoordict


def printoverhoorinstructiesvertalen(key, goed, fout, overhoordict):
    clear()
    printheader()
    menuregel("Vertaal: ")
    menuregel(key)
    menuregel("")
    menuregel("Goed: " + str(goed))
    menuregel("Fout: " + str(fout))
    menuregel("Nog te gaan: " + str(len(overhoordict.keys()) - goed - fout))
    printfooter()


def overhoorloop(overhoordict):
    goed = 0
    fout = 0

    for key in overhoordict:
        printoverhoorinstructiesvertalen(key, goed, fout, overhoordict)
        geradenwoord = input(key + " = ")

        if geradenwoord == overhoordict[key]:
            alert("Dat is goed!")
            goed += 1
        else:
            alert("Helaas! Dat is fout, het moest zijn: " + overhoordict[key])
            fout += 1

    return goed, fout


def berekenscore(goed, fout):
    totaalaantalvragen = goed + fout
    score = goed / totaalaantalvragen * 100
    alert("Je hebt " + str(score) + "% goed!")


def printoverhoorinstructies(recentelijsten):
    printheader()

    menuregel("Welke lijst wil je laten overhoren?")
    printrecentelijsten(recentelijsten)

    printfooter()

    gekozenfile = openrecentelijsten()
    return gekozenfile


def overhoor(recentelijsten):
    gekozenfile = printoverhoorinstructies(recentelijsten)

    if gekozenfile != "":
        overhoordict = zetoverhoorfileindict(gekozenfile)

        alert("We gaan nu " + gekozenfile + " overhoren.")
        goed, fout = overhoorloop(overhoordict)

        berekenscore(goed, fout)


def regelstoevoegen(gekozenfile):
    clear()
    printheader()
    menuregel("Type regels gescheiden door enters: ")
    printfooter()

    i = 0
    regels = []

    regel = input(str(i) + ". ")
    while regel not in ["", "q"]:
        i += 1
        regels.append(regel)
        regel = input(str(i) + ". ")

    writefile(gekozenfile, regels, "a")

    alert("Regels toegevoegd!")


def vraagomverwijderregels(regels):
    regelindex = input()
    while regelindex not in ["", "q"]:
        try:
            regelindex = int(regelindex) - 1
            del regels[regelindex]
        except ValueError:
            print("geen nummer")
        except IndexError:
            print("regel bestaat niet")
        regelindex = input()

    return regels


def regelsverwijderen(gekozenfile):
    regels = readfile(gekozenfile)

    clear()
    printheader()
    menuregel("Geef de nummers van de regels die je wilt verwijderen.")
    menuregel("(Elk nummer op een nieuwe regel)")
    printfooter()

    vraagomverwijderregels(regels)

    writefile(gekozenfile, regels, "w")


def fileverwijderen(gekozenfile):
    clear()
    printheader()
    menuregel("Weet je zeker dat je deze file wilt verwijderen?")
    printfooter()
    verwijderenvraag = input("[y/n]")

    if verwijderenvraag == "y" and os.path.isfile(gekozenfile):
        os.remove(gekozenfile)
        alert("Je file is verwijderd!")
    elif verwijderenvraag == "n":
        alert("De file word niet verwijderd")
    else:
        alert("Dat is geen \"y\" of \"n\"!")


def printwijzigentekst(recentelijsten):
    printheader()
    menuregel("Welke file wil je wijzigen?")
    printrecentelijsten(recentelijsten)
    printfooter()
    gekozenfile = openrecentelijsten()
    return gekozenfile


def printbewerkingen():
    printheader()

    menuregel("Je kan een van de volgende bewerkingen doen: ")
    menuregel("Regels toevoegen: " + REGELSTOEVOEGEN)
    menuregel("Regels verwijderen: " + REGELSVERWIJDEREN)
    menuregel("File verwijderen: " + FILEVERWIJDEREN)

    printfooter()


def wijzigen(recentelijsten):
    gekozenfile = printwijzigentekst(recentelijsten)

    clear()

    printbewerkingen()
    gekozenactie = input("Kies bewerking: ")
    wijzigingendict = {REGELSTOEVOEGEN: regelstoevoegen, REGELSVERWIJDEREN: regelsverwijderen, FILEVERWIJDEREN: fileverwijderen}

    if gekozenactie != STOPPEN:
        try:
            wijzigingendict[gekozenactie](gekozenfile)
        except KeyError:
            alert("Sorry, we hebben je niet helemaal begrepen, probeer het nog een keer. ")


def afscheid():
    alert("doei")


def addrecentelijst(naam):
    writefile(RECENTELIJSTENFILENAAM, [naam + "\n"], "a")


def printrecentelijsten(recentelijsten):
    recentelijsten.clear()

    try:
        recentelijsten = readfile(RECENTELIJSTENFILENAAM)
    except FileNotFoundError:
        menuregel("Geen recente lijsten gevonden")

    for i in range(len(recentelijsten)):
        menuregel(str(i + 1) + ". " + recentelijsten[i - 1])


def openrecentelijstennummer(keuze, recentelijstenlijst):
    keuze = int(keuze)
    keuze -= 1

    try:
        gekozenfile = recentelijstenlijst[keuze]
        return gekozenfile
    except ValueError:
        alert("[ERROR] File not found")
    except IndexError:
        alert("[ERROR] regel bestaat niet")


def openrecentelijstenpath(keuze, recentelijstenlijst):
    gekozenfile = keuze
    if gekozenfile not in recentelijstenlijst:
        addrecentelijst(gekozenfile)

    return gekozenfile


def openrecentelijsten():
    keuze = input()
    gekozenfile = ""
    print(keuze)

    if os.path.isfile(RECENTELIJSTENFILENAAM):
        recentelijstenlijst = readfile(RECENTELIJSTENFILENAAM)

        if keuze.isdigit():
            gekozenfile = openrecentelijstennummer(keuze, recentelijstenlijst)

        if os.path.isfile(keuze):
            gekozenfile = openrecentelijstenpath(keuze, recentelijstenlijst)

    return gekozenfile


def printheader():
    header = str(BOVENKANT * SCHERMBREEDTE) + "\n{0:<{1}}{2:>{3}}"
    print(header.format(ZIJKANT, int(HALVESCHERMBREEDTE), ZIJKANT, int(HALVESCHERMBREEDTE)))


def printfooter():
    for i in range(SCHERMHOOGTE - menuregels - 4):
        zijkant = "{0:<{1}}{2:>{3}}"
        print(zijkant.format(ZIJKANT, int(HALVESCHERMBREEDTE), ZIJKANT, int(HALVESCHERMBREEDTE)))
    footer = "{0:<{1}}{2:>{3}}\n" + str(ONDERKANT * SCHERMBREEDTE)
    print(footer.format(ZIJKANT, int(HALVESCHERMBREEDTE), ZIJKANT, int(HALVESCHERMBREEDTE)))


def menuregel(tekst):
    regel = "{0:<2}{1:" + str(SCHERMBREEDTE - 3) + "}{2}"
    print(regel.format(ZIJKANT, tekst, ZIJKANT))
    global menuregels
    menuregels += 1
    return regel


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    global menuregels
    menuregels = 0


def alert(tekst):
    clear()
    printheader()
    menuregel(tekst)
    printfooter()
    input("Type ENTER om door te gaan")


main()
