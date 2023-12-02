import numpy as np
from openai import OpenAI
import tiktoken
import pandas as pd
import ast
import faiss

class PresightChatBot:
    def __init__(self, api_key ,dataframe_path="./data/output_with_embeddings.csv"):
        # Load data and initialize OpenAI API and models
        self.df = pd.read_csv(dataframe_path)
        self.df['embedding'] = self.df['embedding'].apply(ast.literal_eval)
        self.openai = OpenAI(api_key=api_key)
        self.EMBEDDING_MODEL = "text-embedding-ada-002"
        self.GPT_MODEL = "gpt-3.5-turbo"
        self.token_budget = 2000

        # Create the Faiss index during class initialization
        self.index = faiss.IndexFlatIP(len(self.df['embedding'][0]))
        embeddings = np.array(self.df['embedding'].tolist(), dtype=np.float32)
        self.index.add(embeddings)

        # Initialize the cache
        self.cache = {}

        #history chat
        self.chat_history = [
            {"role": "system", "content": "You answer questions"}]

    def relatedness_fn(self, x, k=3):
        x = np.array(x, dtype=np.float32)
        # Use Faiss to find the k-nearest neighbors
        D, I = self.index.search(x.reshape(1, -1), k)
        return D[0], I[0]

    def strings_ranked_by_relatedness(self, query, top_n=1):
        # Check if the result is in the cache
        if query in self.cache:
            return self.cache[query]

        # Get embeddings for the query and find related strings
        query_embedding_response = self.openai.embeddings.create(
            model=self.EMBEDDING_MODEL,
            input=query
        )
        query_embedding = query_embedding_response.data[0].embedding
        query_embedding_array = np.array(query_embedding)

        D, I = self.relatedness_fn(query_embedding_array, top_n)
        result = (self.df['combined'].iloc[I].to_list(), D)

        # Update the cache
        self.cache[query] = result

        return result

    def num_tokens(self, text, model=None):
        """Return the number of tokens in a string."""
        if not model:
            model = self.GPT_MODEL
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))

    def query_message(self, query, top_n=3, model=None):
        # Build a message to be used as input for openai
        if not model:
            model = self.GPT_MODEL
        strings, relatednesses = self.strings_ranked_by_relatedness(query, top_n)
        introduction = """You are the Presight chatbot, and you need to read and understand the content below, then provide an answer to the customer.     
        If the customer greets or talks about unrelated matters, simply respond in a conventional manner with the customer.
        If you don't know the answer, please respond with a request to contact via email at presight@presight.io."""
        question = f"\n\nQuestion: {query}"
        
        message = introduction
        for string in strings:
            next_article = f'\n"""\n{string}\n"""'
            if (
                self.num_tokens(message + next_article + question, model=model)
                > self.token_budget
            ):
                break
            else:
                message += next_article
        #user 
        user = {"role": "user", "content": message + question} 
        # Update the chat history
        self.chat_history.append({"role": "user", "content": question})

        return message + question

    def generate_answer(self, query, top_n=3, history = True, model=None):
        # Check if the result is in the cache
        if query in self.cache:
            print("Answer retrieved from cache.")
            return self.cache[query][0][0]  # Return the top-ranked string from the cache

        # Generate a response using openai
        if not model:
            model = self.GPT_MODEL

        message = self.query_message(query, top_n, model=model)

        #If using chat history
        if history and len(self.chat_history) > 2:
            messages = self.chat_history

        else:
            messages = [
                {"role": "system", "content": "You answer questions"},
                {"role": "user", "content": message},
            ]

        # Call API
        response = self.openai.chat.completions.create(
            model=self.GPT_MODEL,
            messages=messages
        )
        response_message = response.choices[0].message.content

        # Update the chat history
        if history:
            #assistant
            assistant = {"role": "assistant", "content": response_message}
            self.chat_history.append(assistant)
        
        # Update the cache with the response
        self.cache[query] = ([response_message], 0.0)
        
        return response_message
