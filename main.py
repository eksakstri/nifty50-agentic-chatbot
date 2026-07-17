from graph import graph

class Nifty50Chatbot:

    def __init__(self):

        self.graph = graph

    # --------------------------------------------

    def ask(self, query):

        state = {

            "query": query,

            "route": None,

            "router_confidence": 0,

            "retrieval_source": None,

            "retrieved_context": None,

            "retrieval_confidence": 0,

            "answer": None,

        }

        result = self.graph.invoke(state)

        return result["answer"]


# ======================================================

def chat():

    bot = Nifty50Chatbot()

    print("=" * 70)
    print("NIFTY50 Financial Chatbot")
    print("Type 'exit' to quit.")
    print("=" * 70)

    while True:

        query = input("\nYou : ")

        if query.lower() in {

            "exit",
            "quit",
            "q"

        }:

            break

        try:

            answer = bot.ask(query)

            print()

            print("Bot :")

            print(answer)

        except Exception as e:

            print()

            print("Error:")

            print(e)


# ======================================================

if __name__ == "__main__":

    chat()