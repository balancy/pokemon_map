import folium

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/" \
                    "6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/" \
                    "width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    """Add pokemon to the map.

    :param folium_map: map to add pokemon to
    :param lat: GPS latitude of pokemon
    :param lon: GPS longitude of pokemon
    :param image_url: pokemon's image url
    """

    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally to fix
        # strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    """Show all pokemons.

    :param request: request
    :return: page with pokemons and map
    """

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        image_url = pokemon_entity.pokemon.image.url
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon,
                    request.build_absolute_uri(image_url))

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            "pokemon_id": pokemon.id,
            "img_url": request.build_absolute_uri(pokemon.image.url),
            "title_ru": pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        "map": folium_map._repr_html_(),
        "pokemons": pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    """Show pokemon by it's id.

    :param request: request
    :param pokemon_id: id of pokemon
    :return: pokemon page
    """

    try:
        pokemon_object = Pokemon.objects.get(id=int(pokemon_id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound("<h1>Такой покемон не найден</h1>")

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon_object):
        image_url = pokemon_entity.pokemon.image.url
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon,
                    request.build_absolute_uri(image_url))

    pokemon = {
        "img_url": request.build_absolute_uri(pokemon_object.image.url),
        "title_ru": pokemon_object.title_ru,
        "title_en": pokemon_object.title_en,
        "title_jp": pokemon_object.title_jp,
        "description": pokemon_object.description,
    }

    if previous_evolution := pokemon_object.previous_evolution:
        pokemon.update(
            {
                "previous_evolution": previous_evolution,
                "previous_evolution_id": previous_evolution.id,
                "previous_evolution_title_ru": previous_evolution.title_ru,
                "previous_evolution_image":
                    request.build_absolute_uri(previous_evolution.image.url),
            }
        )

    if next_evolution := pokemon_object.next_evolution.all().first():
        pokemon.update(
            {
                "next_evolution": next_evolution,
                "next_evolution_id": next_evolution.id,
                "next_evolution_title_ru": next_evolution.title_ru,
                "next_evolution_image":
                    request.build_absolute_uri(next_evolution.image.url),
            }
        )

    return render(request, "pokemon.html", context={
        "map": folium_map._repr_html_(), "pokemon": pokemon
    })
