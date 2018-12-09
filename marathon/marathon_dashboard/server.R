library(tidyverse)

# create the server functions for the dashboard
server <- function(input, output) {

  # Read Data
  marathon <- read_csv('../data/clean/marathon.csv')
  source('aux_functions.R')
  # Read inputs
  state <- reactive({input$state})

  output$total <- renderText({
    total <- marathon %>%
      filter(year == 2018 & state_name == state()) %>%
      nrow()
    paste(total, " Finishers in 2018")
  })

  output$totalsby <- renderText({
    num_runners <- marathon %>%
      filter(year == 2018 & state_name == state() & type == 'R') %>%
      nrow()
    num_wheelchairs <- marathon %>%
      filter(year == 2018 & state_name == state() & type == 'W') %>%
      nrow()
    num_handcycles <- marathon %>%
      filter(year == 2018 & state_name == state() & type == 'H') %>%
      nrow()

    paste(
      #"Total finishers: ", total,
          num_runners, " Runners   -   ",
          num_wheelchairs, " Wheelchairs   -   ",
          num_handcycles, " Handcylces")
  })

  #creating  content
  output$genderRatio <- renderPlot({
    plot_genderRatio(marathon, 1, state(), 2018)
  })

  output$densityplot <- renderPlot({
    density_plot_geo(marathon, 1, state(), 2018)
  })

  output$pyramidplot <- renderPlot({
    pyramid_plot(marathon, 1, state(), 2018)
  })

}


