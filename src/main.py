import sys
from chatbot import PresightChatBot
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description='Chatbot script with arguments')
    parser.add_argument('--top_n', type=int, default=3, help='Number of top references (default is 3)')
    parser.add_argument('--history', action='store_true', help='Include chat history in the response')
    parser.add_argument('--api_key')
    args = parser.parse_args()

    chatbot = PresightChatBot(args.api_key)

    while True:
        query = input("Ask a question (type 'exit' to end): ")

        if query.lower() == 'exit':
            break

        start_time = time.time()
        answers = chatbot.generate_answer(query, top_n=args.top_n, history = args.history)
        elapsed_time = time.time() - start_time

        print("Chatbot's Answer:")
        print(answers)
        print("Response Time: {:.2f} seconds\n".format(elapsed_time))
        print("----------------------")

if __name__ == "__main__":
    main()
