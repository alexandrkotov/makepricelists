#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
версия 45_RC07
подготовка прайс листа для zzap, Яндекс.Маркет, Google Merchant, EMEX

входные файлы:
names_jpg_url.csv - ссылки на картинки
ххххххххххххххххх - файл из отчёта сервера аналитики

выходной файл:
price_zzap.csv

    Поля
        ПРОИЗВОДИТЕЛЬ
        НОМЕР АРТИКУЛА
        НАИМЕНОВАНИЕ
        КОЛИЧЕСТВО
        ЦЕНА
        СРОК  ПОСТАВКИ
        URL ИЗОБРАЖЕНИЯ

'''
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QMessageBox, 
QCommandLinkButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QCheckBox, QRadioButton, QFileDialog)
from PyQt5.QtCore import Qt
import sys, os
import time
import shutil
import subprocess
import webbrowser
import codecs

fileURL = "names_jpg_url.csv.hide"
fileGroupYandexGoogle = "groupYandexGoogle.csv.hide"
tStart = time.time()

dicURL = {}
dicGroupYandex = {}
dicGroupGoogle = {}

prZzap = "price_zzap.csv"
prEuropart = "price_europart.csv"
prEmex = "price_emex.csv"
prArmtek = "price_armtek.csv"
prAutoru = "price_autoru.csv"


prGoogle = "price_google.xml"
prYandex = "price_yandex.xml"


def openXMLinNotepad():
    fname = window.labelOut.text()
    #print(dir(window.tableWidgetOut.cursor))
    if window.tableWidgetOut.item(0,0).text() == "Смотри файл XML":
        print("XML")
        window.tableWidgetOut.setCursor(Qt.PointingHandCursor)#CrossCursor)
        try:
            PIPE = subprocess.PIPE
            cmd = 'notepad.exe ' + fname
            p = subprocess.Popen(cmd, shell = True)
        except:
            print("На компьютере не найден notepad.exe")
    else:
        currow = window.tableWidgetOut.currentRow()
        curcol = window.tableWidgetOut.currentColumn()
        item = window.tableWidgetOut.item(currow, curcol)
        val = str(item.text()).strip()
        if val.find("http://") != -1:
            print(val)
            try:
                ie = webbrowser.get(webbrowser.iexplore)
                ie.open(val)
            except:
                print("На компьютере не найден Internet Explorer")
    

def prepDicGroupYandexGoogle(fileGroupYandexGoogle):
    f = open(fileGroupYandexGoogle,'r')
    for line in f:
        l = line.strip().split(";")
        idGoogle = l[0].strip()
        parentId = l[1].strip()
        parentName = l[2].strip()
        IdInt = l[3].strip()
        Id = l[4].strip()
        Name = l[5].strip()

        resYandex = IdInt + ";" + Name + ";" + parentId + ";" + parentName
        dicGroupYandex[Id] = resYandex
        #google_​product_​category;product_​type
        resGoogle = idGoogle + ";" + parentName + " > " + Name
        dicGroupGoogle[Id] = resGoogle
    print("Словари групп Яндекс и Google - готовы")
    #print(dicGroupYandex)
    #print(dicGroupGoogle)
        
  



def prepDicURL(fileURL):
    f = open(fileURL,'r')
    for line in f:
        l = line.strip().split(";")
        brand = l[2].strip()
        art = l[3].strip()
        url = l[6].strip()
        #print("brand = {}, art = {}, url = {}".format(brand,art,url))
        if brand in dicURL:
            curarr = dicURL[brand]
            new = art + ";" + url
            curarr.append(new)
            dicURL[brand] = curarr
        else:
            curarr = []
            new = art + ";" + url
            curarr.append(new)
            dicURL[brand] = curarr      
    f.close()
    print("Словарь URL - готово")


def getURL(brand, art):
    try:
        curarr = dicURL[brand]
        for i in range(len(curarr)):
            if curarr[i].find(art) > -1:
                res = curarr[i].split(";")[1]
                if res == None:
                    res = ""
                return res
    except:
        res = ""
        return res
 
def initNewUrl():
    
    pathLocal = os.path.abspath(os.curdir) + "\\" + fileURL
    pathFTP = r"\\m-backup02\SellOut\price\lost" + "\\" + fileURL
    try:
        print(pathLocal)
        print(pathFTP)
        shutil.copyfile(pathFTP, pathLocal)
        print("Файл names_jpg_url.csv.hide обновлён")
    except:
        print("Ошибка обновления names_jpg_url.csv.hide") 
 
    
initNewUrl()
prepDicURL(fileURL)
prepDicGroupYandexGoogle(fileGroupYandexGoogle)

#print(getURL('Koni', '90 2393SP1'))

def check1251(fname):
    '''
    #сначала ищем поле, внутри которого есть знаки ;
    try:
        s1 = line.split(';"')[0]
        s2 = ((line.split(';"')[1]).split('";')[0]).replace(";",",")
        s3 = (line.split(';"')[1]).split('";')[1]
        line = s1 + ";" + s2 + ";" + s3
    except:
        pass
    '''
    overComma = False

    try:
        f=open(fname,'r')
        #test=f.read()
        foutname = fname[:-4] + "_overcomma.csv"
        for line in f:
            try:
                s1 = line.split(';"')[0]
                s2 = ((line.split(';"')[1]).split('";')[0]).replace(";",",")
                s3 = (line.split(';"')[1]).split('";')[1]
                line = s1 + ";" + s2 + ";" + s3
                overComma = True
            except:
                pass
        if overComma == False:
            f.close()
            return fname
        else:
            f.close()
            f=open(fname,'r')
            fout = open(foutname,'w')
            for line in f:
                try:
                    s1 = line.split(';"')[0]
                    s2 = ((line.split(';"')[1]).split('";')[0]).replace(";",",")
                    s3 = (line.split(';"')[1]).split('";')[1]
                    line = s1 + ";" + s2 + ";" + s3
                except:
                    pass   
                fout.write(line)
            f.close()
            return foutname #os.path.abspath(os.curdir) + "\\" + 
    except:
        foutname = fname[:-4] + "_cp1251.csv"
        foutnameOverComma = fname[:-4] + "_cp1251_overcomma.csv"
        #print(foutname)
        fout = open(foutname,'w')
        fin = codecs.open(fname,'r','utf-8')
        #foutname = os.path.abspath(os.curdir) + "\\" + foutname 
        rowcount = 0

        for line in fin:
            line = line.strip().replace("\u015e","S").replace("\xe7","c")
            line = line.replace("\u017c","z").replace("\xe2","a").replace("\xd6","O")
            line = line.replace("\xdc","U").replace("\ufeff","").replace("\xfc","u")
            line = line.replace("\xf8","d").replace("\xd8","d").replace("\xaa","a")
            line = line.replace("\u25a1","").replace("\uf105","").replace("\xcd","I")+"\n"    
            rowcount = rowcount + 1
            fout.write(line)

        fin.close()
        fout.close()
        print("Строк {}".format(str(rowcount)))
        
        #теперь проверяем на overComma созданный cp1251
        fin = open(foutname,'r')
        for line in fin:
            try:
                s1 = line.split(';"')[0]
                s2 = ((line.split(';"')[1]).split('";')[0]).replace(";",",")
                s3 = (line.split(';"')[1]).split('";')[1]
                line = s1 + ";" + s2 + ";" + s3
                overComma = True
            except:
                pass        
        
        if overComma == False:
            fin.close()
            return foutname
        else:
            fin.close()
            fin=open(foutname,'r')
            fout = open(foutnameOverComma,'w')  
            for line in fin:
                try:
                    s1 = line.split(';"')[0]
                    s2 = ((line.split(';"')[1]).split('";')[0]).replace(";",",")
                    s3 = (line.split(';"')[1]).split('";')[1]
                    line = s1 + ";" + s2 + ";" + s3
                except:
                    pass   
                res = line.strip() + "\n"
                fout.write(res)
            fout.close()
            fin.close()
            return foutnameOverComma               

def fixCommaCRLF(fname):
    #читаем файл построчно, режем по запятым, если полей меньше 29, то прибавляем следующую строку
    #склеиваем вместе и проверяем, чтобы полей было 29
    #в строке все запятые меняем на точку с запятой, а потом ^ на запятые
    #пишем в файл fnameFix = fname[:-4] + "_fix.csv"
    #возвращаем имя fnameFix
    header = True
    
    fnameFix = fname[:-4] + "_fix.csv"
    f = open(fname,'r')
    ffix = open(fnameFix,'w')
    
    tmpline = ""
    for line in f:
        if header == True:
            header = False
            continue
        else:
            l = line.strip().split(",")
            if len(l) != 29:
                if tmpline != "":
                    res = ""
                    res = tmpline + " " + line
                    res = res.replace(",",";")
                    res = res.replace("^"," ")
                    res = res.replace('"'," ")
                    res = res.strip()
                    if len(res.split(";")) == 29:
                        res = res + "\n"
                        ffix.write(res)
                        tmpline = ""
                    else:
                        tmpline = res.strip()
                else:
                    tmpline = line.strip()
            
            else:
                res = ""
                res = line.replace(",",";")
                res = res.replace("^"," ")
                res = res.replace('"'," ")
                res = res.strip()
                res = res + "\n"
                ffix.write(res)
        
    f.close()
    ffix.close()
    return fnameFix

#читаем файл с сервера аналитики
def loadADTS():
    print("Кнопка In")
    fn = QFileDialog()
    fn.setNameFilters(["Текстовый CSV (*.csv)", "Текстовый TXT(*.txt)"])
    fn.exec_()
    fcsv = fn.selectedFiles()[0]
    row=0
    col=0

    print("fcsv={}".format(fcsv))
    fcstmp = check1251(fcsv)
    fcsv1251 = fixCommaCRLF(fcstmp)
    print("fcsv1251={}".format(fcsv1251))
    f=open(fcsv1251,'r')

    
    #f=open(fcsv,'r')#если будет ошибка, то f=codecs.open(fcsv,'r', 'utf-8')
    for line in f:

        l=line.split(";")
        if col == 0:
            col=len(l)
        row = row + 1
    f.close()
    print("row={}, col={}".format(row,col))
    window.tableWidgetIn.setRowCount(row)
    window.tableWidgetIn.setColumnCount(col)
    f=None
    currow=0

    f=open(fcsv1251,'r')
    for line in f:
        l=line.split(";")
        for j in range(col):
            window.tableWidgetIn.setItem(currow,j, QTableWidgetItem(l[j]))
        currow=currow+1
    f.close()
    res = str(fcsv1251).replace("/","\\")
    window.labelIn.setText(res)#(fcsv)
    window.labelLostURL.setText("")
    window.labelOut.setText("")
    window.labelFTP.setText("")
    window.tableWidgetOut.clear()
    window.tableWidgetOut.setRowCount(0)
    window.tableWidgetOut.setColumnCount(0)
    print("Выбран файл {}".format(res))


#формируем итоговый файл и выводим в виджет tableWidgetOut
def makePrice():
    print("Кнопка Out")
    window.tableWidgetOut.setCursor(Qt.ArrowCursor)#PointingHandCursor)#CrossCursor)
    fcsv = window.labelIn.text()
    window.labelLostURL.setText("")
    window.tableWidgetOut.clear()
    window.tableWidgetOut.setRowCount(0)
    window.tableWidgetOut.setColumnCount(0)
    #print(dir(window.tableWidgetOut))

    ferr = open('lostURL.csv','w')
    ferr.close()
    
    if len(fcsv) > 3:
        #print(fcsv)
        
        if window.radioButtonZzap.isChecked() == True:
            fzzap=open(prZzap,'w')    
        if window.radioButtonEuropart.isChecked() == True:
            feuropart=open(prEuropart,'w')
        if window.radioButtonEmex.isChecked() == True:
            femex=open(prEmex,'w')
        if window.radioButtonArmtek.isChecked() == True:
            farmtek=open(prArmtek,'w')            
        if window.radioButtonAutoru.isChecked() == True:
            fautoru=open(prAutoru,'w')

        if window.radioButtonGoogle.isChecked() == True:
            fgoogle=open(prGoogle,'w')
            prefixGoogle(fgoogle)
        if window.radioButtonYandex.isChecked() == True:
            fyandex=open(prYandex,'w')
            prefixYandex(fyandex)
            
            
        #разбираем построчно
        rowCount = 0
        colCount = 0

        fi=open(check1251(fcsv),'r')

        urlError = 0
        urlOk = 0

        for line in fi:
                
            rowCount = rowCount + 1
            l = line.strip().split(";")
            colCount = len(l)
            #print("Строка {}, полей {}".format(str(rowCount),str(colCount)))
            subGroup = l[6].strip()
            codADTS = l[1].strip().replace(".","D")#код товара в АДТС
            brand = l[5].strip()#"Koni"#из строки файла fcsv
            art = l[8].strip()#"90 2393SP1"#из строки файла fcsv
            name = l[2].strip() + "," + l[3].strip()
            qty = l[16].strip()
            if qty == "":
                qty = "0.00"
            price = l[28].strip().replace(",",".")
            if price == "NULL" or price == "":
                price = "0.00"
            priceMCKU = l[23].strip().replace(",",".")
            if priceMCKU == "NULL" or priceMCKU == "":
                priceMCKU = "0.00"
            term = "1"#l[7].strip()
            url = ""
            url = getURL(brand, art)
            if url == None:
                url = ""
            if url == "":
                ferr = open('lostURL.csv','a')

                newPicUrl = "http://sellout.etsp.ru/"
                jpgname = ""
                num = ""
                
                num = art.strip().replace(".","").replace(" ","").replace("/","_")               
                jpgname = subGroup + "_" + brand + "_" + num          

                if len(jpgname) > 24:
                    jpgtmp = jpgname
                    jpgname = jpgtmp[len(jpgtmp)-24:]+".jpg"
                else:
                    jpgname = jpgname + ".jpg"
                newPicUrl = newPicUrl + jpgname

                reserr = codADTS.replace("D",".") +";"+name+";"+brand + ";" + art + ";" + subGroup + ";" + jpgname + ";" + newPicUrl + "\n"
                ferr.write(reserr)
                ferr.close()
                urlError = urlError + 1
                url = "http://sellout.etsp.ru/noimage.jpg"

            stopNoQtyPrice = False    
            if window.checkBoxNoQtyPrice.isChecked() == True and (qty == "0.00" or price == "0.00" or priceMCKU == "0.00"):
                stopNoQtyPrice = True
                #print("stopNoQtyPrice = {}".format(stopNoQtyPrice))
                
            if (window.checkBoxNoImage.isChecked() == True and url == "http://sellout.etsp.ru/noimage.jpg") or (url != "" and url != "http://sellout.etsp.ru/noimage.jpg"):
                    #print("Пропуск картинок разрешён")

                if stopNoQtyPrice == False:
                #####################################################
                    if window.radioButtonZzap.isChecked() == True:
                        #формируем шесть полей и добавляем седьмое url
                        res = ""
                        #костыль в наименовании брендов для Zzap
                        if brand == "Worldwise Industries Limited":
                            brand = "WWI"
                        if brand == "Depo-Dossun":
                            brand = "DEPO"
                        res = brand + ";" + art + ";" + name + ";" + qty + ";" + price + ";" + term + ";" + url
                        fzzap.write(res+"\n")
                        urlOk = urlOk + 1
                    
                    if window.radioButtonEmex.isChecked() == True:
                        res = ""
                        res = brand + ";" + art + ";;" + name + ";" + qty + ";;" + price + ";" + url
                        femex.write(res+"\n")
                        urlOk = urlOk + 1

                    if window.radioButtonAutoru.isChecked() == True:
                        res = ""
                        res = codADTS + ";" + name + ";Москва, ул. 2-я Мелитопольская, вл. 4А.|+7 (495) 276 11 17|Пн.-Вс. круглосуточно;" + art + ";" + brand + ";;True;" + price + ";True;0;3;;" + url + ";;" + qty
                        fautoru.write(res+"\n")
                        urlOk = urlOk + 1

                    if window.radioButtonEuropart.isChecked() == True:
                        #print("Здесь будет сформирована строка прайса Europart")
                        #priceNoNDS = str(float("{0:.2f}".format((float(price.replace(",","."))/118)*100)))
                        res = ""
                        #res = brand + ";" + art + ";" + name + ";" + qty + ";" + priceNoNDS + ";" + url
                        res = brand + ";" + art + ";" + name + ";" + qty + ";" + priceMCKU + ";" + url
                        feuropart.write(res+"\n")
                        urlOk = urlOk + 1


                    if window.radioButtonArmtek.isChecked() == True:
                        res = ""
                        #res = brand + ";" + art + ";" + name + ";" + qty + ";" + price + ";" + url
                        res = brand + ";" + art + ";" + name + ";" + qty + ";" + priceMCKU + ";" + url
                        farmtek.write(res+"\n")
                        urlOk = urlOk + 1
    
                    
                    if (url != "" and url != "http://sellout.etsp.ru/noimage.jpg"):    
                        if window.radioButtonYandex.isChecked() == True:

                            catId = dicGroupYandex[subGroup].split(";")[0]
                            res = ""
                            res = '''<offer id="''' + codADTS + '''" available="true" fee="200">
