import llm


def anki(expression: str) -> str:
    """
    Evaluate a simple expression using the simpleeval library.
    """
    try:
        return "hello world from anki: " + expression
    except Exception as e:
        return f"Error: {str(e)}"


@llm.hookimpl
def register_tools(register):
    register(anki)
