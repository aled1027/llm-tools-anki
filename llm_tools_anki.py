import json
import llm
import httpx


class Anki(llm.Toolbox):
    """
    A toolbox for interacting with Anki through AnkiConnect API.

    This class provides methods to query Anki's database and retrieve documentation
    through the AnkiConnect HTTP API running on localhost:8765.
    """

    def __init__(self):
        """
        Initialize the Anki toolbox with the default AnkiConnect URL.

        Sets up the connection URL to the local AnkiConnect instance.
        """
        self.url = "http://localhost:8765"

    def query(self, request: str) -> str:
        """
        Send a query to the AnkiConnect API.

        Args:
            request (str): A JSON string containing the API request parameters.
                          Should include 'action' and other required fields.

        Returns:
            str: JSON string containing the API response result, or error message
                 if the request fails.

        Example:
            >>> anki = Anki()
            >>> result = anki.query('{"action": "version", "version": 6}')
        """
        try:
            body = json.loads(request)
            response = httpx.post(f"{self.url}/", json=body)
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                return f"Error: {result.get('error')}"
            return json.dumps(result.get("result", {}))
        except Exception as ex:
            return f"Error: {ex}"

    def docs(self) -> str:
        """
        Retrieve the AnkiConnect API documentation.

        Returns:
            str: The contents of the ankiconnect.md documentation file.

        Note:
            This method reads the documentation from the 'ankiconnect.md' file
            in the current directory.
        """
        with open("ankiconnect.md", "r") as f:
            return f.read()

    # def schema(self) -> str:
    #     """
    #     Get the API schema by calling the apiReflect action.
    #
    #     This method retrieves the available actions and their parameters
    #     from the AnkiConnect API.
    #
    #     Returns:
    #         str: JSON string containing the API schema, or error message
    #              if the request fails.
    #     """
    #     # Call  the action apiReflect
    #     body = {
    #         "action": "apiReflect",
    #         "version": 6,
    #         "params": {"scopes": ["actions"], "actions": None},
    #     }

    #     try:
    #         response = httpx.post(f"{self.url}/", json=body)
    #         response.raise_for_status()
    #         result = response.json()
    #         if result.get("error"):
    #             return f"Error: {result.get('error')}"
    #         return json.dumps(result.get("result", {}))
    #     except httpx.RequestError as ex:
    #         return f"Error: {ex}"


@llm.hookimpl
def register_tools(register):
    """
    Register the Anki toolbox with the LLM framework.

    Args:
        register: The registration function provided by the LLM framework.
    """
    register(Anki)
