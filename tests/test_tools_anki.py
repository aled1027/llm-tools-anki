import llm
import json
from llm_tools_anki import Anki


def test_anki_docs():
    # TODO: this test requires AnkiConnect to be running
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
