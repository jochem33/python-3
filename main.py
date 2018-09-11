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


recentelijstenfilenaam = "recentelijsten.lists"
recentelijsten = []


def main():
    clear()

    printheader()

    menuregel("Welkom bij Jochem's overhoor programma!")
    menuregel("Type een van de volgende letters om de bijstaande actie uit te voeren:")
    menuregel("Nieuwe lijst: " + NIEUWE_LIJST)
    menuregel("Overhoren: " + OVERHOREN)
    menuregel("Wijzigen: " + WIJZIGEN)
    menuregel("Stoppen (Kan altijd gebruikt worden): " + STOPPEN)

    printfooter()
    gekozenactie = input("Kies actie: ")

    clear()

    if gekozenactie == NIEUWE_LIJST:
        nieuwelijst()
    elif gekozenactie == OVERHOREN:
        overhoor()
    elif gekozenactie == WIJZIGEN:
        wijzigen()
    elif gekozenactie == STOPPEN:
        afscheid()
    else:
        alert("Sorry, we hebben je niet helemaal begrepen, probeer het nog een keer: ")
    if gekozenactie != STOPPEN:
        main()


def nieuwelijst():
    doorgaan = True
    woordenlijst = {}

    printheader()
    menuregel("type woorden gescheiden door \"=\" (geen spaties!)")
    printfooter()

    while doorgaan:
        nogsplitten = input()
        if nogsplitten == STOPPEN:
            doorgaan = False
            break
        elif nogsplitten != STOPPEN and SCHEIDER in nogsplitten:
            woord1, woord2 = nogsplitten.split(SCHEIDER)
            print(woord1 + ", " + woord2)
            woordenlijst[woord1] = woord2
        else:
            print("Je hebt iets niet goed opgegeven!")

    clear()

    printheader()
    menuregel("Onder welke naam wil je de lijst opslaan?")
    menuregel("Type \"NEE\" om de lijst niet op te slaan ")
    menuregel("Vergeet niet " + EXTENSIE + " acter je filenaam te zetten!")
    printfooter()

    filename = input("naam: ")
    if filename != "NEE":
        file = open(filename, 'w')

        for key in woordenlijst:
            file.write(key + "=" + woordenlijst[key])
            file.write("\n")

        file.close()
        addrecentelijst(filename)
        alert("Je nieuwe lijst is opgeslagen als " + filename)
    else:
        alert("Je file word niet opgeslagen!")

    main()


def overhoor():
    printheader()

    menuregel("Welke lijst wil je laten overhoren?")
    printrecentelijsten()

    printfooter()

    gekozenfile = openrecentelijsten()

    if gekozenfile != "":
        alert("We gaan nu " + gekozenfile + " overhoren.")

        overhoordict = {}
        goed = 0
        fout = 0

        with open(gekozenfile) as overhoorfile:
            bestandsdata = overhoorfile.read().split('\n')

        for item in bestandsdata:
            if not item == '':
                woord1, woord2 = item.split("=")
                overhoordict[woord1] = woord2

        for key in overhoordict:
            clear()
            printheader()
            menuregel("Vertaal: ")
            menuregel(key)
            menuregel("")
            menuregel("Goed: " + str(goed))
            menuregel("Fout: " + str(fout))
            menuregel("Nog te gaan: " + str(len(overhoordict.keys()) - goed - fout))
            printfooter()
            geradenwoord = input(key + " = ")

            if geradenwoord == overhoordict[key]:
                alert("Dat is goed!")
                goed += 1
            else:
                alert("Helaas! Dat is fout, het moest zijn: " + overhoordict[key])
                fout += 1

        totaalaantalvragen = goed + fout
        score = goed / totaalaantalvragen * 100
        alert("Je hebt " + str(score) + "% goed!")

    main()


