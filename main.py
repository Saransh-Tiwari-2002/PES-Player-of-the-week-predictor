import requests
from bs4 import BeautifulSoup
import re
import difflib
import csv
import unidecode
import fotmob_get_match_links
from real_club_name import real_club_name_dict, important_club_list
from latest_Saturday_sunday import last_saturday, last_sunday, last_monday

with open('player_export.csv',errors="ignore", newline='') as csvfile:
    spamreader = list(csv.reader(csvfile, delimiter=','))
    namelist=[]
    for row in spamreader[:-1]:
        namelist.append(row[2].lower().replace(' ', '-').replace('.','-').replace('--', '-'))
column_name=['PlayerID', 'AccentedName', 'Name', 'JapName', 'Shirt', 'ShirtNational', 'Commentary', 'Country', 'Country2', 'Height', 'Weight', 'Age', 'StrongerFoot', 'PlayingStyles', 'RegisteredPosition', 'GK', 'CB', 'LB', 'RB', 'DMF', 'CMF', 'LMF', 'RMF', 'AMF', 'LWF', 'RWF', 'SS', 'CF', 'OffensiveAwareness', 'BallControl', 'Dribbling', 'TightPossession', 'LowPass', 'LoftedPass', 'Finishing', 'Heading', 'PlaceKicking', 'Curl', 'Speed', 'Acceleration', 'KickingPower', 'Jump', 'PhysicalContact', 'Balance', 'Stamina', 'DefensiveAwareness', 'BallWinning', 'Aggression', 'GKAwareness', 'GKCatching', 'GKClearing', 'GKReflexes', 'GKReach', 'WeakFootUsage', 'WeakFootAccuracy', 'Form', 'InjuryResistance', 'Trickster', 'MazingRun', 'SpeedingBullet', 'IncisiveRun', 'LongBallExpert', 'EarlyCross', 'LongRanger', 'ScissorsFeint', 'DoubleTouch', 'FlipFlap', 'MarseilleTurn', 'Sombrero', 'CrossOverTurn', 'CutBehindTurn', 'ScotchMove', 'StepOnSkillControl', 'sHeading', 'LongRangeDrive', 'ChipShotControl', 'LongRangeShooting', 'KnuckleShot', 'DippingShot', 'RisingShots', 'AcrobaticFinishing', 'HeelTrick', 'FirstTimeShot', 'OneTouchPass', 'ThroughPassing', 'WeightedPass', 'PinpointCrossing', 'OutsideCurler', 'Rabona', 'NoLookPass', 'LowLoftedPass', 'GKLowPunt', 'GKHighPunt', 'LongThrow', 'GKLongThrow', 'PenaltySpecialist', 'GKPenaltySaver', 'Gamesmanship', 'ManMarking', 'TrackBack', 'Interception', 'AcrobaticClear', 'Captaincy', 'SuperSub', 'FightingSpirit', 'Reputation', 'PlayingAttitude', 'YouthClub', 'OwnerClub', 'ContractUntil', 'LoanUntil', 'MarketValue', 'NationalCaps', 'HiddenPlayer', 'Condition', 'MAXOffensiveAwareness', 'MAXBallControl', 'MAXDribbling', 'MAXTightPossession', 'MAXLowPass', 'MAXLoftedPass', 'MAXFinishing', 'MAXPlaceKicking', 'MAXCurl', 'MAXHeading', 'MAXDefensiveAwareness', 'MAXBallWinning', 'MAXAggression', 'MAXKickingPower', 'MAXSpeed', 'MAXAcceleration', 'MAXBalance', 'MAXPhysicalContact', 'MAXJump', 'MAXGKAwareness', 'MAXGKCatching', 'MAXGKClearing', 'MAXGKReflexes', 'MAXGKReach', 'MAXStamina', 'Overall', 'LevelCap', 'OverallPotential', 'BaseContractCost', 'MaxContractCost', 'DataPackOneChange', 'DataPackTwoChange', 'Club', 'TeamName', 'Continent', 'LeagueID', 'LeagueName', 'PlayerType', 'overallGK', 'overallCB', 'overallLB', 'overallRB', 'overallDMF', 'overallCMF', 'overallLMF', 'overallRMF', 'overallAMF', 'overallLWF', 'overallRWF', 'overallSS', 'overallCF', 'MAXOverallGK', 'MAXOverallCB', 'MAXOverallLB', 'MAXOverallRB', 'MAXOverallDMF', 'MAXOverallCMF', 'MAXOverallLMF', 'MAXOverallRMF', 'MAXOverallAMF', 'MAXOverallLWF', 'MAXOverallRWF', 'MAXOverallSS', 'MAXOverallCF', 'New'] 
skill_name=['ScissorsFeint', 'DoubleTouch', 'FlipFlap', 'MarseilleTurn', 'Sombrero', 'CrossOverTurn', 'CutBehindTurn', 'ScotchMove', 'StepOnSkillControl', 'Heading', 'LongRangeDrive', 'ChipShotControl', 'LongRangeShooting', 'KnuckleShot', 'DippingShot', 'RisingShots', 'AcrobaticFinishing', 'HeelTrick', 'FirstTimeShot', 'OneTouchPass', 'ThroughPassing', 'WeightedPass', 'PinpointCrossing', 'OutsideCurler', 'Rabona', 'NoLookPass', 'LowLoftedPass', 'GKLowPunt', 'GKHighPunt', 'LongThrow', 'GKLongThrow', 'PenaltySpecialist', 'GKPenaltySaver', 'Gamesmanship', 'ManMarking', 'TrackBack', 'Interception', 'AcrobaticClear', 'Captaincy', 'SuperSub', 'FightingSpirit']

