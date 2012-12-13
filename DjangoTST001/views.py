# -*- coding: utf-8 -*-
# Включили поддержку UTF-8 в Python. Без этого даже комментарии на русском языке нельзя писать.

from django.http import HttpResponse, Http404
import random
import datetime
import time


def hello ( request ) :
    return HttpResponse ( "Hello world! Привет питон!")

def funMainHomePage ( request ) :
    szHello = ""
    for  szCount in u'Главная страница' :
        szHello += szCount*random.randint(1, 3)
    szHello = '<html><body><h1>' + szHello                 \
              + '</h1><h2> %s </h2></body></html>'         \
              % datetime.datetime.now( )
    return HttpResponse ( szHello )

def hours_ahead ( request, offset ) :
    try:
        offset = int ( offset )
    except ValueError:
        raise Http404 ( )
    dt = datetime.datetime.now ( ) + datetime.timedelta( hours = offset )
    html = "<html><body>Через %s часов будет %s.</body></html>"     \
           % ( offset, dt )
    return HttpResponse ( html )

def junk_nav ( request, offsetPageNum ) :
    tStart = time.clock()
    try:
        offsetPageNum = int ( offsetPageNum )
    except ValueError:
        raise Http404 ( )
    random.seed ( offsetPageNum )
    dimX = 30  # число столбцов навигационного массива
    dimY = 15  # число строк навигационного массива
    iCountDown = dimX * dimY   # емкость создаваемого массива (после исползуется как впомогательная)
    iNumNavFocus = random.randint (2, int ( iCountDown / 80. ) )   # число очагов навигации
    iMaxRadiusFocus = 12     # предельный разбег фокуса навигации
    iMinRadiusFocus = 5     # минимальный разбег фокуса навигации
    # инициализируем массив размерностью dimX на dimY и глубиной 2
    dim = [[[ 0 # countY * dimX + countX + 1
        for i in range(2)]
            for countY in range(dimY)]
                for countX in range(dimX)]

    # начинаем заполнять навигационный массив
    lstFocusInfo =  [] # создает вспомогательный лист с даными о рзмерах уздлв фокуса
    for CountFocus in range ( iNumNavFocus ) :
        # перебираем по циклу очаги навигации
        iRadiusFocus = random.randint(iMinRadiusFocus, iMaxRadiusFocus )
        iCurentCenterFocusX = random.randint(1,dimX-2)
        iCurentCenterFocusY = random.randint(1,dimY-2)
        dim[iCurentCenterFocusX][iCurentCenterFocusY][0] = iCountDown
        dim[iCurentCenterFocusX][iCurentCenterFocusY][1] = iNumNavFocus
        iCountDown -= 1
        for CountRadius in range (1, iRadiusFocus ) :
            iCurentFocusSquare = CountRadius * CountRadius
            for CountTmpFocus in range ( 1, iCurentFocusSquare*2 ) :
                iTmp0X = random.randint(iCurentCenterFocusX-CountRadius,iCurentCenterFocusX+CountRadius)
                iTmp0Y = random.randint(iCurentCenterFocusY-CountRadius,iCurentCenterFocusY+CountRadius)
                if iTmp0Y < 0 or iTmp0X < 0 or iTmp0Y >= dimY or iTmp0X >= dimX:
                    continue

                if dim[iTmp0X][iTmp0Y][0] == 0 :
                    dim[iTmp0X][iTmp0Y][0] = iCountDown
                    iCountDown -= 1
        lstFocusInfo.append ( dimX * dimY - iCountDown ) # дописываем во вспомогательный лист промежуточный размер текущего узла фокуса

    # Завершаем обработку данных в листе даных о размерах узлов фокуса
    # for iCountDown

    # результирующий вывод
    html = "<html><body><table cellpadding='5' cellspacing='1'>"
    for CountY in range( dimY ) :
        html += "<tr>"
        for CountX in range( dimX ) :
            html += "<td bgcolor='#"
            html += "99%02x99" % int((dim[CountX][CountY][0]*255.)/(dimX*dimY))
            html += "'><a href='/nav/%03d/'" % dim[CountX][CountY][0]
            html += ">%03d</a></td>" % dim[CountX][CountY][0]
        html += "</tr>"
    html += "</table> Время выполнения: %f " % float(time.clock() - tStart)
    html += "<br /> lstFocusInfo: %d, %s" % (  len(lstFocusInfo), lstFocusInfo )
    html += "</body></html>"
    # вывод
    return HttpResponse ( html )
