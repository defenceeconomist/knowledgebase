# Knowledge Base

This is a retrieval augmented generation application to query a custom knowledge base. 

It uses OpenAI for text embeddings and generation. 

It uses ChromaDB for Vector Storage and retrieval.

It is deployed to ShinyApps.io following the set up guidance here

https://docs.posit.co/shinyapps.io/guide/getting_started/#working-with-shiny-for-python

And thereafter using this command:
rsconnect deploy shiny . --name defenceeconomist --title knowledgebase