def text_search(query, club_name, querytype=2):
    query=query.lower().replace(' ', '-').replace('.','-').replace('--', '-')
    temp=[]
    for x in real_club_name_dict.keys():
        if(club_name.upper() in x):
            temp_club_name=real_club_name_dict.get(x)
    for row in spamreader[:-1]:
        if (query in row[2].lower().replace(' ', '-').replace('.','-').replace('--', '-') and row[152]=='1'):            
            if(temp_club_name in row[148]):            temp.append(row[:-1])
            #else: print(row[148], end=' ')
    
    if(len(temp)==0):
        if(query.count('-')>0):
            return text_search(query[query.index('-')+1:], querytype)
        try: return text_search(difflib.get_close_matches(query, namelist)[0], querytype)
        except: 
            pass
            #print(query, club_name, temp_club_name)
    temp.sort(key= lambda x: int(x[142]), reverse=True)
    return temp





def clean_up_list(temp_list):
    for x in temp_list:
        for y in temp_list:
            if(x[3]==y[3] and x[0]!=y[0]): 
                if(x[2]!=y[2]):

                    if(x[6]==1 and x[2]!=y[2]): #change 8 to 6
                        index=temp_list.index(y)
                        priority=y[7]
                        temp_list.pop(temp_list.index(y))
                        temp_list=adjust_priority_order(temp_list, index, priority) #change 6 to 7
                        return clean_up_list(temp_list)
                    
                    elif(y[6]==1 and x[2]!=y[2]):
                        index=temp_list.index(x)
                        priority=x[7]       #change 8 to 6
                        temp_list.pop(temp_list.index(x))
                        temp_list=adjust_priority_order(temp_list, index, priority)          #change 6 to 7
                        return clean_up_list(temp_list)



                    if(x[8]>=y[8]): #change 7 to 8
                        if(y[5]-x[5]<=100):
                            #print(y,'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',x, '\n')
                            index=temp_list.index(y)
                            priority=y[7]
                            temp_list.pop(temp_list.index(y))   
                            temp_list=adjust_priority_order(temp_list, index, priority)   #change 6 to 7
                            return clean_up_list(temp_list)
                        else:
                            index=temp_list.index(x)
                            priority=x[7]
                            temp_list.pop(temp_list.index(x))
                            temp_list=adjust_priority_order(temp_list, index, priority)    #change 6 to 7
                            return clean_up_list(temp_list)

                    else: 
                        if(x[5]-y[5]<=100):
                            #print(x,'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',y, '\n')
                            temp_list.remove(x)
                            return clean_up_list(temp_list)
                        else:
                            temp_list.remove(y)
                            return clean_up_list(temp_list)

                        
                
    return temp_list