<url>http://www.etsp.ru/search.aspx?mode=nomenclature&text=''' + art + '''&IsNomenclature=true</url>
<price>''' + price + '''</price>
<currencyId>RUR</currencyId>
<categoryId>''' + catId + '''</categoryId>
<picture>''' + url + '''</picture>
<store>true</store>
<pickup>true</pickup>
<delivery>true</delivery>
<name>''' + art + '''</name>
<vendor>''' + brand + '''</vendor>
<description>''' + name + '''</description>
<sales_notes>Доставка при заказе от 1000 рублей.</sales_notes>
</offer>
'''
                            #print("Здесь будет сформирована строка для выходного прайса Яндекс.Маркет")
                            urlOk = urlOk + 1
                            fyandex.write(res)


                        if window.radioButtonGoogle.isChecked() == True:

                            #google_​product_​category;product_​type 
                            googleProductCategory = dicGroupGoogle[subGroup].split(";")[0]
                            productType = dicGroupGoogle[subGroup].split(";")[1].replace(">","&gt;")
                            res = '''<item>
<g:id>''' + codADTS + '''</g:id>
<g:title>''' + art + '''</g:title>
<g:description>''' + name + '''</g:description>
<g:link>http://www.etsp.ru/search.aspx?mode=nomenclature&text=''' + art + '''&IsNomenclature=true</g:link>
<g:image_link>''' + url + '''</g:image_link>
<g:condition>новый</g:condition>
<g:availability>в наличии</g:availability>
<g:price>''' + price + ''' RUR</g:price>
<g:shipping>
    <g:country>РФ</g:country>
    <g:service>Доставка при заказе от 1000 RUR</g:service>
    <g:price> 1200 RUR</g:price>