def wijzigen():

    def regelstoevoegen():
        clear()
        printheader()
        menuregel("Type regels gescheiden door enters: ")
        printfooter()

        regels = []
        i = 0

        while True:
            regel = input(str(i) + ". ")
            if regel != "":
                regels.append(regel)
            else:
                break
            i += 1

        file = open(gekozenfile, 'a')

        for item in regels:
            file.write(item + "\n")
        file.close()

        alert("Regels toegevoegd!")

    def regelsverwijderen():
        with open(gekozenfile) as file:
            bestandsdata = file.read().split('\n')

        clear()
        printheader()
        menuregel("Geef de nummers van de regels die je wilt verwijderen.")
        menuregel("(Elk nummer op een nieuwe regel)")
        printfooter()

        while True:
            regelindex = input()
            if regelindex != "" and regelindex != "q":
                if regelindex.isdigit():
                    regelindex = int(regelindex) - 1
                    if len(bestandsdata) >= regelindex >= 0:
                        del bestandsdata[regelindex]
                    else:
                        print("Die regel bestaat niet!")
                else:
                    print("Dat is geen regelnummer")
            else:
                alert("Regels verwijderd!")
                break

        file = open(gekozenfile, 'w')

        for item in bestandsdata:
            file.write(item + "\n")

        file.close()

    def fileverwijderen():
        clear()
        printheader()
        menuregel("Weet je zeker dat je deze file wilt verwijderen?")
        printfooter()
        verwijderenvraag = input("[y/n]")

        if verwijderenvraag == "y":
            if os.path.isfile(gekozenfile):
                os.remove(gekozenfile)
                alert("Je file is verwijderd!")
        elif verwijderenvraag == "n":
            alert("De file word niet verwijderd")
        else:
            alert("Dat is geen \"y\" of \"n\"!")

    # bewerking kiezen

    printheader()
    menuregel("Welke file wil je wijzigen?")
    printrecentelijsten()
    printfooter()
    gekozenfile = openrecentelijsten()

    clear()

    if "" != gekozenfile:
        printheader()

        menuregel("Je kan een van de volgende bewerkingen doen: ")
        menuregel("Regels toevoegen: " + REGELSTOEVOEGEN)
        menuregel("Regels verwijderen: " + REGELSVERWIJDEREN)
        menuregel("File verwijderen: " + FILEVERWIJDEREN)

        printfooter()

        gekozenactie = input("Kies bewerking: ")

        if gekozenactie == REGELSTOEVOEGEN:
            regelstoevoegen()
        elif gekozenactie == REGELSVERWIJDEREN:
            regelsverwijderen()
        elif gekozenactie == FILEVERWIJDEREN:
            fileverwijderen()
        elif gekozenactie == STOPPEN:
            main()
        else:
            print("Sorry, we hebben je niet helemaal begrepen, probeer het nog een keer: ")
            main()
    else:
        alert("[ERROR] 404 file not found")

    main()


def afscheid():
    print("doei")


def addrecentelijst(naam):
    recentelijstenfile = open(recentelijstenfilenaam, 'a')

    recentelijstenfile.write(naam + "\n")

    recentelijstenfile.close()


def printrecentelijsten():
    leesrecentelijstenfile()

    for i in range(len(recentelijsten)):
        menuregel(str(i + 1) + ". " + recentelijsten[i - 1])


def openrecentelijsten():
    keuze = input()
    gekozenfile = ""

    if keuze.isdigit():
        keuze = int(keuze)
        keuze -= 1

        with open(recentelijstenfilenaam) as recentelijstenfile:
            bestandsdata = recentelijstenfile.read().split("\n")

        if keuze <= len(bestandsdata):
            if keuze >= 0:
                if os.path.isfile(bestandsdata[keuze]):
                    gekozenfile = bestandsdata[keuze]
                else:
                    alert("[ERROR] 404 file not found")
            else:
                alert("[ERROR] 404 file not found")
        else:
            alert("[ERROR] 404 file not found")

    elif os.path.isfile(keuze):
        gekozenfile = keuze

    else:
        alert("We hebben je keuze niet kunnen vinden")

    return gekozenfile


def leesrecentelijstenfile():
    recentelijsten.clear()

    if os.path.isfile(recentelijstenfilenaam):
        recentelijstenfile = open(recentelijstenfilenaam)

        for line in recentelijstenfile:
            recentelijsten.append(line.strip("\n"))

        recentelijstenfile.close()
    else:
        menuregel("Geen recente lijsten gevonden")


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


leesrecentelijstenfile()

main()
