import folium

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lt=timezone.localtime(),
        disappeared_at__gt=timezone.localtime(),
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon.image:
            image_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                image_url
            )
        else:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon
            )

    pokemons_on_page = []

    for pokemon in pokemons:
        if pokemon.image:
            image_url = request.build_absolute_uri(pokemon.image.url)
        else:
            image_url = DEFAULT_IMAGE_URL

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)

    if pokemon.image:
        image_url = request.build_absolute_uri(pokemon.image.url)
    else:
        image_url = DEFAULT_IMAGE_URL

    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lt=timezone.localtime(),
        disappeared_at__gt=timezone.localtime(),
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )

    pokemon_info = {
        'pokemon_id': pokemon_id,
        'title_ru': pokemon.title,
        'img_url': pokemon.image.url,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp
    }

    if pokemon.previous_evolution:
        pokemon_info.update({
            'previous_evolution': {
                'title_ru': pokemon.previous_evolution.title,
                'pokemon_id': pokemon.previous_evolution.pk,
                'img_url': pokemon.previous_evolution.image.url,
            }
        })

    if pokemon.next_evolutions.last():
        next_evolution = pokemon.next_evolutions.last()
        pokemon_info.update({
            'next_evolution': {
                'title_ru': next_evolution.title,
                'pokemon_id': next_evolution.pk,
                'img_url': next_evolution.image.url,
            }
        })

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
