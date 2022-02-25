# Feb 2022
# Katarzyna Gruszczynska
# UJ FAIS IGK
#
# TSP - Problem komiwojazera
#
import sys
import numpy as np
import random
import matplotlib.pyplot as plt

# ile miast
N = 100
# ile osobnikow poczatkowych
# ile_osobnikow = 6
# populacja poczatkowa osobnikow
# population = []
# tabela kosztow podrozy
# koszty = []
# max liczba pokolen, threshold, stop condition
# maxGenerations = 600

# generowanie tabeli kosztow podrozy
# wartosci kosztow 10$ - 99$
# losowa macierz symetryczna
def generateCostTable(N):
    b = np.random.randint(10,99,size=(N,N),dtype=int)  
    b_symm = (b + b.T)/2
    return b_symm

# generowanie ile osobnikow poczatkowych = 50
def generatePopulation(ile_osobnikow):
    population = []
    i = 0
    while i < ile_osobnikow:
        print("+ nowy osobnik", i)
        # nie zaczynamy z tego samego miasta
        # ten generator chyba zapewnia rozne wartosci w liscie generowanej
        # jednak -1 bo zawsze mamy zaczynac z tego samego czy nie trzeba z tego samego ??
        # !! zapewnic zeby byly unikalne wartosci na liscie !!! bo nie moze 2 rzy odwiedzac tego samego !!
        population.append(random.sample(range(0, N, 1), N))
        i += 1
    print("Populacja, osobników: ", len(population))
    print(population)
    return population

# funkcja dopasowania, Fitness function - koszt podrozy
# dla pojedynczego osobnika, n - numer osobnika
def fnDopasowania(population, costTable, n):
    cost = 0
    # dl=len(osobnik)-1 - liczba miast -1 czyli N-1
    i = 0
    for i in range(N-1): 
        print(i)
        print(population[n][i], "->", population[n][i+1])
        cost += costTable[population[n][i], population[n][i+1]]
        print(costTable[population[n][i], population[n][i+1]])
    print("Koszt podrozy: ", cost)
    return cost

# policz koszty dla wszystkich osobnikow w populacji
# znajdz minimalny
def minKosztPodrozy(population, costTable):
    minKoszt = 0
    kosztyOsobnikow = []
    n = 0
    print("len(population) ----> ", len(population))
    for n in range(0, len(population)):
        kosztyOsobnikow.append(fnDopasowania(population, costTable, n))
        print("Koszt dla osobnika", n ,":", kosztyOsobnikow[n])
    print("Koszty osobnikow", kosztyOsobnikow)
    minKoszt = min(kosztyOsobnikow)
    print("Koszt minimalny/najkrotsza trasa", minKoszt)
    return minKoszt

# selekcja turniejowa
# The term “binary tournament” refers to the size of two in a tournament, 
# which is the simplest form of tournament selection [3]. 
# Binary tournament selection (BTS) starts by selecting two individuals at random.
# Then, fitness values of these individuals are evaluated. 
# The one having more satisfactory fitness is then chosen.
# https://www.hindawi.com/journals/mpe/2016/3672758/
def binTounamentSelection(population, costTable):
    # do turnieju 1:1 wylosowac osobnikow
    pair = random.sample(range(0, len(population)), 2)  # ile_osobnikow
    print("para", pair)
    print("population", population)

    if fnDopasowania(population, costTable, pair[0]) < fnDopasowania(population, costTable, pair[1]):
        rodzic = population[pair[0]].copy()  #debug
        print("rodzic to osobnik nr", pair[0], population[pair[0]])
        print("osobnik usuniety nr", pair[1], population[pair[1]])
        # mozna tez usunac rodzica z populacji - czyli "przeniesc" do pula
        # bo sie powtarza ten sam - ale moze byc ...
        del population[pair[1]]
    else:
        rodzic = population[pair[1]].copy()  #debug
        print("rodzic to osobnik nr", pair[1], population[pair[1]])
        print("osobnik usuniety nr", pair[0], population[pair[0]])
        # mozna tez usunac rodzica z populacji - czyli "przeniesc" do pula
        # bo sie powtarza ten sam - ale moze byc ...
        del population[pair[0]]

    print(population)

    return rodzic

