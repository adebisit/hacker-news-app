from django.db import models

# Create your models here.

ITEM_TYPE_CHOICE = [
    ("job", "Job"),
    ("story", "Story"),
    ("comment", "Comment"),
    ("poll", "Poll"),
    ("pollopt", "Poll Opt")
]

class Author(models.Model):
    username = models.CharField(max_length=255)
    created = models.DateTimeField()
    karma = models.IntegerField(default=0)
    no_submitted = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.username}"


class BaseItem(models.Model):
    item_id = models.PositiveIntegerField(unique=True)
    created_date = models.DateTimeField()
    item_type = models.CharField(max_length=255, choices=ITEM_TYPE_CHOICE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, default=None)
    text = models.TextField(blank=True)
    url = models.URLField(null=True)
    title = models.CharField(max_length=255, blank=True)
    score = models.PositiveIntegerField(null=True)
    parent = models.ForeignKey("BaseItem", on_delete=models.CASCADE, null=True, default=None, related_name="subitems")
