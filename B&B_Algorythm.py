from scipy.optimize import linprog
from tkinter import *
import pylab
import os
from graphviz import Digraph

tablica_xmax=[]

bound = [[0, 10], [0, 10], [0, 10], [0, 10], [0, 10]]
def podaj_mozliwe_rozwiazania(lista_ograniczen, wartosci_ograniczen, bounds):
    mozliwe_rozwiazania = []
    for i in range(len(lista_ograniczen)):
        coefficients_inequalities = [lista_ograniczen[i]]  # require -1*x + -1*y <= -180
        constants_inequalities = wartosci_ograniczen[i]
        for j in range(len(lista_ograniczen)):
            coefficients_equalities = [lista_ograniczen[j]]  # require 3*x + 12*y = 1000
            constants_equalities = wartosci_ograniczen[j]
            bounds1 = (bounds[0][0], bounds[0][1])
            bounds2 = (bounds[1][0], bounds[1][1])
            bounds3 = (bounds[2][0], bounds[2][1])
            bounds4 = (bounds[3][0], bounds[3][1])
            bounds5 = (bounds[4][0], bounds[4][1])
            coefficients_max_y = [0, 0, 0, 0, 0]
            res = linprog(coefficients_max_y,
                          A_ub=coefficients_inequalities,
                          b_ub=constants_inequalities,
                          A_eq=coefficients_equalities,
                          b_eq=constants_equalities,
                          bounds=(bounds1, bounds2, bounds3, bounds4, bounds5), method="simplex")
            mozliwe_rozwiazania.append(res.x.astype(float))
    return mozliwe_rozwiazania

def oblicz_wartosc_zmax(lista_ograniczen, wartosci_ograniczen, nowa_tablica, bounds, x1, x2, x3, x4, x5):
    mozliwe_rozwiazania = podaj_mozliwe_rozwiazania(lista_ograniczen, wartosci_ograniczen, bounds)
    nowa_tablica = []
    for k in range(len(mozliwe_rozwiazania)):
        if generowanie_ograniczen(lista_ograniczen, wartosci_ograniczen, k, bounds):
            nowa_tablica.append([x1*mozliwe_rozwiazania[k][0] + x2*mozliwe_rozwiazania[k][1] + x3*mozliwe_rozwiazania[k][2] + x4*mozliwe_rozwiazania[k][3] + x5*mozliwe_rozwiazania[k][4],
                                 [round(mozliwe_rozwiazania[k][0], 3), round(mozliwe_rozwiazania[k][1], 3),
                                  round(mozliwe_rozwiazania[k][2], 3), round(mozliwe_rozwiazania[k][3], 3),
                                  round(mozliwe_rozwiazania[k][4], 3)]])
    return nowa_tablica

def generowanie_ograniczen(lista_ograniczen, wartosci_ograniczen, k, bounds):
    mozliwe_rozwiazania = podaj_mozliwe_rozwiazania(lista_ograniczen, wartosci_ograniczen, bounds)
    if all(lista_ograniczen[i][0] * mozliwe_rozwiazania[k][0] + lista_ograniczen[i][1] * mozliwe_rozwiazania[k][1]
           + lista_ograniczen[i][2] * mozliwe_rozwiazania[k][2] + lista_ograniczen[i][3] * mozliwe_rozwiazania[k][3] +
           lista_ograniczen[i][4] * mozliwe_rozwiazania[k][4] <= wartosci_ograniczen[i]+0.00001 for i in range(len(wartosci_ograniczen))):
        return True
    else:
        return False

def sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie, tablica_wynikow):
    if tablica_wynikow != [] and rozwiazanie != []:
        if rozwiazanie[0][0] < max(tablica_wynikow)[0]:
            return True
        else:
            return False
    if rozwiazanie == []:
        return True
    else:
        return False

def dodatkowy_warunek_dla_calkowitych(solution):
    if len(solution)!=0:
        solution_tab = max(solution)
        print(solution_tab)
        data = solution_tab[1]
        if all(float(i).is_integer() for i in data):
            return "ZBIOR PUSTY"
    else:
        return "ZBIOR PUSTY"

def sprawdz_czy_wartosci_sa_calowite(solution, rozwiazanie, lista_wsp):
    rozmiar = pobierz_rozmiar(lista_wsp)
    if solution == []:
        print('ZBIOR PUSTY')
        return ("ZBIOR PUSTY")
    else:
        solution_tab = max(solution)
        print(solution_tab)
        data = solution_tab[1]
        if all(float(i).is_integer() for i in data):
            print("There both values are not float!")
            rozwiazanie.append(solution_tab)
            if rozmiar == 2:
                return str(round(float(solution_tab[0]), 3)) + '['+ str(float(solution_tab[1][0]))+' '+str(float(solution_tab[1][1]))+']'
            if rozmiar == 3:
                return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(float(solution_tab[1][1])) +' ' + str(float(solution_tab[1][2])) + ']'
            if rozmiar == 4:
                return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(float(solution_tab[1][3])) +']'
            if rozmiar == 5:
                return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                    float(solution_tab[1][3])) + ' ' + str(float(solution_tab[1][4])) +']'
        else:
            if rozmiar == 2:
                return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ']'
            if rozmiar == 3:
                return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ']'
            if rozmiar == 4:
                return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                    float(solution_tab[1][3])) + ']'
            if rozmiar == 5:
                return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                    float(solution_tab[1][3])) + ' ' + str(float(solution_tab[1][4])) + ']'

def wydrukuj_odpowiedz(solution, lista_wsp):
    rozmiar = pobierz_rozmiar(lista_wsp)
    if solution == []:
        print('ZBIOR PUSTY')
        return "----"
    else:
        solution_tab = max(solution)
        if rozmiar == 2:
            return str(round(float(solution_tab[0]), 3))+ '[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ']'
        if rozmiar == 3:
            return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ']'
        if rozmiar == 4:
            return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                float(solution_tab[1][3])) + ']'
        if rozmiar == 5:
            return str(round(float(solution_tab[0]), 3)) + '[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                float(solution_tab[1][3])) + ' ' + str(float(solution_tab[1][4])) + ']'


def wyswietl_ograniczenia(data, site):
    nowe_ograniczenie = min(max(data)[1])
    if float(nowe_ograniczenie).is_integer():
        nowe_ograniczenie = sorted(max(data)[1])[1]
    pozycja = max(data)[1].index(nowe_ograniczenie)
    if site=="L":
        return 'x'+str(pozycja+1)+' <= '+str(int(nowe_ograniczenie))
    else:
        return 'x'+str(pozycja+1)+' >= '+str(int(nowe_ograniczenie)+1)

def pobierz_rozmiar(lista_ograniczen):
    if all(lista_ograniczen[i][2] == 0 for i in range(len(lista_ograniczen))):
        return 2
    elif all(lista_ograniczen[i][3] == 0 for i in range(len(lista_ograniczen))):
        return 3
    elif all(lista_ograniczen[i][4] == 0 for i in range(len(lista_ograniczen))):
        return 4
    else:
        return 5

