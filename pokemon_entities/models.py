from django.db import models


class Pokemon(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemon_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    title_en = models.CharField(max_length=200, null=True, blank=True)
    title_jp = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()
