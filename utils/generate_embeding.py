import pandas as pd
from openai import OpenAI
import argparse
from markdown_2_df import markdown_to_dataframe

def get_embedding(text: str, model: str, openai: OpenAI):
    """
    Get the embedding of a text using the specified OpenAI model.

    Args:
        text (str): Input text for which embedding is required.
        model (str): OpenAI model name.
        openai (OpenAI): OpenAI client instance.
    Returns:
        list: Embedding of the input text.
    """
    result = openai.embeddings.create(
        model=model,
        input=text
    )
    return result.data[0].embedding

if __name__ == "__main__":
    # Use argparse to parse command line arguments
    parser = argparse.ArgumentParser(description="Add embeddings to a dataset")
    parser.add_argument("--api_key", default= "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" ,help="OpenAI API key")
    parser.add_argument("--input_datapath", default="data/output.csv", help="Path input dataset CSV")
    parser.add_argument("--output_datapath", default="data/output_with_embeddings.csv", help="Path to output dataset CSV file with embeddings")
    args = parser.parse_args()

    # Initialize OpenAI client
    client = OpenAI(api_key=args.api_key)

    # Models Config
    EMBEDDING_MODEL = "text-embedding-ada-002"
    GPT_MODEL = "gpt-3.5-turbo"

    # Convert the Markdown to a DataFrame.
    with open("./data/output.md", "r") as f:
        markdown_text = f.read()
    df = markdown_to_dataframe(markdown_text)
    df.to_csv('./data/output.csv', index=False)

    # Load dataset
    df = pd.read_csv(args.input_datapath)

    # Apply get_embedding to each row in DataFrame and add a new 'embedding' column
    df['embedding'] = df['combined'].apply(lambda x: get_embedding(x, EMBEDDING_MODEL, client))

    # Save the DataFrame with embeddings to a new CSV file
    df.to_csv(args.output_datapath, index=False)

#Usage
#python utils/generate_embeding.py 