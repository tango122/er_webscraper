# Elden Ring Web Scraper
This is a web scraping program for the [Elden Ring wiki website](https://eldenring.wiki.fextralife.com/) which extracts weapon and magic information. Retrieves spell name, type, location found, link to map of location, attribute requirements, effects, and number of magic slots. 
Also retrieves weapon name, type, location found, link to map of location, upgrade material, whether it is infusable, ash of war, whether it is melee, attribute requirements, and passive effects.

## Features
- Automatic data retrieval
- Detailed data
- get_magic and get_weapon functions to return data for given name of weapon/spell

## Further Applications and Extensions
- Scrape even more data like if DLC is required or scaling information
- Add armor, consumable item, and talisman data scraping
- Return a list of items based on filters like attribute requirements and item type
- Use filters to return a full build according to the user's liking

## Additional Libraries Used
- BeautifulSoup4
- requests
- lxml
