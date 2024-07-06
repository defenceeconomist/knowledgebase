
get_env_var <- function(x = "LLAMA_CLOUD_API_KEY", file = ".env"){
  dot_env <- readLines(".env")
  dot_env[stringr::str_detect(dot_env, x)] |>
    stringr::str_remove(paste0(x,"="))
}


parse <- function(file = "data-raw/tmp.pdf", api_key = get_env_var("LLAMA_CLOUD_API_KEY")){
  
  f <- httr::upload_file(file, type = "application/pdf")
  
  req <- httr::POST(
    url = 'https://api.cloud.llamaindex.ai/api/parsing/upload',
    httr::add_headers(
      accept = "application/json",
      `Content-Type`= "multipart/form-data",
      Authorization = glue::glue("Bearer {api_key}")
    ),
    body = list(file = f),
    httr::verbose()
  )
  
  httr::content(req)

}

check_status <- function(job_id =  "e778beda-74bd-4f55-a700-beafed677556", 
                         api_key = get_env_var("LLAMA_CLOUD_API_KEY")){
  
  req <- httr::GET(
    url = glue::glue('https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}'),
    httr::add_headers(
      accept = "application/json",
      Authorization = glue::glue("Bearer {api_key}")
    )
  )
  
  httr::content(req)

}

get_markdown <- function(job_id =  "e778beda-74bd-4f55-a700-beafed677556", 
                         api_key = "llx-XTMPRKlsgx8whmOpf4nKf5m1X4EgNnAvJprNjHfoXydNiSLY"){
  
  req <- httr::GET(
    url = glue::glue('https://api.cloud.llamaindex.ai/api/parsing/job/{job_id}/result/markdown'),
    httr::add_headers(
      accept = "application/json",
      Authorization = glue::glue("Bearer {api_key}")
    )
  )
  
  results <- httr::content(req)
  results
}

results$job_metadata


semantic_split <- function(x){
  sts <- reticulate::import("semantic_text_splitter")
  splitter <- sts$TextSplitter$from_tiktoken_model(model = "gpt-3.5-turbo", capacity = 400L)
  sapply(x, function(y){splitter$chunks(y)})
}
# 
# df <- dplyr::tibble(text = results$markdown |>
#                 stringr::str_split("\n") |>
#                 unlist()) |>
#   dplyr::mutate(page = cumsum(stringr::str_detect(text, "^---$"))) |>
#   dplyr::filter(text != "---") |>
#   dplyr::mutate(heading = cumsum(stringr::str_detect(text, "^#\\s"))) |>
#   dplyr::group_by(heading) |>
#   dplyr::summarise(text = paste(text, collapse = "\n"),
#                    page_start = min(page), 
#                    page_end = max(page)) |>
#   dplyr::mutate(chunks = semantic_split(text)) |>
#   tidyr::unnest(chunks) |>
#   dplyr::group_by(heading) |>
#   dplyr::mutate(chunk = 1L:dplyr::n()) |>
#   dplyr::ungroup()
# 
# 
# 
# df
