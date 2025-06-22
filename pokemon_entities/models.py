from django.db import models


class Pokemon(models.Model):
    """Покемон."""
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='children',
        verbose_name='родитель'
    )
    title = models.CharField('имя покемона на русском', max_length=200)
    image = models.ImageField("изображение" ,upload_to='pokemon_images', null=True, blank=True)
    description = models.TextField("описание", blank=True)
    title_en = models.CharField("имя покемона на английском", max_length=200, blank=True)
    title_jp = models.CharField("имя покемона на японском", max_length=200, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="покемон")
    lat = models.FloatField(verbose_name="широта")
    lon = models.FloatField(verbose_name="долгота")
    appeared_at = models.DateTimeField(verbose_name="появление")
    disappeared_at = models.DateTimeField(verbose_name="исчезновение")
    level = models.IntegerField(verbose_name="уровень", null=True, blank=True)
    health = models.IntegerField(verbose_name="здоровье", null=True, blank=True)
    strength = models.IntegerField(verbose_name="сила", null=True, blank=True)
    defence = models.IntegerField(verbose_name="защита", null=True, blank=True)
    stamina = models.IntegerField(verbose_name="выносливость", null=True, blank=True)