# krzyzowanie osobnikow - jednopunktowe
def crossOver(rodzic1_val, rodzic2_val):
    # losowy punkt krzyzowania
    crossPoint = random.randint(1, N-2)
    print("crossPoint", crossPoint)

    print("TEMP ----> rodzic1", rodzic1_val, "rodzic2", rodzic2_val)
    rodzic1 = list(rodzic1_val)
    rodzic2 = list(rodzic2_val)

    print("start ----> rodzic1", rodzic1, "rodzic2", rodzic2)

    rodzic1_orig = list(rodzic1)
    rodzic2_orig = list(rodzic2)
    print("start kopia ---->  rodzic1_orig", rodzic1_orig, "rodzic2_orig", rodzic2_orig)

    dzieci = []
    # aby rozwiazanie bylo valid nie moga sie miasta powtarzac
    # usunac te wylosowane 
    cr = crossPoint # od 0 do N-1
    end = N - 1 - crossPoint
    print("end",end)
    i=0
    for i in range(end):
        print("i", i, "cr", cr, "crossPoint+1", crossPoint+1, "wartosc rodzica1", rodzic1[crossPoint+1+i])
        rodzic2.remove(rodzic1[crossPoint+1+i])
        print("usunelem! z rodzica 2")
        print("rodzic1", rodzic1, "rodzic2", rodzic2)
        cr += 1
        i += 1
    print("teraz extenduj!")
    print("extend part",rodzic1[crossPoint+1:])
    temp = rodzic1[crossPoint+1:]
    print("extend part temp", temp)
    temp.reverse()
    print("extend part reversed -> ", temp)
    reversed = rodzic2 + temp  
    dzieci.append(reversed)
    print("dzieci", dzieci)
    
    print("PRZED reset ---> rodzic1", rodzic1, "rodzic2", rodzic2)

    rodzic1 = list(rodzic1_orig)
    rodzic2 = list(rodzic2_orig)
    
    print("crossPoint", crossPoint)
    print("reset ---> rodzic1_orig", rodzic1_orig, "rodzic2_orig", rodzic2_orig)
    print("reset ---> rodzic1", rodzic1, "rodzic2", rodzic2)

    cr = crossPoint # od 0 do N-1
    end = N - 1 - crossPoint
    print("end",end)
    i=0
    for i in range(end):
        print("i", i, "cr", cr, "crossPoint+1", crossPoint+1, "wartosc rodzica2", rodzic2[crossPoint+1+i])
        rodzic1.remove(rodzic2[crossPoint+1+i])
        print("usunelem! z rodzica 1")
        print("rodzic1", rodzic1, "rodzic2", rodzic2)
        cr += 1
        i += 1
    print("teraz extenduj!")
    print("extend part",rodzic2[crossPoint+1:])
    temp = rodzic2[crossPoint+1:]
    print("extend part temp", temp)
    temp.reverse()
    print("extend part reversed -> ", temp)
    reversed = rodzic1 + temp
    dzieci.append(reversed)
    print("dzieci", dzieci)

    print("PRZED reset ---> rodzic1", rodzic1, "rodzic2", rodzic2)

    rodzic1 = list(rodzic1_orig)
    rodzic2 = list(rodzic2_orig)

    print("koniec fn co")
    print("reset ---> rodzic1", rodzic1, "rodzic2", rodzic2)
    print("reset ---> rodzic1_orig", rodzic1_orig, "rodzic2_orig", rodzic2_orig)

    return dzieci

# tworz nowe pokolenie
# z puli rodzicow po kolei bierz
# crossOver(rodzic1, rodzic2)
def krzyzowanieRodzicow(rodzice):
    newGeneration=[]

    for i in range(len(rodzice)-1):
        print("krzyzowanie")
        dzieci = crossOver(rodzice[i],rodzice[i+1])
        newGeneration.append(dzieci[0])
        newGeneration.append(dzieci[1])
    return newGeneration

# ewolucja 
def evolution(population, rodzice, costTable):
    # a moze doopuki populacja biedzie pusta ??
    # bo zostaly w populacji niewylosowane !?
    # nie ograniczac ilosciowo - ucinac
    # tylko algorytm ma dzialac jak dziala turniejowo
    # az wybije albo przeniesie wszystkich
    # do ostatniej nogi :D
    # ten co zostaje sam jeden w populacji to wyginie

    # wybranie puli rodzicow
    while len(population) >= 2:
        print("while len populacji:", len(population), population)
        rodzice.append(binTounamentSelection(population, costTable))

    print("pula rodzicow:", len(rodzice), rodzice)
    print("ile osobnikow zostalo w populacji poczatkowej - wygina!:", len(population), population)

    newGeneration = krzyzowanieRodzicow(rodzice)

    print("evolution ---> newGeneration", newGeneration)

    # zwroc dzieci czyli nowe pokolenie
    return newGeneration

def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

# def inwersja(list, genes):
#     list[genes[0]:genes[1]].reverse
#     return list

