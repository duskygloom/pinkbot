import discord, json, requests, random, logging, os

try:
    from secret import tenor_api_key
except ModuleNotFoundError:
    tenor_api_key = os.getenv("TENOR_KEY")

def get_member_name(member: discord.Member) -> str:
    name = member.nick
    if name is None:
        name = member.display_name
    return name

def get_gif_url(query: str, client_key: str) -> str:
    if tenor_api_key is None:
        return "" 
    limit = 8
    url = f"https://tenor.googleapis.com/v2/search?q='{query}'&key={tenor_api_key}&client_key={client_key}&limit={limit}"
    r = requests.get(url)
    if r.status_code == 200:
        top8_gifs = json.loads(r.content)
    else:
        return ""
    gifs = []
    for data in top8_gifs['results']:
        gifs.append(data['media_formats']['gif']['url'])
    if len(gifs) == 0:
        return ""
    return random.choice(gifs)
