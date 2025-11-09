# Mining Raw Stat Data
## For Basketball Stats App

Version 0.1  
Prepared by Peter Connelly
2025-11-04

## Table of Contents
<!-- TOC -->
- [Mining Raw Stat Data](#mining-raw-stat-data)
  - [For Basketball Stats App](#for-basketball-stats-app)
  - [Table of Contents](#table-of-contents)
  - [Revision History](#revision-history)
  - [1. Introduction](#1-introduction)
    - [1.1 Document Purpose](#11-document-purpose)
    - [1.2 Subject Scope](#12-subject-scope)
    - [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
      - [1.3.1 Statistics](#131-statistics)
      - [1.3.2 Statistic Types](#132-statistic-types)
    - [1.4 References](#14-references)
    - [1.5 Document Overview](#15-document-overview)
  - [2. Design Overview](#2-design-overview)
    - [2.1 Data Sources](#21-data-sources)
      - [Potential Data Providers](#potential-data-providers)
      - [2.1.1 Provider Decision](#211-provider-decision)
    - [2.2 Schema Definitions](#22-schema-definitions)
      - [2.2.1 Teams and Players](#221-teams-and-players)
      - [2.2.2 Games](#222-games)
      - [2.2.3 Game-by-Game Stats](#223-game-by-game-stats)
        - [Counting Stats Schema](#counting-stats-schema)
        - [Aggregate Stats Schema](#aggregate-stats-schema)
        - [Advanced Stats Schema](#advanced-stats-schema)
    - [2.3 Data Scraping](#23-data-scraping)
      - [2.3.1 Basketball Reference Client Library](#231-basketball-reference-client-library)
        - [API](#api)
      - [2.3.2 Team Data](#232-team-data)
      - [2.3.3 Player Data](#233-player-data)
        - [Table: dim\_players\_nationalities](#table-dim_players_nationalities)
        - [Table: dim\_players](#table-dim_players)
        - [Table: dim\_positions](#table-dim_positions)
      - [2.3.4 Roster Data](#234-roster-data)
        - [Table: dim\_seasons](#table-dim_seasons)
        - [Table: dim\_rosters](#table-dim_rosters)
        - [Table: dim\_rosters\_players\_bios](#table-dim_rosters_players_bios)
      - [2.3.5 Game-by-Game Stats](#235-game-by-game-stats)
        - [Table: fact\_flat\_stats\_counting](#table-fact_flat_stats_counting)
        - [Table: dim\_stat\_offense\_scoring](#table-dim_stat_offense_scoring)
        - [Table: dim\_stat\_offense\_non\_scoring](#table-dim_stat_offense_non_scoring)
        - [Table: dim\_stat\_defense](#table-dim_stat_defense)
    - [2.4 ETL Flow](#24-etl-flow)
      - [2.4.1 Long-Term Storage](#241-long-term-storage)
      - [2.4.2 Data Transformation](#242-data-transformation)
      - [2.4.3 Data Load](#243-data-load)
    - [2.2 Selected Viewpoints](#22-selected-viewpoints)
      - [2.2.1 Context](#221-context)
      - [2.2.2 Composition](#222-composition)
      - [2.2.3 Logical](#223-logical)
      - [2.2.4 Physical](#224-physical)
      - [2.2.5 Structure](#225-structure)
      - [2.2.6 Dependency](#226-dependency)
      - [2.2.7 Information](#227-information)
      - [2.2.8 Interface](#228-interface)
      - [2.2.9 Interaction](#229-interaction)
      - [2.2.10 Algorithm](#2210-algorithm)
      - [2.2.11 State Dynamics](#2211-state-dynamics)
      - [2.2.12 Concurrency](#2212-concurrency)
      - [2.2.13 Patterns](#2213-patterns)
      - [2.2.14 Deployment](#2214-deployment)
      - [2.2.15 Resources](#2215-resources)
  - [3. Design Views](#3-design-views)
  - [4. Decisions](#4-decisions)
  - [5. Appendixes](#5-appendixes)
<!-- TOC -->

## Revision History

| Name | Date | Reason For Changes | Version |
|------|------|--------------------|---------|
|   Peter Connelly   | 2025-11-04     | Creating initial design doc for getting stats data for MVP.                    |    0.1     |
|      |      |                    |         |

## 1. Introduction
In order to create an MVP, we need raw data for both team and player statistics. 

We'll also need to determine key system architecture we'll need in order to store that data in its raw and transformed form.


### 1.1 Document Purpose
This document aims to determine:
* What kinds of stat and categorical data is needed for our MVP.
* Possible data sources and their pros and cons. 
* Which of those sources we'll pull from.
* And the ETL flow we'll use for those sources.


### 1.2 Subject Scope
The scope descibed in the purpose of this document is likely too large for a single design document. This will serve as a place for requirement gathering and brainstorming larger system concerns. Components of those will be documented here first and then moved to individual design docs as time moves on. 

For now, we want the following deliverables:
1. A plan for Extract and Transform operations and data sources for: 
   1. Raw player game data for the 2024-2025 season.
   2. Player and Team bio data for the 2024-2025 season. 
2. A plan for long-term cloud storage for that raw data.
3. An ERD and schema for all related tables.
4. A UML and flow diagram for Loading all related data.

### 1.3 Definitions, Acronyms, and Abbreviations
#### 1.3.1 Statistics 
| Display Name | Description | Identifier | Type |
|---|---|---|---|
2-Point Field Goal Make | A shot taken inside the three-point arc that goes in the basket. | 2P_FGM | Counting |
2-Point Field Goal Attempt | A shot taken inside the three-point arc, regardless of miss or make.  | 2P_FGA | Counting |
3-Point Field Goal Make | A shot taken outside the three-point arc that goes in the basket. | 3P_FGM | Counting |
3-Point Field Goal Attempt | A shot taken outside the three-point arc, regardless of miss or make.  | 3P_FGA | Counting |
Free Throw Make | A shot taken from the free throw line as a result of a shooting foul that goes in the basket. | FTM | Counting |
Free Throw Attempt | A shot taken from the free throw line as a result of a shooting foul, regardless of miss or make. | FTA | Counting |

#### 1.3.2 Statistic Types
| Name | Description |
|---|---|
| `Counting` | Flat sums of values on a game-by-game or season-total basis. |
| `Aggregate` | Percentages/Averages derived from `Counting` stats |
| `Advanced` | Statistics derived from more complex formulas which take into account both `Aggregate` and `Counting` stats.|

### 1.4 References

### 1.5 Document Overview

In "Design Overview," we will: 
* Walk through base requirements for our initial MVP. 
* Provide potential sources for data that meets those requirements and recommendations for which of those sources we'll use.

In "Design Views," we will provide:
* A suggested database schema for that data post-transformation 
* Options for long-term storage of the raw versions of that data. 

## 2. Design Overview
Our initial MVP will clone basic features of [Basketball Reference](https://www.basketball-reference.com/). Though these requirements are very basic and will change almost immediately, we should have data to perform the following functions:

* List all NBA teams 
* List all players, their position, and their team for the 2024-2025 season. 
* List all game-by-game player data for counting stats as seen in the figure below:

![Game-by-Game Data Example](./assets/game-by-game-data-example.png "Figure 1.1: Game-by-Game Data Example")

### 2.1 Data Sources 
#### Potential Data Providers
| Provider Name | Data Source | Type | Pricing | Source Code Link | Client Library Link | Notes |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Basketball Reference Web Scraper | Basketball Reference | Scraper and Self Storage | Free |  [Github](https://github.com/jaebradley/basketball_reference_web_scraper) | [Client Library](https://pypi.org/project/basketball-reference-scraper/) | Provides counting, aggregate, and advanced stats for NBA seasons going back to 1950.
| API-NBA | API-NBA | Web API and Self Storage | Free and Premium Options | N/A | [Rapid API](https://rapidapi.com/api-sports/api/api-nba) & [Docs](https://api-sports.io/documentation/nba/v2) | Similar to the Basketball Reference Option, but more limiting and could cost money in the future.
| Genius | Second Spectrum NBA | Web API and Self Storage | Enterpise-level pricing | N/A | N/A | Not possible currently -- adding this as a note for later if this evolves, and we want a more premium option for advanced tracking.

#### 2.1.1 Provider Decision
Currently, scraping data from Basketball Reference is the cheapest and easiest option. Though our needs may advance beyond this relatively quickly, it should work to get us up and running for now.

### 2.2 Schema Definitions
Users will want to be able to view:
* Full team rosters 
* Players' positional and biographical information 
* Game-by-game statistics for players and teams 
  
#### 2.2.1 Teams and Players
Because this app's main purpose will be to analyze player and team statistics, we aren't going to be too concerned with historical and descriptive data like team lineage, colors, ownership, etc. 

For the most part, we want to know who's on which team, who played who when, and if someone moved teams at any point.

To account for this, we'll have the following schema: 

![Teams & Players](./assets/teams-players-erd.png)

Though at first, we'll only be gathering data for a single season, the need to support multiple seasons where players may be on more than one roster (due to trade or free agency) will come up quickly. To account for this, we have ***DIM_ROSTERS***. 

To start a season, all players on rosters will have an entry for their respective team and season years. E.g., for Tyrese Haliburton's (Player.id 1) Pacer's (Team.id 2) 2025-2026 season, a ***DIM_ROSTERS*** entry would look like this: 

| id | team_id | player_id | season_start_year | season_end_year | sequence
| :---: | :---: | :---: | :---: | :---: | :---: |  
| 1 | 1 | 2 | 2025 | 2026 | 0

If that player were then to be traded to the Chicago Bulls (Team.id 3) in the same season, then this new entry would be added to the table:

| id | team_id | player_id | season_start_year | season_end_year | sequence
| :---: | :---: | :---: | :---: | :---: | :---: |  
| 2 | 1 | 3 | 2025 | 2026 | 1

In the future, there may be a need to add a table or tables to represent how a player ended up on a team (through draft, free agency, or trade). However, for now, just storing which teams a player is or was on will do. 

#### 2.2.2 Games 
The games schema will also be relatively bare-bones for now. Here, we'll just be storing who played who and when:

![Games & Matchups](./assets/games-matchups-erd.png)

Here, the only gotcha is `arena_id`. This field will be left null if the two teams are playing at the expected `home_team_id`'s arena. The field will only have a value if it's at a nuetral site, like in Mexico City or London. 

#### 2.2.3 Game-by-Game Stats
All tracked statistics will be stored in the `DIM_STAT_ATTRIBUTES` table. This will include a `display_name`, `description`, a `type` value (enum with options `counting`, `aggregate`, `advanced`), and finally a `identifier` field. This will correspond to the actual database column where the statistic will be stored in a `DIM_*STAT` table. E.g., an **Offensive Rebound** may have an `identifier` of "orb". And its corresponding table will have a column named `orb`.

##### Counting Stats Schema
![Statistics Schema](./assets/stats-counting-erd.png)

##### Aggregate Stats Schema
`Aggregate` stats will be Views generated from related `counting` stats. For our MVP, we'll just be focusing on `counting` stats. This is just a placeholder section to come back to later. 

##### Advanced Stats Schema 
`Advanced` stats will be Views generated from related `counting` and `aggregate` stats. For our MVP, we'll just be focusing on `counting` stats. This is just a placeholder section to come back to later. 


### 2.3 Data Scraping 

#### 2.3.1 Basketball Reference Client Library
The [Basketball Reference Web Scraper](https://pypi.org/project/basketball-reference-scraper/) offers a simple and easy-to-use client for accessing data from the site. 

##### API
The following methods will be of interest now and for future features:
* [Get Roster](https://pypi.org/project/basketball-reference-scraper/)
* [Get Player Stats](https://pypi.org/project/basketball-reference-scraper/)
* [Get Game Logs](https://pypi.org/project/basketball-reference-scraper/)
* [Get Schedule](https://pypi.org/project/basketball-reference-scraper/)
* [Get Box Score](https://pypi.org/project/basketball-reference-scraper/)
* [Get Play by Play](https://pypi.org/project/basketball-reference-scraper/)
* [Get Shot Chart](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/API.md#shot-charts)
* [Get Team Misc.](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/API.md#shot-charts)
* [Get Roster Stats](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/API.md#shot-charts)

In the following sections, we'll describe how we intend to use each of the above features, and what data is of interest for each feature. 

#### 2.3.2 Team Data

#### 2.3.3 Player Data 
##### Table: dim_players_nationalities
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | 
| --- | --- | --- | --- | --- | 
| get_roster(team, season) | NATIONALITY | string | country | country (enum) |
| get_roster(team, season) | PLAYER | string | player_id | bigint

##### Table: dim_players
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | 
| --- | --- | --- | --- | --- | 
| get_roster(team, season) | PLAYER | string | first_name | string |
| get_roster(team, season) | PLAYER | string | last_name | string |
| get_roster(team, season) | BIRTH_DATE | date | birth_date | date |

##### Table: dim_positions
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | 
| --- | --- | --- | --- | --- | 
| get_roster(team, season) | POS | string | identifier | string

#### 2.3.4 Roster Data 
##### Table: dim_seasons
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | 
| --- | --- | --- | --- | --- | 
| get_roster(team, season) | SEASON_END_YEAR | string | start_year | year
| get_roster(team, season) | SEASON_END_YEAR | string | end_year | year

##### Table: dim_rosters
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | 
| --- | --- | --- | --- | --- | 
| get_roster(team, season) | TEAM | string | season_id | bigint
| get_roster(team, season) | SEASON_END_YEAR | string | season_id | bigint

##### Table: dim_rosters_players_bios
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | 
| --- | --- | --- | --- | --- | 
| get_roster(team, season) | PLAYER | string | player_id | bigint
| get_roster(team, season) | NUMBER | int | jersey_number | int |
| get_roster(team, season) | HEIGHT | int (inches) | height | float (meters) |
| get_roster(team, season) | WEIGHT | int (inches) | weight | float (grams) |
| get_roster(team, season) | POS | int (inches) | position_ids | array<int> |


#### 2.3.5 Game-by-Game Stats 

##### Table: fact_flat_stats_counting
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | Notes |
| --- | --- | --- | --- | --- | --- | 
| get_game_logs(name, start_date, end_date, playoffs=False) | GS | bool | starting | bool | |
| get_game_logs(name, start_date, end_date, playoffs=False) | MP | int | mp | int | |

##### Table: dim_stat_offense_scoring
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | Notes |
| --- | --- | --- | --- | --- | --- | 
| get_game_logs(name, start_date, end_date, playoffs=False) | FG|3PA|3P | int | fgm_2p | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | FGA|3PA|3P | int | fga_2p | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | 3PA | int | fgm_3p | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | 3P | int | fgm_3p | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | FT | int | ftm | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | FTM | int | ftm | int | |

##### Table: dim_stat_offense_non_scoring
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | Notes |
| --- | --- | --- | --- | --- | --- | 
| get_game_logs(name, start_date, end_date, playoffs=False) | ORB | int | orb | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | AST | int | ast | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | TOV | int | tov | int | |

##### Table: dim_stat_defense
| Ext. Endpoint | Ext. Field | Ext. Type | Int. Field | Int. Type | Notes |
| --- | --- | --- | --- | --- | --- | 
| get_game_logs(name, start_date, end_date, playoffs=False) | STL | int | stl | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | BLK | int | blk | int | |
| get_game_logs(name, start_date, end_date, playoffs=False) | DRB | int | drb | int | |

### 2.4 ETL Flow
#### 2.4.1 Long-Term Storage 

#### 2.4.2 Data Transformation 

#### 2.4.3 Data Load

💬 _Defines key stakeholders and their design-related interests._

➥ Identify stakeholder types (e.g., users, developers, operators), their main concerns (e.g., availability, maintainability, risk mitigation) and the viewpoints or design elements of this document that address them.

### 2.2 Selected Viewpoints
💬 _Defines the perspectives used to represent and reason about the system’s design._

➥ Identify and describe the viewpoints that were selected to address the stakeholders' concerns identified in Section 2.1. Each viewpoint addresses specific stakeholder concerns and utilizes visualization languages (e.g., UML, C4, sequence diagrams). Note which concerns each viewpoint addresses.

#### 2.2.1 Context
💬 _Defines the system as a black box, identifying its boundaries and its environment._

**Addresses:** System boundaries, environment actors (users, external systems) and offered services (use cases).
**Typical Languages:** UML Use Case Diagram, C4 Context Diagram.

#### 2.2.2 Composition
💬 _Describes how the system is recursively assembled from major constituent parts (subsystems, components, or modules), and how those are organized and relate to one another_

**Addresses:** Identify the major design elements; allocation of responsibilities, and localization of functionality; modularity (reuse, buy-vs-build) and integration.
**Typical Languages:** UML Component Diagram, Hierarchical Decomposition Diagram, UML Package (functional), Deployment (runtime) Diagram.

💡 Tips:
- Focus on how components fit together and where external, reused, or third-party components integrate.
- Consider organizing into subcategories for clarity: Functional (logical) decomposition and Runtime (physical) decomposition.

#### 2.2.3 Logical
💬 _Captures the static design structure of the system in terms of types and their implementation (class, interface) and their relationships._

**Addresses:** Development and reuse of appropriate abstractions and their implementations; encapsulation and dependencies among entities.
**Typical Languages:** UML Class Diagram, UML Object Diagram.

💡 Tips: 
- Focus on the static and stable abstractions that collaborate to fulfill system goals. 
- Complements Composition (assembly) by clarifying the abstractions that underlie it.

#### 2.2.4 Physical
💬 _Depicts the tangible system infrastructure._

**Addresses:** Hardware configuration, physical topology, and physical constraints.
**Typical Languages:** Hardware Block Diagram, Network Topology Diagram, Rack Layout, Cloud Infrastructure Diagram.

💡 Tips:
- Complements Deployment by showing the platform topology on which software is mapped.

#### 2.2.5 Structure
💬 _Documents internal organization of components and their parts, ports, and connectors_.

**Addresses:** Internal composition of complex entities; reusability of fine-grained components.
**Typical Languages:** UML composite structure diagram, UML class diagram, UML package diagram, C4 Container diagram.

💡 Tips: 
- Complements Composition by focusing on interfaces and connectors.

#### 2.2.6 Dependency
💬 _Shows how design elements interconnect and access each other, illustrating import, service, or build-time relationships._

**Addresses:** Integration needs and prioritization; coupling and dependencies; root cause and change impact analysis.
**Typical Languages:** UML Package Diagram, Dependency Graph, UML Component Diagram

💡 Tips: 
- Draw dependencies directionally (“uses”, “requires”, “provides”).

#### 2.2.7 Information
💬 _Models the persistent data structure, its relationships, and the mechanisms for access and management._

**Addresses:** Data structure and semantics; persistence; metadata; data integrity; data management and access schemes.
**Typical Languages:** Entity-Relationship Diagram, UML Class Diagram, Logical Data Model.

💡 Tips: 
- Use consistent naming with the Logical viewpoint to maintain type alignment.

#### 2.2.8 Interface
💬 _Specifies the externally visible interfaces among components, subsystems, or with external systems._

**Addresses:** Interoperability through contract definition; encapsulation, and integration risks.
**Typical Languages:** API specifications, IDLs, function/method signature, UML Component Diagram

#### 2.2.9 Interaction
💬 _Illustrates how entities collaborate at runtime via messages: who talks to whom, in what order, and under which conditions._

**Addresses:** Allocation of responsibilities; message sequencing, timing, and synchronization; error propagation; distributed components state transition logic and concurrency.
**Typical Languages:** UML Sequence Diagram, UML Collaboration Diagram, BPMN Process Flows.

💡 Tips:
- Provide representative “happy-path” and “failure-path” scenarios.
- If concurrency affects ordering, annotate lifelines/regions and reference the Concurrency viewpoint.

#### 2.2.10 Algorithm
💬 _Details the internal processing logic of an operation: steps, decisions, loops, and error handling, emphasizing critical or novel algorithms within the design._

**Addresses:** Computational complexity; time-space processing logic; performance, determinism, and reproducibility.
**Typical Languages:** Pseudocode, flowchart, Decision Table mathematical formulation.

💡 Tips: 
- Tie each algorithm to its owning class/component.
- Consider referencing Interface contracts to link invariants and pre/postconditions.
- Consider referencing Resource impacts if performance or space is critical.

#### 2.2.11 State Dynamics
💬 _Details how system or component states evolve in response to events or stimuli over time._

**Addresses:** Modes/states, transitions, events/triggers, guards, entry/exit effects, concurrency regions, synchronization.
**Typical Languages:** UML State Machine Diagram, State Transition Table, Automata, Petri Net.

💡 Tips: 
- Complements Interaction/Algorithm when behavior differs by state.

#### 2.2.12 Concurrency
💬 _Describes how the design handles parallelism, synchronization, and coordination among concurrent entities._

**Addresses:** Thread/process structure; synchronization and locking; concurrency control; event ordering; parallel execution and race conditions.
**Typical Languages:** UML Activity Diagram, UML Sequence and State Diagram, actor model.

💡 Tips:
- Complements other dynamic viewpoints when parallelism, synchronization, or ordering guarantees are first-class concerns that would clutter those views.

#### 2.2.13 Patterns
💬 _Identifies reusable design ideas and collaborations—design patterns, architectural styles, or framework templates—that guide or constrain the system’s structure and behavior._

**Addresses:** Reuse of proven solutions; consistency of architectural style; collaboration roles and connectors; template-based component structures.
**Typical Languages:** UML Composite Structure Diagram, UML Package/Class Diagram, Architecture Description Language.

💡 Tips: 
- Record which patterns are applied and where.

#### 2.2.14 Deployment
💬 _Describes how software entities are mapped onto the physical execution environment, what runs where and how nodes are connected_

**Addresses:** Component-to-node allocation; deployment topology; communication mechanisms; distribution, replication, and scaling; operational constraints.
**Typical Languages:** UML Deployment Diagram, Infrastructure-as-Code topology, Network Diagram, CI/CD pipeline diagrams.

💡 Tips: 
- Include environment tiers and deployment sequencing if relevant.

#### 2.2.15 Resources
💬 _Specifies use and management of shared or limited resources, such as memory, bandwidth, threads, or file handles._

**Addresses:** Resource utilization and allocation; contention and availability; performance bottlenecks; locks and priorities; resource management strategies. 
**Typical Languages:** UML Class Diagram (for resource entities), UML Real-Time Profile, UML Object Constraint Language (OCL), Resource Allocation Table.

💡 Tips: 
- Cross-reference with Concurrency (timing) and Deployment (placement) views for a full runtime picture..

## 3. Design Views
💬 _Documents the main architectural and design elements that define the system._

➥ Define design views to a level of detail sufficient to implement the system (prescriptive architecture) or to understand how to operate or maintain the existing product (descriptive architecture). Use unique identifiers, keep elements concise and modular, and include diagrams or links where applicable. Reference relevant design decisions from Section 4 that this view represents. Include applicable SRS requirement IDs that this element implements when available.

📃 Template:
```markdown
- ID: [NNN]-{title}
- Title: Short, descriptive name of the view.
- Viewpoint: The viewpoint of which this view is an instance.
- Representation: The design view representation per the viewpoint and language selected, e.g., natural language description or a diagram or a combination thereof.
- More Information: Additional context. Links to related artifacts.
```

💡 Tips:
- This section should contain enough information to implement the system (prescriptive architecture) or to understand how to operate or maintain the existing product (descriptive architecture).
- If available, include references to the SRS requirement IDs that the design view implements. This demonstrates how requirements are addressed by the design.
- Reference relevant design decisions from Section 4 that influenced or resulted from this design element.

## 4. Decisions
💬 Captures significant architectural or design decisions and their rationale.

➥ Document significant architectural decisions that have substantial long-term impact on the system's structure,
behavior, or quality attributes.

```markdown
- ID: [NNN]-{title}
- Title: short title, representative of solved problem and found solution.
- Context: Describe the context and problem statement.
- Options: Enumerate considered alternatives.
- Outcome: Chosen option: "{title of option 1}", because {justification}.
- More Information: Additional context. Links to related artifacts.
```

💡 Tips:
- Keep one decision per record.
- Consider adopting MADR (Markdown Architecture Decision Record) pattern directly to document decisions. 

## 5. Appendixes
💬 _Optional supporting material that aids understanding without being normative._

➥ Include glossaries, data dictionaries, models/diagrams, sample datasets, or change-impact analyses that support the main sections. Reference rather than duplicate content when possible.

💡 Tips:
- Keep appendixes organized and referenced from the main text.

