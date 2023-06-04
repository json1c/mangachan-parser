import aiohttp
import asyncio
import re
import os
import aiofiles
from bs4 import BeautifulSoup

import collections
collections.Callable = collections.abc.Callable


async def download_image(url, index, aiohttp_session):    
    async with aiohttp_session.get(url) as resp:
        photo = await resp.read()
        
        async with aiofiles.open(f"pics/{index}.jpg", "wb") as file:
            await file.write(photo)
        
        print("Downloaded", url)


async def download_manga(url):
    if not os.path.isdir("pics"):
        os.mkdir("pics")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            
            soup = BeautifulSoup(html, "html.parser")
            links = soup.findAll("a", class_="")
            
            for link in links:
                if link.contents:
                    if link.contents[0] == "Читать онлайн":
                        href = link.attrs["href"]
                        pic_url = "https://y.hentaichan.live" + href
            
        async with session.get(pic_url) as resp:
            html = await resp.text()
            
            soup = BeautifulSoup(html, "html.parser")
            scripts = soup.findAll("script")
            
            script = scripts[2].text
            data = re.findall(r"fullimg\": \[(.*)\]", script)[0]
            
            images = data.replace("'", "").split(",")
            
        await asyncio.gather(*[
            download_image(image.strip(), index, session)
            for index, image in enumerate(images)
        ])


url = input("Manga url: ")
asyncio.run(download_manga(url))

