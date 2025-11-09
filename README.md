# basketball-stats

## Overview 
This is an app that I'm working on with my brother to get better insights into the development of younger NBA players. Currently, there are many apps that provide data related to player performance but no free features that you can easily use to gain more complex insights into game-by-game development and general trends. 

Currently, we're determining the basic reports that we're interested in creating, and I'm defining our basic schema and mining data from different sources available for free.

## User Guide 

### Quick Start 

### Features

#### Player vs. Team Matchups 

#### List Player Stats 
* Counting 
* Aggregate 
* Advanced

#### Explanation of Advanced Stats 


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
  * [Teams and Players](./docs/database/erd/teams/teams-players.mmd)
  * [Teams Misc. Attributes](./docs/database/erd/teams/teams-desciptors.mmd)
  * [Games and Matchups](./docs/database/erd/teams/teams-games.mmd)
* Players
  * [Player Stats](./docs/database/erd/players/players-stats.mmd)
  * [Players Misc. Attributes](./docs/database/erd/players/players-desciptors.mmd)
