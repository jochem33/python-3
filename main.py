import os


EXTENSIE = '.wrd'
MAX_WOORDLENGTE = 20
SCHEIDER = '='
SCHERMBREEDTE = 80
SCHERMHOOGTE = 40
STANDAARD_LIJST = 'EN-NED'

# acties:
NIEUWE_LIJST = 'n'
OVERHOREN = 'o'
WIJZIGEN = "e"
STOPPEN = 'q'


recentelijstenfilenaam = "recentelijsten.lists"
recentelijsten = []


def main():
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

    print("Onder welke naam wil je de lijst opslaan? \nType \"NEE\" om de lijst niet op te slaan \nVergeet niet " + EXTENSIE + " acter je filenaam te zetten!")
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
    leesrecentelijstenfile()

    print("Welke lijst wil je laten overhoren?\n" +
          "Recente lijsten: ")

    i = 0
    for item in recentelijsten:
        print(str(i + 1) + ". " + recentelijsten[i])
        i += 1

    print("Kies een getal van een recente file of geef een filenaam op")

    keuze = input()
    gekozenfile = ""

    if keuze.isdigit():
        keuze = int(keuze)
        keuze -= 1

        with open(recentelijstenfilenaam) as recentelijstenfile:
            bestandsdata = recentelijstenfile.read().split("\n")

        if os.path.isfile(bestandsdata[keuze]):
            gekozenfile = bestandsdata[keuze]
        else:
            print("[ERROR] 404 file not found")

    elif os.path.isfile(keuze):
        gekozenfile = keuze

    else:
        print("We hebben je keuze niet kunnen vinden")

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
    print("dip")

    main()


def afscheid():
    print("doei")


def addrecentelijst(naam):
    recentelijstenfile = open(recentelijstenfilenaam, 'a')

    recentelijstenfile.write(naam + "\n")

    recentelijstenfile.close()


def leesrecentelijstenfile():
    recentelijsten.clear()

    if os.path.isfile(recentelijstenfilenaam):
        recentelijstenfile = open(recentelijstenfilenaam)

        for line in recentelijstenfile:
            recentelijsten.append(line)

        recentelijstenfile.close()
    else:
        print("Geen recente lijsten gevonden")


leesrecentelijstenfile()

main()
