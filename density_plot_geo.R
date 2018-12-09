density_plot_geo <- function(data, geo_type, geo_name, input_year){
  
  m_year <- data %>% filter(year == input_year) 
  m_year$legend <-"general"
  
  if (geo_type == 0){
    m_geo_type <- m_year %>% filter(country == geo_name)
  }else {
    m_geo_type <- m_year %>% filter(state == geo_name)
  }
  
  m_geo_type$legend <- geo_name
  
  merged <- rbind(m_year, m_geo_type)
  5
  ggplot(merged, aes(x= official_time, fill = legend)) + 
    geom_density(alpha=.2) + 
    theme_bw() +
    xlab("Official Time") + 
    ylab("Density Repartition") +
    ggtitle("Official time density distribution") +
    theme(plot.title = element_text(hjust = 0.5, size=15)) 
}