def clean_pos_list(temp_list):
    for x in range(len(temp_list)):
        for y in range(x+1, len(temp_list)):
            if(temp_list[x][3]==temp_list[y][3]):
                if(temp_list[x][5]>temp_list[y][5]): 
                    #print(y,'CCCCCCCCCCCCCCCC', x, '\n')
                    index=y
                    priority=temp_list[y][7]
                    temp_list.pop(y)
                    temp_list=adjust_priority_order(temp_list, index, priority)
                    return clean_pos_list(temp_list)
                else:
                    #print(x, 'DDDDDDDDDDDD', y, '\n')
                    index=x
                    priority=temp_list[x][7]
                    temp_list.pop(x)
                    temp_list=adjust_priority_order(temp_list, index, priority)
                    return clean_pos_list(temp_list)
    #print(temp_list)
    return temp_list   

def adjust_priority_order(temp_list, index, priority):
    for x in range(len(temp_list)):
        if(index<=x):
            if(temp_list[x][7]>priority):    #change 6 to 7
                temp_list[x][7]-=1      #change 6 to 7
            else:
                break    
    return temp_list

def adjust_to_avg(temp_list, temp_avg, max_avg):
    for x in range(len(temp_list)-1):
        temp_list[x][5]*=1000/temp_avg
    return temp_list




