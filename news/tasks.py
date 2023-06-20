import requests
import json
from hackernews.celery import app
from pprint import pprint
import os
from news.models import Item, Author
from django.db.models import Max
from datetime import datetime
from pytz import timezone
from django.db import IntegrityError


utc = timezone("UTC")


def get_max_item():
    resp = requests.get("https://hacker-news.firebaseio.com/v0/maxitem.json")
    return resp.json()


@app.task
def get_history():
    max_item_id = get_max_item()
    max_item_no_db = Item.objects.aggregate(max_item_id=Max("item_id"))["max_item_id"]
    print(f"Max Item ID from API = {max_item_id}")
    print(f"Current Max Item ID from DB = {max_item_no_db}")
    print(f"Catching up with {max_item_id - max_item_no_db}")
    while max_item_no_db < max_item_id:
        max_item_no_db += 1
        get_item.delay(max_item_no_db)


@app.task
def get_item(id):
    resp = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{id}.json')
    item = resp.json()

    parent = None
    if "parent" in item:
        try:
            parent = Item.objects.get(item_id=item["parent"])
        except Item.DoesNotExist:
            get_item(item["parent"])

    try:
        item_db = Item.objects.get(item_id=item["id"])
    except Item.DoesNotExist:
        item_db = Item(
            item_id = item["id"],
            category = item["type"],
            created_date = utc.localize(datetime.utcfromtimestamp(item["time"])) if item.get("time") else None,    
        )
    
    item_db.parent = parent
    item_db.text = item.get("text", "")
    item_db.url = item.get("url")
    item_db.title = item.get("title", "")
    item_db.score = item.get("score")
    
    if "by" in item:
        item_db.author = get_user(item["by"])
    
    try:
        item_db.save()
    except IntegrityError:
        pass

    # kids = []
    for kid_id in item.get("kids", []):
        subitem = get_item(kid_id)
    #     kids.append(subitem)
    # item["kids"] = kids
    return item


def get_user(user_id):
    resp = requests.get(f'https://hacker-news.firebaseio.com/v0/user/{user_id}.json')
    data = resp.json()
    username = data["id"]
    try:
        author = Author.objects.get(username=username)
    except Author.DoesNotExist:
        author = Author(
            username = username,
            created = utc.localize(datetime.utcfromtimestamp(data["created"])),
            karma = data["karma"],
            no_submitted = len(data.get("submitted", []))
        )
        try:
            author.save()
        except IntegrityError:
            pass
    return author
