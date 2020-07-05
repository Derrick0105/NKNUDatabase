from django.shortcuts import render
import pymysql
import json


# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from django.conf.urls import url






def test(request):
    return render(request, 'testpage.html')


def testpage(request):
    db = pymysql.connect("140.127.74.225", "410577033", "410577033", "410577033")
    # db = pymysql.connect(host='140.127.74.225', port=3306, user='410577036', password='410577036', db='410577036')
    cursor = db.cursor()

    cursor.execute("SELECT * from brand")
    data = cursor.fetchone()
    print("Database version : %s " % data)
    db.close()
    return render(request, 'testpage.html', locals())


def index(request):
    db = pymysql.connect("140.127.74.225", "410577033", "410577033", "410577033")
    cursor = db.cursor()

    sql1_1 = "SELECT * FROM `suppliers`"
    cursor.execute(sql1_1)
    suppliers = cursor.fetchall()

    sql1_2 = "SELECT vehicles.`VIN`,transaction.customer,transaction.price FROM `vehicles` INNER JOIN transaction ON vehicles.VIN=transaction.VIN WHERE `transmission` in (SELECT serial FROM transmissions WHERE `supplier` = '1')"
    cursor.execute(sql1_2)
    datas = cursor.fetchall()


    sql2_1 = "SELECT * FROM `transaction`"
    cursor.execute(sql2_1)
    transactions = cursor.fetchall()

    sql2_2 = "SELECT dealer FROM transaction WHERE year(`date`)=year(now())-1 group by dealer ORDER by SUM(price) DESC LIMIT 0,1"
    cursor.execute(sql2_2)
    topsales = cursor.fetchall()

    sql3_1 = "SELECT brand FROM transaction WHERE year(`date`)=year(now())-1 group by brand ORDER by SUM(price) DESC LIMIT 0,2"
    cursor.execute(sql3_1)
    topbrand = cursor.fetchall()[0][0]
    cursor.execute(sql3_1)
    secondbrand = cursor.fetchall()[1][0]

    sql4_1 = "SELECT month(date) FROM `transaction` WHERE `brand`='SUVs' GROUP BY month(`date`) ORDER BY SUM(price) DESC LIMIT 0,1"
    cursor.execute(sql4_1)
    bestmonth = cursor.fetchone()[0]

    db.close()



    return render(request, 'index.html', locals())

def table(request):
    db = pymysql.connect("140.127.74.225", "410577033", "410577033", "410577033")
    cursor = db.cursor()

    sql1 = "SELECT * FROM `vehicles`"
    cursor.execute(sql1)
    vehicles = cursor.fetchall()

    sql2 = "SELECT * FROM `transmissions`"
    cursor.execute(sql2)
    transmissions = cursor.fetchall()

    sql3 = "SELECT * FROM `suppliers`"
    cursor.execute(sql3)
    suppliers = cursor.fetchall()

    sql4 = "SELECT * FROM `transaction` ORDER BY `serial` ASC"
    cursor.execute(sql4)
    transactions = cursor.fetchall()

    sql5 = "SELECT * FROM `models`"
    cursor.execute(sql5)
    models = cursor.fetchall()

    sql6 = "SELECT * FROM `manufacturing_plants`"
    cursor.execute(sql6)
    plants = cursor.fetchall()

    sql7 = "SELECT * FROM `engines`"
    cursor.execute(sql7)
    engines = cursor.fetchall()

    sql8 = "SELECT * FROM `dealer`"
    cursor.execute(sql8)
    dealers = cursor.fetchall()

    sql9 = "SELECT * FROM `customer`"
    cursor.execute(sql9)
    customers = cursor.fetchall()

    db.close()


    return render(request, 'table.html', locals())


def ajax_submit(request):
    db = pymysql.connect("140.127.74.225", "410577033", "410577033", "410577033")
    cursor = db.cursor()


    sql = "SELECT vehicles.`VIN`,transaction.customer,transaction.price  FROM `vehicles` INNER JOIN transaction ON vehicles.VIN=transaction.VIN WHERE `transmission` in (SELECT serial FROM transmissions WHERE `supplier` = %s)"%request.POST['supplier']

    cursor.execute(sql)
    datas = cursor.fetchall()

    total = []
    for data in datas:
        dic={'VIN':data[0],'customerID':data[1],'price':data[2]}
        total.append(dic)




    json_str = json.dumps(total)
    db.close()


    return HttpResponse(json_str)
