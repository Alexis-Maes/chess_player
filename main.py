from client import client

rule_library_id = "0199437a-bb76-7211-890a-f0672c089d6a"
knowledge_library_id = "0199437a-bc56-77ad-afde-dcc0f38414ff"

tools = [
    {"type": "document_library", "library_ids": [rule_library_id, knowledge_library_id]}
]


def create_agent(tools):
    return client.beta.agents.create(
        model="mistral-medium-latest",
        name="chess_player",
        description="this agent plays chess",
        instructions="Use the libraries to understand the rules before playing and define your strategie",
        tools=[tools],
    )
