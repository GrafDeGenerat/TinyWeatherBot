import aiohttp
from cfg.project_config import ProjectConfig
import ast



def case_ending_citiname(name):
    last_char = name[-1]
    if name[-2:] in {'ий', 'ый', 'ой'}:
        return name[:-2] + 'ом'
    if last_char == 'а':
        return name[:-1] + 'е'
    if last_char in {'е', 'ё', 'и', 'й', 'о', 'у', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'}:
        return name
    return name + 'e'


async def general_info_coord(lat, lon):
    api_url = (f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={ProjectConfig.get_api()}'
               f'&lang=ru&units=metric')
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            info = await response.read()
    general_dict = ast.literal_eval(info.decode('utf-8'))
    city, weather_desc = (general_dict['name'],
                          general_dict['weather'][0]['description'])
    temp, pressure, humidity, wind = (general_dict['main']['temp'],
                                      general_dict['main']['pressure'],
                                      general_dict['main']['humidity'],
                                      general_dict['wind']['speed'])
    return {'city': case_ending_citiname(city),
            'weather_desc': weather_desc,
            'temp': int(round(temp, 0)),
            'pressure': int(pressure * 0.750064),
            'humidity': humidity,
            'wind': wind}


async def general_info_citiname(name):
    api_url = (f'http://api.openweathermap.org/geo/1.0/direct?q={name}&limit={1}&appid={ProjectConfig.get_api()}'
               f'&lang=ru&units=metric')
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            info = await response.read()
    decoded = ast.literal_eval(info.decode('utf-8'))
    if decoded:
        general_dict = decoded[0]
    else:
        return None
    lat, lon = (general_dict['lat'],
                general_dict['lon'])
    return await general_info_coord(lat, lon)


