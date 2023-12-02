import pandas as pd

def markdown_to_dataframe(markdown):
  """Converts Markdown to a Pandas DataFrame with two columns: Summary and Text.

  Args:
    markdown: A string containing Markdown text.

  Returns:
    A Pandas DataFrame with two columns: Summary and Text.
  """

  # Split the Markdown into lines.
  lines = markdown.splitlines()

  # Create a list to store the Summary and Text columns.
  summary_column = []
  text_column = []
  text = ''
  # Iterate over the lines and extract the Heading and Text for each line.
  for line in lines:
    # If the line starts with a hash (#), it is a heading.
    if line.startswith('#') and len(line) > 1 and line[1] != '#':
      # Extract the Heading text from the heading.
      summary = line[1:].strip()
      # Add the Heading text to the Heading column.
      text_column.append(text)
      text = ''
      summary_column.append(summary)
      # Add an empty string to the Text column for the heading. 
    else:
      # The line is not a heading, so it is Text.
      text = text + line.strip()
  # Create a Pandas DataFrame from the Summary and Text columns.
  text_column.append(text)
  df = pd.DataFrame({'Heading': summary_column, 'Text': text_column[1:]})

  df['Text'] = df['Text'].str.strip().fillna('')
  df["combined"] = (
    "Heading: " + df.Heading.str.strip() + "; Text: " + df.Text
    )
  print(df.columns)
  return df