</g:shipping>
<g:brand>''' + brand + '''</g:brand>
<g:mpn>''' + art + '''</g:mpn>
<g:google_product_category>''' + googleProductCategory + '''</g:google_product_category>
<g:product_type>''' + productType + '''</g:product_type>
</item>
'''
                            #print("Здесь будет сформирована строка для выходного прайса Google Merchant")
                            urlOk = urlOk + 1
                            fgoogle.write(res)

                    ##########################
                ###########


                    
        if window.radioButtonZzap.isChecked() == True:
            fzzap.close()
            fname = os.path.abspath(os.curdir) + "\\" + prZzap #+"\\price_zzap.csv"
            window.labelOut.setText(fname)
            print("Прайс Zzap - сформирован успешно")
            #выводим в window.tableWidgetOut
            print(fname)
            showOut(fname, False)
            
        if window.radioButtonYandex.isChecked() == True:
            postfixYandex(fyandex)
            fyandex.close()
            fname = os.path.abspath(os.curdir) + "\\" + prYandex #+ "\\price_yandex.xml"
            window.labelOut.setText(fname)
            print("Прайс Яндекс.Маркет - сформирован успешно")
            showOut(fname, True)

        if window.radioButtonGoogle.isChecked() == True:
            postfixGoogle(fgoogle)
            fgoogle.close()
            fname = os.path.abspath(os.curdir) + "\\" + prGoogle #+ "\\price_google.xml"
            window.labelOut.setText(fname)
            print("Прайс Google Merchant  - сформирован успешно")
            showOut(fname, True)

        if window.radioButtonEmex.isChecked() == True:
            femex.close()
            fname = os.path.abspath(os.curdir) + "\\" + prEmex #+ "\\price_emex.csv"
            window.labelOut.setText(fname)
            print("Прайс EMEX - сформирован успешно")
            print(fname)
            showOut(fname, False)

        if window.radioButtonAutoru.isChecked() == True:
            fautoru.close()
            fname = os.path.abspath(os.curdir) + "\\" + prAutoru #+ "\\price_autoru.csv"
            window.labelOut.setText(fname)
            print("Прайс Авто.ру - сформирован успешно")
            print(fname)
            showOut(fname, False)

        if window.radioButtonEuropart.isChecked() == True:
            feuropart.close()
            fname = os.path.abspath(os.curdir) + "\\" + prEuropart
            window.labelOut.setText(fname)
            print("Прайс Europart - БУДЕТ сформирован успешно")
            print(fname)
            showOut(fname, False)

        if window.radioButtonArmtek.isChecked() == True:
            farmtek.close()
            fname = os.path.abspath(os.curdir) + "\\" + prArmtek
            window.labelOut.setText(fname)
            print("Прайс Armtek - БУДЕТ сформирован успешно")
            print(fname)
            showOut(fname, False)


        if urlError > 0 and urlOk > 0 and window.checkBoxNoImage.isChecked() == False:
            window.labelLostURL.setText("сформирован неполный прайс-лист, не хватает " + str(urlError) + " изображения(й) товаров")
            window.commandLinkButtonURL.setEnabled(True)
        if urlError > 0 and urlOk > 0 and window.checkBoxNoImage.isChecked() == True:
            window.labelLostURL.setText("сформирован полный прайс-лист, пропущенно " + str(urlError) +" изображение(й) товаров")
            window.commandLinkButtonURL.setEnabled(True)            
                        
        if urlOk == 0:
            window.labelLostURL.setText("прайс-лист не сформирован")
        window.labelFTP.setText("")
        if urlError > 0:
            pathLost = fname = os.path.abspath(os.curdir) + "\\lostURL.csv"
            ftpPathLost = r"\\m-backup02\SellOut\price\lost\lostURL.csv"
            try:               
                shutil.copyfile(pathLost, ftpPathLost)
                print("lostURL.csv скопирован в \\m-backup02\SellOut\price\lost")
                
            except:
                print("Ошибка копирования lostURL.csv на FTP")

            
def showOut(fname, xml):
    
    row=0
    col=0

    if xml == True:
        window.tableWidgetOut.setRowCount(1)
        window.tableWidgetOut.setColumnCount(1)
        window.tableWidgetOut.setItem(0,0, QTableWidgetItem("Смотри файл XML"))
        window.lineEditFilter.setDisabled(True)
        return 0
    
    f=open(fname,'r')
    for line in f:
        l=line.split(";")
        if col == 0:
            col=len(l)
        row = row + 1
    f.close()
    #print("row={}, col={}".format(row,col))
    window.tableWidgetOut.setRowCount(row)
    window.tableWidgetOut.setColumnCount(col)

    currow=0
    f=open(fname,'r')
    for line in f:
        l=line.split(";")
        for j in range(col):
            window.tableWidgetOut.setItem(currow,j, QTableWidgetItem(l[j]))
        currow=currow+1
    f.close()
    window.lineEditFilter.setEnabled(True)


def getNewUrl():
    
    pathLocal = os.path.abspath(os.curdir) + "\\" + fileURL
    pathFTP = r"\\m-backup02\SellOut\price\lost" + "\\" + fileURL
    try:
        print(pathLocal)
        print(pathFTP)
        shutil.copyfile(pathFTP, pathLocal)
        print("Файл names_jpg_url.csv.hide обновлён")
        window.labelLostURL.setText("изображения обновлены")
        window.commandLinkButtonURL.setDisabled(True)
        prepDicURL(fileURL)
    except:
        print("Ошибка обновления names_jpg_url.csv.hide")
        window.labelLostURL.setText("ошибка обновления изображений")
        
def putOnFTP():

    if window.checkBoxAll.isChecked() == True:

        ftpPathDir = r"\\m-backup02\SellOut\price"
        ftpZzap = ftpPathDir + "\\"+ prZzap
        ftpYandex = ftpPathDir + "\\"+ prYandex        
        ftpGoogle = ftpPathDir + "\\"+ prGoogle
        ftpEmex = ftpPathDir + "\\"+ prEmex
        ftpAutoru = ftpPathDir + "\\"+ prAutoru
        ftpEuropart = ftpPathDir + "\\"+ prEuropart
        ftpArmtek = ftpPathDir + "\\"+ prArmtek

        locPathDir = os.path.abspath(os.curdir)
        locZzap = locPathDir + "\\"+ prZzap
        locYandex = locPathDir + "\\"+ prYandex        
        locGoogle = locPathDir + "\\"+ prGoogle
        locEmex = locPathDir + "\\"+ prEmex
        locAutoru = locPathDir + "\\"+ prAutoru
        locEuropart = locPathDir + "\\"+ prEuropart
        locArmtek = locPathDir + "\\"+ prArmtek

        
        try:
            shutil.copyfile(locZzap, ftpZzap)
            shutil.copyfile(locYandex, ftpYandex)
            shutil.copyfile(locGoogle, ftpGoogle)
            shutil.copyfile(locEmex, ftpEmex)
            shutil.copyfile(locAutoru, ftpAutoru)
            shutil.copyfile(locEuropart, ftpEuropart)
            shutil.copyfile(locArmtek, ftpArmtek)
            print("Все прайсы опубликованы")
            window.labelLostURL.setText("все прайсы опубликованы")
        except:
            print("Внимание! Не все прайсы опубликованы")
            window.labelLostURL.setText("Внимание! Не все прайсы опубликованы")

        window.checkBoxAll.setChecked(False)
        window.radioButtonZzap.setEnabled(True)
        window.radioButtonYandex.setEnabled(True)
        window.radioButtonGoogle.setEnabled(True)
        window.radioButtonEmex.setEnabled(True)             
        window.radioButtonAutoru.setEnabled(True)
        window.radioButtonEuropart.setEnabled(True)
        window.radioButtonArmtek.setEnabled(True)
        return 0

    if window.labelLostURL.text() == "прайс-лист не сформирован":
        return 0
    
    fftp = window.labelOut.text()
    window.labelFTP.setText("")
    if len(fftp) > 3:
        
        fqq = fftp.split('\\')
        fname = fqq[len(fqq)-1]
        
        ftpPath = r"\\m-backup02\SellOut\price" + "\\"+ fname
        
        try:
            shutil.copyfile(fftp, ftpPath)
            print("Публикация на FTP - успешно")
            print(ftpPath)
            window.labelFTP.setText(ftpPath)
        except:
            print("Ошибка копирования на FTP")
            infoBox = QMessageBox()
            infoBox.setIcon(QMessageBox.Critical)
            infoBox.setText("Недоступен FTP")
            #infoBox.setInformativeText("Informative Text")
            infoBox.setWindowTitle("Ошибка")
            #infoBox.setDetailedText("Detailed Text")
            infoBox.setStandardButtons(QMessageBox.Ok)# | QMessageBox.Cancel)
            infoBox.setEscapeButton(QMessageBox.Close)
            infoBox.exec_() 
            
def prefixYandex(file):

    t=time.localtime()
    Y=t.tm_year
    M=t.tm_mon
    D=t.tm_mday
    h=t.tm_hour
    m=t.tm_min
    s=t.tm_sec

    if M < 10:
        M = "0" + str(M)
    if D < 10:
        D = "0" + str(D)
    if h < 10:
        h = "0" + str(h)
    if m < 10:
        m = "0" + str(m)
    tstr = "{}-{}-{} {}:{}".format(Y,M,D,h,m)
    
    #f=open(file,'w')    
    res = '''<?xml version="1.0" encoding="windows-1251"?>
