import os
import discord
from discord.ext import commands
import requests
from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
# Define the intents your bot needs
intents = discord.Intents.all()


# Create a bot instance with intents
bot = commands.Bot(command_prefix='.', intents=intents)

def partial_perk_sources(partial_perks):
    partial_perks_source_links = []
    for i in range(len(partial_perks)):
        src_list = [img['src'] for img in partial_perks[i]]
        partial_perks_source_links.append(src_list[0])
    return partial_perks_source_links
def extract_build_src(resulset):
    for div_element in resulset:
        # Find all 'a' tags with class 'champ-build__item'
        item_links = div_element.find_all('a', class_='champ-build__item')

        # Extract 'data-original' attribute from each 'img' tag
        links=[]
        for item_link in item_links:
            img_tag = item_link.find('img')
            if img_tag:
                data_original = img_tag.get('data-original')
                if data_original:
                    links.append(f"https://www.mobafire.com/{data_original}")
                else:
                    print("data-original attribute not found.")
            else:
                print("img tag not found.")
        return links

def find_champion_url(champion_name):
    """
    Finds the full URL of the champion based on the champion name.
    """
    # HTML content containing champion URLs
    champs_url = "https://www.mobafire.com/league-of-legends/champions"
    champs_response = requests.get(champs_url)

    # Parse the HTML content
    soup = BeautifulSoup(champs_response.text, 'html.parser')

    # Find all anchor tags within the div with class 'footer-links'
    links = soup.find('div', class_='footer-links').find_all('a')

    # Iterate through the links to find the matching champion name
    for link in links:
        # Extract the champion name and URL
        champ_name = link.text
        champ_url = link.get('href')

        # If the champion name matches the input, return the URL
        if champ_name.lower() == champion_name.lower():
            return f"https://www.mobafire.com{champ_url}"

    # Return None if the champion name is not found
    return None

async def download_send_remove_multiple_img(ctx,sources):
    for idx, source in enumerate(sources):
        img_response = requests.get(source)
        if img_response.status_code == 200:
            with open(f'image{idx}.webp', 'wb') as f:
                f.write(img_response.content)

    # Send the images as attachments
    for idx, source in enumerate(sources):
        file = discord.File(f'image{idx}.webp')
        await ctx.send(file=file)

    # Remove the temporary files after sending
    for idx, _ in enumerate(sources):
        os.remove(f'image{idx}.webp')
async def download_send_remove_single_img(ctx,source):
    img_response = requests.get(source)
    with open('image.webp', 'wb') as f:
        f.write(img_response.content)

    file = discord.File('image.webp')
    await ctx.send(file=file)

    # Remove the saved image file
    os.remove("image.webp")

async def download_send_remove_multiple_img(ctx, sources):
    try:
        images = []
        # Download images
        for idx, source in enumerate(sources):
            img_response = requests.get(source)
            if img_response.status_code == 200:
                img_path = f'image{idx}.webp'
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                images.append(Image.open(img_path))

        # Determine the dimensions of the merged image
        total_width = sum(image.width for image in images)
        max_height = max(image.height for image in images)

        # Create a new blank image with the determined dimensions
        merged_image = Image.new('RGB', (total_width, max_height))

        # Paste each image onto the blank image at the desired position
        x_offset = 0
        for image in images:
            merged_image.paste(image, (x_offset, 0))
            x_offset += image.width

        # Save the merged image
        merged_image.save("merged_image.jpg")

        # Send the merged image file
        with open("merged_image.jpg", "rb") as f:
            await ctx.send(file=discord.File(f))

        # Remove the temporary files after sending

        os.remove("merged_image.jpg")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
async def crop(ctx,left,right,upper,lower):
    # Open the image
    image_path = "https://cdnportal.mobalytics.gg/production/2024/02/LoL-TierList-LowElo-Patch14-3.jpg"
    response = requests.get(image_path)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    cropped_image = image.crop((left, upper, right, lower))

    # Save the cropped image
    cropped_image.save("cropped_image.jpg")

    # Send the cropped image file
    with open("cropped_image.jpg", "rb") as f:
        await ctx.send(file=discord.File(f))

    # Remove the saved image file
    os.remove("cropped_image.jpg")
@bot.command()
async def ct(ctx,*, champion: str):
    url = f'https://u.gg/lol/champions/{champion.lower()}/build'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        toughest_matchups_div = soup.find('div', {'class': 'toughest-matchups'})
        matchups = toughest_matchups_div.find_all('a', {'class': 'champion-matchup'})

        matchup_list = []
        for matchup in matchups:

            matchup_text = matchup.text.strip().replace("%","%   ")
            # Find the index of the '%' character
            index = matchup_text.find('%')

            # Insert a space before 4 characters before the '%' character
            transformed_text = matchup_text[:index - 4] + ' ' + matchup_text[index - 4:index] + matchup_text[index:]

            matchup_list.append(transformed_text)

        await ctx.send('\n'.join(matchup_list))
    else:

        await ctx.send('Failed to retrieve the toughest matchups.')

