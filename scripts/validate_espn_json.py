import sys
import json


def main():
    input_json_file = sys.argv[1]

    team_names = {}

    with open(input_json_file) as json_file:
        team_data = json.load(json_file)
        for team_def in team_data:
            team_name = team_def['name']
            if team_name in team_names:
                print team_name, 'Duplicate Team'
            team_names[team_name] = True
            roster = team_def.get('roster', [])
            games = team_def.get('games', [])
            if len(roster) == 0:
                print team_name, 'Missing Roster'
            if len(games) == 0:
                print team_name, 'Missing Games'


if __name__ == '__main__':
    sys.exit(main())