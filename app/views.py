from django.shortcuts import render,get_object_or_404,redirect
import requests
from pprint import pprint
from .models import Coin
from django.contrib import messages


def home(request):
    coin=request.GET.get("coin_name") or "hello"
    # print("inputtan gelen", coin)
    
    url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    # get kullanabilmel için pip install requests yaptık
    response=requests.get(url)
    content=response.json()
    
   # pprint(content[0]["name"] )
   # aynı verinin tekrar kaydedilmesini engellemek için döngü aşağıda
   
    for i in content:
        if i["name"].lower()==coin.lower():
            name_c=i["name"]

            if Coin.objects.filter(name=name_c):
            # aynı isimden var
                continue
            else:
                Coin.objects.create(name=name_c)
                #veriyi kaydettik
        else:
               #girilen veri apide yok  
            continue

    coin_data = []

    coins =Coin.objects.all().order_by("-id") 

    for k in coins:
        # print(type(k))
        for n in content:
            # pprint(n)
            if n["name"]==str(k):
                data ={
                "k":k,
                "name":n["name"],
                "image":n["image"],
                "market":n["current_price"],
                "change":n["price_change_24h"],
                }

                pprint(data)

                coin_data.append(data)

    context={
        "coin_data":coin_data
    }            



           
    
    return render(request,"app/home.html",context) 

def delete_coin(request, id):
    coin = get_object_or_404(Coin, id=id)
    coin.delete()
    messages.success(request, 'City deleted!')
    return redirect('home')