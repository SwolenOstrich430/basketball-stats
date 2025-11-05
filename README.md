# basketball-stats

## Overview 

## User Guide 

### Quick Start 

### Features

#### Player vs. Team Matchups 
#### Player vs. Player Matchups 
#### 

## Data 

### Provider Options
| Provider Name | Data Source | Type | Pricing | Source Code Link | Client Library Link | 
| :---: | :---: | :---: | :---: | :---: | :---: | 
| Basketball Reference Web Scraper | Basketball Reference | Scraper and Self Storage | Free |  [Github](https://github.com/jaebradley/basketball_reference_web_scraper) | [Client Library](https://pypi.org/project/basketball-reference-scraper/) 
| API-NBA | API-NBA | Web API and Self Storage | Free and Premium Options | N/A | [Rapid API](https://rapidapi.com/api-sports/api/api-nba) & [Docs](https://api-sports.io/documentation/nba/v2)

## Architecture 

### File Storage  
| Provider Name | Storage Type | Pricing | S3/GCS Compatible | 
| :---: | :---: | :---: | :---: | 
| [iDrive E2](https://www.idrive.com/s3-storage-e2/) | Cloud | 2.06/TB/Month | S3 Compatible | 
[Dropbox](https://www.dropbox.com) | Cloud | 9.99/2TB/Month | N/A
[Google Drive](https://workspace.google.com/products/drive/) | Cloud | Free up to 15GB | GCS Copmatible 
| [Scaleway Glacier](https://www.scaleway.com/en/glacier-cold-storage/) | Cloud | 2.00/1TB | S3 Compatible 

### Cloud Providers 
| Provider Name | Pricing  | 
| :---: | :---: | 
| AWS | $300 dollar credit | 
GCP | $200 dollar credit | 

### Database 
* MySQL/Postgres (used at previous job)
* Oracle/SQL Server (need to learn these for my new job)

#### ERD 
* Teams
  * [Teams and Players](./uml/teams/teams-players.mmd)
  * [Teams Misc. Attributes](./uml/teams/teams-desciptors.mmd)
  * [Games and Matchups](./uml/teams/teams-games.mmd)
* Players
  * [Player Stats](./uml/players/players-stats.mmd)
  * [Players Misc. Attributes](./uml/players/players-desciptors.mmd)
