library(timevis)
library(shinythemes)


fluidPage(
  title = "DeltaX", theme = "flatly",
  tags$head(
    tags$link(href = "style.css", rel = "stylesheet")
  ),
  div(id = "header",
    div(id = "title",
      "DeltaX"
    ),
    div(id = "subtitle","Timeline visualizations of optimal bus schedules")
  ),
  tabsetPanel(
    id = "mainnav",
    tabPanel(
      div(icon("calendar"), "Schedule"),
      selectInput("month", label = p("Month"), selected = csvFile$Month[1], choices = c(levels(unique(csvFile$Month)))),
      selectInput("route", label = p("Route"), choices = c(unique(csvFile$Route))),
      timevisOutput("timelineGroups")
        ), 
    tabPanel(div(icon("bus"), "Fleet Info"),
             tableOutput("table")
    ),
    tabPanel(
               div(icon("battery-quarter"), "Charging"),
               selectInput("month1", label = p("Month1"), selected = csvFile1$Month[1], choices = c(levels(unique(csvFile1$Month)))),
               timevisOutput("timelineCharging")
               
               #selectInput("route1", label = p("Route1"), choices = c(unique(csvFile1$Route)))
          )
  )
)
