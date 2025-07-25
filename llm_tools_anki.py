import json
import llm


class Anki(llm.Toolbox):
    def __init__(self):
        pass

    def query(self, expression: str) -> str:
        try:
            return "hello world from anki: " + expression
        except Exception as ex:
            return f"Error: {ex}"


@llm.hookimpl
def register_tools(register):
    register(Anki)
