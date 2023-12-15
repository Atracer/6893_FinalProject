import urllib.request
import ssl
import json

def get_live_data():
    url = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
    scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
    scontext.verify_mode = ssl.VerifyMode.CERT_NONE
    with urllib.request.urlopen(url = url, context=scontext) as f:
        return json.loads(f.read().decode('utf-8'))
    
def get_level_diff(x):
    """input json output avg lvl diff """
    t1_avg = 0
    t2_avg = 0
    for i in range(0,5):
        t1_avg += x[-1]["allPlayers"][i]["level"]
        t2_avg += x[-1]["allPlayers"][i+5]["level"]
    t1_avg = t1_avg/5
    t2_avg = t2_avg/5
    return t1_avg - t2_avg
    
t2_towers_ID=[ "Turret_T2_L_03_A",
                "Turret_T2_C_05_A",
                "Turret_T2_R_03_A",
                "Turret_T2_L_02_A",
                "Turret_T2_C_04_A",
                "Turret_T2_R_02_A",
                "Turret_T2_L_01_A",
                "Turret_T2_C_03_A",
                "Turret_T2_R_01_A",
                "Turret_T2_C_02_A",
                "Turret_T2_C_01_A"]

t1_towers_ID=["Turret_T1_L_03_A",
                "Turret_T1_C_05_A",
                "Turret_T1_R_03_A",
                "Turret_T1_L_02_A",
                "Turret_T1_C_04_A",
                "Turret_T1_R_02_A",
                "Turret_T1_L_01_A",
                "Turret_T1_C_03_A",
                "Turret_T1_R_01_A",
                "Turret_T1_C_02_A",
                "Turret_T1_C_01_A"]
    
def get_teams(x):
    t1_team = []
    t2_team = []
    for i in range(0,5):
        t1_team.append(x["allPlayers"][i]["summonerName"])
        t2_team.append(x["allPlayers"][i+5]["summonerName"])
    return t1_team,t2_team

#what team is active player in?
def team_of_active_player(x):
    name_of_active_player = x['activePlayer']["summonerName"]
    t1_team, _ = get_teams(x)
    if name_of_active_player in t1_team:
        return "t1"
    else:
        return "t2"
    
def towers(x):
    #input game data, #of destroyed towers of active player
    t1_towers_amount = 0
    t2_towers_amount = 0
    for i in range(0,len(x["events"]['Events'])):
        
        if x["events"]['Events'][i]["EventName"]  == "TurretKilled": #filtering "tower killed" events
            
            if x["events"]['Events'][i]['TurretKilled'] in t2_towers_ID:
                t1_towers_amount += 1
            else:
                t2_towers_amount += 1
    if team_of_active_player(x) == "t1":
        return t1_towers_amount
    else:
        return t2_towers_amount
    
def get_assists_diff(x):
    t1_assists_total = 0
    t2_assists_total = 0
    for i in range(0,5):
        t1_assists_total += x["allPlayers"][i]["scores"]["assists"]
        t2_assists_total += x["allPlayers"][i+5]["scores"]["assists"]
    assists_diff = t1_assists_total - t2_assists_total
    if team_of_active_player(x) == "t1":
        return assists_diff
    else:
        return assists_diff*(-1)
    
def get_deaths_diff(x):
    t1_assists_total = 0
    t2_assists_total = 0
    for i in range(0,5):
        t1_assists_total += x["allPlayers"][i]["scores"]["deaths"]
        t2_assists_total += x["allPlayers"][i+5]["scores"]["deaths"]
    assists_diff = t1_assists_total - t2_assists_total
    if team_of_active_player(x) == "t1":
        return assists_diff
    else:
        return assists_diff*(-1)
    
def get_kills_diff(x):
    t1_assists_total = 0
    t2_assists_total = 0
    for i in range(0,5):
        t1_assists_total += x["allPlayers"][i]["scores"]["kills"]
        t2_assists_total += x["allPlayers"][i+5]["scores"]["kills"]
    assists_diff = t1_assists_total - t2_assists_total
    if team_of_active_player(x) == "t1":
        return assists_diff
    else:
        return assists_diff*(-1)
    
    
def get_dragons_amount(x):
    t2_dragons_amount = 0
    t1_dragons_amount = 0
    t1_players,t2_players = get_teams(x)
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"] == "DragonKill":
            if x["events"]['Events'][i]['KillerName'] in t1_players:
                t1_dragons_amount += 1
            else:
                 t2_dragons_amount += 1
    if team_of_active_player(x) == "t1":
        return t1_dragons_amount
    else:
        return t2_dragons_amount
    
def first_drake(x):
    team_pov = team_of_active_player(x) #"t1" or "t2"
    t1_players, _ = get_teams(x) 
    first_drake_taker = ""
    
    for i in range(0,len(x["events"]['Events'])):
        if (x["events"]['Events'][i]["EventName"] == "DragonKill"):
            if (x["events"]['Events'][i]['KillerName'] in t1_players):
                first_drake_taker = "t1"
                break
            else:
                first_drake_taker = "t2"
                break

    if first_drake_taker == "t1" and team_pov =="t1":
        return 1
    elif first_drake_taker == "t2" and team_pov =="t2":
        return 1
    else:
        return 0
    
