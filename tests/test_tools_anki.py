import llm
import json
from llm_tools_anki import Anki


api_reflect_result = {
    "scopes": ["actions"],
    "actions": [
        "addNote",
        "addNotes",
        "addTags",
        "answerCards",
        "apiReflect",
        "areDue",
        "areSuspended",
        "canAddNote",
        "canAddNoteWithErrorDetail",
        "canAddNotes",
        "canAddNotesWithErrorDetail",
        "cardReviews",
        "cardsInfo",
        "cardsModTime",
        "cardsToNotes",
        "changeDeck",
        "clearUnusedTags",
        "cloneDeckConfigId",
        "createDeck",
        "createModel",
        "deckNameFromId",
        "deckNames",
        "deckNamesAndIds",
        "deleteDecks",
        "deleteMediaFile",
        "deleteNotes",
        "exportPackage",
        "findAndReplaceInModels",
        "findCards",
        "findModelsById",
        "findModelsByName",
        "findNotes",
        "forgetCards",
        "getActiveProfile",
        "getCollectionStatsHTML",
        "getDeckConfig",
        "getDeckStats",
        "getDecks",
        "getEaseFactors",
        "getIntervals",
        "getLatestReviewID",
        "getMediaDirPath",
        "getMediaFilesNames",
        "getNoteTags",
        "getNumCardsReviewedByDay",
        "getNumCardsReviewedToday",
        "getProfiles",
        "getReviewsOfCards",
        "getTags",
        "guiAddCards",
        "guiAnswerCard",
        "guiBrowse",
        "guiCheckDatabase",
        "guiCurrentCard",
        "guiDeckBrowser",
        "guiDeckOverview",
        "guiDeckReview",
        "guiEditNote",
        "guiExitAnki",
        "guiImportFile",
        "guiReviewActive",
        "guiSelectCard",
        "guiSelectNote",
        "guiSelectedNotes",
        "guiShowAnswer",
        "guiShowQuestion",
        "guiStartCardTimer",
        "guiUndo",
        "importPackage",
        "insertReviews",
        "loadProfile",
        "modelFieldAdd",
        "modelFieldDescriptions",
        "modelFieldFonts",
        "modelFieldNames",
        "modelFieldRemove",
        "modelFieldRename",
        "modelFieldReposition",
        "modelFieldSetDescription",
        "modelFieldSetFont",
        "modelFieldSetFontSize",
        "modelFieldsOnTemplates",
        "modelNameFromId",
        "modelNames",
        "modelNamesAndIds",
        "modelStyling",
        "modelTemplateAdd",
        "modelTemplateRemove",
        "modelTemplateRename",
        "modelTemplateReposition",
        "modelTemplates",
        "multi",
        "notesInfo",
        "notesModTime",
        "relearnCards",
        "reloadCollection",
        "removeDeckConfigId",
        "removeEmptyNotes",
        "removeTags",
        "replaceTags",
        "replaceTagsInAllNotes",
        "requestPermission",
        "retrieveMediaFile",
        "saveDeckConfig",
        "setDeckConfigId",
        "setDueDate",
        "setEaseFactors",
        "setSpecificValueOfCard",
        "storeMediaFile",
        "suspend",
        "suspended",
        "sync",
        "unsuspend",
        "updateModelStyling",
        "updateModelTemplates",
        "updateNote",
        "updateNoteFields",
        "updateNoteModel",
        "updateNoteTags",
        "version",
    ],
}


def test_anki_query():
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {"name": "Anki_query", "arguments": {"expression": "3 * 14"}}
                ]
            }
        ),
        tools=[Anki()],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert tool_results == [
        {
            "name": "Anki_query",
            "output": "hello world from anki: 3 * 14",
            "tool_call_id": None,
        }
    ]


def test_anki_schema():
    # TODO: this test requires AnkiConnect to be running
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps({"tool_calls": [{"name": "Anki_schema", "arguments": {}}]}),
        tools=[Anki()],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert tool_results[0]["name"] == "Anki_schema"
    assert tool_results[0]["tool_call_id"] is None

    tool_result_dict = json.loads(tool_results[0]["output"])
    assert tool_result_dict == api_reflect_result


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
    assert tool_results[0]["output"] == Anki().docs() + "foo"
