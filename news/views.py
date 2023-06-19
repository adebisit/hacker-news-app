from django.shortcuts import render
from .forms import NewsFilterForm
from django.db.models import Q
from news.models import BaseItem
from pprint import pprint


# Create your views here.

def home(request):
    return render(request, 'news/home.html')


def latest_news(request):
    keyword = request.GET.get("keyword", "")
    category = request.GET.get("category")
    count = int(request.GET.get("count", "25"))
    page = int(request.GET.get("page", "1"))

    items = BaseItem.objects.filter((Q(text__icontains=keyword) | Q(title__icontains=keyword)) & ~Q(item_type="comment"))
    if category and category != "all" and category.lower() != "none":
        items = items.filter(Q(item_type=category))
    
    # print(f"Page = {page}, Count = {count}, no_items = {items.count()}")
    # print(f"[{(page - 1) * count}:{page * count}]")
    return render(request, 'news/search.html', context = {
        "items": items[(page - 1) * count : page * count],
        "query": {
            "keyword": keyword,
            "category": category if category != "all" else None
        },
        "pageObj": {
            "next": page + 1 if (items.count() > (page * count))  else None,
            "page": page,
            "prev": page - 1 if page != 1 else None,
            "count": count
        }
    })


def news_details(request, item_id):
    try:
        item = BaseItem.objects.get(item_id=item_id)
    except BaseItem.DoesNotExist:
        item = None
    return render(request, 'news/news-details.html', context={"item": item})