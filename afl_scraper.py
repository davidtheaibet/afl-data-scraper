#!/usr/bin/env python3
"""
AFL Data Scraper
Scrapes teams, players, stats, and upcoming games from Footywire
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
import re

class AFLScraper:
    def __init__(self):
        self.base_url = "https://www.footywire.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.data = {
            'teams': [],
            'players': [],
            'fixtures': [],
            'ladder': [],
            'stats': []
        }
    
    def scrape_teams(self):
        """Scrape all AFL teams"""
        print("Scraping teams...")
        url = f"{self.base_url}/afl/footy/ft_teams"
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        teams = []
        # Find team links
        team_links = soup.find_all('a', href=re.compile(r'/afl/footy/th-'))
        for link in team_links:
            team_name = link.text.strip()
            team_url = link.get('href')
            if team_name and team_url:
                team_id = team_url.split('-')[-1]
                teams.append({
                    'id': team_id,
                    'name': team_name,
                    'url': f"{self.base_url}{team_url}"
                })
        
        self.data['teams'] = teams
        print(f"Found {len(teams)} teams")
        return teams
    
    def scrape_ladder(self):
        """Scrape current AFL ladder"""
        print("Scraping ladder...")
        url = f"{self.base_url}/afl/footy/ft_ladder"
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        ladder = []
        # Find ladder table
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header
                cols = row.find_all('td')
                if len(cols) >= 8:
                    ladder.append({
                        'position': cols[0].text.strip(),
                        'team': cols[1].text.strip(),
                        'points': cols[2].text.strip(),
                        'games': cols[3].text.strip(),
                        'wins': cols[4].text.strip(),
                        'losses': cols[5].text.strip(),
                        'draws': cols[6].text.strip(),
                        'percentage': cols[7].text.strip()
                    })
        
        self.data['ladder'] = ladder
        print(f"Found {len(ladder)} ladder positions")
        return ladder
    
    def scrape_fixtures(self):
        """Scrape upcoming games/fixtures"""
        print("Scraping fixtures...")
        url = f"{self.base_url}/afl/footy/ft_match_list"
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        fixtures = []
        # Find match rows
        match_rows = soup.find_all('tr', class_=re.compile(r'[odd|even]'))
        for row in match_rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                try:
                    round_info = cols[0].text.strip()
                    date = cols[1].text.strip()
                    teams = cols[2].text.strip()
                    venue = cols[3].text.strip()
                    
                    fixtures.append({
                        'round': round_info,
                        'date': date,
                        'match': teams,
                        'venue': venue
                    })
                except:
                    continue
        
        self.data['fixtures'] = fixtures
        print(f"Found {len(fixtures)} fixtures")
        return fixtures
    
    def scrape_player_stats(self, limit=50):
        """Scrape top player stats"""
        print(f"Scraping top {limit} player stats...")
        url = f"{self.base_url}/afl/footy/ft_player_rankings"
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        players = []
        # Find player ranking table
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for i, row in enumerate(rows[1:limit+1]):  # Top players only
                cols = row.find_all('td')
                if len(cols) >= 4:
                    try:
                        rank = cols[0].text.strip()
                        player = cols[1].text.strip()
                        team = cols[2].text.strip()
                        stat = cols[3].text.strip()
                        
                        players.append({
                            'rank': rank,
                            'name': player,
                            'team': team,
                            'stat_value': stat
                        })
                    except:
                        continue
        
        self.data['players'] = players
        print(f"Found {len(players)} players")
        return players
    
    def save_to_json(self, filename='afl_data.json'):
        """Save all data to JSON"""
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"Data saved to {filename}")
    
    def save_to_csv(self):
        """Save data to CSV files"""
        # Teams
        if self.data['teams']:
            pd.DataFrame(self.data['teams']).to_csv('teams.csv', index=False)
            print("Saved teams.csv")
        
        # Ladder
        if self.data['ladder']:
            pd.DataFrame(self.data['ladder']).to_csv('ladder.csv', index=False)
            print("Saved ladder.csv")
        
        # Fixtures
        if self.data['fixtures']:
            pd.DataFrame(self.data['fixtures']).to_csv('fixtures.csv', index=False)
            print("Saved fixtures.csv")
        
        # Players
        if self.data['players']:
            pd.DataFrame(self.data['players']).to_csv('players.csv', index=False)
            print("Saved players.csv")
    
    def run(self):
        """Run full scrape"""
        print("Starting AFL data scrape...")
        print("=" * 50)
        
        self.scrape_teams()
        self.scrape_ladder()
        self.scrape_fixtures()
        self.scrape_player_stats()
        
        print("=" * 50)
        print("Saving data...")
        self.save_to_json()
        self.save_to_csv()
        
        print("=" * 50)
        print("Scrape complete!")
        print(f"Teams: {len(self.data['teams'])}")
        print(f"Ladder: {len(self.data['ladder'])}")
        print(f"Fixtures: {len(self.data['fixtures'])}")
        print(f"Players: {len(self.data['players'])}")

if __name__ == "__main__":
    scraper = AFLScraper()
    scraper.run()
