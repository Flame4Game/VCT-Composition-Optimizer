import vlrdevapi as vlr
from scipy.optimize import linear_sum_assignment
import numpy as np

def find_roster(team_id):
    pid_list = []
    try:
        ros = vlr.team.roster(team_id=team_id)
        for i in ros.players:
            if i.is_active and not i.is_sub:
                pid_list.append(i.id)
        if len(pid_list) == 5:
            return pid_list
    except vlr.exceptions.DataNotFoundError:
        pass
    pid_list = []
    matches_l = vlr.team.upcoming_matches(team_id=team_id)
    if not matches_l.matches:
        matches_l = vlr.team.completed_matches(team_id=team_id)
    info = vlr.series.players(series_id=matches_l.matches[0].match_id)
    if info.team1.team_id == team_id:
        for i in info.team1.players:
            pid_list.append(i.player_id)
    else:
        for i in info.team2.players:
            pid_list.append(i.player_id)
    return pid_list

ag_list = ['Miks','Clove','Harbor','Omen','Brimstone','Astra','Viper','Cypher','Vyse','Deadlock','Killjoy','Sage','Veto','Chamber','Jett','Iso','Reyna','Yoru','Phoenix','Raze','Neon','Waylay','Kayo','Skye','Breach','Gekko','Tejo','Fade','Sova']
d = {}

print("What team do you want? Please input the team id, or player ids separated by spaces.")

lst = list(map(int, input().split()))
if len(lst) == 1:
    pid_list = find_roster(lst[0])
else:
    pid_list = lst

print("---------")
print("Player pool:")

def agent_to_row_index(agent):
    i = 0
    while ag_list[i] != agent:
        i += 1
    return i

for pid in pid_list:
    name = vlr.player.profile(player_id=pid)
    print(name.name)
    stats = vlr.player.agents(player_id=pid)
    d[name.name] = [0]
    for s in stats.agents:
        d[name.name][0] += s.rounds
        d[name.name].append([s.agent, s.rounds])
print("--------")
player_list = []
for player in d:
    player_list.append(player)
    for i in range (1, len(d[player])):
        d[player][i][1] = (d[player][i][1])/(d[player][0])

master = []
for agent in ag_list:
    current_ag = []
    for p in d:
        score = 0
        for i in range (1, len(d[p])):
            if agent == d[p][i][0]:
                score = d[p][i][1]
        current_ag.append(score)
    master.append(current_ag)

a = np.array(master, dtype=float)
releaseKey = False
while not releaseKey:
    print("What comp would you like to use? Enter d for pre-built dict of comps. Enter e to exit.")
    comp_dict = [["Omen", "Killjoy", "Jett", "Kayo", "Sova"], ["Omen", "Viper", "Vyse", "Raze", "Fade"], ["Brimstone", "Cypher", "Raze", "Phoenix", "Fade"], ["Viper", "Killjoy", "Jett", "Sage", "Sova"], ["Omen", "Cypher", "Sage", "Deadlock", "Fade"], ["Astra", "Jett", "Kayo", "Fade", "Sova"], ["Jett", "Raze", "Cypher", "Omen", "Sage"], ["Chamber", "Killjoy", "Sova", "Sage", "Viper"]]

    cmp = list(input().split())
    cmp = [agent.capitalize() for agent in cmp]
    if cmp == ["D"]:
        for comp in comp_dict:
            mat = np.array([a[agent_to_row_index(agent)] for agent in comp], dtype=float)
            logged = -np.log(mat + 0.000001)
            row_ind, col_ind = linear_sum_assignment(logged)
            total = 0
            for i in range(len(comp)):
                ag = comp[row_ind[i]]
                p = player_list[col_ind[i]]
                score = a[agent_to_row_index(ag)][col_ind[i]] * 100
                total += score
                print(ag + " goes to " + p + ". Pick rate is " + f"{score:.2f}%")
            print("--------")
    elif all(agent in ag_list for agent in cmp):
        mat = np.array([a[agent_to_row_index(agent)] for agent in cmp], dtype=float)
        logged = -np.log(mat + 0.000001)
        row_ind, col_ind = linear_sum_assignment(logged)
        total = 0
        for i in range(len(cmp)):
            ag = cmp[row_ind[i]]
            p = player_list[col_ind[i]]
            score = a[agent_to_row_index(ag)][col_ind[i]] * 100
            total += score
            print(ag + " goes to " + p + ". Pick rate is " + f"{score:.2f}%")
        print("--------")
    elif cmp == ["E"]:
        releaseKey = True
    else: print("Sry, comp DNE")

print("Credit goes to vlrdevapi.")