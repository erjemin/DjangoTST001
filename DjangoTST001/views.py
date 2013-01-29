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
    html = "<html><body>"
    dimX = 30  # число столбцов навигационного массива
    dimY = 15  # число строк навигационного массива
    iCountDown = iTotalDim = dimX * dimY   # емкость создаваемого массива (после исползуется как впомогательная)
    iMaxRadiusFocus = 12     # предельный разбег фокуса навигации
    iMinRadiusFocus = 5     # минимальный разбег фокуса навигации
    iNumNavFocus = random.randint(2 , int ( iTotalDim / 75 ))   # число очагов навигации
    if iNumNavFocus > 6 :
        iNumNavFocus = 6
    # инициализируем массив размерностью dimX на dimY и глубиной 2
    dim = [[[ 0 # iTmpY * dimX + countX + 1
        for i in range(2)]
            for iTmpY in range(dimY)]
                for iTmpX in range(dimX)]

    lstFocusInfo =  [[ 0       # создает вспомогательный лист с даными о рзмерах уздлв фокуса
        for i in range (2) ]
            for iTmpY in range( iNumNavFocus )]

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
                iTmpX = random.randint(iCurentCenterFocusX-CountRadius,iCurentCenterFocusX+CountRadius)
                iTmpY = random.randint(iCurentCenterFocusY-CountRadius,iCurentCenterFocusY+CountRadius)
                if iTmpY < 0 or iTmpX < 0 or iTmpY >= dimY or iTmpX >= dimX:
                    continue

                if dim[iTmpX][iTmpY][0] == 0 :
                    dim[iTmpX][iTmpY][0] = iCountDown
                    dim[iTmpX][iTmpY][1] = CountFocus+1
                    iCountDown -= 1
        lstFocusInfo[CountFocus][0] = iCountDown # дописываем во вспомогательный лист промежуточный размер текущего узла фокуса
    # Добиваем оставшееся пустое ролстранство белым шумом
    # этот кусок кода можно изъять он все сильно замедляет
    while iCountDown > 1 :
        iTmpX = random.randint (0, dimX-1)
        iTmpY = random.randint (0, dimY-1)
        if dim[iTmpX][iTmpY][0] == 0 :
            dim[iTmpX][iTmpY][0] = iCountDown
            iCountDown -=1
    # контрольный выстрел если всетаки еще остались незаполненный клетки
    #if iCountDown > 1 :
    #    html += "контрольный выстрел т.к. iCountDown = %d<br />" % iCountDown
    #    for iTmpY in range( dimY ) :
    #        for iTmpX in range( dimX ) :
    #            if dim[iTmpX][iTmpY][0] == 0 :
    #                dim[iTmpX][iTmpY][0] = iCountDown
    #                iCountDown -= 1
    #            if iCountDown < 0 : break
    #        if iCountDown < 0 : break
    if iCountDown > 1 :
        html += "<h1>ERROR:: несколько нулевых клеток %d" % iCountDown

