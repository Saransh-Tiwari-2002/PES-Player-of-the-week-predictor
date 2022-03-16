import requests
from bs4 import BeautifulSoup
import re
import webbrowser
from latest_Saturday_sunday import last_sunday, last_saturday, last_monday
match_url_list, lower_league_url_list=[],[]

def get_link(saturday=last_saturday, sunday=last_sunday, monday=last_monday):
    for temp_date in [saturday, sunday, monday]:
        print(temp_date)
        r=requests.get(f'https://www.fotmob.com/?date={temp_date}')
        soup=BeautifulSoup(r.content, "html.parser")
        league_container=soup.findAll('div', {'class':'css-1akrvvq-Group e7pc1842'})
        for league_temp in league_container:
            try: league_name=league_temp.find('div',{'class':'css-cujevt-GroupHeaderContainer e7pc1843'}).text
            except: continue
            if(league_name in ['SPAIN - LALIGA', 'ITALY - SERIE A', 'GERMANY - 1. BUNDESLIGA','FRANCE - LIGUE 1', 'ENGLAND - PREMIER LEAGUE', 'PORTUGAL - LIGA PORTUGAL']):
            #if(league_name in ['ENGLAND - PREMIER LEAGUE']):
                print(league_name, '\n')
                for x in league_temp.findAll('a', {'class':'css-1r2we3n-MatchWrapper ew7iiy60'}):
                    if(league_name=='GERMANY - 1. BUNDESLIGA'):
                        if('bayer-leverkusen' in x["href"] or 'bayern-münchen' in x['href']):
                            match_url_list.append([f"https://www.fotmob.com{x['href']}", league_name])
                    else: match_url_list.append([f"https://www.fotmob.com{x['href']}", league_name])
                    #print(x['href'])

            elif(league_name in ['BELGIUM - FIRST DIVISION A', 'NETHERLANDS - EREDIVISIE', 'SCOTLAND - PREMIERSHIP', 'RUSSIA - PREMIER LEAGUE']):
                for x in league_temp.findAll('a', {'class':'css-1r2we3n-MatchWrapper ew7iiy60'}):
                    match_url_list.append([f"https://www.fotmob.com{x['href']}", league_name])
    return match_url_list