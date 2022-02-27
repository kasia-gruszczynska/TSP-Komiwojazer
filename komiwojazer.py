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

# ile miast, default N = 100
N = 100

# generowanie tabeli kosztow podrozy
# wartosci kosztow 10$ - 99$
# losowa macierz symetryczna
def generateCostTable(N):
    b = np.random.randint(10,99,size=(N,N),dtype=int)  
    b_symm = (b + b.T)/2
    return b_symm

# generowanie osobnikow poczatkowych, default = 50
def generatePopulation(ile_osobnikow):
    population = []
    i = 0
    while i < ile_osobnikow:
        # print("+ nowy osobnik", i)
        population.append(random.sample(range(0, N, 1), N))
        i += 1
    print("Poczatkowa populacja osobników: ", len(population))
    # print(population)
    return population

# funkcja dopasowania, fitness function - koszt podrozy
# dla pojedynczego osobnika, n - numer osobnika
def fnDopasowania(population, costTable, n):
    cost = 0
    i = 0
    for i in range(N-1): 
        # print(population[n][i], "->", population[n][i+1])
        cost += costTable[population[n][i], population[n][i+1]]
        # print(costTable[population[n][i], population[n][i+1]])
    print("Koszt podrozy: ", cost)
    return cost

# policz koszty dla wszystkich osobnikow w populacji
# znajdz minimalny
def minKosztPodrozy(population, costTable):
    minKoszt = 0
    kosztyOsobnikow = []
    n = 0
    # print("len(population) ----> ", len(population))
    for n in range(0, len(population)):
        kosztyOsobnikow.append(fnDopasowania(population, costTable, n))
        # print("Koszt dla osobnika", n ,":", kosztyOsobnikow[n])
    # print("Koszty osobnikow", kosztyOsobnikow)
    minKoszt = min(kosztyOsobnikow)
    print("Koszt minimalny/najkrotsza trasa", minKoszt)
    return minKoszt

# selekcja turniejowa
# Binary tournament selection (BTS)
def binTounamentSelection(population, costTable):
    # do turnieju 1:1 wylosowac osobnikow
    pair = random.sample(range(0, len(population)), 2)
    # print("para", pair)
    # print("population", population)

    if fnDopasowania(population, costTable, pair[0]) < fnDopasowania(population, costTable, pair[1]):
        rodzic = population[pair[0]].copy()
        # print("rodzic to osobnik nr", pair[0], population[pair[0]])
        # print("osobnik usuniety nr", pair[1], population[pair[1]])
        del population[pair[1]]
    else:
        rodzic = population[pair[1]].copy()
        # print("rodzic to osobnik nr", pair[1], population[pair[1]])
        # print("osobnik usuniety nr", pair[0], population[pair[0]])
        del population[pair[0]]

    print(population)

    return rodzic

# krzyzowanie osobnikow, jednopunktowe
def crossOver(rodzic1_val, rodzic2_val):
    # losowy punkt krzyzowania
    crossPoint = random.randint(1, N-2)
    rodzic1 = list(rodzic1_val)
    rodzic2 = list(rodzic2_val)
    rodzic1_orig = list(rodzic1)
    rodzic2_orig = list(rodzic2)

    dzieci = []
    # aby rozwiazanie bylo valid nie moga sie miasta powtarzac
    # usunac te wylosowane 
    cr = crossPoint
    end = N - 1 - crossPoint
    i=0
    for i in range(end):
        rodzic2.remove(rodzic1[crossPoint+1+i])
        cr += 1
        i += 1
    temp = rodzic1[crossPoint+1:]
    temp.reverse()
    reversed = rodzic2 + temp  
    dzieci.append(reversed)

    # print("dzieci", dzieci)
    
    rodzic1 = list(rodzic1_orig)
    rodzic2 = list(rodzic2_orig)

    cr = crossPoint
    end = N - 1 - crossPoint
    i=0
    for i in range(end):
        rodzic1.remove(rodzic2[crossPoint+1+i])
        cr += 1
        i += 1

    temp = rodzic2[crossPoint+1:]
    temp.reverse()
    reversed = rodzic1 + temp
    dzieci.append(reversed)

    # print("dzieci", dzieci)

    rodzic1 = list(rodzic1_orig)
    rodzic2 = list(rodzic2_orig)

    return dzieci

