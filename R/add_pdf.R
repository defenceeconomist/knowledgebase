library(shiny)
library(miniUI)

source("R/llama-parse.R")

add_pdf <- function(llama_parse_api = get_env_var("LLAMA_CLOUD_API_KEY")) {
  
  ui <- miniPage(
    gadgetTitleBar("Upload File to Vector Database"),
    miniContentPanel(
      fileInput(
        inputId = "upload",
        label = "Upload PDF",
        multiple = FALSE,
        accept = "application/pdf"
      )
    )
  )
  
  server <- function(input, output, session) {
    # Define reactive expressions, outputs, etc.
    observeEvent(input$upload,{
      
      uri <- input$upload$datapath
  
      results <- parse(uri, llama_parse_api)
      
      # Check Status
      
      # Download Markdown
      
      # Chunk
      
      # Add to Vector Database
      
    },ignoreInit = TRUE, ignoreNULL = TRUE)
    
    # When the Done button is clicked, return a value
    observeEvent(input$done, {
      returnValue <- ...
      stopApp(returnValue)
    })
  }
  
  runGadget(ui, server)
}

