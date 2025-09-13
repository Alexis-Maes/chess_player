from client import client


def create_library(name: str, description: str):
    return client.beta.libraries.create(name=name, description=description)


if __name__ == "__main__":
    rule_library = create_library(
        name="rule_library",
        description="This library contains all the rules about chess",
    )
    knowledge_library = create_library(
        name="knowledge_library",
        description="this library give knowledge on techniques for chess",
    )

    print("rule_library", rule_library)
    print("knowledge_library", knowledge_library)