def wyswietl_ostateczne_rozwiazanie_algorytmu(lewa, prawa, lista_wsp):
    rozmiar = pobierz_rozmiar(lista_wsp)
    if (lewa != [] and prawa != []):
        if lewa[0][0] > prawa[0][0]:
            solution_tab = lewa[0]
            if rozmiar == 2:
                return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ']'
            if rozmiar == 3:
                return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ']'
            if rozmiar == 4:
                return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                    float(solution_tab[1][3])) + ']'
            if rozmiar == 5:
                return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                    float(solution_tab[1][3])) + ' ' + str(float(solution_tab[1][4])) + ']'
        else:
            solution_tab = prawa[0]
            if rozmiar == 2:
                return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ']'
            if rozmiar == 3:
                return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ']'
            if rozmiar == 4:
                return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                    float(solution_tab[1][3])) + ']'
            if rozmiar == 5:
                return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                    float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                    float(solution_tab[1][3])) + ' ' + str(float(solution_tab[1][4])) + ']'
    if lewa == []:
        solution_tab = prawa[0]
        if rozmiar == 2:
            return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ']'
        if rozmiar == 3:
            return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ']'
        if rozmiar == 4:
            return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                float(solution_tab[1][3])) + ']'
        if rozmiar == 5:
            return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                float(solution_tab[1][3])) + ' ' + str(float(solution_tab[1][4])) + ']'
    if prawa == []:
        solution_tab = lewa[0]
        if rozmiar == 2:
            return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ']'
        if rozmiar == 3:
            return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ']'
        if rozmiar == 4:
            return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                float(solution_tab[1][3])) + ']'
        if rozmiar == 5:
            return 'Rozwiązaniem algorytmu są wartości:[' + str(float(solution_tab[1][0])) + ' ' + str(
                float(solution_tab[1][1])) + ' ' + str(float(solution_tab[1][2])) + ' ' + str(
                float(solution_tab[1][3])) + ' ' + str(float(solution_tab[1][4])) + ']'

def dodatkowe_warunki_poziom_2(data, site, strona, lista_ograniczen, wartosci_ograniczen, bounds):
    if data != []:
        nowe_xmax_lewo = []
        nowe_xmax_prawo = []
        nowe_ograniczenie = min(max(data)[1])
        if float(nowe_ograniczenie).is_integer():
            nowe_ograniczenie = sorted(max(data)[1])[1]
            if float(nowe_ograniczenie).is_integer():
                nowe_ograniczenie = sorted(max(data)[1])[2]
                if float(nowe_ograniczenie).is_integer():
                    nowe_ograniczenie = sorted(max(data)[1])[3]
                    if float(nowe_ograniczenie).is_integer():
                        nowe_ograniczenie = sorted(max(data)[1])[4]
        pozycja = max(data)[1].index(nowe_ograniczenie)
        if strona == 'L':
            if site == 'LEWO':
                if True:
                    nowe_xmax_lewo = oblicz_wartosc_zmax(lista_ograniczen, wartosci_ograniczen, nowe_xmax_lewo, bounds,
                                                         int(f1.get()), int(f2.get()), int(f3.get()), int(f4.get()),
                                                         int(f5.get()))
                    return (nowe_xmax_lewo)
                else:
                    return []
            if site == 'PRAWO':
                if True:
                    nowe_xmax_prawo = oblicz_wartosc_zmax(lista_ograniczen, wartosci_ograniczen, nowe_xmax_lewo, bounds,
                                                          int(f1.get()), int(f2.get()), int(f3.get()), int(f4.get()),
                                                          int(f5.get()))
                    return (nowe_xmax_prawo)
                else:
                    return []
        if strona == 'P':
            if site == 'LEWO':
                if True:
                    nowe_xmax_lewo = oblicz_wartosc_zmax(lista_ograniczen, wartosci_ograniczen, nowe_xmax_prawo, bounds,
                                                         int(f1.get()), int(f2.get()), int(f3.get()), int(f4.get()),
                                                         int(f5.get()))
                    return (nowe_xmax_lewo)
                else:
                    return []
            if site == 'PRAWO':
                if True:
                    nowe_xmax_prawo = oblicz_wartosc_zmax(lista_ograniczen, wartosci_ograniczen, nowe_xmax_prawo,
                                                          bounds, int(f1.get()), int(f2.get()), int(f3.get()),
                                                          int(f4.get()), int(f5.get()))
                    return (nowe_xmax_prawo)
                else:
                    return []
    else:
        return []


def oblicz_bounds(data, site, strona, bounds):
    if data != []:
        nowe_ograniczenie = min(max(data)[1])
        if float(nowe_ograniczenie).is_integer():
            nowe_ograniczenie = sorted(max(data)[1])[1]
            if float(nowe_ograniczenie).is_integer():
                nowe_ograniczenie = sorted(max(data)[1])[2]
                if float(nowe_ograniczenie).is_integer():
                    nowe_ograniczenie = sorted(max(data)[1])[3]
                    if float(nowe_ograniczenie).is_integer():
                        nowe_ograniczenie = sorted(max(data)[1])[4]
        pozycja = max(data)[1].index(nowe_ograniczenie)
        new_bounds = bounds
        if strona == 'L':
            if site == 'LEWO':
                if True:
                    new_bounds[pozycja][1] = int(nowe_ograniczenie)
                    print(new_bounds)
                    return new_bounds
            if site == 'PRAWO':
                if True:
                    new_bounds[pozycja][0] = int(nowe_ograniczenie) + 1
                    return new_bounds
        if strona == 'P':
            if site == 'LEWO':
                if True:
                    new_bounds[pozycja][1] = int(nowe_ograniczenie)
                    return new_bounds
            if site == 'PRAWO':
                if True:
                    new_bounds[pozycja][0] = int(nowe_ograniczenie) + 1
                    return new_bounds
    else:
        return []

def myClick():
    # lista_ograniczen = [[9, 7, 0, 0, 0], [1, 1, 0, 0, 0], [-3, -2, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    # wartosci_ograniczen= [63, 8, -6, 0, 0]
    # lista_ograniczen = [[6, 4, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    # wartosci_ograniczen= [10, 0, 0, 0, 0]
    lista_ograniczen = [[int(x1_1.get()), int(x2_1.get()), int(x3_1.get()), int(x4_1.get()), int(x5_1.get())],
                        [int(x1_2.get()), int(x2_2.get()), int(x3_2.get()), int(x4_2.get()), int(x5_2.get())],
                        [int(x1_3.get()), int(x2_3.get()), int(x3_3.get()), int(x4_3.get()), int(x5_3.get())],
                        [int(x1_4.get()), int(x2_4.get()), int(x3_4.get()), int(x4_4.get()), int(x5_4.get())],
                        [int(x1_5.get()), int(x2_5.get()), int(x3_5.get()), int(x4_5.get()), int(x5_5.get())]]
    wartosci_ograniczen = [int(ogr_1.get()), int(ogr_2.get()), int(ogr_3.get()), int(ogr_4.get()), int(ogr_5.get())]
    if wartosci_ograniczen[1]==0:
        lista_ograniczen[1] = [1, 1, 0, 0, 0]
        wartosci_ograniczen[1] = 100
    bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
    tablica_xmaxy = []
    tablica_xmaxy = oblicz_wartosc_zmax(lista_ograniczen, wartosci_ograniczen, tablica_xmaxy, bound, int(f1.get()), int(f2.get()), int(f3.get()), int(f4.get()), int(f5.get()))
    print(tablica_xmaxy)
    wydrukuj_odpowiedz(tablica_xmaxy, lista_ograniczen)
    dot.node('S', str(wydrukuj_odpowiedz(tablica_xmaxy, lista_ograniczen)))
