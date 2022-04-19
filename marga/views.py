import re
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.db.models import F
from django.contrib import messages

from marga.models import Product, Price, Url, Store
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet

from marga.serializers import ProductsSerializer

from marga.utils import *
from .forms import Searchdb, Addurl, Deleteurl
 

@login_required
def addurltodb(request):
    reply = ""
    
    allurls = Url.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        #searched = (request.POST)["urluser"]
        form_addurl = Addurl(request.POST)
        if form_addurl.is_valid():
            searched = form_addurl.cleaned_data["name"]
        if "https://barbora.lv/" not in searched and "https://www.rimi.lv/e-veikals/" not in searched:
            reply = "Saite ir nepareiza. Pievienot var tikai Rimi vai Barbora produkta vai produktu grupas saiti."
            print(reply)
        if Url.objects.filter(url=searched, user_id=request.user.id).exists():
            reply = "Šī saite jau bija pievienota!"
            print(reply)
        elif "https://www.rimi.lv/e-veikals/" in searched:
            u = (Url(url=searched, store_id=Store.RIMI_ID, user_id=request.user.id))
            u.save()
            url_id = Url.objects.filter(url=searched, user_id=request.user.id)[0].id
            grabresults = grab_rimi(str(searched), url_id)
            if grabresults == []:
                reply = "Kļūda! No ievadītās RIMI saites neizdevās iegūt datus!"
                u.delete()
            else:
                addtodb_results = add_to_db(grabresults, request)
                if addtodb_results == 1:
                    reply = "Produkts jau bija pievienots, un tā cena ir vienāda ar iepriekšējo cenu."
                    u.delete()
                if addtodb_results == 2:
                    reply = "Produkts jau bija pievienots, bet tā cena tika atjaunota."
                    u.delete()
                if addtodb_results == 0:
                    reply = "Rimi saite un tās produkti ir pievienoti."
                print(reply)
        elif "https://barbora.lv/" in searched:
            u = (Url(url=searched, store_id=Store.BARBORA_ID, user_id=request.user.id))
            u.save()
            url_id = Url.objects.filter(url=searched, user_id=request.user.id)[0].id
            grabresults = grab_barbora(str(searched), url_id)
            if grabresults == []:
                reply = "Kļūda! No ievadītās BARBORA saites neizdevās iegūt datus!"
                u.delete()
            else:
                addtodb_results = add_to_db(grabresults, request)
                if addtodb_results == 1:
                    reply = "Produkts jau bija pievienots, un tā cena ir vienāda ar iepriekšējo cenu."
                    u.delete()
                if addtodb_results == 2:
                    reply = "Produkts jau bija pievienots, bet tā cena tika atjaunota."
                    u.delete()
                if addtodb_results == 0:
                    reply = "Barbora saite un tās produkti ir pievienoti."
                print(reply)
        form_addurl = Addurl()
        return render (request, "marga/addurltodb.html", {"reply": reply, "allurls": allurls, "form_addurl": form_addurl})
    else:
        form_addurl = Addurl
        return render (request, "marga/addurltodb.html", {"allurls": allurls , "form_addurl": form_addurl})


@login_required
def deleteurl(request):
    allurls = Url.objects.filter(user_id=request.user.id)
    form_deleteurl = Deleteurl
    if request.method == "POST":
        #searched = (request.POST)["deleteurl"]
        form_deleteurl = Deleteurl(request.POST)
        if form_deleteurl.is_valid():
            searched = form_deleteurl.cleaned_data["name"]
            if searched == "0":
                allurls.delete()
                reply = "Visas saites ir dzēstas"
                form_deleteurl = Deleteurl()
                return render (request, "marga/deleteurl.html", {"allurls": allurls, "reply": reply, "form_deleteurl": form_deleteurl})
            if searched.isnumeric() == True:
                if not Url.objects.filter(user_id=request.user.id, id=searched).exists():
                    reply = "Saite ar šādu ID neeksistē!"
                    form_deleteurl = Deleteurl()
                    return render (request, "marga/deleteurl.html", {"allurls": allurls, "reply": reply, "form_deleteurl": form_deleteurl})   
                Url.objects.filter(user_id=request.user.id, id=searched).delete()
                reply = "Dzēsta saite ar ID: " + str(searched)
                form_deleteurl = Deleteurl()
                return render (request, "marga/deleteurl.html", {"allurls": allurls, "reply": reply, "form_deleteurl": form_deleteurl})
            else:
                reply = "Nepareizi iedvadīts ID"
                form_deleteurl = Deleteurl()
                return render (request, "marga/deleteurl.html", {"allurls": allurls, "reply": reply, "form_deleteurl": form_deleteurl})
    else:
        return render (request, "marga/deleteurl.html", {"allurls": allurls, "form_deleteurl": form_deleteurl})


