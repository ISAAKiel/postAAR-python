#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#

if (!require("pacman")) install.packages("pacman")
pacman::p_load(shiny, ggplot2, geometry)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("postAAR rectangle estimation"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            sliderInput("p1x",
                        "p1 x-value:",
                        min = 0,
                        max = .25,
                        value = .05),
            sliderInput("p1y",
                        "p1 y-value:",
                        min = .7,
                        max = 1,
                        value = .9),
            sliderInput("p2x",
                        "p2 x-value:",
                        min = .75,
                        max = 1,
                        value = .8)
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$distPlot <- renderPlot({
      x<- c(0, input$p2x, 1, input$p1x)
      y<-c(0, 0, 1, input$p1y)
      a1 <- round(geometry::polyarea(x,y),2)

      ggplot() +
        geom_rect(aes(xmin = 0, xmax = 1, ymin = 0, ymax = 1), fill ="grey") +
        geom_polygon(aes(x, y), fill ="red") +
        geom_text(aes(x[c(2, 4)], y[c(2,4)], label = c("p2", "p1")), size=10) +
        geom_text(aes(x=0.5, y=0.5, label = paste("a = ", a1)), size = 15) +
        theme(aspect.ratio=1)
      })
}

# Run the application 
shinyApp(ui = ui, server = server)
