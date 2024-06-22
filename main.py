from bs4 import BeautifulSoup
import requests

# class to handle magic info
class Magic():
    # initialized with name of spell and link to its wiki page
    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.type = ''
        self.location = []
        self.location_link = ''
        self.requires = []
        self.effect = ''
        self.slots = ''
    
    # function to extract magic data from website
    def get_info(self):
        global wiki_site
        # fetch and parse magic web page
        magic_site = requests.get(self.link).text
        magic_info = BeautifulSoup(magic_site, 'lxml')
        # extract data table
        table_list = magic_info.find('table', class_ = 'wiki_table').find_all('tr')
        table_info = table_list[-1].find_all('div', class_ = 'lineleft')
        # extract magic effect
        self.effect = table_info[0]
        param_list = table_info[-1].text.split('\n')
        # extract magic requirement parameters
        for i in param_list:
            self.requires.append(i)
        # extract number of spell slots taken
        self.slots = table_list[-2].find_all('td')[-1].text
        # extract location data
        location_list = magic_info.find('div', id = 'wiki-content-block').find('ul').find_all('li')
        for i in location_list:
            self.location.append(i.text)
            loc_link = i.find_all('a', 'wiki_link')
            for j in loc_link:
                if 'Map Link' in j.text or 'Elden Ring Map' in j.text:
                    self.location_link = wiki_site+j['href']
                    break

# class to handle weapon data
class Weapon():
    # initialized with name of weapon and its wiki page
    def __init__(self, name, link):
        self.name = name
        self.type = ''
        self.link = link
        self.upgrade_mat = ''
        self.infusable = False
        self.location = []
        self.location_link = ''
        self.ashofwar = ''
        self.ashofwar_link = ''
        self.melee = False
        self.requires = []
        self.passive = ''
    
    # function to set the type of weapon
    def set_type(self, type):
        self.type = type
        # Check if weapon is of melee type
        if self.type not in ['Tools', 'Sacred Seals', 'Glintstone Staves', 'Ballistas', 'Crossbows', 'Greatbows', 'Bows', 'Light Bows', 'Perfume Bottles', 'Throwing Blades']:
            self.melee = True
        
    # function to extract weapon data from website
    def get_info(self):
        global wiki_site
        # fetch and parse weapon web page
        weapon_site = requests.get(self.link).text
        weapon_info = BeautifulSoup(weapon_site, 'lxml')
        # extract weapon requirement parameters
        attribute_list = weapon_info.find_all('div', class_ = 'lineleft')
        for i in attribute_list:
            if i.text.split()[0] in ['Str', 'Dex', 'Int', 'Fai', 'Arc']:  
                if i.text.split()[-1].isdigit():            
                    self.requires.append(i.text)
        # extract location data
        location_list = weapon_info.find('div', id = 'wiki-content-block').find('ul').find_all('li')
        for i in location_list:
            self.location.append(i.text)
            loc_link = i.find_all('a', 'wiki_link')
            for j in loc_link:
                if 'Map Link' in j.text or 'Elden Ring Map' in j.text:
                    self.location_link = wiki_site+j['href']
                    break
        # extract data table
        table_list = weapon_info.find('table', class_ = 'wiki_table').find_all('tr')
        # extract passive and ash of war
        self.passive = table_list[-1].find_all('td')[-1].find_all('a', class_ = 'wiki_link')[-1]['title']
        self.ashofwar = table_list[-2].find('td').text
        self.ashofwar_link = wiki_site+table_list[-2].find('td').a['href']
        # extract upgrade material info
        other_list = weapon_info.find('div', id = 'wiki-content-block').find_all('ul')[1].find_all('li')
        if not 'cannot' in other_list[1].text:
            self.infusable = True
        upgrade_list = weapon_info.find_all('p')
        for i in upgrade_list:
            if 'Smithing Stones' in i.text:
                self.upgrade_mat = i.text
        for i in other_list:
            if 'Smithing Stones' in i.text:
                self.upgrade_mat = i.text
        
# function to fetch magic info for given magic name
def get_magic(mag):
    for i in magic_list:
        if i.name == mag:
            i.get_info()
            return i
    return
    
# function to fetch weapon info for given weapon name
def get_weapon(weap):
    for i in weapon_list:
        if i.name == weap:
            i.get_info()
            return i
    return
    
# base wiki site
wiki_site = 'https://eldenring.wiki.fextralife.com'
# lists containing the number of weapons/spells in each category
weapon_amount = [17,124,25,16,8,6,19,10,10,8,17,14,16,6,16,20,19,10,18,5,7,14,4,6,8,5,9,3,20,12,8,52,2,2,1,3,5,3,3,3]
magic_amount = [84,129]
# counters
index = 0
count = 0

# get and parse weapon wiki page
weapons_site = requests.get(wiki_site+'/Weapons').text
weapons = BeautifulSoup(weapons_site, 'lxml')
# dict to store weapons according to weapon types
weapon_type = {}
weapon_type_list = []
# extract weapon type categories
weapon_type_get = weapons.find_all('div', class_ = 'col-xs-4 col-sm-2')
# list for all weapons
weapon_list = []
# extract all weapons
weapon_list_get = weapons.find_all('div', class_ = 'col-xs-6 col-sm-2')
# list for all weapon names
weapon_name = []

# add weapon types to weapon type dict
for i in weapon_type_get:
    weapon_type[i.text.strip()] = []
    weapon_type_list.append(i.text.strip())
    
# add all weapons to list and dict
for i in weapon_list_get:
    if len(i.text.replace('\n','').strip()) > 0:
        weap = Weapon(i.text.replace('\n',''), wiki_site+i.find('a')['href'])
        weapon_list.append(weap)
        weapon_name.append(i.text.replace('\n',''))
        weap.set_type(weapon_type_list[index])
        weapon_type[weapon_type_list[index]].append(weap)
        count+=1
        if count == weapon_amount[index]:
            index+=1
            count = 0 

# reset counters
count = 0
index = 0
            
# get and parse magic wiki page
magic_site = requests.get(wiki_site+'/Magic+Spells').text
magic = BeautifulSoup(magic_site, 'lxml')
# extract all magic
magic_get = magic.find_all('div', class_ = 'col-sm-3 col-xs-6')
# list for all magic
magic_list = []
# list for all magic names
magic_name = []
# dict to store magic according to magic type
magic_type = {}
# add the two category types to dict
magic_type['Sorcery'] = []
magic_type['Incantation'] = []

# add all magic to lists and dict
for i in magic_get:
    if len(i.text.replace('\n','').strip()) > 0:
        mag = Magic(i.text.replace('\n','').strip(), wiki_site+i.find('a')['href'])
        magic_list.append(mag)
        magic_name.append(i.text.replace('\n','').strip())
        if index == 0:
            magic_type['Sorcery'].append(mag)
            mag.type = 'Sorcery'
        else:
            magic_type['Incantation'].append(mag)
            mag.type = 'Incantation'
        count+=1
        if count == magic_amount[index]:
            index+=1
            if index > 1:
                break
            count = 0
    

