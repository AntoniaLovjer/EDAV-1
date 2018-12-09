# load the required packages
library(shiny)
require(shinydashboard)
library(ggplot2)
library(dplyr)


#Dashboard header carrying the title of the dashboard
header <- dashboardHeader(title = "NYC Marathon")

#Sidebar content of the dashboard
sidebar <- dashboardSidebar(
  sidebarMenu(
    menuItem("States", #icon = icon("bar-chart-o"),
             # Input directly under menuItem
             selectInput('state', 'Select a state', c(Choose='', state.name), selectize=FALSE)
          ),
    menuItem("Countries", #icon = icon("bar-chart-o"),
             # Input directly under menuItem
             selectInput('country', 'Select a state', c(Choose='', state.name), selectize=FALSE)
    )
    ))

frow1 <- fluidRow(
  box(
    width = 12,
    h2(textOutput("total")),
    h3(textOutput("totalsby"))
  )
)

frow2 <- fluidRow(
  box(title = "Distribution of Age By Gender",
      plotOutput("pyramidplot", height = "400px")
  ),
  box(title = "Ratio of woman and men by state",
  plotOutput("genderRatio", height = "400px")
  )
)

frow3 <- fluidRow(
  box(title = 'Official time density distribution',
      plotOutput("densityplot", height = "400px")
  ),
  box(
    #title = 'Official time density distribution',
     # plotOutput("pyramidplot", height = "400px")
  )
)


# combine the two fluid rows to make the body
body <- dashboardBody(frow1, frow2, frow3)

#completing the ui part with dashboardPage
ui <- dashboardPage(title = 'This is my Page title', header, sidebar, body, skin='red')