def main(match_url, league_name, final_list, final_list_lower_league):
    r=requests.get(match_url)
    soup=BeautifulSoup(r.content, "html.parser")
    count=0
    try:
    #if(True):
        team1_score, team2_score=soup.find('span', {'class': 'css-jkaqxa'}).text.replace(' ','').split('-')
        #if(team1_score>team2_score): rating_offset=1.1

        data=soup.find('header', {'class':'css-kiurn-LineupTitleContainer e1ykd9ch0'})
        team1=data.findAll('h2')[0].text
        team2=data.findAll('h2')[1].text
        #print(team1, team2)


        
        
        data=soup.find('section', {'class':'css-c4r9g5-LineupMapContainer eu5dgts4'})
        TeamContainer=data.findAll('div', {'class':'css-18ykv9q-TeamContainer eu5dgts1'})
        team_list=[]
        for team_temp in TeamContainer:  
            if(TeamContainer.index(team_temp)==0): 
                team_name=team1 
                other_team=team2
            else: 
                team_name=team2
                other_team=team1

            if((('GERMANY' in league_name and team_name in['Bayern München','Bayer Leverkusen'])) or 'GERMANY' not in league_name):
                RowContainer=team_temp.findAll('div', {'class':'css-1v37p2g-RowContainer eu5dgts0'})
                
                for div in RowContainer:
                    for x in div: 
                        if(x.text):
                            
                            #blah=str(x)
                            #print(x)
                            #print(blah[blah.find('href="')+6:blah.find('"><div class')])

                            


                            rating_offset=1
                            if(TeamContainer.index(team_temp)==0): 
                                if(team1_score>team2_score): rating_offset=1.2
                                elif(team1_score<team2_score): rating_offset=0.8
                            else: 
                                if(team2_score>team1_score): rating_offset=1.2
                                elif(team2_score<team1_score): rating_offset=0.8


                            bottom_right=x.find('div',{'class':'css-ed21d0-BottomRightLineupBadgesContainer e1eitw0d8'})

                            #match_card=bottom_right.parent.parent['href']
                            G=bottom_right.findAll('div',{'class':'css-jmke63-BadgeContainer e1eitw0d0'})  
                            goal_count, assist_count=0,0
                            for goals in G:
                                if(goals.find('svg', {'viewbox':'0 0 20 20'})):
                                    goal_count+=1
                                elif(goals.find('svg', {'viewbox':'0 0 14 14'})):
                                    assist_count+=1

                            try: motm_flag=bool(x.find('div', {'class':'css-2yce43-LineupPlayerRatingContainer e1eitw0d3'}).findAll('div',{'class':'css-1i7ahr2-PlayerRatingStyled e1sodkt20'})[0].find('svg',{'viewbox':"0 0 13 13"}))
                            except: motm_flag=0
                            #print(motm_flag)
                            rating_offset=rating_offset*(1.02**motm_flag)


                            #if(goal_count>0):
                             #   soup1=BeautifulSoup(requests.get(match_card).content, "html.parser")
                            

                            
                            count+=1
                            temp=re.sub(r"(?<=[\d])(?=[^\d\s^.])", '-', x.text)
                            if("'" in temp[:4]): temp=temp[temp.index("'")+1:]
                            
                            rating=temp[:temp.index('-')]
                            name=temp[temp.index('-')+1:]
                            for p in soup.findAll('span', {'class':'css-qnozj7-EventTime e3q4wbq7'}):
                                penalty_count=p.text.count('Pen')
                                if(penalty_count>0 and p.previous_sibling.text==name): goal_count=goal_count-penalty_count + (0.22*penalty_count)
                                
                            
                            if((RowContainer.index(div)==0 and TeamContainer.index(team_temp)==0) or (RowContainer.index(div)==len(RowContainer)-1 and TeamContainer.index(team_temp)==1)): pos='GK'
                            elif((RowContainer.index(div)==1 and TeamContainer.index(team_temp)==0) or (RowContainer.index(div)==len(RowContainer)-2 and TeamContainer.index(team_temp)==1)): pos='DEF'
                            elif((RowContainer.index(div)==len(RowContainer)-1 and TeamContainer.index(team_temp)==0) or (RowContainer.index(div)==0 and TeamContainer.index(team_temp)==1)): pos='ATT'
                            else: pos='MID'
                            #print(rating, name, pos,end='      ')
                            
                            #print(name, rating, team_name)
                            try: 
                            #if(True):
                                OVR=text_search(unidecode.unidecode(name), unidecode.unidecode(team_name))[0][140]
                                player_pos=text_search(unidecode.unidecode(name), unidecode.unidecode(team_name))[0][column_name.index('RegisteredPosition')]
                                if(text_search(unidecode.unidecode(name), unidecode.unidecode(team_name))[0][column_name.index('Country')]=='13'):
                                    rating_offset*=1.15
                
                                if(rating_offset<=1 and goal_count>0 and abs(int(team1_score)-int(team2_score))<=goal_count): rating_offset*=1.05
                                if(player_pos in ['9', '10', '11']): 
                                    rating_offset=rating_offset*(1.05**goal_count)
                                    pos='ATT'
                                elif(player_pos in ['6', '7', '8']): rating_offset=rating_offset*(1.05**goal_count)
                                elif(player_pos in ['2', '3','4', '5']): rating_offset=rating_offset*(1.1**goal_count)
                                elif(player_pos in ['1']): 
                                    rating_offset*=1.02
                                    rating_offset=rating_offset*(1.25**goal_count)
                                else: rating_offset=rating_offset*(1.025**goal_count)
                                
                                if(goal_count+assist_count>1): rating_offset=rating_offset*(1.02**(goal_count+assist_count-1))
                                #print(name, goal_count)

                                if(team_name in ['Bayer Leverkusen', 'Lazio','Roma', 'Celtic', 'Rangers'] and pos!='GK'):
                                    rating_offset*=1.1
                                elif(team_name in ['Barcelona', 'Juventus','Bayern München','Manchester United', 'Arsenal'] and pos!='GK'):
                                    rating_offset*=1.13
                                
                                if('PORTUGAL' in league_name):
                                    if(team_name in ['FC Porto', 'Sporting CP', 'Benfica']): rating_offset*=1.05
                                    else: continue
                                
                                if('Ajax' in team_name):    rating_offset*=1.05
                                        
            
                    

                                if(int(OVR)>84): OVR='85'
                                

                                
                                
                                if(name=="de Jong" and pos=='ATT' and team_name=='Barcelona'): OVR='80'

                                if(other_team.upper() in important_club_list): rating_offset*=1.15
                                #if(team_name.upper() in important_club_list): rating_offset*=1.0
                                rating_offset=rating_offset*(1.02**assist_count)
                                #print(f'Goals: {goal_count} Assists: {assist_count}')

                                special=float(rating)*int(OVR)*rating_offset                              
                                #print(name, rating, pos, team_name, OVR, special, motm_flag)
                                team_list.append([name, rating, pos, team_name, OVR, special, motm_flag])
                            except: continue
                
        #print('----------SUBS------------------')
        Bench_Container=soup.findAll('ul', {'class':'css-dvtdw9-BenchContainer elhbny51'})
        for bench in Bench_Container:
            for subs in bench.findAll('li', {'class':'css-yrdwx3-BenchItem elhbny52'}):
                try:
                    goal_count=0
                    subs.select('div[class*="PlayerRatingStyled e1sodkt20"]')[0].text
                    try: 
                        rating=subs.findAll('span', class_=False)[0].text
                        motm_flag=bool(subs.find('svg', {'viewbox':'0 0 13 13'}))
                    except: rating=None
                    name=re.sub(r'[0-9]+', '',subs.findAll('span', class_=False)[1].text)
                    name=name[name.find(' ')+1:]
                    minutes_played=90-int(subs.find('span', {'class':'css-a6zhpl-SubText elhbny57'}).text[:-1])
                    #print(name, rating, Bench_Container.index(bench), minutes_played)
                    if(Bench_Container.index(bench)==0): 
                        team_name=team1
                        other_team=team2
                        if(team1_score>team2_score): rating_offset=1.2
                        elif(team1_score<team2_score): rating_offset=0.8
                        else:rating_offset=1
                    elif(Bench_Container.index(bench)==1): 
                        team_name=team2
                        other_team=team1
                        if(team2_score>team1_score): rating_offset=1.2
                        elif(team2_score<team1_score): rating_offset=0.8
                        else:rating_offset=1
                    if(('GERMANY' in league_name and team_name in['Bayern München','Bayer Leverkusen']) or 'GERMANY' not in league_name):
                    
                        for p in soup.findAll('span', {'class':'css-qnozj7-EventTime e3q4wbq7'}):
                            if(p.previous_sibling.text==name or p.previous_sibling.text==name.split(' ')[-1]): 
                                goal_count=p.text.count(',')+1
                                #print(goal_count)
                            penalty_count=p.text.count('Pen')
                            if(penalty_count>0 and p.previous_sibling.text==name): goal_count=goal_count-penalty_count + (0.22*penalty_count)
                        
                        if(rating_offset>=1 and goal_count>0 and abs(int(team1_score)-int(team2_score))<=goal_count): rating_offset*=1.05

                        OVR=text_search(unidecode.unidecode(name), unidecode.unidecode(team_name))[0][140]
                        player_pos=text_search(unidecode.unidecode(name), unidecode.unidecode(team_name))[0][column_name.index('RegisteredPosition')]
                        if(text_search(unidecode.unidecode(name), unidecode.unidecode(team_name))[0][column_name.index('Country')]=='13'):
                            rating_offset*=1.15
        
                        
                        if(player_pos in ['9', '10', '11']): 
                            rating_offset=rating_offset*(1.07**goal_count)
                            pos='ATT'
                        elif(player_pos in ['6', '7', '8']): 
                            rating_offset=rating_offset*(1.1**goal_count)
                            pos='MID'
                        elif(player_pos in ['2', '3','4', '5']): 
                            rating_offset=rating_offset*(1.15**goal_count)
                            if(player_pos in ['4', '5']): pos='MID'
                            else: pos='DEF'
                        elif(player_pos in ['1']): 
                            rating_offset*=1.02
                            rating_offset=rating_offset*(1.3**goal_count)

                            pos='DEF'
                        else: 
                            if(player_pos in ['12']): 
                                rating_offset=rating_offset*(1.05**goal_count)
                                pos='ATT'
                            else: pos='GK'
                        
                        if(goal_count>1): rating_offset=rating_offset*(1.04**(goal_count-1))
                        #print(name, goal_count)

                        if(team_name in ['Bayer Leverkusen', 'Lazio','Roma', 'Celtic', 'Rangers'] and pos!='GK'):
                            rating_offset*=1.1
                        elif(team_name in ['Barcelona', 'Juventus','Bayern München','Manchester United', 'Arsenal'] and pos!='GK'):
                            rating_offset*=1.13
                        
                        if('PORTUGAL' in league_name):
                            if(team_name in ['FC Porto', 'Sporting CP', 'Benfica']): rating_offset*=1.05
                            else: continue
                        
                        if('Ajax' in team_name):    rating_offset*=1.05
                                    

                        if(int(OVR)>84): OVR='85'
                        

                        
                        
                        if(name=="de Jong" and pos=='ATT' and team_name=='Barcelona'): OVR='80'

                        if(other_team.upper() in important_club_list): rating_offset*=1.15
                        #if(team_name.upper() in important_club_list): rating_offset*=1.0
                        
                        
                        #rating_offset=rating_offset*(1.02**assist_count)
                        #print(f'Goals: {goal_count} Assists: {assist_count}')

                        if(minutes_played<31): rating_offset*=1.1
                        elif(minutes_played<47): rating_offset*=1.05
                        else: rating_offset*=1.02
                        
                        rating_offset=rating_offset*(1.02**motm_flag)

                        special=float(rating)*int(OVR)*rating_offset                              
                        #print(name, rating, pos, team_name, OVR, special, motm_flag)
                        team_list.append([name, rating, pos, team_name, OVR, special, motm_flag])    
                    
                except: pass
        
        team_list.sort(key= lambda x: x[5], reverse=True)
        #print(team_list[:2])
        pos_category=['GK', 'DEF','MID','ATT', 'GK', 'DEF', 'MID', 'ATT']
        for x in team_list:
            if(x[2] in pos_category):   
                if(league_name in ['SPAIN - LALIGA', 'ITALY - SERIE A', 'GERMANY - 1. BUNDESLIGA','FRANCE - LIGUE 1', 'ENGLAND - PREMIER LEAGUE', 'PORTUGAL - LIGA PORTUGAL']):
                    final_list.append(x)
                elif(league_name in ['BELGIUM - FIRST DIVISION A', 'NETHERLANDS - EREDIVISIE', 'SCOTLAND - PREMIERSHIP', 'RUSSIA - PREMIER LEAGUE', 'UKRAINE - PREMIER LEAGUE']):
                    final_list_lower_league.append(x)  
                pos_category.remove(x[2])
        #print(final_list)
        #final_list.append(team_list[0])
        #final_list.append(team_list[1])
    except: pass
    return final_list, final_list_lower_league

