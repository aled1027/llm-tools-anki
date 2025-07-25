import llm
import json
from llm_tools_anki import anki


def test_simple_eval():
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {"tool_calls": [{"name": "anki", "arguments": {"expression": "3 * 14"}}]}
        ),
        tools=[anki],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert tool_results == [
        {
            "name": "anki",
            "output": "hello world from anki: 3 * 14",
            "tool_call_id": None,
        }
    ]