# Завершаем обработку данных в листе даных о размерах узлов фокуса
    lstFocusInfo[0][1] = iTotalDim - lstFocusInfo[0][0] # дописываем во вспомогательный лист площадь текущего узла фокуса
    for i in range ( 1, iNumNavFocus ) :
        lstFocusInfo[i][1] = lstFocusInfo[i-1][0] - lstFocusInfo[i][0]

    # результирующий вывод
    html += "<table cellpadding='5' cellspacing='1'>"
    for iTmpY in range( dimY ) :
        html += "<tr>"
        for iTmpX in range( dimX ) :
            if dim[iTmpX][iTmpY][1] == 0 :
                i = 0x80 + random.randint(-16,16)
                html += "<td bgcolor='#%02x%02x%02x'>" % ( i, i, i )
                html += "<a href='/nav/%04d/' style='color:#909090'>%04d</a>" % (dim[iTmpX][iTmpY][0], dim[iTmpX][iTmpY][0])
            elif dim[iTmpX][iTmpY][1] == 1 :
                html += "<td bgcolor='#%02x0000'>" % int(0x9d+((dim[iTmpX][iTmpY][0]-lstFocusInfo[0][0])*98.)/lstFocusInfo[0][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[iTmpX][iTmpY][0], dim[iTmpX][iTmpY][0])
            elif dim[iTmpX][iTmpY][1] == 2 :
                html += "<td bgcolor='#00%02x00'>" % int(0x9d+((dim[iTmpX][iTmpY][0]-lstFocusInfo[1][0])*98.)/lstFocusInfo[1][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[iTmpX][iTmpY][0], dim[iTmpX][iTmpY][0])
            elif dim[iTmpX][iTmpY][1] == 3 :
                html += "<td bgcolor='#0000%02x'>" % int(0x9d+((dim[iTmpX][iTmpY][0]-lstFocusInfo[2][0])*98.)/lstFocusInfo[2][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[iTmpX][iTmpY][0], dim[iTmpX][iTmpY][0])
            elif dim[iTmpX][iTmpY][1] == 4 :
                html += "<td bgcolor='#FF%02xFf'>" % int(0x9d-((dim[iTmpX][iTmpY][0]-lstFocusInfo[3][0])*98.)/lstFocusInfo[3][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[iTmpX][iTmpY][0], dim[iTmpX][iTmpY][0])
            elif dim[iTmpX][iTmpY][1] == 5 :
                html += "<td bgcolor='#FFFF%02x'>" % int(0x9d-((dim[iTmpX][iTmpY][0]-lstFocusInfo[4][0])*98.)/lstFocusInfo[4][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[iTmpX][iTmpY][0], dim[iTmpX][iTmpY][0])
            elif dim[iTmpX][iTmpY][1] == 6 :
                html += "<td bgcolor='#%02xe0e0'>" % int(0x9d-((dim[iTmpX][iTmpY][0]-lstFocusInfo[5][0])*98.)/lstFocusInfo[5][1])
                html += "<a href='/nav/%04d/'>%04d</a>" % ( dim[iTmpX][iTmpY][0], dim[iTmpX][iTmpY][0])
            else :
                html += "<td>err0"
            html += "</td>"
        html += "</tr>"
    html += "</table> Время выполнения: %f " % float(time.clock() - tStart)
    html += "<br /> lstFocusInfo: %d, %s" % (  len(lstFocusInfo), lstFocusInfo )
    html += "</body></html>"
    # вывод
    return HttpResponse ( html )

# строчка для вызова эерана с котировками c RBC:
# http://export.rbc.ru/free/index.0/free.fcgi?period=DAILY&tickers=NASD&d1=20&m1=12&y1=2012&d2=25&m2=01&y2=2013&lastdays=09&separator=%3B&data_format=BROWSER&header=1
# Общий формат:
# Вызов http://export.rbc.ru/free/index.0/free.fcgi?
# - period=DAILY -- перод. бесплатно доступны только дневные
# - tickers=NASD -- тикет (проверить, кажется доступны несколько тикетов или группы)
# - d1=20 -- дата1, день,  (два символа, лидирующий ноль, не обязательно)
# - m1=12 -- дата1, месяц (два символа, лидирующий ноль,  не обязательно)
# - y1=2012 -- дата1, год (четыре символа,  не обязательно)
# - d2=25 -- дата2, стартуем с дня,  (два символа, лидирующий ноль, не обязательно)
# - m2=01 -- дата2, стартуем с месяца (два символа, лидирующий ноль,  не обязательно)
# - y2=2013 -- дата2, год (четыре символа,  не обязательно)
# - lastdays=09 -- покзать на это колличесто дней. Ели нет дата1 или дата2 то показывает lastdays последних дней из базы
# - separator=%3B -- сепаратор (в данном сслучае ";"
# - data_format=BROWSER -- выводить в броузер (можно в файл, но его сложнее парсить).
# - header=1 -- выводить заголовок (1) или нет (0)... TICKER;DATE;OPEN;HIGH;LOW;CLOSE;VOL;WAPRICE
# порядок выдачи:
# - TICKER -- тикер
# - DATE -- дата в формате YYYY-MM-DD
# - OPEN -- цена (уровень) открытия
# - HIGH -- цена (уровень) максимум дня
# - LOW -- цена (уровень) минимум дня
# - CLOSE --цена (уровень) закрытия
# - VOL -- объём (для индексов не доступен)
# - WAPRICE -- ???? фигня какая-то