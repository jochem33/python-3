import os

EXTENSIE = '.wrd'
MAX_WOORDLENGTE = 20
SCHEIDER = '='
SCHERMBREEDTE = 80
HALVESCHERMBREEDTE = SCHERMBREEDTE / 2
SCHERMHOOGTE = 40


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
    printheader()

    printfooter()
    gekozenactie = input("Kies actie: ")
    if gekozenactie == NIEUWE_LIJST:
        nieuwelijst()
    elif gekozenactie == OVERHOREN:
        overhoor()
    elif gekozenactie == WIJZIGEN:
        wijzigen()
    elif gekozenactie == STOPPEN:
        afscheid()
    else:
        print("Sorry, we hebben je niet helemaal begrepen, probeer het nog een keer: ")
    if gekozenactie != STOPPEN:
        main()


def nieuwelijst():
    doorgaan = True
    woordenlijst = {}

    print("type woorden gescheiden door \"=\" (geen spaties!)")

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

    print(
        "Onder welke naam wil je de lijst opslaan? \nType \"NEE\" om de lijst niet op te slaan \nVergeet niet " + EXTENSIE + " acter je filenaam te zetten!")
    filename = input("naam: ")
    if filename != "NEE":
        file = open(filename, 'w')

        for key in woordenlijst:
            file.write(key + "=" + woordenlijst[key])
            file.write("\n")

        file.close()
        addrecentelijst(filename)
        print("Je nieuwe lijst is opgeslagen als " + filename)

    main()


def overhoor():
    print("Welke lijst wil je laten overhoren?\n")

    gekozenfile = printrecentelijsten(True)

    if gekozenfile != "":
        print("We gaan nu " + gekozenfile + " overhoren.")

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
            print("\n" * 2)
            geradenwoord = input(key + " = ")
            print("\n" * 2)

            if geradenwoord == overhoordict[key]:
                print("Dat is goed!")
                goed += 1
            else:
                print("Helaas! Dat is fout, het moest zijn: " + overhoordict[key])
                fout += 1

        totaalaantalvragen = goed + fout
        score = goed / totaalaantalvragen * 100
        print("Je hebt " + str(score) + "% goed!")

    main()


def wijzigen():

    def regelstoevoegen():
        print("Type regels gescheiden door enters: ")

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
        print("Regels toegevoegd")

    def regelsverwijderen():
        with open(gekozenfile) as file:
            bestandsdata = file.read().split('\n')

        print("Geef de nummers van de regels die je wilt verwijderen. (Elk nummer op een nieuwe regel)")

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
                print("Regels verwijderd")
                break

        file = open(gekozenfile, 'w')

        for item in bestandsdata:
            file.write(item + "\n")

        file.close()

    def fileverwijderen():
        verwijderenvraag = input("Weet je zeker dat je deze file wilt verwijderen? [y/n]")

        if verwijderenvraag == "y":
            if os.path.isfile(gekozenfile):
                os.remove(gekozenfile)
                print("Je file is verwijderd")
        elif verwijderenvraag == "n":
            print("De file word niet verwijderd")

    # bewerking kiezen

    print("Welke file wil je wijzigen?")
    gekozenfile = printrecentelijsten(True)

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

    main()


def afscheid():
    print("doei")


def addrecentelijst(naam):
    recentelijstenfile = open(recentelijstenfilenaam, 'a')

    recentelijstenfile.write(naam + "\n")

    recentelijstenfile.close()


def printrecentelijsten(openen):
    leesrecentelijstenfile()

    i = 0
    for item in recentelijsten:
        print(str(i + 1) + ". " + recentelijsten[i])
        i += 1

    if openen:
        print("Kies een getal van een recente file of geef een filenaam op")

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
                    print("[ERROR] 404 file not found")
            else:
                print("[ERROR] 404 file not found")
        else:
            print("[ERROR] 404 file not found")

    elif os.path.isfile(keuze):
        gekozenfile = keuze

    else:
        print("We hebben je keuze niet kunnen vinden")

    return gekozenfile


def leesrecentelijstenfile():
    recentelijsten.clear()

    if os.path.isfile(recentelijstenfilenaam):
        recentelijstenfile = open(recentelijstenfilenaam)

        for line in recentelijstenfile:
            recentelijsten.append(line)

        recentelijstenfile.close()
    else:
        print("Geen recente lijsten gevonden")


def printheader():
    header = str(BOVENKANT * SCHERMBREEDTE) + "\n{0:<{1}}{2:>{3}}"
    print(header.format(ZIJKANT, int(HALVESCHERMBREEDTE), ZIJKANT, int(HALVESCHERMBREEDTE)))


def printfooter():
    footer = "{0:<{1}}{2:>{3}}\n" + str(ONDERKANT * SCHERMBREEDTE)
    print(footer.format(ZIJKANT, int(HALVESCHERMBREEDTE), ZIJKANT, int(HALVESCHERMBREEDTE)))


leesrecentelijstenfile()

main()
