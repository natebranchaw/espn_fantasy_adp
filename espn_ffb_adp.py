import time 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def get_espn_fantasy_football_adp(pages_to_scrape:int):
    '''Takes as input the number of pages you wish to scrape from ESPN's ADP (Average Draft Position) Live Results.
    Returns a dataframe with the columns: Player, Team, Position, and ADP'''
    
    
    espn_url = 'https://fantasy.espn.com/football/livedraftresults'
    player_list = []
    team_list = []
    pos_list = [] 
    adp_list = []
    page = 0
    
    #Define options for Chrome Driver
    options = webdriver.ChromeOptions() 
    options.add_argument('headless')#it's more scalable to work in headless mode 

    #Normally, selenium waits for all resources to download 
    #We don't need it as the page also populated with the running javascript code. 
    options.page_load_strategy = 'none' 

    #This returns the path web driver downloaded 
    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 

    #Pass the defined options and service objects to initialize the web driver 
    driver = Chrome(service = chrome_service, options = options) 
    driver.implicitly_wait(10)
    driver.get(espn_url)
   
    time.sleep(2)

    next_page_button = driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[2]/div/div/div/div[3]/nav/button[2]')

    #Loop through the first seven pages of projections
    while page <= pages_to_scrape:
        
        adp_table = driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[2]/div/div/div/div[3]').get_attribute('outerHTML')
        soup = BeautifulSoup(adp_table, 'html')

        #Loop over all span elements with the class truncate for player names and append to player list
        for player in soup.find_all('span', {'class': 'truncate'}):
            if len(player.text) > 0:
                player_list.append(player.text)
        
        #Loop over all span elements with the class playerinfo__playerteam for team names and append to team list
        for team in soup.find_all('span', {'class': 'playerinfo__playerteam'}):
            team_list.append((team.text).upper())
        
        #Loop over all span elements with the class playerinfo__playerpos ttu for player positons and append to pos list
        for pos in soup.find_all('span', {'class': 'playerinfo__playerpos ttu'}):
            pos_list.append(pos.text.upper())
        
        #Loop over all span elements with the class jsx-2810852873 table--cell sortedAscending adp tar sortable for player adp and append to adp list
        for adp in soup.find_all('div', {'class': 'jsx-2810852873 table--cell sortedAscending adp tar sortable'}):
            adp_list.append(adp.text)
                
        next_page_button.send_keys(Keys.END)
        
        time.sleep(1)
        
        next_page_button.click()
        
        page = page + 1
        
        time.sleep(4)
        
    driver.quit()
    
    adp_df = pd.DataFrame({'Player': player_list, 'Team': team_list, 'Position': pos_list, 'ADP': adp_list})
        
    return adp_df    