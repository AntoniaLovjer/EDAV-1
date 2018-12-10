# load the required packages
library(shiny)
library(shinydashboard)
library(shinyWidgets)
library(ggplot2)
library(dplyr)
library(tidyverse)


#Dashboard header carrying the title of the dashboard
header <- dashboardHeader(title = "NYC Marathon")

marathon <- read_csv('marathon.csv')
countries <- marathon %>% select(country) %>%
              group_by(country) %>%
              mutate(n = n()) %>% ungroup() %>%
        filter(!is.na(country) & n > 10) %>%
        distinct() %>%
        arrange(country) %>%
        flatten_chr()

#Sidebar content of the dashboard
sidebar <- dashboardSidebar(
  width = 200,
  sidebarMenu(

    radioGroupButtons(inputId = "input_year",
                         label = "Select a Year",
                         choices = c(2015, 2016, 2017, 2018),
                         size = 'sm',
                         selected = 2018, status='primary',
                         justified = TRUE),
    radioGroupButtons(inputId = 'loc',
                      label = 'By',
                      choices = c('State', 'Country'),
                      justified = TRUE),
    conditionalPanel(
      pickerInput(inputId = "state",
                label = "States",
                choices = state.name,
                selected = 'New York',
                options = list(`live-search` = TRUE)),
      condition = "input.loc == 'State'"),
    conditionalPanel(
    pickerInput(inputId = "country",
                label = "Countries",
                choices = countries,
                selected = 'USA',
                options = list(`live-search` = TRUE)),
    condition = "input.loc == 'Country'")
    )
    )



frow1 <- fluidRow(
  box(
    width = 18,
    h1(textOutput("cityyear")),
    h2(textOutput("total"))
  )
)

frow2 <- fluidRow(
      valueBoxOutput("runners"),
      valueBoxOutput("wheelchairs"),
      valueBoxOutput("handcycles")

)

frow3 <- fluidRow(

      box(title = "Distribution of Age By Gender",
        plotOutput("pyramidplot", height = "450px")),
      box(title = "Proportion of woman and men by location",
        plotOutput("genderRatio", height = "450px"))
)

frow4 <- fluidRow(
  box(title = 'Official time density distribution',
      plotOutput("densityplot", height = "450px")
  ),
  box(
    title = 'Performance between athletes widens as race advances',
    plotOutput("boxplot", height = "450px")
  )
)

# combine the two fluid rows to make the body
body <- dashboardBody(frow1, frow2, frow3, frow4)

#completing the ui part with dashboardPage
ui <- dashboardPage(title = 'This is my Page title', header, sidebar, body, skin='black')
