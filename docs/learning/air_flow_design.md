
# Hooks 
## Seasons 
### GetRegularSeasonScheduleRaw(season_start_year) : string (storage_path)
#### Args 
* season_start_year: int - integer representing the year a season will start 

#### Throws 
* InvalidInputError: 
  * if season_start_year is not a year NBA games were played 
  * if season_start_year is in the future and the schedule isn't available 

#### Returns 
* a string representing the path to the unprocessed file 

#### Components 
* ScheduleProvider 
  - class: BasketballReferenceClient::SeasonClient 
  - method: get_season_schedule
* FileProcessor
  - method: get_csv_from_df
* StorageProvider
  - method: upload_file

### ProcessRegularSeasonSchedule(raw_file_path) : string (storage_path)
#### Args 
* raw_file_path : string - path to a raw file produced from `GetRegularSeasonScheduleRaw`

#### Throws 
* FileDoesNotExist:
  - if raw_file_path is not found for the current file provider
* InvalidFileType: 
  - if raw_file_path exists but is not able to be processed to the expected format

#### Returns 
* a string representing the path to the processed version of the raw file 

#### Components 
* ScheduleMapper 
  - class: BasketballReferenceMapper::SheduleMapper 
  - method: get_schedule_from_file
* FileProcessor
  - method: get_df_from_file
* StorageProvider
  - method: download_file, upload_file

### WriteRegularSeasonSchedule(processed_file_path) : void 
#### Args 
* processed_file_path : string - path to a processed file produced from `ProcessRegularSeasonSchedule`

#### Throws 
* FileDoesNotExist:
  - if raw_file_path is not found for the current file provider
* InvalidFileType: 
  - if raw_file_path exists but is not able to be processed to the expected format

#### Returns 
* void 

#### Components 
* ScheduleWriter 
  - class: TODO
  - method: TODO
* FileProcessor
  - method: get_df_from_file
* StorageProvider
  - method: download_file

### ValidateRegularSeasonScheduleWrite
TODO 

# Jobs 
## Download Regular Season Schedule 
  * Scheduling: 
    - only do once a year 
    - stop checking the jobs once it's complete 
  * Logic/Steps
    1. GetRegularSeasonScheduleRaw
    2. ProcessRegularSeasonSchedule
    3. WriteRegularSeasonSchedule
    4. ValidateRegularSeasonScheduleWrite