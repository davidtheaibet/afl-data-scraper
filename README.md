# AFL Data Scraper

Scrapes AFL (Australian Football League) data from Footywire.

## Data Collected

### Teams
- All 18 AFL teams
- Team names and IDs
- URLs for detailed team pages

### Ladder/Standings
- Current season ladder
- Position, points, wins, losses, draws
- Percentage

### Fixtures (Upcoming Games)
- Round-by-round schedule
- Dates, times, venues
- Matchups

### Player Stats
- Top 50 players by ranking
- Player names, teams
- Key statistics

## Usage

```bash
# Install dependencies
pip install requests beautifulsoup4 pandas

# Run scraper
python afl_scraper.py
```

## Output

- `afl_data.json` — All data in JSON format
- `teams.csv` — Team list
- `ladder.csv` — Current standings
- `fixtures.csv` — Upcoming games
- `players.csv` — Player statistics

## Data Source

[Footywire](https://www.footywire.com) — AFL statistics and information

## Sample Data

### Teams (18 total)
- Adelaide Crows
- Brisbane Lions
- Carlton Blues
- Collingwood Magpies
- Essendon Bombers
- Fremantle Dockers
- Geelong Cats
- Gold Coast Suns
- Greater Western Sydney Giants
- Hawthorn Hawks
- Melbourne Demons
- North Melbourne Kangaroos
- Port Adelaide Power
- Richmond Tigers
- St Kilda Saints
- Sydney Swans
- West Coast Eagles
- Western Bulldogs

### Latest Fixtures
- Round 4 games scheduled
- Includes dates, venues, matchups

### Player Stats
- Top 50 players by performance
- Includes disposals, goals, marks, tackles

## License

MIT License — Free to use for AIbet projects
