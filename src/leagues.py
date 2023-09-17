def leagues():
    leagues_data = json.load(open("esports-data/leagues.json", "r"))
    return leagues_data

def league_points(league_id):
    leagues = leagues()
    league = [league for league in leagues if league["id"] == league_id][0]
    league_dict = {
        "international": ["Worlds", "MSI"],
        "major": ["LCK", "LEC", "LCS","LPL"],
        "minor": ["CBLOL", "LCL", "LCO", "LJL", "LLA", "PCS", "TCL", "VCS"],
        "challenger": ["LCK Challengers", "EMEA Masters", "LCS Challengers Qualifiers", "LCS Challengers"],
        "regional": ["Ultraliga", "Prime League", "College Championship", "All-Star Event", "La Ligue FranÃ§aise", "NLC", "Elite Series", "Liga Portuguesa", "PG Nationals", "SuperLiga", "Hitpoint Masters", "Esports Balkan League", "Greek Legends League", "Arabian League", "LCK Academy", "LJL Academy", "CBLOL Academy", "North Regional League", "South Regional League", "TFT Rising Legends"]
    }
    league_region = [key for key, value in league_dict.items() if league["name"] in value][0]
    points_mapping = {
        "international": 100,
        "major": 80,
        "minor": 60,
        "challenger": 40,
        "regional": 20
    }

    return points_mapping[league_region]