<yml_catalog date='''+tstr+'''">
<shop>
<name>ГК ОМЕГА</name>
<company>ООО "Кэт Логистик"</company>
<url>http://www.etsp.ru/</url>

<currencies>
<currency  id="RUR" rate="1"/>
</currencies>

<categories>
<category id="10000">Разное</category>
<category id="9999" parentId="10000">Другие части</category>
<category id="1" parentId="10000">Детали без группы</category>
<category id="2" parentId="10000"></category>
<category id="3" parentId="10000"></category>
<category id="4" parentId="10000"></category>
<category id="5" parentId="10000"></category>
<category id="98" parentId="10000"></category>
<category id="99" parentId="10000"></category>
<category id="9998" parentId="10000"></category>
<category id="2" parentId="10000"></category>
<category id="2" parentId="10000"></category>
<category id="10001">Масла, жидкости, автохимия</category>
<category id="10" parentId="10001">Масла моторные</category>
<category id="11" parentId="10001">Масла трансмисионные</category>
<category id="12" parentId="10001">Масла гидравлические</category>
<category id="13" parentId="10001">Смазки консистентные</category>
<category id="14" parentId="10001">Масла другие</category>
<category id="20" parentId="10001">Жидкость для систем SCR ADBLUE</category>
<category id="21" parentId="10001">Жидкости технические</category>
<category id="22" parentId="10001">Жидкости охлаждающие</category>
<category id="23" parentId="10001">Жидкость омывания окон</category>
<category id="30" parentId="10001">Автохимия</category>
<category id="40" parentId="10001">Герметики, клей</category>
<category id="80" parentId="10001">Газ</category>
<category id="10002">Диагностическое оборудование</category>
<category id="110" parentId="10002">Диагностическое оборудование</category>
<category id="10003">Пневматические системы</category>
<category id="111" parentId="10003">Воздушные краны тормозной системы</category>
<category id="112" parentId="10003">Ремкомплекты кранов</category>
<category id="113" parentId="10003">Энергоаккумуляторы и тормозные камеры</category>
<category id="1131" parentId="10003">Энергоаккумуляторы</category>
<category id="1132" parentId="10003">Камеры тормозные</category>
<category id="114" parentId="10003">Соединения воздушной системы</category>
<category id="115" parentId="10003">Ремкомплекты энергоаккумуляторов и мембраны тормозные</category>
<category id="116" parentId="10003">Шланги и трубки воздушной системы</category>
<category id="118" parentId="10003">Ресивера воздушные</category>
<category id="120" parentId="10003">Датчики воздушной системы</category>
<category id="121" parentId="10003">Датчики ABS, кронштейны и втулки датчика ABS</category>
<category id="1211" parentId="10003">Кронштейны и втулки датчика ABS</category>
<category id="1212" parentId="10003">Датчики ABS</category>
<category id="122" parentId="10003">Модуляторы и Блоки электронные</category>
<category id="123" parentId="10003">Ретрофиты и комплекты ABS</category>
<category id="10004">ДВС</category>
<category id="200" parentId="10004">Двигатель</category>
<category id="202" parentId="10004">Насосы системы охлаждения</category>
<category id="203" parentId="10004">Ремкомплекты водяных насосов</category>
<category id="204" parentId="10004">Муфты системы охлаждения двигателя</category>
<category id="2041" parentId="10004">Муфты в сборе с крыльчаткой</category>
<category id="2042" parentId="10004">Муфты без крыльчатки</category>
<category id="2043" parentId="10004">Крыльчатки муфт</category>
<category id="205" parentId="10004">Термостаты</category>
<category id="207" parentId="10004">Трубки системы охлаждения</category>
<category id="210" parentId="10004">Турбокомпрессора</category>
<category id="211" parentId="10004">вкладыши(подшипники скольжения) коренные и шатунные</category>
<category id="212" parentId="10004">Прокладки ,кроме прокладок головки двигателя</category>
<category id="213" parentId="10004">Прокладки ГБЦ двигателя и их комплекты</category>
<category id="214" parentId="10004">Ремкомплекты турбокомпрессоров</category>
<category id="215" parentId="10004">Насосы масляные и их ремкомплекты</category>
<category id="2151" parentId="10004">Насосы масляные двигателей и их ремкомплекты</category>
<category id="2152" parentId="10004">Насосы масляные трансмисси и их ремкомплекты</category>
<category id="216" parentId="10004">Колпачки маслосъемные</category>
<category id="220" parentId="10004">Ремни генератора, кондиционера</category>
<category id="221" parentId="10004">Кольца поршневые</category>
<category id="222" parentId="10004">Поршневые группы двигателя</category>
<category id="223" parentId="10004">Головка блока,шатуны,картеры</category>
<category id="224" parentId="10004">Поршнекомплекты двигателя</category>
<category id="225" parentId="10004">Гильзы цилиндров двигателя</category>
<category id="226" parentId="10004">Уплотнительные кольца гильзы</category>
<category id="227" parentId="10004">Направляющие втулки и клапаны</category>
<category id="228" parentId="10004">Коленвалы</category>
<category id="229" parentId="10004">Распредвалы</category>
<category id="230" parentId="10004">Щупы масляные</category>
<category id="231" parentId="10004">Другие моторные части</category>
<category id="232" parentId="10004">Рокеры</category>
<category id="233" parentId="10004">Маховик,Венец</category>
<category id="234" parentId="10004">Натяжители ремней и ролики</category>
<category id="235" parentId="10004">Трубки масляные</category>
<category id="240" parentId="10004">Насосы топливные высокого давления</category>
<category id="241" parentId="10004">Ремкомплекты насосов топливных</category>
<category id="242" parentId="10004">Распылители топлива</category>
<category id="243" parentId="10004">Ремкомплекты форсунок и их части</category>
<category id="244" parentId="10004">Клапаны топливной системы</category>
<category id="245" parentId="10004">Плунжерные пары топливной системы</category>
<category id="246" parentId="10004">Другие части насоса топливной системы</category>
<category id="247" parentId="10004">Клапаны плунжеров</category>
<category id="248" parentId="10004">Насосы топливные низкого давления</category>
<category id="249" parentId="10004">Трубки топливные</category>
<category id="250" parentId="10004">Насос-форсунки и форсунки в сборе</category>
<category id="308" parentId="10004">Ограничители скорости</category>
<category id="312" parentId="10004">Шкивы</category>
<category id="10005">Радиаторы, бачки расширительные</category>
<category id="201" parentId="10005">Радиаторы и кондиционеры</category>
<category id="2011" parentId="10005">Радиаторы охлаждения и интеркулеры</category>
<category id="2012" parentId="10005">Радиаторы масляные</category>
<category id="2013" parentId="10005">Радиаторы отопителя</category>
<category id="2014" parentId="10005">Радиаторы системы кондиционирования</category>
<category id="2015" parentId="10005">Другие радиаторы и кондиционеры</category>
<category id="206" parentId="10005">Бачки расширительные</category>
<category id="10006">Фильтрующие элементы</category>
<category id="117" parentId="10006">Фильтрующие элементы осушителя воздуха</category>
<category id="208" parentId="10006">Фильтры</category>
<category id="2081" parentId="10006">Фильтры топливные</category>
<category id="2082" parentId="10006">Фильтры масляные</category>
<category id="2083" parentId="10006">Фильтры воздушные</category>
<category id="2084" parentId="10006">Фильтры кабины</category>
<category id="2085" parentId="10006">Другие фильтры</category>
<category id="209" parentId="10006">Фильтры в сборе и их части</category>
<category id="2091" parentId="10006">Фильтры топливные в сборе и их части</category>
<category id="2092" parentId="10006">Фильтры воздушные в сборе и их части</category>
<category id="2093" parentId="10006">Фильтры в сборе другие и их части</category>
<category id="10007">Детали климата кабины</category>
<category id="218" parentId="10007">Детали климата кабины</category>
<category id="2181" parentId="10007">Детали системы кондиционирования</category>
<category id="2182" parentId="10007">Детали системы отопления</category>
<category id="304" parentId="10007">Автономные отопители</category>
<category id="3041" parentId="10007">Отопители</category>
<category id="3042" parentId="10007">Запчасти для автономных отопителей</category>
<category id="305" parentId="10007">Свечи накала</category>
<category id="10008">Педали газа</category>
<category id="237" parentId="10008">Педали газа</category>
<category id="10010">Баки топливные, масляные и ADBlue</category>
<category id="270" parentId="10010">Баки топливные, масляные и ADBlue и их крепления</category>
<category id="10011">Элементы выпускной системы</category>
<category id="280" parentId="10011">Бочки глушителя выхлопной системы</category>
<category id="281" parentId="10011">Трубы глушителя выхлопной системы</category>
<category id="282" parentId="10011">Гофры глушителя выхлопной системы</category>
<category id="283" parentId="10011">Хомуты и крепления выхлопной системы</category>
<category id="284" parentId="10011">Детали системы дозировки AdBlue</category>
<category id="285" parentId="10011">Детали системы рециркуляции отработавших газов</category>
<category id="286" parentId="10011">Другие детали выхлопной системы</category>
<category id="10012">Крышки резервуаров</category>
<category id="290" parentId="10012">Крышки резервуаров</category>
<category id="10013">Электрические и электронные компоненты</category>
<category id="119" parentId="10013">Кабели соединительные</category>
<category id="300" parentId="10013">Предохранители и реле электрической системы</category>
<category id="3001" parentId="10013">Реле электрической системы</category>
<category id="3002" parentId="10013">Предохранители</category>
<category id="301" parentId="10013">Датчики и другие части электрической системы</category>
<category id="3011" parentId="10013">Датчики электрической системы</category>
<category id="3012" parentId="10013">Датчики топлива, топливозаборники</category>
<category id="3013" parentId="10013">Переключатели, выключатели</category>
<category id="3014" parentId="10013">Блоки электрической системы</category>
<category id="3015" parentId="10013">Другие части электрической системы</category>
<category id="302" parentId="10013">Электрической системы соединительные провода</category>
<category id="3032" parentId="10013">Оборудование и комплектующие к аккумуляторам</category>
<category id="306" parentId="10013">Двигатели электрические</category>
<category id="309" parentId="10013">Товары для электромонтажа</category>
<category id="310" parentId="10013">Стартеры и генераторы</category>
<category id="311" parentId="10013">Детали генераторов и стартеров</category>
<category id="317" parentId="10013">Датчики износа колодок</category>
<category id="332" parentId="10013">Лампочки</category>
<category id="333" parentId="10013">Система освещения</category>
<category id="3331" parentId="10013">Фары</category>
<category id="3332" parentId="10013">Фонари</category>
<category id="3333" parentId="10013">Другие детали системы освещения</category>
<category id="805" parentId="10013">Спидометры,тахографы</category>
<category id="10014">АКБ</category>
<category id="3031" parentId="10014">Аккумуляторы</category>
<category id="10015">Системы очистки окон</category>
<category id="397" parentId="10015">Щетки стеклоочистителя</category>
<category id="398" parentId="10015">Бачки омывателя</category>
<category id="399" parentId="10015">Системы очистки окон (тяги, кронштейны)</category>
<category id="10016">Трансмссия</category>
<category id="400" parentId="10016">Трансмисионные узлы</category>
<category id="401" parentId="10016">Синхронизаторы</category>
<category id="402" parentId="10016">Подшипники подвесные</category>
<category id="403" parentId="10016">Валы трансмиссии и полуоси</category>
<category id="405" parentId="10016">Детали редукторов</category>
<category id="409" parentId="10016">Другие детали трансмисии</category>
<category id="410" parentId="10016">Сцепления и ремкомплекты</category>
<category id="411" parentId="10016">Прокладки трансмиссии</category>
<category id="417" parentId="10016">Подшипники выжимные сцепления</category>
<category id="418" parentId="10016">Диски сцепления и дискаторы</category>
<category id="4181" parentId="10016">Диски сцепления</category>
<category id="4182" parentId="10016">Корзины сцепления</category>
<category id="4183" parentId="10016">Комплекты сцепления</category>
<category id="420" parentId="10016">Цилиндры и бачки сцепления</category>
<category id="421" parentId="10016">Ремкомплекты цилиндров сцепления.</category>
<category id="422" parentId="10016">Управление коробкой передач</category>
<category id="4221" parentId="10016">Краны и Блоки управления КПП</category>
<category id="4222" parentId="10016">Детали управления КПП</category>
<category id="444" parentId="10016">Крестовины</category>
<category id="10017">Тормозная система</category>
<category id="511" parentId="10017">Тормозные барабаны и диски</category>
<category id="5111" parentId="10017">Барабаны тормозные</category>
<category id="5112" parentId="10017">Диски тормозные</category>
<category id="5113" parentId="10017">Прочие диски и барабаны</category>
<category id="512" parentId="10017">Тормозные валы</category>
<category id="513" parentId="10017">ремкомплекты тормозных валов</category>
<category id="514" parentId="10017">Защиты тормозных колодок</category>
<category id="515" parentId="10017">Суппорта тормозные</category>
<category id="516" parentId="10017">Колодки тормозные металлические и комплекты (колодки + накладки)</category>
<category id="5161" parentId="10017">Колодки тормозные металлические</category>
<category id="5162" parentId="10017">Комплекты (колодки + накладки)</category>
<category id="517" parentId="10017">Накладки тормозные</category>
<category id="5171" parentId="10017">Дисковые колодки</category>
<category id="5172" parentId="10017">Барабанные накладки</category>
<category id="518" parentId="10017">Заклёпки тормозных накладок</category>
<category id="519" parentId="10017">Другие тормозные части</category>
<category id="520" parentId="10017">Цилиндры и бачки тормозной системы</category>
<category id="521" parentId="10017">Ремкомплекты тормозных цилиндров</category>
<category id="522" parentId="10017">Рычаги тормозные</category>
<category id="523" parentId="10017">Ремкомплекты дисковых тормозов</category>
<category id="524" parentId="10017">Ремкомплекты барабанных тормозов</category>
<category id="525" parentId="10017">Пружины тормозных колодок</category>
<category id="555" parentId="10017">Компрессора воздушные</category>
<category id="556" parentId="10017">Ремкомплекты компрессоров</category>
<category id="10018">Подвеска. Рулевое управление</category>
<category id="600" parentId="10018">оси,мосты,подвесные мосты</category>
<category id="601" parentId="10018">Наконечники рулевых тяг</category>
<category id="602" parentId="10018">Шкворня</category>
<category id="603" parentId="10018">Шарниры</category>
<category id="604" parentId="10018">Кулаки поворотные</category>
<category id="609" parentId="10018">Другие части рулевого механизма</category>
<category id="610" parentId="10018">Валы рулевые</category>
<category id="611" parentId="10018">Тяги рулевые</category>
<category id="6111" parentId="10018">Тяги рулевые продольные</category>
<category id="6112" parentId="10018">Тяги рулевые поперечные</category>
<category id="664" parentId="10018">Ремкомплекты рулевых насосов</category>
<category id="665" parentId="10018">Насос рулевого управления</category>
<category id="666" parentId="10018">Рулевая колонка</category>
<category id="667" parentId="10018">Ремкомплект рулевой колонки</category>
<category id="700" parentId="10018">Балансиры</category>
<category id="701" parentId="10018">Ремкомплекты балансиров</category>
<category id="716" parentId="10018">Кольца ABS</category>
<category id="740" parentId="10018">Ступицы</category>
<category id="741" parentId="10018">Ремкомплекты ступиц</category>
<category id="742" parentId="10018">Крышки и гайки ступиц</category>
<category id="750" parentId="10018">Тяги реактивные (I/V/X - образные)</category>
<category id="7501" parentId="10018">Тяги реактивные</category>
<category id="7502" parentId="10018">Тяги реактивные (V/X - образные)</category>
<category id="751" parentId="10018">Ремкомплекты реактивных тяг</category>
<category id="752" parentId="10018">Стабилизаторы шасси и их тяги</category>
<category id="7521" parentId="10018">Стабилизаторы шасси</category>
<category id="7522" parentId="10018">Тяги стабилизаторов шасси</category>
<category id="753" parentId="10018">Ремкомплекты стабилизаторов шасси</category>
<category id="775" parentId="10018">Серьги, кронштейны рессор и амортизаторов</category>
<category id="776" parentId="10018">Ремкомплекты рессор</category>
<category id="777" parentId="10018">Рессоры, полурессоры</category>
<category id="7771" parentId="10018">Рессоры и полурессоры</category>
<category id="7772" parentId="10018">Листы рессор и полурессор</category>
<category id="778" parentId="10018">Пальцы, болты рессор и амортизаторов</category>
<category id="779" parentId="10018">Стремянки рессор</category>
<category id="780" parentId="10018">Другие детали подвески шасси</category>
<category id="10019">Рама</category>
<category id="620" parentId="10019">Рама, лонжероны и поперечены</category>
<category id="901" parentId="10019">Опорные устройства</category>
<category id="902" parentId="10019">Тяговые и сцепные устройства и их ремкомплекты</category>
<category id="9021" parentId="10019">Тяговые и сцепные устройства</category>
<category id="9022" parentId="10019">РМК тяговых и сцепных устройств</category>
<category id="10020">Крепеж</category>
<category id="702" parentId="10020">болты,шпильки</category>
<category id="703" parentId="10020">Гайки</category>
<category id="704" parentId="10020">Шайбы</category>
<category id="705" parentId="10020">Втулки</category>
<category id="709" parentId="10020">Кольца металлические</category>
<category id="911" parentId="10020">Хомуты</category>
<category id="10021">Резинометаллические изделия</category>
<category id="706" parentId="10021">Сайлентблоки</category>
<category id="707" parentId="10021">Сальники</category>
<category id="7071" parentId="10021">Сальники ступиц и трансмиссии</category>
<category id="7072" parentId="10021">Сальники двигателя</category>
<category id="7073" parentId="10021">Другие сальники и уплотнения</category>
<category id="708" parentId="10021">Кольца резиновые круглого сечения</category>
<category id="710" parentId="10021">Кольца резиновые некруглого сечения</category>
<category id="10023">Троса</category>
<category id="711" parentId="10023">Троса</category>
<category id="10024">Пружины</category>
<category id="712" parentId="10024"></category>
<category id="713" parentId="10024"></category>
<category id="850" parentId="10024"></category>
<category id="10025">Рессоры пневматические</category>
<category id="733" parentId="10025">Подушки воздушные</category>
<category id="734" parentId="10025">Аксессуары воздушных подушек</category>
<category id="851" parentId="10025">Подушки воздушные кабины</category>
<category id="8512" parentId="10025">Пневмоподушки кабины</category>
<category id="8513" parentId="10025">Пневмоподушки сиденья</category>
<category id="10026">Амортизаторы</category>
<category id="737" parentId="10026">Амортизаторы</category>
<category id="7371" parentId="10026">Амортизаторы гидравлические (масляные)</category>
<category id="7372" parentId="10026">Амортизаторы газонаполненные (газовые)</category>
<category id="8511" parentId="10026">Амортизаторы кабины</category>
<category id="10027">Подшипники</category>
<category id="748" parentId="10027">Подшипники</category>
<category id="10028">Кабина</category>
<category id="800" parentId="10028">Кабина</category>
<category id="801" parentId="10028">Детали кабины пластмассовые</category>
<category id="802" parentId="10028">Детали кабины металлические</category>
<category id="803" parentId="10028">Гидравлические части кабин</category>
<category id="8031" parentId="10028">Насосы подъема кабины</category>
<category id="8032" parentId="10028">Цилиндры подъема кабины</category>
<category id="8033" parentId="10028">Другие гидравлические части кабин</category>
<category id="804" parentId="10028">Ремкомплекты гидравлических частей кабины</category>
<category id="808" parentId="10028">Двери и дверные механизмы</category>
<category id="809" parentId="10028">Ручки двери наружные</category>
<category id="810" parentId="10028">Бампера</category>
<category id="8101" parentId="10028">Бампера в сборе</category>
<category id="8102" parentId="10028">Составляющие части бампера</category>
<category id="811" parentId="10028">Детали подвески кабины</category>
<category id="812" parentId="10028">Ремкомплекты подвески кабины</category>
<category id="818" parentId="10028">L-пакеты и защиты кабины</category>
<category id="819" parentId="10028">другие части кабины</category>
<category id="10029">Стёкла. Зеркала</category>
<category id="806" parentId="10029">Стёкла кабин</category>
<category id="807" parentId="10029">Зеркала</category>
<category id="8071" parentId="10029">Зеркала в сборе</category>
<category id="8072" parentId="10029">Элементы зеркальные</category>
<category id="8073" parentId="10029">Составляющие части зеркал</category>
<category id="10030">Надстройка прицепная</category>
<category id="903" parentId="10030">Детали контейнерного оборудования</category>
<category id="905" parentId="10030">Детали автовозных установок</category>
<category id="10031">Аксессуары</category>
<category id="908" parentId="10031">Детали крепления груза</category>
<category id="9081" parentId="10031">Ремни</category>
<category id="9082" parentId="10031">Штанги</category>
<category id="909" parentId="10031">Аксессуары</category>
<category id="920" parentId="10031">Инструмент и принадлежности</category>
<category id="9201" parentId="10031">Специальный инструмент для ремонта разных узлов автомобиля</category>
<category id="9202" parentId="10031">Универсальный инструмент и принадлежности</category>
<category id="715" parentId="10031">Защиты,заглушки,пробки</category>
<category id="714" parentId="10031">Маслёнки</category>
<category id="904" parentId="10031">Цепи противоскольжения</category>
<category id="906" parentId="10031">Детали строительной техники</category>
<category id="10032">Диски колёсные</category>
<category id="917" parentId="10032">Диски колёсные</category>
<category id="10033">Крылья, брызговики и крепления</category>
<category id="907" parentId="10033">Крылья, брызговики и крепления</category>
<category id="9071" parentId="10033">Крылья и брызговики</category>
<category id="9072" parentId="10033">Крепления крыльев</category>
<category id="10034">Покрышки резиновые</category>
<category id="918" parentId="10034">Покрышки резиновые</category>
<category id="10035">Опора ДВС, КПП</category>
<category id="219" parentId="10035">Подушки двигателя и трансмиссии</category>
<category id="10036">Кузов</category>
<category id="307" parentId="10036">Лифты,цилиндры гидравлические</category>
<category id="900" parentId="10036">Кузов</category>
</categories>