# tworz nowe pokolenie
# z puli rodzicow bierz pary
def krzyzowanieRodzicow(rodzice):
    newGeneration=[]

    for i in range(len(rodzice)-1):
        print("krzyzowanie")
        dzieci = crossOver(rodzice[i],rodzice[i+1])
        newGeneration.append(dzieci[0])
        newGeneration.append(dzieci[1])
    return newGeneration

# ewolucja, krzyzowanieRodzicow wywolaj dla populacji
def evolution(population, rodzice, costTable):
    # wybranie puli rodzicow
    while len(population) >= 2:
        # print("while len populacji:", len(population), population)
        rodzice.append(binTounamentSelection(population, costTable))

    print("pula rodzicow:", len(rodzice), rodzice)
    # print("ile osobnikow zostalo w populacji poczatkowej - wygina!:", len(population), population)

    newGeneration = krzyzowanieRodzicow(rodzice)

    # print("evolution ---> newGeneration", newGeneration)

    # zwroc dzieci czyli nowe pokolenie
    return newGeneration

def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

# mutacja, 1:1000 genow
# wzajemna wymiana (wybranie dwóch miast i zamienienie ich ze sobą)
# do mutacji wybierac 1 osobnika na n-osobnikow, wg mutationRate
def mutation(newGeneration, mutationRate):
    i = 0
    while (mutationRate < len(newGeneration)):
        mutowany = random.randint(i, mutationRate)
        # do mutacji wylosowac pare genow osobnika
        genes = random.sample(range(0, N), 2)
        # print("geny do mutacji:", genes)
        # zamiana miast
        swapPositions(newGeneration[mutowany], genes[0], genes[1]) 
        i += mutationRate
        mutationRate += mutationRate
    # return mutated generation
    return newGeneration

def nextGeneration(population, costTable):
    rodzice = []
    newGeneration = []

    # print("pula rodzicow:", len(rodzice), rodzice)
    # print("len populacji:", len(population), population)

    # ewolucja przez krzyzowanie osobnikow - jednopunktowe
    newGeneration = evolution(population, rodzice, costTable)

    # mutacja - 1:1000 osobników
    # 1000 / 100 = 10 czyli co ~10ty osobnik mutuje
    # 1000 / N = mutationRate
    mutationRate = int(1000 / N)

    if (mutationRate < len(newGeneration)):
        mutation(newGeneration, mutationRate)
        print("zmutowana generacja", newGeneration)
    else:
        print("za duzy mutationRate!")

    # print("nextGeneration ----> newGeneration:", newGeneration)

    return newGeneration

# run geneticAlgorithm dla x pokolen
def geneticAlgorithm(ile_osobnikow, generations):

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

    print("Tworzenie nowego pokolenia")
    nowePokolenie = population.copy()
    print("nowePokolenie = population", nowePokolenie)

    for i in range(0, generations):
        print("pokolenie nr", i+1)
        nowePokolenie = nextGeneration(nowePokolenie, costTable)
        print("generations -----> nowePokolenie", nowePokolenie)
        minKoszt = minKosztPodrozy(nowePokolenie, costTable)
        print("Koszt minimalny/najkrotsza trasa dla pokolenia nr", i+1 ,":", minKoszt)
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

# ile miast, constant, default=100
# ile osobnikow, default=50
# ile pokolen, default=500

# argumenty podane z command line'a
ile_osobnikow = int(sys.argv[1])
generations = int(sys.argv[2])

# run everything and draw a plot: Koszt podrozy per Generation
geneticAlgorithm(ile_osobnikow, generations)
