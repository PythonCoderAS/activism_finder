from django.db import models


# Create your models here.


class Source(models.Model):
    name = models.CharField(max_length=250, null=False, unique=True)
    description = models.CharField(max_length=4096, null=False)
    website = models.URLField(max_length=512, null=False)
    code = models.CharField(max_length=24, null=False, unique=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(code="search") & ~models.Q(code="list") & ~models.Q(code="tag") & ~models.Q(code="tags"),
                                   name="no_reserved_names_code"),
            models.CheckConstraint(check=~models.Q(code__contains=" ") & ~models.Q(code__contains="/"), name="no_invalid_characters_code")]

    def __str__(self):
        return self.name


class Keyword(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=False)
    word = models.CharField(max_length=64, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("source", "word"), name="No duplicate rows")
        ]

    @property
    def word_url(self):
        return self.word.replace(" ", "_")

    def __str__(self):
        return f"[{self.source}: {self.word}]"