# mutacja - 1:1000 osobników
def mutation(newGeneration, mutationRate):

    # wzajemna wymiana (wybranie dwóch miast i zamienienie ich ze sobą)

    # do mutacji wybierac 1 osobnika na n-osobnikow, wg mutationRate
    i = 0
    while (mutationRate < len(newGeneration)):
        mutowany = random.randint(i, mutationRate)
        # do mutacji wylosowac pare genow osobnika
        genes = random.sample(range(0, N), 2)
        print("geny do mutacji:", genes)
        # zamiana miast
        swapPositions(newGeneration[mutowany], genes[0], genes[1]) 
        # inwersja(newGeneration[mutatowany], genes[0], genes[1])
        i += mutationRate
        mutationRate += mutationRate

    # inwersja (wybór fragmentu trasy i odwrócenie kolejności odwie-
    # dzenia tych miast, na przykład: trasa początkowa: 1 2 3 4 5 6 7 8. 
    # Inwersji podlegają podkreślone elementy, a zatem trasa końcowa ma postać [22]: 1 2 3 6 5 4 7 8;
    # inwersja(newGeneration[mutatowany], genes[0], genes[1])

    # return mutated generation
    return newGeneration

def nextGeneration(population, costTable):
    rodzice = []
    newGeneration = []

    print("pula rodzicow:", len(rodzice), rodzice)
    print("len populacji:", len(population), population)

    # ewolucja przez krzyzowanie osobnikow - jednopunktowe
    newGeneration = evolution(population, rodzice, costTable)

    # mutacja - 1:1000 osobników
    # 1000 / 100 = 10 czyli co ~10ty osobnik mutuje
    # 1000 / N = mutationRate
    mutationRate = int(1000 / N)
    # mutationRate = 1 #debug
    print("mutationRate:", mutationRate)

    print("ile teraz jest i czy zmutuja to len newGeneration: ", len(newGeneration))
    if (mutationRate < len(newGeneration)):
        mutation(newGeneration, mutationRate)
        print("zmutowana generacja", newGeneration)
    else:
        print("za duzy mutationRate!")

    print("nextGeneration ----> newGeneration:", newGeneration)

    return newGeneration

# run geneticAlgorithm zrob tyle pokolen
def geneticAlgorithm(ile_osobnikow, generations): # population

    print("Liczba miast:", N)
    print("Liczba osobnikow poczatkowych:", ile_osobnikow)
    print("Liczba pokolen:", generations)
    # generacja tabeli kosztow podrozy
    costTable = []
    print("\n-------- Tabela kosztow podrozy (10$ - 99$) --------")
    costTable = generateCostTable(N)
    print(costTable,"\n")

    # generuj populacje poczatkowa 
    population = generatePopulation(ile_osobnikow)
    print("Ilosc osobnikow w populacji:", len(population))

    # koszty podrozy dla wszystkich osobnikow w poczatkowej populacji
    # i koszt minimalny/najkrotsza trasa w poczatkowej populacji
    minKoszt = minKosztPodrozy(population, costTable)
    print("Koszt minimalny/najkrotsza trasa w poczatkowej populacji:", minKoszt)

    progress = []
    progress.append(minKoszt)

    print("pokolenie tera")
    nowePokolenie = population.copy()
    print("nowePokolenie = population", nowePokolenie)

    for i in range(0, generations):
        print("pokolenie nr", i+1)
        nowePokolenie = nextGeneration(nowePokolenie, costTable)
        print("petla generations -----> nowePokolenie", nowePokolenie)
        minKoszt = minKosztPodrozy(nowePokolenie, costTable)
        print("Koszt minimalny/najkrotsza trasa dla pokolenia nr", i+1 ,":", minKoszt)
        # progress.append(1 / minKosztPodrozy(population, costTable)[0][1])
        progress.append(minKoszt)

    # koszty podrozy dla wszystkich osobnikow w ostatnim pokoleniu populacji
    # i koszt minimalny/najkrotsza trasa w ostatnim pokoleniu populacji
    # minKoszt = minKosztPodrozy(population, costTable)
    print("Koszt minimalny/najkrotsza trasa w ostatnim pokoleniu populacji:", minKoszt)

    plt.plot(progress)
    plt.title('Problem komiwojazera')
    plt.ylabel('Koszt podrozy')
    plt.xlabel('Pokolenie')
    plt.savefig('komiwojazer_cost_per_generation.png')
    plt.show()

    return 0

# ------------------------------ execute genetic algorithm --------------------------------

# ile pokolen, default=500
# ile_miast, default=100
# ile_osobnikow, default=50

# ile_miast=10, 
# N = 10 
# ile_osobnikow = 6
# maxGenerations = 600

# argumenty podane z command line'a
ile_osobnikow = int(sys.argv[1])
generations = int(sys.argv[2])

# liczba miast stala: 100, N = 100
# run everything and draw a plot: Koszt podrozy per Generation
geneticAlgorithm(ile_osobnikow, generations)

# geneticAlgorithm(ile_osobnikow=5, generations=1)
