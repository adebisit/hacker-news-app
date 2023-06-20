from django.db import models

# Create your models here.

CATEGORY_CHOICE = [
    ("job", "Job"),
    ("story", "Story"),
    ("comment", "Comment"),
    ("poll", "Poll"),
    ("pollopt", "Poll Opt")
]

class Author(models.Model):
    username = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField()
    karma = models.IntegerField(default=0)
    no_submitted = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.username}"


class Item(models.Model):
    item_id = models.PositiveIntegerField(unique=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, default=None)
    text = models.TextField(blank=True)
    url = models.URLField(null=True)
    title = models.CharField(max_length=255, blank=True)
    score = models.PositiveIntegerField(null=True)
    parent = models.ForeignKey("Item", on_delete=models.CASCADE, null=True, default=None, related_name="subitems")
    is_admin = models.BooleanField(default=False)
