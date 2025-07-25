import pytest
import json
import httpx
from unittest.mock import patch, Mock
from llm_tools_anki import Anki


class TestAnki:
    """Test suite for the Anki toolbox."""

    def setup_method(self):
        """Set up test fixtures."""
        self.anki = Anki()
        self.base_url = "http://localhost:8765"

    @patch("httpx.post")
    def test_query_success(self, mock_post):
        """Test successful query to AnkiConnect."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"result": {"note_id": 12345}, "error": None}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        request = json.dumps(
            {
                "action": "addNote",
                "version": 5,
                "params": {
                    "note": {
                        "deckName": "Default",
                        "modelName": "Basic",
                        "fields": {"Front": "Test", "Back": "Answer"},
                    }
                },
            }
        )

        result = self.anki.query(request)

        # Verify the request was made correctly
        mock_post.assert_called_once_with(f"{self.base_url}/", json=json.loads(request))

        # Verify the result
        assert result == '{"note_id": 12345}'

    @patch("httpx.post")
    def test_query_with_error(self, mock_post):
        """Test query that returns an error from AnkiConnect."""
        # Mock error response
        mock_response = Mock()
        mock_response.json.return_value = {
            "result": None,
            "error": "Deck 'NonExistent' does not exist",
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        request = json.dumps(
            {
                "action": "addNote",
                "version": 5,
                "params": {"note": {"deckName": "NonExistent"}},
            }
        )

        result = self.anki.query(request)

        assert "There was an error" in result
        assert "Deck 'NonExistent' does not exist" in result

    @patch("httpx.post")
    def test_query_http_error(self, mock_post):
        """Test query that raises an HTTP error."""
        mock_post.side_effect = httpx.HTTPError("Connection failed")

        request = json.dumps({"action": "test", "version": 5})
        result = self.anki.query(request)

        assert "Error: Connection failed" in result

    @patch("httpx.post")
    def test_query_invalid_json(self, mock_post):
        """Test query with invalid JSON input."""
        result = self.anki.query("invalid json")
        assert "Error:" in result

    @patch("httpx.post")
    def test_add_note_success(self, mock_post):
        """Test successful note addition."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": 12345, "error": None}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.anki.add_note(
            deck_name="Default",
            model_name="Basic",
            fields={"Front": "What is 2+2?", "Back": "4"},
            tags=["math", "basic"],
        )

        # Verify the request structure
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]

        assert request_body["action"] == "addNote"
        assert request_body["version"] == 5
        assert request_body["params"]["note"]["deckName"] == "Default"
        assert request_body["params"]["note"]["modelName"] == "Basic"
        assert request_body["params"]["note"]["fields"] == {
            "Front": "What is 2+2?",
            "Back": "4",
        }
        assert request_body["params"]["note"]["tags"] == ["math", "basic"]

        assert result == "12345"

    @patch("httpx.post")
    def test_add_note_with_audio(self, mock_post):
        """Test note addition with audio."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": 12345, "error": None}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        audio_config = {
            "url": "https://example.com/audio.mp3",
            "filename": "audio.mp3",
            "skipHash": "abc123",
            "fields": ["Front"],
        }

        result = self.anki.add_note(
            deck_name="Default",
            model_name="Basic",
            fields={"Front": "Test", "Back": "Answer"},
            audio=audio_config,
        )

        # Verify audio was included in request
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]
        assert request_body["params"]["note"]["audio"] == audio_config

    @patch("httpx.post")
    def test_add_notes_batch(self, mock_post):
        """Test adding multiple notes in batch."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": [12345, 12346], "error": None}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        notes = [
            {
                "deckName": "Default",
                "modelName": "Basic",
                "fields": {"Front": "Question 1", "Back": "Answer 1"},
                "tags": ["batch"],
            },
            {
                "deckName": "Default",
                "modelName": "Basic",
                "fields": {"Front": "Question 2", "Back": "Answer 2"},
                "tags": ["batch"],
            },
        ]

        result = self.anki.add_notes(notes)

        # Verify the request structure
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]

        assert request_body["action"] == "addNotes"
        assert request_body["version"] == 5
        assert request_body["params"]["notes"] == notes

        assert result == "[12345, 12346]"

    @patch("httpx.post")
    def test_update_note_fields(self, mock_post):
        """Test updating note fields."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": None, "error": None}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.anki.update_note_fields(
            note_id=1514547547030,
            fields={"Front": "Updated question", "Back": "Updated answer"},
        )

        # Verify the request structure
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]

        assert request_body["action"] == "updateNoteFields"
        assert request_body["version"] == 5
        assert request_body["params"]["note"]["id"] == 1514547547030
        assert request_body["params"]["note"]["fields"] == {
            "Front": "Updated question",
            "Back": "Updated answer",
        }

        assert result == "null"

    @patch("httpx.post")
    def test_find_notes(self, mock_post):
        """Test finding notes with search query."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": [12345, 12346], "error": None}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.anki.find_notes("deck:current")

        # Verify the request structure
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]

        assert request_body["action"] == "findNotes"
        assert request_body["version"] == 5
        assert request_body["params"]["query"] == "deck:current"

        assert result == "[12345, 12346]"

    @patch("httpx.post")
    def test_get_notes_info(self, mock_post):
        """Test getting detailed note information."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "result": [
                {
                    "noteId": 12345,
                    "modelName": "Basic",
                    "tags": ["test"],
                    "fields": {
                        "Front": {"value": "Question"},
                        "Back": {"value": "Answer"},
                    },
                }
            ],
            "error": None,
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.anki.get_notes_info([12345])

        # Verify the request structure
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]

        assert request_body["action"] == "notesInfo"
        assert request_body["version"] == 5
        assert request_body["params"]["notes"] == [12345]

        # Verify the result contains the expected structure
        result_data = json.loads(result)
        assert len(result_data) == 1
        assert result_data[0]["noteId"] == 12345

    @patch("httpx.post")
    def test_get_deck_names(self, mock_post):
        """Test getting all deck names."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "result": ["Default", "Math", "Science"],
            "error": None,
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.anki.get_deck_names()

        # Verify the request structure
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]

        assert request_body["action"] == "deckNames"
        assert request_body["version"] == 5

        assert result == '["Default", "Math", "Science"]'

    @patch("httpx.post")
    def test_get_deck_names_and_ids(self, mock_post):
        """Test getting deck names and their IDs."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "result": {"Default": 1, "Math": 2, "Science": 3},
            "error": None,
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.anki.get_deck_names_and_ids()

        # Verify the request structure
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]

        assert request_body["action"] == "deckNamesAndIds"
        assert request_body["version"] == 5

        assert result == '{"Default": 1, "Math": 2, "Science": 3}'

    @patch("httpx.post")
    def test_get_deck_config(self, mock_post):
        """Test getting deck configuration."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "result": {
                "name": "Default",
                "new": {"perDay": 20},
                "review": {"perDay": 100},
            },
            "error": None,
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.anki.get_deck_config("Default")

        # Verify the request structure
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]

        assert request_body["action"] == "getDeckConfig"
        assert request_body["version"] == 5
        assert request_body["params"]["deck"] == "Default"

        result_data = json.loads(result)
        assert result_data["name"] == "Default"

    @patch("builtins.open", create=True)
    def test_docs(self, mock_open):
        """Test retrieving documentation."""
        mock_content = "# AnkiConnect API Documentation\n\nThis is the documentation..."
        mock_file = Mock()
        mock_file.read.return_value = mock_content
        mock_open.return_value.__enter__.return_value = mock_file

        result = self.anki.docs()

        mock_open.assert_called_once_with("ankiconnect.md", "r")
        assert result == mock_content

    def test_init(self):
        """Test Anki toolbox initialization."""
        anki = Anki()
        assert anki.url == "http://localhost:8765"

    @patch("httpx.post")
    def test_query_with_empty_result(self, mock_post):
        """Test query that returns empty result."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": None, "error": None}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        request = json.dumps({"action": "test", "version": 5})
        result = self.anki.query(request)

        assert result == "null"

    @patch("httpx.post")
    def test_query_with_missing_result(self, mock_post):
        """Test query that doesn't include result in response."""
        mock_response = Mock()
        mock_response.json.return_value = {"error": None}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        request = json.dumps({"action": "test", "version": 5})
        result = self.anki.query(request)

        assert result == "{}"


class TestAnkiIntegration:
    """Integration tests for the Anki toolbox with LLM framework."""

    def test_anki_docs_integration(self):
        """Test Anki docs tool integration with LLM framework."""
        import llm

        model = llm.get_model("echo")
        chain_response = model.chain(
            json.dumps({"tool_calls": [{"name": "Anki_docs", "arguments": {}}]}),
            tools=[Anki()],
        )
        responses = list(chain_response.responses())
        tool_results = json.loads(responses[-1].text())["tool_results"]

        assert tool_results[0]["name"] == "Anki_docs"
        assert tool_results[0]["tool_call_id"] is None
        assert len(tool_results[0]["output"]) > 50
