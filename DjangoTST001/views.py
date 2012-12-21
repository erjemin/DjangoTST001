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
    iCountDown = iTotalDim = dimX * dimY   # емкость создаваемого массива (после исползуется как впомогательная)
    iMaxRadiusFocus = 12     # предельный разбег фокуса навигации
    iMinRadiusFocus = 5     # минимальный разбег фокуса навигации
    iNumNavFocus = random.randint(2 , int ( iTotalDim / 75 ))   # число очагов навигации
    if iNumNavFocus > 6 :
        iNumNavFocus = 6
    # инициализируем массив размерностью dimX на dimY и глубиной 2
    dim = [[[ 0 # countY * dimX + countX + 1
        for i in range(2)]
            for countY in range(dimY)]
                for countX in range(dimX)]

    lstFocusInfo =  [[ 0       # создает вспомогательный лист с даными о рзмерах уздлв фокуса
        for i in range (2) ]
            for countY in range( iNumNavFocus )]

    # начинаем заполнять навигационный массив
    for CountFocus in range ( iNumNavFocus ) :
        # перебираем по циклу очаги навигации
        iRadiusFocus = random.randint(iMinRadiusFocus, iMaxRadiusFocus )
        iCurentCenterFocusX = random.randint(1,dimX-2)
        iCurentCenterFocusY = random.randint(1,dimY-2)
        dim[iCurentCenterFocusX][iCurentCenterFocusY][0] = iCountDown
        dim[iCurentCenterFocusX][iCurentCenterFocusY][1] = CountFocus+1
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
                    dim[iTmp0X][iTmp0Y][1] = CountFocus+1
                    iCountDown -= 1
        lstFocusInfo[CountFocus][0] = iCountDown # дописываем во вспомогательный лист промежуточный размер текущего узла фокуса

    # Завершаем обработку данных в листе даных о размерах узлов фокуса
    lstFocusInfo[0][1] = iTotalDim - lstFocusInfo[0][0] # дописываем во вспомогательный лист площадь текущего узла фокуса
    for iCountDown in range ( 1, iNumNavFocus ) :
        lstFocusInfo[iCountDown][1] = lstFocusInfo[iCountDown-1][0] - lstFocusInfo[iCountDown][0]

    # результирующий вывод
    html = "<html><body><table cellpadding='5' cellspacing='1'>"
    for CountY in range( dimY ) :
        html += "<tr>"
        for CountX in range( dimX ) :
            if dim[CountX][CountY][1] == 0 :
                html += "<td bgcolor='#808080'>"
                html += "<a href='/nav/%04d/' style='color:#909090'>0000</a>" % dim[CountX][CountY][0]
            elif dim[CountX][CountY][1] == 1 :
                html += "<td bgcolor='#%02x0000'>" % int(0x9d+((dim[CountX][CountY][0]-lstFocusInfo[0][0])*98.)/lstFocusInfo[0][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[CountX][CountY][0], dim[CountX][CountY][1])
            elif dim[CountX][CountY][1] == 2 :
                html += "<td bgcolor='#00%02x00'>" % int(0x9d+((dim[CountX][CountY][0]-lstFocusInfo[1][0])*98.)/lstFocusInfo[1][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[CountX][CountY][0], dim[CountX][CountY][1])
            elif dim[CountX][CountY][1] == 3 :
                html += "<td bgcolor='#0000%02x'>" % int(0x9d+((dim[CountX][CountY][0]-lstFocusInfo[2][0])*98.)/lstFocusInfo[2][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[CountX][CountY][0], dim[CountX][CountY][1])
            elif dim[CountX][CountY][1] == 4 :
                html += "<td bgcolor='#FF%02xFf'>" % int(0x9d-((dim[CountX][CountY][0]-lstFocusInfo[3][0])*98.)/lstFocusInfo[3][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[CountX][CountY][0], dim[CountX][CountY][1])
            elif dim[CountX][CountY][1] == 5 :
                html += "<td bgcolor='#FFFF%02x'>" % int(0x9d-((dim[CountX][CountY][0]-lstFocusInfo[4][0])*98.)/lstFocusInfo[4][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[CountX][CountY][0], dim[CountX][CountY][1])
            elif dim[CountX][CountY][1] == 6 :
                html += "<td bgcolor='#%02xFFFF'>" % int(0x9d-((dim[CountX][CountY][0]-lstFocusInfo[5][0])*98.)/lstFocusInfo[5][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[CountX][CountY][0], dim[CountX][CountY][1])
            else :
                html += "<td>err0"
            html += "</td>"
        html += "</tr>"
    html += "</table> Время выполнения: %f " % float(time.clock() - tStart)
    html += "<br /> lstFocusInfo: %d, %s" % (  len(lstFocusInfo), lstFocusInfo )
    html += "</body></html>"
    # вывод
    return HttpResponse ( html )
