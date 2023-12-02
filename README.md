# Question-3-Chatbot-Development

This repository contains a sample solution for Question-3-Chatbot-Development.

## Quickstart

1. **Prepare Environment:**
    ```bash
    # Install Python 3.9
    pip install -r requirements.txt
    ```

2. **Crawling Data:**
    ```bash
    python utils/crawl_data.py https://www.presight.io/privacy-policy.html data/output.md
    ```

3. **Preprocess and Structure Data into a Searchable Index:**
    ```bash
    python utils/generate_embedding.py 
    ```

4. **Using the Chatbot:**
    ```bash
    python src/main.py --top_n 3 --history

    --top_n: Number of top references (default is 3). The larger the number, 
    the better the result, but it runs slower and incurs more cost.
    --history: Save chat history, maintain historical context.

    # Example 1
    "Give me information on Types of Data Collected" 
    
    # Answer 1
    The types of data collected by our service include personally identifiable information 
    and usage data.Personally identifiable information may include email address, first and 
    last name, phone number, address, state, province, zip/postal code, city, cookies, 
    and usage data. Usage data refers to information such as your computer's internet
    protocol (IP) address, browser type and version, the pages visited on our service,
    the time and date of your visit, the time spent on those pages, and unique device identifiers.
    ```
