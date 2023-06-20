from django.shortcuts import render
from django.db.models import Q
from news.models import Item
from pprint import pprint
from django.http import JsonResponse


# Create your views here.

def home(request):
    return render(request, 'news/home.html')


def latest_news(request):
    keyword = request.GET.get("keyword", "")
    category = request.GET.get("category")
    admin = bool(request.GET.get('admin', None))
    count = int(request.GET.get("count", "25"))
    page = int(request.GET.get("page", "1"))

    items = Item.objects.filter((Q(text__icontains=keyword) | Q(title__icontains=keyword)) & ~Q(category="comment") & Q(is_admin=admin))
    if category == "story" or category == "job":
        items = items.filter(category=category)
    elif category == "ask":
        items = items.filter(title__istartswith="Ask HN")
    elif category == "show":
        items = items.filter(title__istartswith="Show HN")
    else:
        category = "all"
    
    context = {
        "items": items[(page - 1) * count : page * count],
        "query": {
            "keyword": keyword,
            "category": category,
            "admin": admin
        },
        "pageObj": {
            "next": page + 1 if (items.count() > (page * count))  else None,
            "page": page,
            "prev": page - 1 if page != 1 else None,
            "count": count
        }
    }
    pprint(context)
    return render(request, 'news/search.html', context = context)


def news_details(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        item = None
    return render(request, 'news/news-details.html', context={"item": item})

def get_sub_items(request, pk):
    try:
        items = Item.objects.filter(parent__id=pk)
        data = []
        for item in items:
            data.append({
                "author": item.author.username if item.author else None,
                "date": item.created_date,
                "text": item.text
            })
    except Item.DoesNotExist:
        data = []

    return JsonResponse(data, safe=False)