from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200,
                                verbose_name="Название на русском")
    title_en = models.CharField(max_length=200,
                                default="",
                                verbose_name="Название на английском",
                                blank=True)
    title_jp = models.CharField(max_length=200,
                                default="",
                                verbose_name="Название на японском",
                                blank=True)
    description = models.TextField(default="",
                                   verbose_name="Описание",
                                   blank=True)
    image = models.ImageField(upload_to="pokemons/",
                              null=True,
                              blank=True,
                              verbose_name="Путь к картинке")
    previous_evolution = models.ForeignKey("self",
                                           related_name="next_evolution",
                                           on_delete=models.DO_NOTHING,
                                           null=True,
                                           blank=True,
                                           verbose_name="Предыдущая эволюция")

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                verbose_name="Покемон")
    lat = models.FloatField(verbose_name="GPS Широта")
    lon = models.FloatField(verbose_name="GPS Долгота")

    appeared_at = models.DateTimeField(verbose_name="Время появления",
                                       null=True,
                                       blank=True)
    disappeared_at = models.DateTimeField(verbose_name="Время исчезновения",
                                          null=True,
                                          blank=True)

    level = models.IntegerField(verbose_name="Уровень",
                                blank=True,
                                null=True)
    health = models.IntegerField(verbose_name="Здоровье",
                                 blank=True,
                                 null=True)
    strength = models.IntegerField(verbose_name="Сила",
                                   blank=True,
                                   null=True)
    defence = models.IntegerField(verbose_name="Защита",
                                  blank=True,
                                  null=True)
    stamina = models.IntegerField(verbose_name="Выносливость",
                                  blank=True,
                                  null=True)

    def __str__(self):
        return f"{self.pokemon} at {(self.lat, self.lon)}"