# Command to display a .webp image
@bot.command()
async def rune(ctx,*, champion: str):
    url = f'https://u.gg/lol/champions/{champion.lower()}/build'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with the specified classes under the primary tree
    primary_perks = soup.find('div', class_='rune-tree_v2 primary-tree').find_all('div',
                                                                                  class_='perk keystone perk-active') + \
                    soup.find('div', class_='rune-tree_v2 primary-tree').find_all('div', class_='perk perk-active')

    # print(partial_perk_sources(primary_perks))
    secondary_perks = soup.find('div', class_='secondary-tree').find_all('div', class_='perk perk-active')

    shards = soup.find('div', class_='rune-tree_v2 stat-shards-container_v2').find_all('div',
                                                                                       class_='shard shard-active')
    list=[]
    list.append(partial_perk_sources(primary_perks))
    list.append(partial_perk_sources(secondary_perks))
    list.append(partial_perk_sources(shards))


    for i in list:
        await download_send_remove_multiple_img(ctx,i)

# Bot command
@bot.command()
async def build(ctx,*, champion: str):

    champ_url = find_champion_url(champion)

    response = requests.get(champ_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with the class "champ-build__item"
        starter_core_items = soup.find_all(
            class_="champ-build__section champ-build__section--half champ-build__section--toggleDrop")
        boots = soup.find_all(
            class_="champ-build__section champ-build__section--oneSixth champ-build__section--toggleDrop champ-build__section--mobileNoMarg")
        additionals = soup.find_all(
            class_="champ-build__section champ-build__section--half luxury-half champ-build__section--toggleDrop champ-build__section--tabletNoMarg")

        starter_items = starter_core_items[0].find_all(class_="champ-build__section__content__tab current")
        core_items = starter_core_items[1].find_all(class_="champ-build__section__content__tab current")
        boot_item = boots[0].find_all(class_="champ-build__section__content__tab current")
        additonal_items = additionals[0].find_all(class_="champ-build__section__content__tab current")
        # Extract the src attributes from img tags within champ-build__item elements
        # Assuming your ResultSet is named 'result_set'

        link_starter = extract_build_src(starter_items)
        link_core = extract_build_src(core_items)
        link_boot = extract_build_src(boot_item)
        link_additional = extract_build_src(additonal_items)


        ll=[]
        ll.append(link_starter)
        ll.append(link_boot)
        ll.append(link_core)
        ll.append(link_additional)

        for i in ll:
            if i==link_starter:
                await ctx.send("Starters: ")
            elif i==link_boot:
                await ctx.send("Boot: ")
            elif i==link_core:
                await ctx.send("Core Items: ")
            elif i==link_additional:
                await ctx.send("Luxury Items: ")

            await download_send_remove_multiple_img(ctx, i)


@bot.command()
async def stat(ctx,*, champion:str):

    if champion.find(" "):
        champion=champion.replace(" ","")

    url=f"https://lolalytics.com/lol/{champion.lower()}/build/"

    response=requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')

    img=soup.find(class_="relative h-[144px] w-[144px] rounded-full border-[2px] border-[#333333] bg-black")

    img_tag = img.find('img')

    src = img_tag['src']
    await download_send_remove_single_img(ctx,src)

    items=soup.find(class_="flex justify-around border border-[#333333] p-2 text-center").find_all(class_="mb-1 font-bold")
    # Define the mapping of indices to the corresponding stats
    stats_mapping = {
        0: "win rate",
        2: "rank",
        3: "tier",
        4: "pick rate",
        5: "ban rate",
        6: "games"
    }

    # Iterate through the elements in the ResultSet
    stats = []
    for index, item in enumerate(items):
        # Exclude the second information
        if index == 1:
            continue
        # Extract the text content from each element and append it to the stats list
        stats.append({stats_mapping[index]: item.get_text(strip=True)})

    for stat in stats:
        for key, value in stat.items():
            message = f"{key}: {value}"
            await ctx.send(message)

@bot.command()
async def meta(ctx, role):
    # Define the file paths for each role
    role_images = {
        'top': 'top.png',
        'solo': 'top.png',
        'jungle': 'jng.png',
        'jung': 'jng.png',
        'mid': 'mid.png',
        'adc': 'adc.png',
        'support': 'sup.png',
        'sup': 'sup.png'
    }

    # Check if the role exists in the dictionary
    if role.lower() in role_images:
        # Load the appropriate file path
        file_path = role_images[role.lower()]

        # Send the image file
        with open(file_path, "rb") as f:
            await ctx.send(file=discord.File(f))
    else:
        await ctx.send("Role not found!")


# Run the bot with your token
bot.run('TOKEN')