@login_required
def addinfotodb(request):
    urlsfromdb = Url.objects.filter(user_id=request.user.id)
    for i in urlsfromdb: 
        print(i.url)
        if i.store_id == Store.RIMI_ID:
            grabresults = grab_rimi(i.url, i.id)
            add_to_db(grabresults, request)
        if i.store_id == Store.BARBORA_ID:
            grabresults = grab_barbora(i.url, i.id)
            add_to_db(grabresults, request)
    grabresults = grab_maxima_sirsniga()
    add_to_db(grabresults, request)
    #del results[:]
    messages.success(request, 'Dati atjaunoti!')
    return redirect('index')
    



@login_required
def searchdb (request):
    if len(Url.objects.filter(user_id=request.user.id)) and len(Product.objects.filter(user_id=request.user.id)) == 0:
        form_search = Searchdb
        return render (request, "marga/index.html", {"form_search": form_search})
    searched = ""
    orderby = "prices__discount"
    form_search = Searchdb
    if request.method == "GET":
        form_search = Searchdb(request.GET)
        if form_search.is_valid():
            searched = form_search.cleaned_data["name"]
        try:
            orderby = request.GET['orderby']
        except:
            pass
    if orderby == "prices__date_time_grab":
        selection = Product.objects.filter(user_id=request.user.id, name__icontains=searched).order_by("-" + orderby)
    elif orderby == "prices__discount":
        selection = Product.objects.filter(user_id=request.user.id, name__icontains=searched).order_by(F(orderby).desc(nulls_last=True))
    else: #ja kaartots peec cenas vai atlaides, tad iipashs selection, kur Nulls rezultaati ir peedeejie
        selection = Product.objects.filter(user_id=request.user.id, name__icontains=searched).order_by(F(orderby).asc(nulls_last=True))
    selection = list(dict.fromkeys(selection)) #remove duplicates
    p = Paginator(selection, 500)
    page = request.GET.get('page')
    reply = p.get_page(page)

    return render (request, "marga/index.html", {"reply": reply, "form_search": form_search, "searched": searched, "orderby": orderby})
      

def test(request):
    return render(request, "marga/test.html")


def searchdbvalues(request):
    if request.method == "POST":
        was_search=1
        searched = (request.POST)["itemname"]
        print (searched)
        reply = Product.objects.filter(user_id=request.user.id, name__icontains=searched).order_by("prices__price").values("name", "link_to_picture", "store_id", "prices__price", "prices__price_old", "prices__price_per_unit", "prices__discount_period", "prices__date_time_grab")
        return render (request, "marga/test.html", {"reply": reply, "searched": searched, "was_search": was_search})
    else:
        return render (request, "marga/test.html")


def dbsortbypython (request):
    sort_by = request.GET.get('sort_by', None)
    prices = Price.objects.all()
    prices_and_products = []
    for i in prices:
        item = {"name": i.product.name, "store": i.product.store.name, "price": i.price, "date": i.date_time_grab}
        prices_and_products.append(item)
    if sort_by:
        #def sort_key(item):
        #    return (item[sort_by], item['date'])
        #prices_and_products.sort(key=sort_key)
        prices_and_products.sort(key=lambda k: (k[sort_by], k["date"]))
        print (prices_and_products)
    return render (request, "marga/test.html", {"prices_and_products": prices_and_products})


class Productsview(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

