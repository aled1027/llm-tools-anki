import json
import llm
import httpx
import os


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
        self.unsplash_access_key = llm.get_key(
            explicit_key="unsplash", key_alias="unsplash", env_var="UNSPLASH_ACCESS_KEY"
        )

    def get_image_url(self, query: str) -> str:
        """
        Get a random image URL from Unsplash using the official API.

        Args:
            query (str): Search query for the image

        Returns:
            str: URL of a random image matching the query, or fallback URL if API fails

        Note:
            Requires UNSPLASH_ACCESS_KEY environment variable to be set.
            Falls back to the old random URL method if API key is not available.
        """
        if not self.unsplash_access_key:
            # Fallback to the old method if no API key is provided
            return f"https://source.unsplash.com/random/400x300/?{query}"

        try:
            headers = {
                "Authorization": f"Client-ID {self.unsplash_access_key}",
                "Accept-Version": "v1",
            }

            params = {"query": query, "per_page": 1, "orientation": "landscape"}

            response = httpx.get(
                "https://api.unsplash.com/photos/random",
                headers=headers,
                params=params,
                timeout=10.0,
            )
            response.raise_for_status()

            data = response.json()
            if data and "urls" in data:
                # Return the regular size URL (800x600 equivalent)
                return data["urls"]["small"]
            else:
                # Fallback if no image found
                return f"https://source.unsplash.com/random/400x300/?{query}"

        except Exception as e:
            # Fallback to the old method if API call fails
            return f"https://source.unsplash.com/random/400x300/?{query}"

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
              >>> request = (
              ...     '{'
              ...     '"action": "addNote",'
              ...     '"version": 5,'
              ...     '"params": {'
              ...         '"note": {'
              ...             '"deckName": "Default",'
              ...             '"modelName": "Basic",'
              ...             '"fields": {'
              ...                 '"Front": "front content",'
              ...                 '"Back": "back content"'
              ...             '},'
              ...             '"tags": ["demo"],'
              ...         '}'
              ...     '}'
              ... )
              >>> print(anki.query(request))
              '{"result": 1496198395707, "error": null}'
        ```
        """
        try:
            body = json.loads(request)
            response = httpx.post(f"{self.url}/", json=body)
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                err_msg = (
                    "There was an error. If you want to check the docs, use the Anki_docs tool. "
                    f"This was the error message: {result.get('error')}"
                )
                return err_msg
            return json.dumps(result.get("result", {}))
        except Exception as ex:
            return f"Error: {ex}"

    def add_note(
        self,
        deck_name: str,
        model_name: str,
        fields: dict,
        tags: list = None,
        audio: dict = None,
    ) -> str:
        """
        Add a single note to Anki.

        Args:
            deck_name (str): Name of the deck to add the note to
            model_name (str): Name of the note model (e.g., "Basic", "Cloze")
            fields (dict): Dictionary of field names and their values
            tags (list, optional): List of tags to add to the note
            audio (dict, optional): Audio configuration with url, filename, skipHash, and fields

        Returns:
            str: JSON string containing the note ID if successful, or error message

        Example:
            >>> anki = Anki()
            >>> result = anki.add_note(
            ...     deck_name="Default",
            ...     model_name="Basic",
            ...     fields={"Front": "What is 2+2?", "Back": "4"},
            ...     tags=["math", "basic"]
            ... )
        """
        note_data = {"deckName": deck_name, "modelName": model_name, "fields": fields}

        if tags:
            note_data["tags"] = tags

        if audio:
            note_data["audio"] = audio

        request = {"action": "addNote", "version": 5, "params": {"note": note_data}}

        return self.query(json.dumps(request))

    def add_notes(self, notes: list) -> str:
        """
        Add multiple notes to Anki.

        Args:
            notes (list): List of note dictionaries, each containing deckName, modelName, fields, etc.

        Returns:
            str: JSON string containing array of note IDs if successful, or error message

        Example:
            >>> anki = Anki()
            >>> notes = [
            ...     {
            ...         "deckName": "Default",
            ...         "modelName": "Basic",
            ...         "fields": {"Front": "Question 1", "Back": "Answer 1"},
            ...         "tags": ["batch"]
            ...     },
            ...     {
            ...         "deckName": "Default",
            ...         "modelName": "Basic",
            ...         "fields": {"Front": "Question 2", "Back": "Answer 2"},
            ...         "tags": ["batch"]
            ...     }
            ... ]
            >>> result = anki.add_notes(notes)
        """
        request = {"action": "addNotes", "version": 5, "params": {"notes": notes}}

        return self.query(json.dumps(request))

    def update_note_fields(self, note_id: int, fields: dict) -> str:
        """
        Update the fields of an existing note.

        Args:
            note_id (int): ID of the note to update
            fields (dict): Dictionary of field names and their new values

        Returns:
            str: JSON string containing null if successful, or error message

        Example:
            >>> anki = Anki()
            >>> result = anki.update_note_fields(
            ...     note_id=1514547547030,
            ...     fields={"Front": "Updated question", "Back": "Updated answer"}
            ... )
        """
        request = {
            "action": "updateNoteFields",
            "version": 5,
            "params": {"note": {"id": note_id, "fields": fields}},
        }

        return self.query(json.dumps(request))

    def find_notes(self, query: str) -> str:
        """
        Find notes using a search query.

        Args:
            query (str): Search query (same syntax as Anki's browse function)

        Returns:
            str: JSON string containing array of note IDs, or error message

        Example:
            >>> anki = Anki()
            >>> result = anki.find_notes("deck:current")
            >>> result = anki.find_notes("tag:important")
            >>> result = anki.find_notes("front:hello")
        """
        request = {"action": "findNotes", "version": 5, "params": {"query": query}}

        return self.query(json.dumps(request))

    def get_notes_info(self, note_ids: list) -> str:
        """
        Get detailed information about notes.

        Args:
            note_ids (list): List of note IDs to get information for

        Returns:
            str: JSON string containing note information, or error message

        Example:
            >>> anki = Anki()
            >>> result = anki.get_notes_info([1502298033753, 1502298036657])
        """
        request = {"action": "notesInfo", "version": 5, "params": {"notes": note_ids}}

        return self.query(json.dumps(request))

    def get_deck_names(self) -> str:
        """
        Get all deck names.

        Returns:
            str: JSON string containing array of deck names, or error message

        Example:
            >>> anki = Anki()
            >>> result = anki.get_deck_names()
        """
        request = {"action": "deckNames", "version": 5}

        return self.query(json.dumps(request))

    def get_deck_names_and_ids(self) -> str:
        """
        Get all deck names and their IDs.

        Returns:
            str: JSON string containing dictionary of deck names and IDs, or error message

        Example:
            >>> anki = Anki()
            >>> result = anki.get_deck_names_and_ids()
        """
        request = {"action": "deckNamesAndIds", "version": 5}

        return self.query(json.dumps(request))

    def get_deck_config(self, deck_name: str) -> str:
        """
        Get configuration for a specific deck.

        Args:
            deck_name (str): Name of the deck to get configuration for

        Returns:
            str: JSON string containing deck configuration, or error message

        Example:
            >>> anki = Anki()
            >>> result = anki.get_deck_config("Default")
        """
        request = {
            "action": "getDeckConfig",
            "version": 5,
            "params": {"deck": deck_name},
        }

        return self.query(json.dumps(request))

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