<delivery-options>
<option cost="1200" days="1-3"/>
</delivery-options>

<cpa>1</cpa>

<offers>
'''
    file.write(res)    
    #f.close()

def postfixYandex(file):
    
    #f=open(file,'a')    
    res = '''
</offers>
</shop>
</yml_catalog>'''
    file.write(res)    
    #f.close()            

def prefixGoogle(file):
    
    res = '''<?xml version="1.0" encoding="windows-1251"?>
<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">
<channel>
<title>ГК ОМЕГА</title>
<link>http://www.etsp.ru/</link>
<description>Запчасти для коммерческого автотранспорта</description>
'''
    file.write(res) 

def postfixGoogle(file):
        
    res = '''</channel>
</rss>'''
    file.write(res)    


def radioSet():
    if window.checkBoxAll.isChecked() == True:
        window.radioButtonZzap.setDisabled(True)
        window.radioButtonYandex.setDisabled(True)
        window.radioButtonGoogle.setDisabled(True)
        window.radioButtonEmex.setDisabled(True)             
        window.radioButtonAutoru.setDisabled(True)
        window.radioButtonEuropart.setDisabled(True)
        window.radioButtonArmtek.setDisabled(True)
    else:
        window.radioButtonZzap.setEnabled(True)
        window.radioButtonYandex.setEnabled(True)
        window.radioButtonGoogle.setEnabled(True)
        window.radioButtonEmex.setEnabled(True)             
        window.radioButtonAutoru.setEnabled(True)
        window.radioButtonEuropart.setEnabled(True)
        window.radioButtonArmtek.setEnabled(True)

def makePriceAll():
    if window.checkBoxAll.isChecked() == True:
        print("Все")
        
        window.radioButtonZzap.setChecked(True)
        QApplication.processEvents()
        print("zzap")
        makePrice()
        time.sleep(0.5)

        window.radioButtonEuropart.setChecked(True)
        QApplication.processEvents()
        print("europart")
        makePrice()
        time.sleep(0.5)
        
        window.radioButtonEmex.setChecked(True)
        QApplication.processEvents()
        print("emex")
        makePrice()
        time.sleep(0.5)

        window.radioButtonArmtek.setChecked(True)
        QApplication.processEvents()
        print("armtek")
        makePrice()
        time.sleep(0.5)
        
        window.radioButtonAutoru.setChecked(True)
        QApplication.processEvents()
        print("авто.ру")
        makePrice()
        time.sleep(0.5)

        window.radioButtonGoogle.setChecked(True)
        QApplication.processEvents()
        print("google")
        makePrice()
        time.sleep(0.5)

        window.radioButtonYandex.setChecked(True)
        QApplication.processEvents()
        print("yandex")
        makePrice()
        time.sleep(0.5)
        
        window.checkBoxAll.setChecked(False)
        window.radioButtonZzap.setEnabled(True)
        window.radioButtonYandex.setEnabled(True)
        window.radioButtonGoogle.setEnabled(True)
        window.radioButtonEmex.setEnabled(True)             
        window.radioButtonAutoru.setEnabled(True)
        window.radioButtonEuropart.setEnabled(True)
        window.radioButtonArmtek.setEnabled(True)
    else:
        makePrice()
        
def searchItem():
    res = window.lineEditFilter.text()
    #print(res)#tableWidgetOut
    row = window.tableWidgetOut.rowCount()
    col = window.tableWidgetOut.columnCount()
    #print("row={}, col={}".format(row,col))
    for x in range(col):
        for y in range(row):
            item = window.tableWidgetOut.item(y, x).text()
            #print("res={}".format(res))
            #print("item={}".format(item))
            if str(res).strip() == str(item).strip():
                print("Совпадение в строке {}, столбце {}".format(y+1,x+1))
                window.tableWidgetOut.setCurrentCell(y,x)
                return 0

def callOrion():

    try:
        ie = webbrowser.get(webbrowser.iexplore)
        url = "http://orion.etsp.ru/Reports/Pages/Report.aspx?ItemPath=%2f%d0%9f%d1%80%d0%be%d0%b4%d0%b0%d0%b6%d0%b8%2f%d0%a0%d0%be%d0%b7%d0%bd%d0%b8%d1%87%d0%bd%d1%8b%d0%b9+%d0%bf%d1%80%d0%b0%d0%b9%d1%81-%d0%bb%d0%b8%d1%81%d1%82+%d0%bd%d0%b5%d0%b0%d1%81%d1%81%d0%be%d1%80%d1%82%d0%b8%d0%bc%d0%b5%d0%bd%d1%82%d0%bd%d0%be%d0%b3%d0%be+%d0%bd%d0%b5%d0%bb%d0%b8%d0%ba%d0%b2%d0%b8%d0%b4%d0%b0+(%d0%be%d0%bf%d0%b5%d1%80%d0%b0%d1%82%d0%b8%d0%b2.)"
        ie.open(url)
    except:
        print("На компьютере не найден Internet Explorer")
 
   
app = QApplication(sys.argv)
window = QMainWindow()
window = uic.loadUi("make_price.ui")
#getNewUrl() 

window.pushButtonIn.clicked.connect(loadADTS)
window.pushButtonOut.clicked.connect(makePriceAll)#(makePrice)
window.pushButtonFTP.clicked.connect(putOnFTP)
window.commandLinkButtonURL.clicked.connect(getNewUrl)
#window.radioButtonYandex.setDisabled(True)#пока отключаем
window.tableWidgetOut.cellClicked.connect(openXMLinNotepad)
window.checkBoxAll.clicked.connect(radioSet)
window.lineEditFilter.textChanged.connect(searchItem)
window.commandLinkButtonOrion.clicked.connect(callOrion)

window.show()
sys.exit(app.exec_())

   
'''
ft=open('dicURL','w')
ft.write(str(dicURL))
ft.close()
'''
print("Время выполнения: %f сек." % (time.time()-tStart))

















