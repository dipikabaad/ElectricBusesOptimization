library(timevis)


function(input, output, session) {
  output$timelineGroups <- renderTimevis({
    csvFile = subset(csvFile, Month == input$month)
    csvFile = subset(csvFile, Route == input$route)
    colorVector = ifelse(csvFile$type == "charging", "background-color: orange;", "background-color:lightgreen;")
    dataGroups4 = data.frame(
      content = ifelse(csvFile$type == "charging", c("C"), c("Running")),
      start = c(as.character(csvFile$start)),
      end = c(as.character(csvFile$end)),
      group = c(as.character(csvFile$Bus)),
      style = colorVector
    )
    groups4 = data.frame(
      id = c(unique(as.character(csvFile$Bus))),
      content = c(paste("Bus ", unique(as.character(csvFile$Bus))))
    )
    timevis(data = dataGroups4, groups = groups4)
  })
  output$table = renderTable({
    csvPrices = subset(csvPrices, Month == input$month)
    csvPrices = subset(csvPrices, Route == input$route)
    csvPrices
  })
  output$timelineCharging <- renderTimevis({
    csvFile1 = subset(csvFile1, Month == input$month1)
    #csvFile1 = subset(csvFile1, Route == input$route1)
    colorVector = ifelse(csvFile1$type == "charging", "background-color: aquamarine;", NA)
    dataGroups5 = data.frame(
      content = c(paste("Bus ",as.character(csvFile1$Bus))),
      start = c(as.character(csvFile1$start)),
      end = c(as.character(csvFile1$end)),
      group = c(as.character(csvFile1$Route)),
      style = colorVector
    )
    groups5 = data.frame(
      id = c(unique(as.character(csvFile1$Route))),
      content = c(paste("Route ", unique(as.character(csvFile1$Route))))
    )
    timevis(data = dataGroups5, groups = groups5)
  })
  observeEvent(input$jumpToDetails, {
    updateNavlistPanel(session, "mainnav", selected = "details")
  })
    
}
