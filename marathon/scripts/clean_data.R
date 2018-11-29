library(tidyverse)
library(maps)


get_state_name <- function(abb){
  index <- match(abb, state.abb)
  return(state.name[index])
}


add_location <- function(marathon_df){
  data(world.cities)
  
  #get non repeated cities
  repeated_cities <- world.cities %>% 
    group_by(name) %>% 
    summarise(n = n()) %>% filter(n>1) %>% 
    select(name) %>% flatten_chr()
  cities <- world.cities %>% 
    filter(! name %in% repeated_cities) %>% 
    rename(city = name) %>% 
    select(city, country.etc, lat, long)
  
  # Split columns (city/state, gender/age) and do basic cleaning on city names
  marathon_df <- marathon_df %>% 
    separate(place, c('city', 'state'), sep=",") %>% 
    mutate(state = toupper(trimws(state)),
           state_name = get_state_name(state),
           city = gsub("[.]","", city),
           city = gsub("District","", city),
           city = trimws(city))
  # Join
  marathon_df <- marathon_df %>% 
    left_join(cities, by='city')
  # Fix city
  marathon_df <- marathon_df %>% 
    mutate(country=ifelse(state %in% state.abb, 'USA', country.etc)) %>% 
    select(-country.etc)
  return(marathon_df)
}


clean_marathon_data <- function(input_path='../data/raw',
                                output_path='../data/clean',
                                year = 2018){
  
  input_filename <- paste0(input_path, '/marathon_', year, '.csv')
  output_filename <- paste0(output_path, '/marathon_', year, '.csv')
  # Read Data
  marathon <- read_csv(input_filename)
  
  # Check inconsistencies 
  # Sanity Check
  marathon_clean <- marathon %>% 
    filter(is.na(splint_5k)  | is.na(splint_10k) | splint_5k <= splint_10k ) %>% 
    filter(is.na(splint_10k) | is.na(splint_15k) | splint_10k <= splint_15k ) %>% 
    filter(is.na(splint_15k) | is.na(splint_20k) | splint_15k <= splint_20k ) %>% 
    filter(is.na(splint_20k) | is.na(splint_25k) | splint_20k <= splint_25k ) %>% 
    filter(is.na(splint_25k) | is.na(splint_30k) | splint_25k <= splint_30k ) %>% 
    filter(is.na(splint_30k) | is.na(splint_35k) | splint_30k <= splint_35k ) %>% 
    filter(is.na(splint_35k) | is.na(splint_40k) | splint_35k <= splint_40k ) %>% 
    filter(is.na(splint_half) | is.na(splint_20k) | splint_20k <= splint_half) %>% 
    filter(is.na(splint_half) | is.na(splint_25k) | splint_half <= splint_25k)
  
  # place overall
  if (year == 2018){
    runners <- 52697
    wheelchairs <- 56
    handcycles <- 52
  } else if (year == 2017){
    runners <- 50641
    wheelchairs <- 51
    handcycles <- 69
  } else if (year == 2016){
    runners <- 51275
    wheelchairs <- 49
    handcycles <- 68
  } else {
    runners <- 49461
    wheelchairs <- 48
    handcycles <- 78
  }
  
  # Add type of participant
  marathon_clean <- marathon_clean %>% 
    separate(gender_age, c('gender','age' ), sep=1) %>% 
    mutate(type = ifelse(place_overall_of == runners | gun_place > max(wheelchairs, handcycles), 'R',
                         ifelse(place_overall_of == wheelchairs, 'W', 'H')),
           age = as.numeric(age),
           team = ifelse(team == '0', NA, team),
           year = year)
     
  marathon_clean <- add_location(marathon_clean)
  write_csv(marathon_clean, output_filename)
  #return(marathon_clean)
}

clean_marathon_data(year=2018)
clean_marathon_data(year=2017)
clean_marathon_data(year=2016)
clean_marathon_data(year=2015)

