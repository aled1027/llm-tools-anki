import json
import llm
import httpx
import hashlib
import time
import base64
import tempfile
import os


class Anki(llm.Toolbox):
    """
    A toolbox for interacting with Anki through AnkiConnect API.

    This class provides methods to query Anki's database, retrieve documentation,
    and create notes with audio content through the AnkiConnect HTTP API running on localhost:8765.

    The toolbox includes audio generation capabilities using OpenAI's TTS API, with a file-based
    workflow to prevent flooding the LLM with large audio data. Audio content is generated as
    temporary HTML files that can be referenced when creating notes.
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
        self.openai_api_key = llm.get_key(
            explicit_key="openai", key_alias="openai", env_var="OPENAI_API_KEY"
        )
        self.replicate_api_key = llm.get_key(
            explicit_key="replicate", key_alias="replicate", env_var="REPLICATE_API_KEY"
        )
        self.gemini_api_key = llm.get_key(
            explicit_key="gemini", key_alias="gemini", env_var="GEMINI_API_KEY"
        )

        self.replicate_api_key = None  # TODO: remove this 
        self.openai_api_key = None  # TODO: remove this

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
        use_front_from_file: str = None,
    ) -> str:
        """
        Add a single note to Anki.

        This method creates a new note in the specified deck. The front field content can be
        loaded from a file using the use_front_from_file parameter, which is particularly useful
        when working with audio-generated HTML content from the generate_audio method.

        Args:
            deck_name (str): The name of the deck to add the note to.
            model_name (str): The name of the note type (model) to use.
            fields (dict): A dictionary mapping field names to their values.
                Note: The "Front" and "Back" fields are often HTML strings, not plain text.
                If use_front_from_file is provided, the "Front" field in this dict will be
                overridden by the file content.
            tags (list, optional): A list of tags to assign to the note.
            use_front_from_file (str, optional): Path to a file containing the front field content.
                The file content will replace any "Front" field specified in the fields dict.
                This is useful for loading HTML content with embedded audio from files generated
                by the generate_audio method.

        Returns:
            str: JSON string containing the note ID if successful, or an error message.

        Example:
            >>> anki = Anki()
            >>> # Basic note creation
            >>> result = anki.add_note(
            ...     deck_name="Default",
            ...     model_name="Basic",
            ...     fields={"Front": "<b>Capital of Oregon</b>", "Back": "<i>Salem</i>"},
            ...     tags=["demo"]
            ... )
            >>> # Note with front content loaded from file (e.g., audio HTML)
            >>> result = anki.add_note(
            ...     deck_name="Default",
            ...     model_name="Basic",
            ...     fields={"Back": "Hello world"},
            ...     tags=["demo"],
            ...     use_front_from_file="/path/to/front_content.html"
            ... )
            >>> # Complete workflow with audio generation
            >>> audio_file = anki.generate_audio("Capital of Oregon")
            >>> result = anki.add_note(
            ...     deck_name="Geography",
            ...     model_name="Basic",
            ...     fields={"Back": "Salem"},
            ...     tags=["geography", "audio"],
            ...     use_front_from_file=audio_file
            ... )
        """
        note_data = {"deckName": deck_name, "modelName": model_name, "fields": fields}

        if tags:
            note_data["tags"] = tags

        if use_front_from_file:
            try:
                with open(use_front_from_file, "r", encoding="utf-8") as f:
                    front_content = f.read()
                note_data["fields"]["Front"] = front_content
            except Exception as e:
                return f"Error reading front file: {str(e)}"

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

    def generate_audio(
        self,
        text: str,
        language_code: str = "en-US",
    ) -> str:
        """
        Generate an audio HTML element from text using OpenAI's TTS API and write it to a temporary file.

        Args:
            text (str): The text to convert to speech.
            language_code (str): Language code (e.g., "en-US", "es-ES", "fr-FR"). Defaults to "en-US".
        """
        if self.gemini_api_key:
            return self._generate_audio_with_gemini(text, language_code)
        elif self.replicate_api_key:
            return self._generate_audio_with_replicate(text)
        elif self.openai_api_key:
            return self._generate_audio_with_openai(text)
        else:
            return "Error: No API key found"

    def _generate_audio_with_gemini(
        self,
        text: str,
        language_code: str = "en-US",
    ) -> str:
        """
        Generate an audio HTML element from text using Gemini's TTS API and write it to a temporary file.

        This method converts text to speech using Google's Text-to-Speech API (Gemini), creates an HTML audio element
        with base64-encoded audio, and writes it to a temporary file. The temporary file persists
        until manually cleaned up, allowing it to be referenced when creating Anki notes.

        Args:
            text (str): The text to convert to speech.
            language_code (str): Language code (e.g., "en-US", "es-ES", "fr-FR"). Defaults to "en-US".

        Returns:
            str: Path to the temporary file containing the HTML audio element, or an error message
                 if generation fails. The temporary file contains an HTML <audio> element with
                 base64-encoded audio that can be embedded in Anki notes.

        Note:
            Requires the GEMINI_API_KEY environment variable to be set.
            Temporary files are not automatically cleaned up and should be removed manually
            when no longer needed to prevent disk space accumulation.

        Example:
            >>> anki = Anki()
            >>> # Basic usage
            >>> audio_file = anki.generate_audio("Hello world")
            >>> # With specific language
            >>> audio_file = anki.generate_audio("Buenos dias", "es-ES", "es-ES-Chirp3-HD-Schedar")
            >>> # Use the returned file path with add_note's use_front_from_file parameter
            >>> result = anki.add_note(
            ...     deck_name="Default",
            ...     model_name="Basic",
            ...     fields={"Back": "Hello world"},
            ...     use_front_from_file=audio_file
            ... )

        """
        try:
            # Get Gemini API key from environment
            if not self.gemini_api_key:
                return "Error: GEMINI_API_KEY environment variable not set"

            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.gemini_api_key,
            }

            # Set default voice
            voice_name = "en-US-Neural2-F"
            if language_code == "en-US":
                voice_name = "en-US-Neural2-F"
            elif language_code == "es-ES":
                voice_name = "es-ES-Neural2-A"
            elif language_code == "fr-FR":
                voice_name = "fr-FR-Neural2-A"
            else:
                voice_name = f"{language_code}-Neural2-A"

            # Build voice configuration
            voice_config = {
                "languageCode": language_code,
                "name": voice_name,
            }

            payload = {
                "input": {"text": text},
                "voice": voice_config,
                "audioConfig": {"audioEncoding": "LINEAR16", "speakingRate": 0.85},
            }

            response = httpx.post(
                "https://texttospeech.googleapis.com/v1/text:synthesize",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()

            # Get the response data
            result = response.json()

            # Extract the base64 audio content
            audio_content = result.get("audioContent")
            if not audio_content:
                return "Error: No audio content in response"

            # Decode the base64 audio data
            audio_data = base64.b64decode(audio_content)

            # Generate filename
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            timestamp = int(time.time())
            filename = f"tts_gemini_{text_hash}_{timestamp}.wav"

            # Create HTML audio element with base64 encoded audio
            audio_html = f'<audio controls><source src="data:audio/wav;base64,{audio_content}" type="audio/wav">Your browser does not support the audio element.</audio>'

            # Write HTML to temporary file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False
            ) as temp_file:
                temp_file.write(audio_html)
                temp_file_path = temp_file.name

            return temp_file_path

        except httpx.HTTPStatusError as e:
            return f"Error: HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _generate_audio_with_replicate(
        self,
        text: str,
    ) -> str:
        """
        Generate an audio HTML element from text using Replicate's TTS API and write it to a temporary file.

        This method converts text to speech using Replicate's TTS API, creates an HTML audio element
        with base64-encoded audio, and writes it to a temporary file. The temporary file persists
        until manually cleaned up, allowing it to be referenced when creating Anki notes.

        Args:
            text (str): The text to convert to speech.
            voice (str, optional): The voice to use for TTS. Defaults to "alloy".
                Available voices: "af_nicole", "en_jenny", "en_ryan", "en_tony", "en_will", "en_grace"
            format (str, optional): The audio format to use (e.g., "mp3"). Defaults to "mp3".
            filename (str, optional): Optional filename for the generated audio. If not provided,
                a unique filename is generated using text hash and timestamp.

        Returns:
            str: Path to the temporary file containing the HTML audio element, or an error message
                 if generation fails. The temporary file contains an HTML <audio> element with
                 base64-encoded audio that can be embedded in Anki notes.

        Note:
            Requires the REPLICATE_API_KEY environment variable to be set.
            Temporary files are not automatically cleaned up and should be removed manually
            when no longer needed to prevent disk space accumulation.

        Example:
            >>> anki = Anki()
            >>> audio_file = anki.generate_audio("Hello world")
            >>> # Use the returned file path with add_note's use_front_from_file parameter
            >>> result = anki.add_note(
            ...     deck_name="Default",
            ...     model_name="Basic",
            ...     fields={"Back": "Hello world"},
            ...     use_front_from_file=audio_file
            ... )
        """
        voice = "af_nicole"
        format = "mp3"
        filename = None

        try:
            # Get Replicate API key from environment
            if not self.replicate_api_key:
                return "Error: REPLICATE_API_KEY environment variable not set"

            headers = {
                "Authorization": f"Bearer {self.replicate_api_key}",
                "Content-Type": "application/json",
                "Prefer": "wait=30",
            }

            payload = {
                "version": "f559560eb822dc509045f3921a1921234918b91739db4bf3daab2169b71c7a13",
                "input": {"text": text, "voice": voice},
            }

            response = httpx.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=payload,
                timeout=60.0,
            )
            response.raise_for_status()

            # Get the response data
            result = response.json()
            prediction_id = result.get("id")

            if not prediction_id:
                return "Error: No prediction ID in response"

            # Poll for completion
            max_attempts = 30  # 30 seconds with 1-second intervals
            for attempt in range(max_attempts):
                # Get prediction status
                status_response = httpx.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers={"Authorization": f"Bearer {self.replicate_api_key}"},
                    timeout=10.0,
                )
                status_response.raise_for_status()
                status_result = status_response.json()

                status = status_result.get("status")

                if status == "succeeded":
                    result = status_result
                    break
                elif status in ["failed", "canceled"]:
                    return f"Error: Prediction failed with status: {status}"
                elif status == "processing":
                    # Wait 1 second before next poll
                    time.sleep(1)
                else:
                    # Wait 1 second for other statuses (starting, etc.)
                    time.sleep(1)
            else:
                return f"Error: Prediction timed out after {max_attempts} seconds. Status: {status}"

            # Get the audio URL from the output
            audio_url = result.get("output")
            if not audio_url:
                return "Error: No audio URL in response"

            # Download the audio file
            audio_response = httpx.get(audio_url, timeout=30.0)
            audio_response.raise_for_status()
            audio_data = audio_response.content

            # Generate filename if not provided
            if not filename:
                text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                timestamp = int(time.time())
                filename = f"tts_replicate_{voice}_{text_hash}_{timestamp}.{format}"

            # Convert to base64 for inline embedding
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")

            # Create HTML audio element with base64 encoded audio
            audio_html = f'<audio controls><source src="data:audio/{format};base64,{audio_base64}" type="audio/{format}">Your browser does not support the audio element.</audio>'

            # Write HTML to temporary file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False
            ) as temp_file:
                temp_file.write(audio_html)
                temp_file_path = temp_file.name

            return temp_file_path

        except httpx.HTTPStatusError as e:
            return f"Error: HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _generate_audio_with_openai(self, text: str) -> str:
        """
        Generate an audio HTML element from text using OpenAI's TTS API and write it to a temporary file.

        This method converts text to speech using OpenAI's TTS API, creates an HTML audio element
        with base64-encoded audio, and writes it to a temporary file. The temporary file persists
        until manually cleaned up, allowing it to be referenced when creating Anki notes.

        Args:
            text (str): The text to convert to speech.

        Returns:
            str: Path to the temporary file containing the HTML audio element, or an error message
                 if generation fails. The temporary file contains an HTML <audio> element with
                 base64-encoded audio that can be embedded in Anki notes.

        Note:
            Requires the OPENAI_API_KEY environment variable to be set.
            Temporary files are not automatically cleaned up and should be removed manually
            when no longer needed to prevent disk space accumulation.

        Example:
            >>> anki = Anki()
            >>> audio_file = anki.generate_audio("Hello world")
            >>> # Use the returned file path with add_note's use_front_from_file parameter
            >>> result = anki.add_note(
            ...     deck_name="Default",
            ...     model_name="Basic",
            ...     fields={"Back": "Hello world"},
            ...     use_front_from_file=audio_file
            ... )
        """
        voice = "alloy"
        format = "mp3"
        filename = None

        try:
            # Get OpenAI API key from environment
            if not self.openai_api_key:
                return "Error: OPENAI_API_KEY environment variable not set"

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": "tts-1",
                "input": text,
                "voice": voice,
                "response_format": format,
            }

            response = httpx.post(
                "https://api.openai.com/v1/audio/speech",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()

            # Get the audio data
            audio_data = response.content

            # Generate filename if not provided
            if not filename:
                text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                timestamp = int(time.time())
                filename = f"tts_{voice}_{text_hash}_{timestamp}.{format}"

            # Convert to base64 for inline embedding
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")

            # Create HTML audio element with base64 encoded audio
            audio_html = f'<audio controls><source src="data:audio/{format};base64,{audio_base64}" type="audio/{format}">Your browser does not support the audio element.</audio>'

            # Write HTML to temporary file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False
            ) as temp_file:
                temp_file.write(audio_html)
                temp_file_path = temp_file.name

            return temp_file_path

        except httpx.HTTPStatusError as e:
            return f"Error: HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


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
