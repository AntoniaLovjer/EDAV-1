
### Counting

count_finishers <- function(df, year, state, type){
  total <- df %>%
    filter(year == year & state_name == state & type == type) %>%
    nrow()
  return(total)
}


plot_genderRatio <- function(data, geo_type, geo_name, input_year){
  if (geo_type == 1) {
    p <- data %>%
      filter(type == 'R') %>%
      filter(state_name != 'NA') %>%
      group_by(state_name, year) %>%
      summarise(n = n(),
            num_male = sum(gender == 'M', na.rm=TRUE),
            num_female = sum(gender == 'F', na.rm=TRUE),
            ratio_gender = num_female / num_male,
            more_woman = ratio_gender > 1) %>%
      filter(year == input_year) %>%
      mutate(new_color = state_name == geo_name) %>%
      arrange(desc(ratio_gender)) %>%
      ggplot(aes(x = ratio_gender,
             y = fct_reorder2(state_name, year == input_year, ratio_gender, .desc=FALSE),
             color = new_color
      )) +
      geom_point(size=3) +
      scale_color_manual(values=c("lightblue", "midnightblue")) +
      geom_vline(xintercept=1, color='midnightblue', size=0.1) +
      theme(
        panel.grid.major.x=element_line(size=0.05),
        panel.background = element_blank(),
        panel.grid.major.y = element_line(linetype=3, color="lightgray", size=0.6),
        axis.text.y = element_text(size=rel(1)),
        axis.title.y = element_blank(),
        axis.title.x = element_blank(),
        legend.position="none")
  }
  else {
    p <- data %>%
      filter(type == 'R') %>%
      filter(!is.na(country)) %>%
      group_by(country, year) %>%
      summarise(n = n(),
                num_male = sum(gender == 'M', na.rm=TRUE),
                num_female = sum(gender == 'F', na.rm=TRUE),
                ratio_gender = num_female / num_male,
                more_woman = ratio_gender > 1) %>%
      filter(year == input_year & n > 5) %>%
      mutate(new_color = country == geo_name) %>%
      arrange(desc(ratio_gender)) %>%
      ggplot(aes(x = ratio_gender,
                 y = fct_reorder2(country, year == input_year, ratio_gender, .desc=FALSE),
                 color = new_color
      )) +
      geom_point(size=3) +
      scale_color_manual(values=c("lightblue", "midnightblue")) +
      geom_vline(xintercept=1, color='midnightblue', size=0.1) +
      theme(
        panel.grid.major.x=element_line(size=0.05),
        panel.background = element_blank(),
        panel.grid.major.y = element_line(linetype=3, color="lightgray", size=0.6),
        axis.text.y = element_text(size=rel(.8)),
        axis.title.y = element_blank(),
        axis.title.x = element_blank(),
        legend.position="none")
  }
  return(p)
}


density_plot_geo <- function(data, geo_type, geo_name, input_year){

  m_year <- data %>% filter(year == input_year & type == 'R')
  m_year$legend <-"general"

  if (geo_type == 0){
    m_geo_type <- m_year %>% filter(country == geo_name)
  }else {
    m_geo_type <- m_year %>% filter(state_name == geo_name)
  }

  m_geo_type$legend <- geo_name

  merged <- rbind(m_year, m_geo_type)

  ggplot(merged, aes(x= official_time, fill = legend)) +
    geom_density(alpha=.2) +
    #theme_bw() +
    xlab("Official Time") +
    ylab("Density Repartition") +
    #ggtitle("Official time density distribution") +
    theme(plot.title = element_text(hjust = 0.5, size=15),
          legend.position="bottom",
          panel.grid.major.x=element_line(size=0.05),
          panel.background = element_blank(),
          panel.grid.major.y = element_line(linetype=3, color="lightgray", size=0.6), axis.text.y = element_text(size=rel(1.3)),
          axis.title.y = element_blank(),
          axis.title.x = element_blank())
}



pyramid_plot <- function(data, geo_type, geo_name, input_year){
  #function(marathon, state, place_name, input_year){

  # change the name of gender column to have a capital letter for the legend
  names(data)[names(data) == 'gender'] <- 'Gender'

  # select the state/country and the year
  if (geo_type == 1){
    df <- data %>%
      filter(state_name == geo_name) %>%
      filter(year == input_year)
  } else {
    df <- data %>%
      filter(country == geo_name) %>%
      filter(year == input_year)
  }

  max_men <- df %>%
    filter(Gender == "M")

  x <- data.frame(table(df$age))
  max_value <- max(x$Freq)
  max_value <- plyr::round_any(max_value, 50, f = ceiling)

  # create the pyramid plot
  plot_return <- ggplot(df, aes(x = age, fill = Gender)) +
    geom_histogram(data = subset(df, Gender == "F"), binwidth =2) +
    geom_histogram(data = subset(df, Gender == "M"), binwidth =2, aes(y=..count..*(-1))) +
    scale_y_continuous(breaks = seq(-max_value, max_value, 50),
                       labels=abs(seq(-max_value, max_value, 50))) +
    scale_fill_manual(values = c("darkorange1",
                                 "royalblue2")) +
    coord_flip() +
   # theme_bw() +
   # ggtitle('Distribution of Age By Gender') +
    ylab("Count") +
    xlab("Age") +
    theme(plot.title = element_text(hjust = 0.5, size = 15),
          axis.title=element_text(size=14),
          panel.background = element_blank())

  return(plot_return)
}