def final_list_function(saturday=last_saturday, sunday=last_sunday, monday=last_monday):
    final_list,final_list_lower_league=[],[]

    match_url_list=fotmob_get_match_links.get_link(saturday, sunday, monday)
    for x in match_url_list:
        final_list, final_list_lower_league=main(x[0], x[1], final_list, final_list_lower_league)


    final_list.sort(key= lambda x: x[5], reverse=True)
    final_list_lower_league.sort(key= lambda x: x[5], reverse=True)
    gk_list, def_list, mid_list, att_list=[],[],[],[]
    lineup_list=[]
    #print(final_list)
    count_GK, count_DEF, count_MID, count_ATT=0,0,0,0
    #print(final_list)
    for x in final_list:
        if(x[2]=='GK' and count_GK<2):
            #print(x, end=" ")
            temp=final_list[final_list.index(x)]
            temp.append(count_GK)
            print(temp)
            gk_list.append(temp)
            
            count_GK+=1
    print('\n')
    for x in final_list:    
        if(x[2]=='DEF' and count_DEF<8):
            #print(x, end=" ")
            temp=final_list[final_list.index(x)]
            temp.append(count_DEF)
            #print(temp)
            def_list.append(temp)
            count_DEF+=1
    print('\n')
    for x in final_list:    
        if(x[2]=='MID' and count_MID<12):
            #print(x, end=" ")
            temp=final_list[final_list.index(x)]
            temp.append(count_MID)
            #print(temp)
            mid_list.append(temp)
            count_MID+=1
    print('\n')
    for x in final_list:    
        if(x[2]=='ATT' and count_ATT<10):
            #print(x, end=" ")
            temp=final_list[final_list.index(x)]
            temp.append(count_ATT)
            #print(temp)
            att_list.append(temp)
            count_ATT+=1
    print('\n')
    #print(lineup_list)
    #print(lineup_list[0][3])

    gk_list=clean_pos_list(gk_list)
    def_list=clean_pos_list(def_list)
    mid_list=clean_pos_list(mid_list)
    att_list=clean_pos_list(att_list)

    lower_league_pos_temp=['ATT', 'MID', 'DEF', 'GK', 'ATT', 'MID', 'DEF', 'GK']
    for x in final_list_lower_league:
        if(x[2] in lower_league_pos_temp):
            print(x)
            lower_league_pos_temp.remove(x[2])

    gk_avg, def_avg, mid_avg, att_avg=0,0,0,0
    for x in range(len(gk_list)-1):
        gk_list[x].append(gk_list[x][5]-gk_list[x+1][5])
        print(gk_list[x])
        gk_avg+=gk_list[x][5]

    print('\n')

    for x in range(len(def_list)-1):
        def_list[x].append(def_list[x][5]-def_list[x+1][5])
        print(def_list[x])
        def_avg+=def_list[x][5]
    print('\n')

    for x in range(len(mid_list)-1):
        mid_list[x].append(mid_list[x][5]-mid_list[x+1][5])
        print(mid_list[x])
        mid_avg+=mid_list[x][5]
    print('\n')

    for x in range(len(att_list)-1):
        att_list[x].append(att_list[x][5]-att_list[x+1][5])
        print(att_list[x])
        att_avg+=att_list[x][5]
    print('\n')

    #gk_list=adjust_to_avg(gk_list, gk_avg, max_avg)
    #def_list=adjust_to_avg(def_list, def_avg, max_avg)
    #mid_list=adjust_to_avg(mid_list, mid_avg, max_avg)
    #att_list=adjust_to_avg(att_list, att_avg, max_avg)








    

    lineup_list=gk_list[:-1]+def_list[:-1]+mid_list[:-1]+att_list[:-1]
    lineup_list=clean_up_list(lineup_list)
    """if((x[2] in ['GK', 'DEF']) and (y[2] in ['MID', 'ATT']) and (x[5]>y[5])): 
                    print(x,y)
                    lineup_list.remove(y)
                elif((y[2] in ['GK', 'DEF']) and (x[2] in ['MID', 'ATT']) and (y[5]>x[5])): 
                    print(x,y)
                    lineup_list.remove(x)
                    break
                else:
                    if(x[6]<y[6]):   
                        print(x,y, '-----------------------------------')  
                        lineup_list.remove(y)
                    elif(x[6]==y[6]):
                        if(x[5]>y[5]): lineup_list.remove(y)
                        elif(y[5]>x[5]): 
                            print(x,y)
                            lineup_list.remove(x)
                            break
                    else: 
                        print(x,y, '+++++++++++++++') 
                        lineup_list.remove(x)
                        break"""

    #print(lineup_list)
    lineup_list.sort(key= lambda x: x[2], reverse=True)
    count_GK, count_DEF, count_MID, count_ATT=0,0,0,0



    for x in lineup_list:
        if(x[2]=='GK' and count_GK<1):
            print(x)
            count_GK+=1
        if(x[2]=='DEF' and count_DEF<4):
            print(x)
            count_DEF+=1
        if(x[2]=='MID' and count_MID<5):
            print(x)
            count_MID+=1
        if(x[2]=='ATT' and count_ATT<4):
            print(x)
            count_ATT+=1
    print(f'GK avg: {gk_avg} \nDEF avg: {def_avg} \nMID avg: {mid_avg} \nATT avg: {att_avg}')

final_list_function(20220212,20220213, 20220214)
