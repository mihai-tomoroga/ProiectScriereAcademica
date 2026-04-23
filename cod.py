import random
import time
import csv


def bubble_sort(a):
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1]=a[j+1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(a):
     
    for i in range(1, len(a)):
        k = a[i]
        j = i-1
        while j >= 0 and a[j] > k:
            a[j+1] = a[j]
            j = j - 1
        a[j+1] = k
    return a


def selection_sort(a):
     
    n = len(a)
    for i in range(n):
        min_i = i
        for j in range(i+1, n):
            if a[j] < a[min_i]:
                min_i = j
        a[i], a[min_i]=a[min_i], a[i]
    return a


def merge_sort(a):
     
    if len(a) <= 1:
        return a
    mij = len(a) // 2
    st = merge_sort(a[:mij])
    dr = merge_sort(a[mij:])
    return merge(st, dr)


def merge(st, dr):
    rez = []
    i=j=0
    while i<len(st) and j<len(dr):
        if st[i] < dr[j]:
            rez.append(st[i])
            i += 1
        else:
            rez.append(dr[j])
            j += 1
    return rez + st[i:] + dr[j:]


def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = random.choice(a)
    st = [x for x in a if x < pivot]
    mij = [x for x in a if x == pivot]
    dr = [x for x in a if x > pivot]
    return quick_sort(st) + mij + quick_sort(dr)

def counting_sort_radix(a, exp):
    n = len(a)
    l = [0] * n
    count = [0] * 10

    for i in range(n):
        ind = (a[i]//exp) % 10
        count[ind] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i=n-1
    while i >= 0:
        ind = (a[i] // exp) % 10
        l[count[ind] - 1] = a[i]
        count[ind] -= 1
        i -= 1

    return l


def radix_sort(a):
     
    if len(a) == 0:
        return a

    max_val = max(a)
    exp = 1

    while max_val//exp > 0:
        a = counting_sort_radix(a, exp)
        exp *= 10

    return a

def lista_aleatoare(n):
    return [random.randint(0, 100000) for _ in range(n)]

def lista_sortata(n):
    return list(range(n))

def lista_inversata(n):
    return list(range(n, 0, -1))

def lista_aproape_sortata(n):
    a = list(range(n))
    for _ in range(max(1, n // 10)):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        a[i], a[j] = a[j], a[i]
    return a

def lista_plata(n):
    return [random.randint(0, 5) for _ in range(n)]

def lista_aleatoare_float(n):
    return [random.uniform(0, 100000) for _ in range(n)]

def lista_sortata_float(n):
    return [float(i) for i in range(n)]

def lista_inversata_float(n):
    return [float(i) for i in range(n, 0, -1)]

def lista_aproape_sortata_float(n):
    a = [float(i) for i in range(n)]
    for _ in range(max(1, n // 10)):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        a[i], a[j] = a[j], a[i]
    return a

def lista_plata_float(n):
    return [float(random.randint(0, 5)) for _ in range(n)]
    

def measure_time(sort_function, a, max_time=30):
    start = time.perf_counter()
    sort_function(a)
    end = time.perf_counter()

    durata = end - start

    return durata

def get_repetari(size):
    if size <= 100:
        return 5000
    elif size <= 10000:
        return 25
    else:
        return 3
    
def rez(csv_f="rezultate.csv"):
    sizes = [10, 50, 100, 1000, 5000, 15000, 50000, 100000, 1000000,10000000 ]

    date_de_test = {
        "Aleatoare": lista_aleatoare,
        "Sortata": lista_sortata,
        "Invers Sortata": lista_inversata,
        "Aproape sortata": lista_aproape_sortata,
        "Plata": lista_plata,
        "Aleatoare Float": lista_aleatoare_float,
        "Sortata Float": lista_sortata_float,
        "Invers Sortata Float": lista_inversata_float,
        "Aproape sortata Float": lista_aproape_sortata_float,
        "Plata Float": lista_plata_float
    }

    algoritmi = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Radix Sort": radix_sort
    }
    skip_alg = {}

    with open(csv_f, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Algoritm", "Tip Lista", "Dimensiune", "Timp(s)"])

        for date_n, date_f in date_de_test.items():
            print(f"\n===== Tip lista: {date_n} =====")

            for alg_n in algoritmi:
                skip_alg[(alg_n, date_n)] = False

            for n in sizes:
                print(f"\nDimensiune: {n}")
                a = date_f(n)

                for alg_n, alg_f in algoritmi.items():

                    if skip_alg[(alg_n, date_n)]:
                        continue
 
                    if "Float" in date_n and alg_n == "Radix Sort":
                        continue

                    rep = get_repetari(n)
                    t_total = 0
                    timeout_hit = False

                    for _ in range(rep):
                        t = measure_time(alg_f, a.copy())

                        if t > 30:
                            timeout_hit = True
                            print(f"{alg_n}: {t:.6f} sec")
                            writer.writerow([alg_n, date_n, n, f"{t:.6f}"])
                            skip_alg[(alg_n, date_n)] = True
                            break

                        t_total += t

                    if timeout_hit:
                        continue

                    t_avg = t_total / rep
                    print(f"{alg_n}: {t_avg:.6f} sec")
                    writer.writerow([alg_n, date_n, n, f"{t_avg:.6f}"])




rez("rezultate.csv")
print("\nRezultatele au fost salvate")