def first_tower(x):
    team_pov = team_of_active_player(x) #"t1" or "t2"
    t1_players, _ = get_teams(x) #2lists of players
    first_tower_receivers = ""
    
    for i in range(0,len(x["events"]['Events'])):
        if (x["events"]['Events'][i]["EventName"] == "TurretKilled"):
            if (x["events"]['Events'][i]["TurretKilled"] in t2_towers_ID):
                first_tower_receivers = "t1"
                break
            else:
                first_tower_receivers = "t2"
                break

def first_blood(x):
    t1_players, _ = get_teams(x)
    fb_recipient =""
    
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"] == "FirstBlood":
            if x["events"]['Events'][i]["Recipient"] in t1_players:
                fb_recipient = "t1"
            else:
                fb_recipient = "t2"
    
    if team_of_active_player(x) == "t1" and fb_recipient == "t1":
        return 1
    elif team_of_active_player(x) == "t2" and fb_recipient == "t2":
        return 1
    else:
        return 0
    
def get_inhibs_amount(x):
    t2_inhibs = ["Barracks_T2_L1", "Barracks_T2_C1", "Barracks_T2_R1"]
    t1_team_destroyed_num = 0
    t2_team_destroyed_num = 0
    for i in range(len(x["events"]['Events'])):
        if x["events"]['Events'][i]['EventName'] == 'InhibKilled':
            if x["events"]['Events'][i]['InhibKilled'] in t2_inhibs:
                t1_team_destroyed_num +=1
            else:
                t2_team_destroyed_num +=1
    if team_of_active_player(x) == "t1":
        return t1_team_destroyed_num
    else:
        return t2_team_destroyed_num
    
def herald_amount(x):
    t1_heralds=0
    t2_heralds=0
    t1_players, _ = get_teams(x)
    
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"] == "HeraldKill":
            if x["events"]['Events'][i]["KillerName"] in t1_players:
                t1_heralds+=1
            else:
                t2_heralds+=1
    if team_of_active_player(x) == "t1":
        return t1_heralds
    else:
        return t2_heralds
    
def first_inhib(x):
    t2_inhibs = ["Barracks_T2_L1", "Barracks_T2_C1", "Barracks_T2_R1"]
    first_inhib_receiver = ""
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"]=="InhibKilled":
            if x["events"]['Events'][i]["InhibKilled"] in t2_inhibs:
                first_inhib_receiver = "t1"
            else:
                first_inhib_receiver = "t2"
    if team_of_active_player(x) == "t1" and first_inhib_receiver == "t1":
        return 1
    elif team_of_active_player(x) == "t2" and first_inhib_receiver == "t2":
        return 1
    else:
        return 0
    
def cs_diff(x):
    t1_cs=0
    t2_cs=0
    for i in range(5):
        t1_cs += x["allPlayers"][i]['scores']["creepScore"]
        t2_cs += x["allPlayers"][i+5]['scores']["creepScore"]
    cs_diff = t1_cs - t2_cs
    if team_of_active_player(x) == "t1":
        return cs_diff
    else:
        return cs_diff*(-1)
    
def jungle_cs_diff(x):
    t1_jg_cs = 0
    t2_jg_cs = 0
    for i in range(5):
        if x["allPlayers"][i]['position'] == "JUNGLE":
            if x["allPlayers"][0]["team"] == "ORDER": 
                t1_jg_cs = x["allPlayers"][i]['scores']["creepScore"]
            else:
                t2_jg_cs += x["allPlayers"][i]['scores']["creepScore"]
    cs_diff = t1_jg_cs - t2_jg_cs
    if team_of_active_player(x) == "blue":
        return cs_diff
    else:
        return cs_diff*(-1) 
    
def timestamp(x):
    return x['gameData']["gameTime"]

def current_stats(x):
    current_game_stats = {}
    current_game_stats["time"] = timestamp(x)
    current_game_stats["first_blood"] = first_blood(x)
    current_game_stats["first_tower"] = first_tower(x)
    current_game_stats["first_inhib"] = first_inhib(x)
    current_game_stats["inhibs_amount"] = get_inhibs_amount(x)
    current_game_stats["first_dragon"] = first_drake(x)
    current_game_stats["Dragons_Amount"] = get_dragons_amount(x)
    current_game_stats["Heralds_amount"] = herald_amount(x)
    current_game_stats["Kills_Diff"] = get_kills_diff(x)
    current_game_stats["Death_Diff"] = get_deaths_diff(x)
    current_game_stats["Assist_Diff"] = get_assists_diff(x)
    current_game_stats["Lvl_Diff"] = get_level_diff(x)
    current_game_stats["cs_Diff"] = cs_diff(x)
    current_game_stats["jungle_cs_Diff"] = jungle_cs_diff(x)
    current_game_stats["win_probability"] = 0.5
    return current_game_stats