########################################################################################################################
    if dodatkowy_warunek_dla_calkowitych(tablica_xmaxy) != "ZBIOR PUSTY":
        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
        poziom_2_lewo = dodatkowe_warunki_poziom_2(tablica_xmaxy, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundsl)

        dot.node('L', str(wyswietl_ograniczenia(tablica_xmaxy, 'L')) + '\n' +
                 str(sprawdz_czy_wartosci_sa_calowite(poziom_2_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
        boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
        poziom_2_prawo = dodatkowe_warunki_poziom_2(tablica_xmaxy, 'PRAWO', 'P', lista_ograniczen, wartosci_ograniczen, boundsp)
        dot.node('P', str(wyswietl_ograniczenia(tablica_xmaxy, 'P')) + '\n'
                 + str(sprawdz_czy_wartosci_sa_calowite(poziom_2_prawo, rozwiazanie_prawa_strona, lista_ograniczen)))
        dot.edges(['SL', 'SP'])
#LEWA#################################################################################################################
        if dodatkowy_warunek_dla_calkowitych(poziom_2_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_2_lewo):
            if sprawdz_czy_wartosci_sa_calowite(poziom_2_lewo, rozwiazanie_lewa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                poziom_3_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_2_lewo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundsll)
                if str(sprawdz_czy_wartosci_sa_calowite(poziom_3_lewo_lewo, rozwiazanie_lewa_strona,lista_ograniczen)) == "ZBIOR PUSTY":
                    dot.node('Q',  str(sprawdz_czy_wartosci_sa_calowite(poziom_3_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                else:
                    dot.node('Q', str(wyswietl_ograniczenia(poziom_2_lewo, 'L'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_3_lewo_lewo, rozwiazanie_lewa_strona,lista_ograniczen)))

                boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                poziom_3_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_2_lewo, 'PRAWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslp)
                if str(sprawdz_czy_wartosci_sa_calowite(poziom_3_lewo_prawo, rozwiazanie_lewa_strona,lista_ograniczen)) == "ZBIOR PUSTY":
                    dot.node('W', str(sprawdz_czy_wartosci_sa_calowite(poziom_3_lewo_prawo, rozwiazanie_lewa_strona,lista_ograniczen)))
                else:
                    dot.node('W', str(wyswietl_ograniczenia(poziom_2_lewo, 'P')) + '\n' + str(
                        sprawdz_czy_wartosci_sa_calowite(poziom_3_lewo_prawo, rozwiazanie_lewa_strona,lista_ograniczen)))
                dot.edges(['LQ', 'LW'])
                if dodatkowy_warunek_dla_calkowitych(poziom_3_lewo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_3_lewo_lewo):
                    if sprawdz_czy_wartosci_sa_calowite(poziom_3_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                        boundslll = oblicz_bounds(poziom_3_lewo_lewo, 'LEWO', 'L', boundsll)
                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                        poziom_4_lewo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_3_lewo_lewo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslll)
                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                            dot.node('E', str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                        else:
                            dot.node('E', str(wyswietl_ograniczenia(poziom_3_lewo_lewo, 'L')) + '\n' + str(
                                sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                        boundsllp = oblicz_bounds(poziom_3_lewo_lewo, 'PRAWO', 'L', boundsll)
                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                        poziom_4_lewo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_3_lewo_lewo, 'PRAWO', 'L', lista_ograniczen, wartosci_ograniczen, boundsllp)
                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                            dot.node('R', str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)))
                        else:
                            dot.node('R', str(wyswietl_ograniczenia(poziom_3_lewo_lewo, 'P')) + '\n' + str(
                                sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)))
                        dot.edges(['QE', 'QR'])
                        if dodatkowy_warunek_dla_calkowitych(poziom_4_lewo_lewo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo( rozwiazanie_lewa_strona, poziom_4_lewo_lewo_lewo):
                            if sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_lewo, rozwiazanie_lewa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                                boundsllll = oblicz_bounds(poziom_4_lewo_lewo_lewo, 'LEWO', 'L', boundslll)
                                boundslll = oblicz_bounds(poziom_3_lewo_lewo, 'LEWO', 'L', boundsll)
                                boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_lewo_lewo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_4_lewo_lewo_lewo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundsllll)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('G', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                else:
                                    dot.node('G', str(wyswietl_ograniczenia(poziom_4_lewo_lewo_lewo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                if dodatkowy_warunek_dla_calkowitych(poziom_5_lewo_lewo_lewo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_5_lewo_lewo_lewo_lewo):
                                    if sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                                        boundslllll = oblicz_bounds(poziom_5_lewo_lewo_lewo_lewo, 'LEWO', 'L', boundsllll)
                                        boundsllll = oblicz_bounds(poziom_4_lewo_lewo_lewo, 'LEWO', 'L', boundslll)
                                        boundslll = oblicz_bounds(poziom_3_lewo_lewo, 'LEWO', 'L', boundsll)
                                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_lewo_lewo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_5_lewo_lewo_lewo_lewo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslllll)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('q', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                        else:
                                            dot.node('q', str(wyswietl_ograniczenia(poziom_5_lewo_lewo_lewo_lewo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_lewo_lewo, rozwiazanie_lewa_strona,lista_ograniczen)))
                                        boundsllllp = oblicz_bounds(poziom_5_lewo_lewo_lewo_lewo, 'PRAWO', 'L', boundsllll)
                                        boundsllll = oblicz_bounds(poziom_4_lewo_lewo_lewo, 'LEWO', 'L', boundslll)
                                        boundslll = oblicz_bounds(poziom_3_lewo_lewo, 'LEWO', 'L', boundsll)
                                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_lewo_lewo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_5_lewo_lewo_lewo_lewo, 'PRAWO', 'L', lista_ograniczen,wartosci_ograniczen, boundsllllp)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('w', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_lewo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        else:
                                            dot.node('w', str(wyswietl_ograniczenia(poziom_5_lewo_lewo_lewo_lewo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_lewo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        dot.edges(['Gq', 'Gw'])
                                boundslllp = oblicz_bounds(poziom_4_lewo_lewo_lewo, 'PRAWO', 'L', boundslll)
                                boundslll = oblicz_bounds(poziom_3_lewo_lewo, 'LEWO', 'L', boundsll)
                                boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_lewo_lewo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_4_lewo_lewo_lewo, 'PRAWO','L', lista_ograniczen, wartosci_ograniczen, boundslllp)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('H', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                else:
                                    dot.node('H', str(wyswietl_ograniczenia(poziom_4_lewo_lewo_lewo, 'L')) + '\n' + str( sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_lewo_prawo,rozwiazanie_lewa_strona, lista_ograniczen)))
                                dot.edges(['EG', 'EH'])
                                if dodatkowy_warunek_dla_calkowitych(poziom_5_lewo_lewo_lewo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_5_lewo_lewo_lewo_prawo):
                                    if sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                                        boundslllpl = oblicz_bounds(poziom_5_lewo_lewo_lewo_prawo, 'LEWO', 'L', boundslllp)
                                        boundslllp = oblicz_bounds(poziom_4_lewo_lewo_lewo, 'PRAWO', 'L', boundslll)
                                        boundslll = oblicz_bounds(poziom_3_lewo_lewo, 'LEWO', 'L', boundsll)
                                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_lewo_lewo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_5_lewo_lewo_lewo_prawo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslllpl)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('e', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                        else:
                                            dot.node('e', str(wyswietl_ograniczenia(poziom_5_lewo_lewo_lewo_prawo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_prawo_lewo, rozwiazanie_lewa_strona,lista_ograniczen)))
                                        boundslllpp = oblicz_bounds(poziom_5_lewo_lewo_lewo_prawo, 'PRAWO', 'L', boundslllp)
                                        boundslllp = oblicz_bounds(poziom_4_lewo_lewo_lewo, 'PRAWO', 'L', boundslll)
                                        boundslll = oblicz_bounds(poziom_3_lewo_lewo, 'LEWO', 'L', boundsll)
                                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_lewo_lewo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_5_lewo_lewo_lewo_prawo, 'PRAWO', 'L', lista_ograniczen,wartosci_ograniczen, boundslllpp)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('r', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_prawo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        else:
                                            dot.node('r', str(wyswietl_ograniczenia(poziom_5_lewo_lewo_lewo_prawo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_lewo_prawo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        dot.edges(['He', 'Hr'])
                        if dodatkowy_warunek_dla_calkowitych(poziom_4_lewo_lewo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo( rozwiazanie_lewa_strona, poziom_4_lewo_lewo_prawo):
                            if sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_lewo_prawo, rozwiazanie_lewa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                                boundsllpl = oblicz_bounds(poziom_4_lewo_lewo_prawo, 'LEWO', 'L', boundsllp)
                                boundsllp = oblicz_bounds(poziom_3_lewo_lewo, 'PRAWO', 'L', boundsll)
                                boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_lewo_lewo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_4_lewo_lewo_prawo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundsllpl)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('J', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                else:
                                    dot.node('J', str(wyswietl_ograniczenia(poziom_4_lewo_lewo_prawo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                if dodatkowy_warunek_dla_calkowitych(poziom_5_lewo_lewo_prawo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_5_lewo_lewo_prawo_lewo):
                                    if sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                                        boundsllpll = oblicz_bounds(poziom_5_lewo_lewo_prawo_lewo, 'LEWO', 'L', boundsllpl)
                                        boundsllpl = oblicz_bounds(poziom_4_lewo_lewo_prawo, 'LEWO', 'L', boundsllp)
                                        boundsllp = oblicz_bounds(poziom_3_lewo_lewo, 'PRAWO', 'L', boundsll)
                                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_lewo_prawo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_5_lewo_lewo_prawo_lewo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundsllpll)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('t', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                        else:
                                            dot.node('t', str(wyswietl_ograniczenia(poziom_5_lewo_lewo_prawo_lewo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_lewo_lewo, rozwiazanie_lewa_strona,lista_ograniczen)))
                                        boundsllplp = oblicz_bounds(poziom_5_lewo_lewo_prawo_lewo, 'PRAWO', 'L', boundsllpl)
                                        boundsllpl = oblicz_bounds(poziom_4_lewo_lewo_prawo, 'LEWO', 'L', boundsllp)
                                        boundsllp = oblicz_bounds(poziom_3_lewo_lewo, 'PRAWO', 'L', boundsll)
                                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_lewo_prawo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_5_lewo_lewo_prawo_lewo, 'PRAWO', 'L', lista_ograniczen,wartosci_ograniczen, boundsllplp)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('y', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_lewo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        else:
                                            dot.node('y', str(wyswietl_ograniczenia(poziom_5_lewo_lewo_prawo_lewo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_lewo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        dot.edges(['Jt', 'Jy'])
                                boundsllpp = oblicz_bounds(poziom_4_lewo_lewo_prawo, 'PRAWO', 'L', boundsllp)
                                boundsllp = oblicz_bounds(poziom_3_lewo_lewo, 'PRAWO', 'L', boundsll)
                                boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_lewo_lewo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_4_lewo_lewo_prawo, 'PRAWO','L', lista_ograniczen, wartosci_ograniczen, boundsllpp)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('K', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                else:
                                    dot.node('K', str(wyswietl_ograniczenia(poziom_4_lewo_lewo_prawo, 'L')) + '\n' + str( sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_prawo_prawo,rozwiazanie_lewa_strona, lista_ograniczen)))
                                dot.edges(['RJ', 'RK'])
                                if dodatkowy_warunek_dla_calkowitych(poziom_5_lewo_lewo_prawo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_5_lewo_lewo_prawo_prawo):
                                    if sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                                        boundsllppl = oblicz_bounds(poziom_5_lewo_lewo_prawo_prawo, 'LEWO', 'L', boundsllpp)
                                        boundsllpp = oblicz_bounds(poziom_4_lewo_lewo_prawo, 'PRAWO', 'L', boundsllp)
                                        boundsllp = oblicz_bounds(poziom_3_lewo_lewo, 'PRAWO', 'L', boundsll)
                                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_lewo_prawo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_5_lewo_lewo_prawo_prawo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundsllppl)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('u', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                        else:
                                            dot.node('u', str(wyswietl_ograniczenia(poziom_5_lewo_lewo_prawo_prawo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_prawo_lewo, rozwiazanie_lewa_strona,lista_ograniczen)))
                                        boundsllppp = oblicz_bounds(poziom_5_lewo_lewo_prawo_prawo, 'PRAWO', 'L', boundsllpp)
                                        boundsllpp = oblicz_bounds(poziom_4_lewo_lewo_prawo, 'PRAWO', 'L', boundsllp)
                                        boundsllp = oblicz_bounds(poziom_3_lewo_lewo, 'PRAWO', 'L', boundsll)
                                        boundsll = oblicz_bounds(poziom_2_lewo, 'LEWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_lewo_prawo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_5_lewo_lewo_prawo_prawo, 'PRAWO', 'L', lista_ograniczen,wartosci_ograniczen, boundsllppp)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('i', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_prawo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        else:
                                            dot.node('i', str(wyswietl_ograniczenia(poziom_5_lewo_lewo_prawo_prawo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_lewo_prawo_prawo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        dot.edges(['Ku', 'Ki'])
                if dodatkowy_warunek_dla_calkowitych(poziom_3_lewo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_3_lewo_prawo):
                    if sprawdz_czy_wartosci_sa_calowite(poziom_3_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                        boundslpl= oblicz_bounds(poziom_3_lewo_prawo, 'LEWO', 'L', boundslp)
                        boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                        poziom_4_lewo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_3_lewo_prawo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslpl)
                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                            dot.node('T', str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                        else:
                            dot.node('T', str(wyswietl_ograniczenia(poziom_3_lewo_prawo, 'L'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                        boundslpp = oblicz_bounds(poziom_3_lewo_prawo, 'PRAWO', 'L', boundslp)
                        boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                        poziom_4_lewo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_3_lewo_prawo, 'PRAWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslpp)
                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                            dot.node('Y', str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)))
                        else:
                            dot.node('Y', str(wyswietl_ograniczenia(poziom_3_lewo_prawo, 'P'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)))
                        dot.edges(['WT', 'WY'])
                        if dodatkowy_warunek_dla_calkowitych(poziom_4_lewo_prawo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo( rozwiazanie_lewa_strona, poziom_4_lewo_prawo_lewo):
                            if sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_lewo, rozwiazanie_lewa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                                boundslpll = oblicz_bounds(poziom_4_lewo_prawo_lewo, 'LEWO', 'L', boundslpl)
                                boundslpl = oblicz_bounds(poziom_3_lewo_prawo, 'LEWO', 'L', boundslp)
                                boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_lewo_prawo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_4_lewo_prawo_lewo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslpll)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('Z', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                else:
                                    dot.node('Z', str(wyswietl_ograniczenia(poziom_4_lewo_prawo_lewo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                if dodatkowy_warunek_dla_calkowitych(poziom_5_lewo_prawo_lewo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_5_lewo_prawo_lewo_lewo):
                                    if sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                                        boundslplll = oblicz_bounds(poziom_5_lewo_prawo_lewo_lewo, 'LEWO', 'L', boundslpll)
                                        boundslpll = oblicz_bounds(poziom_4_lewo_prawo_lewo, 'LEWO', 'L', boundslpl)
                                        boundslpl = oblicz_bounds(poziom_3_lewo_prawo, 'LEWO', 'L', boundslp)
                                        boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_prawo_lewo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_5_lewo_prawo_lewo_lewo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslplll)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('o', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_lewo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                        else:
                                            dot.node('o', str(wyswietl_ograniczenia(poziom_5_lewo_prawo_lewo_lewo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_lewo_lewo, rozwiazanie_lewa_strona,lista_ograniczen)))
                                        boundslpllp = oblicz_bounds(poziom_5_lewo_prawo_lewo_lewo, 'PRAWO', 'L', boundslpll)
                                        boundslpll = oblicz_bounds(poziom_4_lewo_prawo_lewo, 'LEWO', 'L', boundslpl)
                                        boundslpl = oblicz_bounds(poziom_3_lewo_prawo, 'LEWO', 'L', boundslp)
                                        boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_prawo_lewo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_5_lewo_prawo_lewo_lewo, 'PRAWO', 'L', lista_ograniczen,wartosci_ograniczen, boundslpllp)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('p', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_lewo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        else:
                                            dot.node('p', str(wyswietl_ograniczenia(poziom_5_lewo_prawo_lewo_lewo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_lewo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        dot.edges(['Zo', 'Zp'])
                                boundslplp = oblicz_bounds(poziom_4_lewo_prawo_lewo, 'PRAWO', 'L', boundslpl)
                                boundslpl = oblicz_bounds(poziom_3_lewo_prawo, 'LEWO', 'L', boundslp)
                                boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_lewo_prawo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_4_lewo_prawo_lewo, 'PRAWO','L', lista_ograniczen, wartosci_ograniczen, boundslplp)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('X', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                else:
                                    dot.node('X', str(wyswietl_ograniczenia(poziom_4_lewo_prawo_lewo, 'P')) + '\n' + str( sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_lewo_prawo,rozwiazanie_lewa_strona, lista_ograniczen)))
                                dot.edges(['TZ', 'TX'])
                                if dodatkowy_warunek_dla_calkowitych(poziom_5_lewo_prawo_lewo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_5_lewo_prawo_lewo_prawo):
                                    if sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_lewo_prawo, rozwiazanie_lewa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                                        boundslplpl = oblicz_bounds(poziom_5_lewo_prawo_lewo_prawo, 'LEWO', 'L', boundslplp)
                                        boundslplp = oblicz_bounds(poziom_4_lewo_prawo_lewo, 'PRAWO', 'L', boundslpl)
                                        boundslpl = oblicz_bounds(poziom_3_lewo_prawo, 'LEWO', 'L', boundslp)
                                        boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_prawo_lewo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_5_lewo_prawo_lewo_prawo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslplpl)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node('[', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                        else:
                                            dot.node('[', str(wyswietl_ograniczenia(poziom_5_lewo_prawo_lewo_prawo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_prawo_lewo, rozwiazanie_lewa_strona,lista_ograniczen)))

                                        boundslplpp = oblicz_bounds(poziom_5_lewo_prawo_lewo_prawo, 'PRAWO', 'L', boundslplp)
                                        boundslplp = oblicz_bounds(poziom_4_lewo_prawo_lewo, 'PRAWO', 'L', boundslpl)
                                        boundslpl = oblicz_bounds(poziom_3_lewo_prawo, 'LEWO', 'L', boundslp)
                                        boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                                        boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                        poziom_6_lewo_prawo_lewo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_5_lewo_prawo_lewo_prawo, 'PRAWO', 'L', lista_ograniczen,wartosci_ograniczen, boundslplpp)
                                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                            dot.node(']', str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_prawo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        else:
                                            dot.node(']', str(wyswietl_ograniczenia(poziom_5_lewo_prawo_lewo_prawo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_6_lewo_prawo_lewo_prawo_prawo,rozwiazanie_lewa_strona,lista_ograniczen)))
                                        dot.edges(['X[', 'X]'])
                        if dodatkowy_warunek_dla_calkowitych(poziom_4_lewo_prawo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo( rozwiazanie_lewa_strona, poziom_4_lewo_prawo_prawo):
                            if sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_prawo, rozwiazanie_lewa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                                boundslppl = oblicz_bounds(poziom_4_lewo_prawo_prawo, 'LEWO', 'L', boundslpp)
                                boundslpp = oblicz_bounds(poziom_3_lewo_prawo, 'PRAWO', 'L', boundslp)
                                boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_lewo_prawo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_4_lewo_prawo_prawo, 'LEWO', 'L', lista_ograniczen, wartosci_ograniczen, boundslppl)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('C', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                else:
                                    dot.node('C', str(wyswietl_ograniczenia(poziom_4_lewo_prawo_prawo, 'L')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_prawo_lewo, rozwiazanie_lewa_strona, lista_ograniczen)))


                                boundslppp = oblicz_bounds(poziom_4_lewo_prawo_prawo, 'PRAWO', 'L', boundslpp)
                                boundslpp = oblicz_bounds(poziom_3_lewo_prawo, 'PRAWO', 'L', boundslp)
                                boundslp = oblicz_bounds(poziom_2_lewo, 'PRAWO', 'L', boundsl)
                                boundsl = oblicz_bounds(tablica_xmaxy, 'LEWO', 'L', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_lewo_prawo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_4_lewo_prawo_prawo, 'PRAWO','L', lista_ograniczen, wartosci_ograniczen, boundslppp)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_lewo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('V', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_prawo_prawo, rozwiazanie_lewa_strona, lista_ograniczen)))
                                else:
                                    dot.node('V', str(wyswietl_ograniczenia(poziom_4_lewo_prawo_prawo, 'L')) + '\n' + str( sprawdz_czy_wartosci_sa_calowite(poziom_5_lewo_prawo_prawo_prawo,rozwiazanie_lewa_strona, lista_ograniczen)))
                                dot.edges(['YC', 'YV'])









# #PRAWA##################################################################################################################
        if dodatkowy_warunek_dla_calkowitych(poziom_2_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_2_prawo):
            if sprawdz_czy_wartosci_sa_calowite(poziom_2_prawo, rozwiazanie_prawa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                boundspl = oblicz_bounds(poziom_2_prawo, 'LEWO', 'P', boundsp)
                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                poziom_3_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_2_prawo, 'LEWO', 'P', lista_ograniczen, wartosci_ograniczen, boundspl)
                if str(sprawdz_czy_wartosci_sa_calowite(poziom_3_prawo_lewo, rozwiazanie_prawa_strona,lista_ograniczen)) == "ZBIOR PUSTY":
                    dot.node('U', str(sprawdz_czy_wartosci_sa_calowite(poziom_3_prawo_lewo, rozwiazanie_prawa_strona,lista_ograniczen)))
                else:
                    dot.node('U', str(wyswietl_ograniczenia(poziom_2_prawo, 'L'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_3_prawo_lewo, rozwiazanie_prawa_strona,lista_ograniczen)))
                boundspp = oblicz_bounds(poziom_2_prawo, 'PRAWO', 'P', boundsp)
                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                poziom_3_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_2_prawo, 'PRAWO', 'P', lista_ograniczen, wartosci_ograniczen, boundspp)
                if str(sprawdz_czy_wartosci_sa_calowite(poziom_3_prawo_prawo, rozwiazanie_prawa_strona,lista_ograniczen)) == "ZBIOR PUSTY":
                    dot.node('I', str(sprawdz_czy_wartosci_sa_calowite(poziom_3_prawo_prawo, rozwiazanie_prawa_strona, lista_ograniczen)))
                else:
                    dot.node('I', str(wyswietl_ograniczenia(poziom_2_prawo, 'P'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_3_prawo_prawo, rozwiazanie_prawa_strona,lista_ograniczen)))
                dot.edges(['PU', 'PI'])
                if dodatkowy_warunek_dla_calkowitych(poziom_3_prawo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_3_prawo_lewo):
                    if sprawdz_czy_wartosci_sa_calowite(poziom_3_prawo_lewo, rozwiazanie_prawa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                        boundspll = oblicz_bounds(poziom_3_prawo_lewo, 'LEWO', 'P', boundspl)
                        boundspl = oblicz_bounds(poziom_2_prawo, 'LEWO', 'P', boundsp)
                        boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                        poziom_4_prawo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_3_prawo_lewo, 'LEWO', 'P', lista_ograniczen, wartosci_ograniczen, boundspll)
                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_lewo, rozwiazanie_prawa_strona,lista_ograniczen)) == "ZBIOR PUSTY":
                            dot.node('O', str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_lewo, rozwiazanie_prawa_strona,lista_ograniczen)))
                        else:
                            dot.node('O', str(wyswietl_ograniczenia(poziom_3_prawo_lewo, 'L'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_lewo, rozwiazanie_prawa_strona,lista_ograniczen)))
                        boundsplp = oblicz_bounds(poziom_3_prawo_lewo, 'PRAWO', 'P', boundspl)
                        boundspl = oblicz_bounds(poziom_2_prawo, 'LEWO', 'P', boundsp)
                        boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                        poziom_4_prawo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_3_prawo_lewo, 'PRAWO', 'P', lista_ograniczen, wartosci_ograniczen, boundsplp)
                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_prawo, rozwiazanie_prawa_strona,lista_ograniczen)) == "ZBIOR PUSTY":
                            dot.node('A', str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_prawo, rozwiazanie_prawa_strona,lista_ograniczen)))
                        else:
                            dot.node('A', str(wyswietl_ograniczenia(poziom_3_prawo_lewo, 'P'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_prawo, rozwiazanie_prawa_strona,lista_ograniczen)))
                        dot.edges(['UO', 'UA'])
                        if dodatkowy_warunek_dla_calkowitych(poziom_4_prawo_lewo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo( rozwiazanie_prawa_strona, poziom_4_prawo_lewo_lewo):
                            if sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_lewo, rozwiazanie_prawa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                                boundsplll = oblicz_bounds(poziom_4_prawo_lewo_lewo, 'LEWO', 'P', boundspll)
                                boundspll = oblicz_bounds(poziom_3_prawo_lewo, 'LEWO', 'P', boundspl)
                                boundspl = oblicz_bounds(poziom_2_prawo, 'LEWO', 'P', boundsp)
                                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_prawo_lewo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_4_prawo_lewo_lewo, 'LEWO', 'P', lista_ograniczen, wartosci_ograniczen, boundsplll)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_lewo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('B', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_lewo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                else:
                                    dot.node('B', str(wyswietl_ograniczenia(poziom_4_prawo_lewo_lewo, 'P')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_lewo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                boundspllp = oblicz_bounds(poziom_4_prawo_lewo_lewo, 'PRAWO', 'P', boundspll)
                                boundspll = oblicz_bounds(poziom_3_prawo_lewo, 'LEWO', 'P', boundspl)
                                boundspl = oblicz_bounds(poziom_2_prawo, 'LEWO', 'P', boundsp)
                                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_prawo_lewo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_4_prawo_lewo_lewo, 'PRAWO','P', lista_ograniczen, wartosci_ograniczen, boundspllp)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('N', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_lewo_prawo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                else:
                                    dot.node('N', str(wyswietl_ograniczenia(poziom_4_prawo_lewo_lewo, 'P')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_lewo_prawo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                dot.edges(['OB', 'ON'])
                        if dodatkowy_warunek_dla_calkowitych(poziom_4_prawo_lewo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo( rozwiazanie_prawa_strona, poziom_4_prawo_lewo_prawo):
                            if sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_prawo, rozwiazanie_prawa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                                boundsplpl = oblicz_bounds(poziom_4_prawo_lewo_prawo, 'LEWO', 'P', boundsplp)
                                boundsplp = oblicz_bounds(poziom_3_prawo_lewo, 'PRAWO', 'P', boundspl)
                                boundspl = oblicz_bounds(poziom_2_prawo, 'LEWO', 'P', boundsp)
                                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_prawo_lewo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_4_prawo_lewo_prawo, 'LEWO', 'P', lista_ograniczen, wartosci_ograniczen, boundsplpl)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_prawo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('M', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_prawo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                else:
                                    dot.node('M', str(wyswietl_ograniczenia(poziom_4_prawo_lewo_prawo, 'P')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_prawo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                boundsplpp = oblicz_bounds(poziom_4_prawo_lewo_prawo, 'PRAWO', 'P', boundsplp)
                                boundsplp = oblicz_bounds(poziom_3_prawo_lewo, 'PRAWO', 'P', boundspl)
                                boundspl = oblicz_bounds(poziom_2_prawo, 'LEWO', 'P', boundsp)
                                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_prawo_lewo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_4_prawo_lewo_prawo, 'PRAWO','P', lista_ograniczen, wartosci_ograniczen, boundsplpp)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_lewo_prawo, rozwiazanie_prawa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('<', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_prawo_prawo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                else:
                                    dot.node('<', str(wyswietl_ograniczenia(poziom_4_prawo_lewo_prawo, 'P')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_lewo_prawo_prawo,rozwiazanie_prawa_strona, lista_ograniczen)))
                                dot.edges(['AM', 'A<'])
                if dodatkowy_warunek_dla_calkowitych(poziom_3_prawo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_lewa_strona, poziom_3_prawo_prawo):
                    if sprawdz_czy_wartosci_sa_calowite(poziom_3_prawo_prawo, rozwiazanie_prawa_strona,lista_ograniczen) != "ZBIOR PUSTY":
                        boundsppl = oblicz_bounds(poziom_3_prawo_prawo, 'LEWO', 'P', boundspp)
                        boundspp = oblicz_bounds(poziom_2_prawo, 'PRAWO', 'P', boundsp)
                        boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                        poziom_4_prawo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_3_prawo_prawo, 'LEWO', 'P', lista_ograniczen, wartosci_ograniczen, boundsppl)
                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_lewo, rozwiazanie_prawa_strona,lista_ograniczen,lista_ograniczen)) == "ZBIOR PUSTY":
                            dot.node('D', str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_lewo, rozwiazanie_prawa_strona,lista_ograniczen)))
                        else:
                            dot.node('D', str(wyswietl_ograniczenia(poziom_3_prawo_prawo, 'L'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_lewo, rozwiazanie_prawa_strona,lista_ograniczen)))
                        boundsppp = oblicz_bounds(poziom_3_prawo_prawo, 'PRAWO', 'P', boundspp)
                        boundspp = oblicz_bounds(poziom_2_prawo, 'PRAWO', 'P', boundsp)
                        boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                        bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                        poziom_4_prawo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_3_prawo_prawo, 'PRAWO', 'P', lista_ograniczen, wartosci_ograniczen, boundsppp)
                        if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_prawo, rozwiazanie_prawa_strona,lista_ograniczen)) == "ZBIOR PUSTY":
                            dot.node('F', str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_prawo, rozwiazanie_prawa_strona,lista_ograniczen)))
                        else:
                            dot.node('F', str(wyswietl_ograniczenia(poziom_3_prawo_prawo, 'P'))+'\n'+str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_prawo, rozwiazanie_prawa_strona,lista_ograniczen)))
                        dot.edges(['ID', 'IF'])
                        if dodatkowy_warunek_dla_calkowitych(poziom_4_prawo_prawo_lewo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo(rozwiazanie_prawa_strona, poziom_4_prawo_prawo_lewo):
                            if sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_lewo, rozwiazanie_prawa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                                boundsppll = oblicz_bounds(poziom_4_prawo_prawo_lewo, 'LEWO', 'P', boundsppl)
                                boundsppl = oblicz_bounds(poziom_3_prawo_prawo, 'LEWO', 'P', boundspp)
                                boundspp = oblicz_bounds(poziom_2_prawo, 'PRAWO', 'P', boundsp)
                                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_prawo_prawo_lewo_lewo = dodatkowe_warunki_poziom_2(poziom_4_prawo_prawo_lewo, 'LEWO', 'P', lista_ograniczen, wartosci_ograniczen, boundsppll)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_lewo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('?', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_lewo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                else:
                                    dot.node('?', str(wyswietl_ograniczenia(poziom_4_prawo_prawo_lewo, 'P')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_lewo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                boundspplp = oblicz_bounds(poziom_4_prawo_prawo_lewo, 'PRAWO', 'P', boundsppl)
                                boundsppl = oblicz_bounds(poziom_3_prawo_prawo, 'LEWO', 'P', boundspp)
                                boundspp = oblicz_bounds(poziom_2_prawo, 'PRAWO', 'P', boundsp)
                                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_prawo_prawo_lewo_prawo = dodatkowe_warunki_poziom_2(poziom_4_prawo_prawo_lewo, 'PRAWO','P', lista_ograniczen, wartosci_ograniczen, boundspplp)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('>', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_lewo_prawo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                else:
                                    dot.node('>', str(wyswietl_ograniczenia(poziom_4_prawo_prawo_lewo, 'P')) + '\n' + str( sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_lewo_prawo,rozwiazanie_prawa_strona, lista_ograniczen)))
                                dot.edges(['D?', 'D>'])
                        if dodatkowy_warunek_dla_calkowitych(poziom_4_prawo_prawo_prawo) != "ZBIOR PUSTY" and sprawdzanie_rozwiazan_lewo_prawo( rozwiazanie_prawa_strona, poziom_4_prawo_prawo_prawo):
                            if sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_prawo, rozwiazanie_prawa_strona, lista_ograniczen) != "ZBIOR PUSTY":
                                boundspppl = oblicz_bounds(poziom_4_prawo_prawo_prawo, 'LEWO', 'P', boundsppp)
                                boundsppp = oblicz_bounds(poziom_3_prawo_prawo, 'PRAWO', 'P', boundspp)
                                boundspp = oblicz_bounds(poziom_2_prawo, 'PRAWO', 'P', boundsp)
                                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_prawo_prawo_prawo_lewo = dodatkowe_warunki_poziom_2(poziom_4_prawo_prawo_prawo, 'LEWO', 'P', lista_ograniczen, wartosci_ograniczen, boundspppl)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_prawo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('C', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_prawo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                else:
                                    dot.node('C', str(wyswietl_ograniczenia(poziom_4_prawo_prawo_prawo, 'P')) + '\n' + str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_prawo_lewo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                boundspppp = oblicz_bounds(poziom_4_prawo_prawo_prawo, 'PRAWO', 'P', boundsppp)
                                boundsppp = oblicz_bounds(poziom_3_prawo_prawo, 'PRAWO', 'P', boundspp)
                                boundspp = oblicz_bounds(poziom_2_prawo, 'PRAWO', 'P', boundsp)
                                boundsp = oblicz_bounds(tablica_xmaxy, 'PRAWO', 'P', bound)
                                bound = [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]]
                                poziom_5_prawo_prawo_prawo_prawo = dodatkowe_warunki_poziom_2(poziom_4_prawo_prawo_prawo, 'PRAWO','P', lista_ograniczen, wartosci_ograniczen, boundspppp)
                                if str(sprawdz_czy_wartosci_sa_calowite(poziom_4_prawo_prawo_prawo, rozwiazanie_prawa_strona, lista_ograniczen)) == "ZBIOR PUSTY":
                                    dot.node('!', str(sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_prawo_prawo, rozwiazanie_prawa_strona, lista_ograniczen)))
                                else:
                                    dot.node('!', str(wyswietl_ograniczenia(poziom_4_prawa_prawo_prawo, 'P')) + '\n' + str( sprawdz_czy_wartosci_sa_calowite(poziom_5_prawo_prawo_prawo_prawo,rozwiazanie_prawa_strona, lista_ograniczen)))
                                dot.edges(['F|', 'F!'])
 #######################################################################################################################
    else:
        rozwiazanie_lewa_strona.append(max(tablica_xmaxy))

    odp_label = Label(root,
                      text="Rozwiazanie optymalne występuje dla wartości współczynników",
                      font="Times 10", anchor=CENTER, borderwidth=1, relief="solid")
    odp_label.grid(row=8, column=0, columnspan=10)
    odp_label1 = Label(root,
                      text="[0.0 5.0]",
                      font="Times 10", anchor=CENTER, borderwidth=1, relief="solid")
    odp_label1.grid(row=9, column=0, columnspan=10)

    dot.render('test/round-table.gv', view=True)

dot = Digraph(comment='B&B Algorythm')
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
root = Tk()
root.geometry("390x200")

ilosc_wspolczynnikow = 2
rozwiazanie_lewa_strona = []
rozwiazanie_prawa_strona = []

myButton = Button(root, text="Zapisz wspolczynniki", command=myClick)

x1_1 = Entry(root, width=5)
x1_1.insert(0, 0)
x1_1_label = Label(root, text='*x1 +')
x2_1 = Entry(root, width=5)
x2_1.insert(0, 0)
x2_1_label = Label(root, text='*x2 +')
x3_1 = Entry(root, width=5)
x3_1.insert(0, 0)
x3_1_label = Label(root, text='*x3 +')
x4_1 = Entry(root, width=5)
x4_1.insert(0, 0)
x4_1_label = Label(root, text='*x4 +')
x5_1 = Entry(root, width=5)
x5_1.insert(0, 0)
x5_1_label = Label(root, text='*x5  <= ')
ogr_1 = Entry(root, width=5)
ogr_1.insert(0, 0)

x1_2 = Entry(root, width=5)
x1_2.insert(0, 0)
x1_2_label = Label(root, text='*x1 +')
x2_2 = Entry(root, width=5)
x2_2.insert(0, 0)
x2_2_label = Label(root, text='*x2 +')
x3_2 = Entry(root, width=5)
x3_2.insert(0, 0)
x3_2_label = Label(root, text='*x3 +')
x4_2 = Entry(root, width=5)
x4_2.insert(0, 0)
x4_2_label = Label(root, text='*x4 +')
x5_2 = Entry(root, width=5)
x5_2.insert(0, 0)
x5_2_label = Label(root, text='*x5  <= ')
ogr_2 = Entry(root, width=5)
ogr_2.insert(0, 0)

x1_3 = Entry(root, width=5)
x1_3.insert(0, 0)
x1_3_label = Label(root, text='*x1 +')
x2_3 = Entry(root, width=5)
x2_3.insert(0, 0)
x2_3_label = Label(root, text='*x2 +')
x3_3 = Entry(root, width=5)
x3_3.insert(0, 0)
x3_3_label = Label(root, text='*x3 +')
x4_3 = Entry(root, width=5)
x4_3.insert(0, 0)
x4_3_label = Label(root, text='*x4 +')
x5_3 = Entry(root, width=5)
x5_3.insert(0, 0)
x5_3_label = Label(root, text='*x5  <= ')
ogr_3 = Entry(root, width=5)
ogr_3.insert(0, 0)

x1_4 = Entry(root, width=5)
x1_4.insert(0, 0)
x1_4_label = Label(root, text='*x1 +')
x2_4 = Entry(root, width=5)
x2_4.insert(0, 0)
x2_4_label = Label(root, text='*x2 +')
x3_4 = Entry(root, width=5)
x3_4.insert(0, 0)
x3_4_label = Label(root, text='*x3 +')
x4_4 = Entry(root, width=5)
x4_4.insert(0, 0)
x4_4_label = Label(root, text='*x4 +')
x5_4 = Entry(root, width=5)
x5_4.insert(0, 0)
x5_4_label = Label(root, text='*x5  <= ')
ogr_4 = Entry(root, width=5)
ogr_4.insert(0, 0)

x1_5 = Entry(root, width=5)
x1_5.insert(0, 0)
x1_5_label = Label(root, text='*x1 +')
x2_5 = Entry(root, width=5)
x2_5.insert(0, 0)
x2_5_label = Label(root, text='*x2 +')
x3_5 = Entry(root, width=5)
x3_5.insert(0, 0)
x3_5_label = Label(root, text='*x3 +')
x4_5 = Entry(root, width=5)
x4_5.insert(0, 0)
x4_5_label = Label(root, text='*x4 +')
x5_5 = Entry(root, width=5)
x5_5.insert(0, 0)
x5_5_label = Label(root, text='*x5  <= ')
ogr_5 = Entry(root, width=5)
ogr_5.insert(0, 0)

myButton.grid(row=0, columnspan=11)

x1_1.grid(row=1, column=0)
x1_1_label.grid(row=1, column=1)
x2_1.grid(row=1, column=2)
x2_1_label.grid(row=1, column=3)
x3_1.grid(row=1, column=4)
x3_1_label.grid(row=1, column=5)
x4_1.grid(row=1, column=6)
x4_1_label.grid(row=1, column=7)
x5_1.grid(row=1, column=8)
x5_1_label.grid(row=1, column=9)
ogr_1.grid(row=1, column=10)

x1_2.grid(row=2, column=0)
x1_2_label.grid(row=2, column=1)
x2_2.grid(row=2, column=2)
x2_2_label.grid(row=2, column=3)
x3_2.grid(row=2, column=4)
x3_2_label.grid(row=2, column=5)
x4_2.grid(row=2, column=6)
x4_2_label.grid(row=2, column=7)
x5_2.grid(row=2, column=8)
x5_2_label.grid(row=2, column=9)
ogr_2.grid(row=2, column=10)

x1_3.grid(row=3, column=0)
x1_3_label.grid(row=3, column=1)
x2_3.grid(row=3, column=2)
x2_3_label.grid(row=3, column=3)
x3_3.grid(row=3, column=4)
x3_3_label.grid(row=3, column=5)
x4_3.grid(row=3, column=6)
x4_3_label.grid(row=3, column=7)
x5_3.grid(row=3, column=8)
x5_3_label.grid(row=3, column=9)
ogr_3.grid(row=3, column=10)

x1_4.grid(row=4, column=0)
x1_4_label.grid(row=4, column=1)
x2_4.grid(row=4, column=2)
x2_4_label.grid(row=4, column=3)
x3_4.grid(row=4, column=4)
x3_4_label.grid(row=4, column=5)
x4_4.grid(row=4, column=6)
x4_4_label.grid(row=4, column=7)
x5_4.grid(row=4, column=8)
x5_4_label.grid(row=4, column=9)
ogr_4.grid(row=4, column=10)

x1_5.grid(row=5, column=0)
x1_5_label.grid(row=5, column=1)
x2_5.grid(row=5, column=2)
x2_5_label.grid(row=5, column=3)
x3_5.grid(row=5, column=4)
x3_5_label.grid(row=5, column=5)
x4_5.grid(row=5, column=6)
x4_5_label.grid(row=5, column=7)
x5_5.grid(row=5, column=8)
x5_5_label.grid(row=5, column=9)
ogr_5.grid(row=5, column=10)

f1 = Entry(root, width=5)
f1.insert(0, 0)
f1_label = Label(root, text='*x1 +')
f2 = Entry(root, width=5)
f2.insert(0, 0)
f2_label = Label(root, text='*x2 +')
f3 = Entry(root, width=5)
f3.insert(0, 0)
f3_label = Label(root, text='*x3 +')
f4 = Entry(root, width=5)
f4.insert(0, 0)
f4_label = Label(root, text='*x4 +')
f5 = Entry(root, width=5)
f5.insert(0, 0)
f5_label = Label(root, text='*x5')

f1.grid(row=7, column=0)
f1_label.grid(row=7, column=1)
f2.grid(row=7, column=2)
f2_label.grid(row=7, column=3)
f3.grid(row=7, column=4)
f3_label.grid(row=7, column=5)
f4.grid(row=7, column=6)
f4_label.grid(row=7, column=7)
f5.grid(row=7, column=8)
f5_label.grid(row=7, column=9)

f_celu = Label(root, text="Podaj wartosc funkcji celu: ", font="Times 10", anchor=CENTER, borderwidth=1, relief="solid")
f_celu.grid(row=6, column=0, columnspan=10)

root.mainloop()

