
semantic_split <- function(x){
  sts <- reticulate::import("semantic_text_splitter")
  splitter <- sts$TextSplitter$from_tiktoken_model(model = "gpt-3.5-turbo", capacity = 400L)
  sapply(x, function(y){splitter$chunks(y)})
}