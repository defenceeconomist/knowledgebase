from shiny import App, Inputs, Outputs, Session, module, render, ui, reactive
from pathlib import Path
from ragui.about import about_ui

import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from openai import OpenAI

import asyncio
from typing import AsyncGenerator

load_dotenv()
openaiclient = OpenAI()

# Connect to Vector Database
chromaclient = chromadb.PersistentClient(path="chromadb")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-ada-002"
                )

collection = chromaclient.get_collection(name="defecon-kb", embedding_function=openai_ef)



@module.server
def rag_server(input: Inputs, output: Outputs, session: Session, config):
  
    logged_in: reactive.Value(False)
    chat_history_md: reactive.Value[str] = reactive.Value("")
    chat_string: reactive.Value[str] = reactive.Value("")
    system_prompt: reactiveValue[str] = reactive.Value(config["SYSTEM_PROMPT"])
    temperature: reactiveValue[str] = reactive.Value(config["TEMPERATURE"])
    model: reactiveValue[str] = reactive.Value(config["DEFAULT_MODEL"])
    last_answer: reactive.Value[str] = reactive.Value("")
    history = reactive.Value([])
    
    
    # Show a modal when the about is clicked.
    @reactive.Effect
    @reactive.event(input.info, ignore_init=True, ignore_none=True)
    def _():
        return ui.modal_show(
            ui.modal(
                about_ui(),
                size = "l"
                )
            )
            
    # RAG -----
    @reactive.Calc
    def retrieve():
        results = collection.query(
            query_texts = [input.query()],
            n_results = 10
            ) 
        print(results)
        return results
    

    @reactive.Calc
    def augment():
        context = '"""'.join(retrieve()["documents"][0])
        return context
      
    @reactive.Effect
    @reactive.event(input.ask)
    def _():
        # Load History
        if chat_history_md() == "":
            chat_history_md.set(f"__You__:<br>{input.query()}<br><br>__GPT__:<br>") 
        else:  chat_history_md.set(chat_history_md() + last_answer() + f"\n\n__You__:<br>{input.query()}<br><br>__GPT__:<br>")
 
        # Stream Chat
        chat_string.set("")
        asyncio.Task(
            set_val_streaming(
                chat_string, do_query_streaming(input.query(), chat_string), session
            )
        )
    
    async def do_query_streaming(
        message: str, v: reactive.Value[str]
    ) -> AsyncGenerator[str, None]:
        
        messages = [
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": "Question: " + message + 
             "=======" + 
             " Context: " + augment() + 
             "=======" +
             "\n Answer:"}
            ]
        print(messages)
        for resp in openaiclient.chat.completions.create(
            model=model(),
            messages = messages,
            temperature= temperature(),
            stream=True,
        ):
            if resp.choices[0].finish_reason == "stop":
                last_answer.set(chat_string())
                messages.append({"role": "assistant", "content": last_answer()})
                history.set(history() + messages) 
                yield ""
                
            if resp.choices[0].delta.content is not None:
                yield resp.choices[0].delta.content 
    
    async def set_val_streaming(
            v: reactive.Value[str], stream: AsyncGenerator[str, None], session: Session
        ):
            async for tok in stream:
                v.set(v.get() + tok)
                await reactive.flush()
    
    
    @output
    @render.ui
    def response():
        return ui.TagList(
            ui.tags.script(
            "el = document.getElementById('kb-response').parentNode;" +
            "el.scrollTo(0, el.scrollHeight)"
            ), 
            ui.markdown(chat_history_md() + chat_string())
            )
            
    
