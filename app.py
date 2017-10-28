import requests
import json
import configparser


# Initialize variables
BASE_URL = "https://na1.api.riotgames.com/lol/"

def init():
    ''' Retrieve API KEY from config file '''

    config = configparser.ConfigParser()
    config.read('config.ini')
    API_KEY = config['KEY']['API_KEY']
    
    return API_KEY

def request_user(name, header):
    ''' GET USER ID ''' 
    USER_URL = BASE_URL + "summoner/v3/summoners/by-name/{}"

    r = requests.get(USER_URL.format(name), headers = header)
    r = r.json()
    return r['accountId']

def request_matches(id, header):
    ''' GET MATCHES '''
    MATCH_URL = BASE_URL + "match/v3/matchlists/by-account/{}"

    r = requests.get(MATCH_URL.format(id), headers = header)
    return r.json()

def main():
    header = {'X-Riot-Token': init()}

    # Perform regex 
    # ^[0-9\\p{L} _\\.]+$ ======> provided by RIOT API
    summoner_name = input("Enter summoner name: ")
    summoner_id = request_user(summoner_name, header)

    # Request matches
    matches = request_matches(summoner_id, header)

    
    champions = {}
    for match in matches['matches']:
        if match['champion'] in champions:
            champions[match['champion']] += 1
        else:
            champions[match['champion']] = 1

    print(champions)

main()