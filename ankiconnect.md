Below is a comprehensive list of currently supported actions.

#### Miscellaneous

- **version**

  Gets the version of the API exposed by this plugin. Currently versions `1` through `5` are defined.

  This should be the first call you make to make sure that your application and AnkiConnect are able to communicate
  properly with each other. New versions of AnkiConnect are backwards compatible; as long as you are using actions
  which are available in the reported AnkiConnect version or earlier, everything should work fine.

  _Sample request_:

  ```json
  {
    "action": "version",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": 5,
    "error": null
  }
  ```

- **upgrade**

  Displays a confirmation dialog box in Anki asking the user if they wish to upgrade AnkiConnect to the latest version
  from the project's [master branch](https://raw.githubusercontent.com/FooSoft/anki-connect/master/AnkiConnect.py) on
  GitHub. Returns a boolean value indicating if the plugin was upgraded or not.

  _Sample request_:

  ```json
  {
    "action": "upgrade",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **multi**

  Performs multiple actions in one request, returning an array with the response of each action (in the given order).

  _Sample request_:

  ```json
  {
    "action": "multi",
    "version": 5,
    "params": {
      "actions": [
        { "action": "deckNames" },
        {
          "action": "browse",
          "params": { "query": "deck:current" }
        }
      ]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [["Default"], [1494723142483, 1494703460437, 1494703479525]],
    "error": null
  }
  ```

#### Decks

- **deckNames**

  Gets the complete list of deck names for the current user.

  _Sample request_:

  ```json
  {
    "action": "deckNames",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": ["Default"],
    "error": null
  }
  ```

- **deckNamesAndIds**

  Gets the complete list of deck names and their respective IDs for the current user.

  _Sample request_:

  ```json
  {
    "action": "deckNamesAndIds",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": { "Default": 1 },
    "error": null
  }
  ```

- **getDecks**

  Accepts an array of card IDs and returns an object with each deck name as a key, and its value an array of the given
  cards which belong to it.

  _Sample request_:

  ```json
  {
    "action": "getDecks",
    "version": 5,
    "params": {
      "cards": [1502298036657, 1502298033753, 1502032366472]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": {
      "Default": [1502032366472],
      "Japanese::JLPT N3": [1502298036657, 1502298033753]
    },
    "error": null
  }
  ```

- **changeDeck**

  Moves cards with the given IDs to a different deck, creating the deck if it doesn't exist yet.

  _Sample request_:

  ```json
  {
    "action": "changeDeck",
    "version": 5,
    "params": {
      "cards": [1502098034045, 1502098034048, 1502298033753],
      "deck": "Japanese::JLPT N3"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

- **deleteDecks**

  Deletes decks with the given names. If `cardsToo` is `true` (defaults to `false` if unspecified), the cards within
  the deleted decks will also be deleted; otherwise they will be moved to the default deck.

  _Sample request_:

  ```json
  {
    "action": "deleteDecks",
    "version": 5,
    "params": {
      "decks": ["Japanese::JLPT N5", "Easy Spanish"],
      "cardsToo": true
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

- **getDeckConfig**

  Gets the configuration group object for the given deck.

  _Sample request_:

  ```json
  {
    "action": "getDeckConfig",
    "version": 5,
    "params": {
      "deck": "Default"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": {
      "lapse": {
        "leechFails": 8,
        "delays": [10],
        "minInt": 1,
        "leechAction": 0,
        "mult": 0
      },
      "dyn": false,
      "autoplay": true,
      "mod": 1502970872,
      "id": 1,
      "maxTaken": 60,
      "new": {
        "bury": true,
        "order": 1,
        "initialFactor": 2500,
        "perDay": 20,
        "delays": [1, 10],
        "separate": true,
        "ints": [1, 4, 7]
      },
      "name": "Default",
      "rev": {
        "bury": true,
        "ivlFct": 1,
        "ease4": 1.3,
        "maxIvl": 36500,
        "perDay": 100,
        "minSpace": 1,
        "fuzz": 0.05
      },
      "timer": 0,
      "replayq": true,
      "usn": -1
    },
    "error": null
  }
  ```

- **saveDeckConfig**

  Saves the given configuration group, returning `true` on success or `false` if the ID of the configuration group is
  invalid (such as when it does not exist).

  _Sample request_:

  ```json
  {
    "action": "saveDeckConfig",
    "version": 5,
    "params": {
      "config": {
        "lapse": {
          "leechFails": 8,
          "delays": [10],
          "minInt": 1,
          "leechAction": 0,
          "mult": 0
        },
        "dyn": false,
        "autoplay": true,
        "mod": 1502970872,
        "id": 1,
        "maxTaken": 60,
        "new": {
          "bury": true,
          "order": 1,
          "initialFactor": 2500,
          "perDay": 20,
          "delays": [1, 10],
          "separate": true,
          "ints": [1, 4, 7]
        },
        "name": "Default",
        "rev": {
          "bury": true,
          "ivlFct": 1,
          "ease4": 1.3,
          "maxIvl": 36500,
          "perDay": 100,
          "minSpace": 1,
          "fuzz": 0.05
        },
        "timer": 0,
        "replayq": true,
        "usn": -1
      }
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **setDeckConfigId**

  Changes the configuration group for the given decks to the one with the given ID. Returns `true` on success or
  `false` if the given configuration group or any of the given decks do not exist.

  _Sample request_:

  ```json
  {
    "action": "setDeckConfigId",
    "version": 5,
    "params": {
      "decks": ["Default"],
      "configId": 1
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **cloneDeckConfigId**

  Creates a new configuration group with the given name, cloning from the group with the given ID, or from the default
  group if this is unspecified. Returns the ID of the new configuration group, or `false` if the specified group to
  clone from does not exist.

  _Sample request_:

  ```json
  {
    "action": "cloneDeckConfigId",
    "version": 5,
    "params": {
      "name": "Copy of Default",
      "cloneFrom": 1
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": 1502972374573,
    "error": null
  }
  ```

- **removeDeckConfigId**

  Removes the configuration group with the given ID, returning `true` if successful, or `false` if attempting to
  remove either the default configuration group (ID = 1) or a configuration group that does not exist.

  _Sample request_:

  ```json
  {
    "action": "removeDeckConfigId",
    "version": 5,
    "params": {
      "configId": 1502972374573
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

#### Models

- **modelNames**

  Gets the complete list of model names for the current user.

  _Sample request_:

  ```json
  {
    "action": "modelNames",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": ["Basic", "Basic (and reversed card)"],
    "error": null
  }
  ```

- **modelNamesAndIds**

  Gets the complete list of model names and their corresponding IDs for the current user.

  _Sample request_:

  ```json
  {
    "action": "modelNamesAndIds",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": {
      "Basic": 1483883011648,
      "Basic (and reversed card)": 1483883011644,
      "Basic (optional reversed card)": 1483883011631,
      "Cloze": 1483883011630
    },
    "error": null
  }
  ```

- **modelFieldNames**

  Gets the complete list of field names for the provided model name.

  _Sample request_:

  ```json
  {
    "action": "modelFieldNames",
    "version": 5,
    "params": {
      "modelName": "Basic"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": ["Front", "Back"],
    "error": null
  }
  ```

- **modelFieldsOnTemplates**

  Returns an object indicating the fields on the question and answer side of each card template for the given model
  name. The question side is given first in each array.

  _Sample request_:

  ```json
  {
    "action": "modelFieldsOnTemplates",
    "version": 5,
    "params": {
      "modelName": "Basic (and reversed card)"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": {
      "Card 1": [["Front"], ["Back"]],
      "Card 2": [["Back"], ["Front"]]
    },
    "error": null
  }
  ```

#### Notes

- **addNote**

  Creates a note using the given deck and model, with the provided field values and tags. Returns the identifier of
  the created note created on success, and `null` on failure.

  AnkiConnect can download audio files and embed them in newly created notes. The corresponding `audio` note member is
  optional and can be omitted. If you choose to include it, the `url` and `filename` fields must be also defined. The
  `skipHash` field can be optionally provided to skip the inclusion of downloaded files with an MD5 hash that matches
  the provided value. This is useful for avoiding the saving of error pages and stub files. The `fields` member is a
  list of fields that should play audio when the card is displayed in Anki.

  _Sample request_:

  ```json
  {
    "action": "addNote",
    "version": 5,
    "params": {
      "note": {
        "deckName": "Default",
        "modelName": "Basic",
        "fields": {
          "Front": "front content",
          "Back": "back content"
        },
        "tags": ["yomichan"],
        "audio": {
          "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
          "filename": "yomichan_ねこ_猫.mp3",
          "skipHash": "7e2c2f954ef6051373ba916f000168dc",
          "fields": "Front"
        }
      }
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": 1496198395707,
    "error": null
  }
  ```

- **addNotes**

  Creates multiple notes using the given deck and model, with the provided field values and tags. Returns an array of
  identifiers of the created notes (notes that could not be created will have a `null` identifier). Please see the
  documentation for `addNote` for an explanation of objects in the `notes` array.

  _Sample request_:

  ```json
  {
    "action": "addNotes",
    "version": 5,
    "params": {
      "notes": [
        {
          "deckName": "Default",
          "modelName": "Basic",
          "fields": {
            "Front": "front content",
            "Back": "back content"
          },
          "tags": ["yomichan"],
          "audio": {
            "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
            "filename": "yomichan_ねこ_猫.mp3",
            "skipHash": "7e2c2f954ef6051373ba916f000168dc",
            "fields": "Front"
          }
        }
      ]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [1496198395707, null],
    "error": null
  }
  ```

- **canAddNotes**

  Accepts an array of objects which define parameters for candidate notes (see `addNote`) and returns an array of
  booleans indicating whether or not the parameters at the corresponding index could be used to create a new note.

  _Sample request_:

  ```json
  {
    "action": "canAddNotes",
    "version": 5,
    "params": {
      "notes": [
        {
          "deckName": "Default",
          "modelName": "Basic",
          "fields": {
            "Front": "front content",
            "Back": "back content"
          },
          "tags": ["yomichan"]
        }
      ]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [true],
    "error": null
  }
  ```

- **updateNoteFields**

  Modify the fields of an exist note.

  _Sample request_:

  ```json
  {
    "action": "updateNoteFields",
    "version": 5,
    "params": {
      "note": {
        "id": 1514547547030,
        "fields": {
          "Front": "new front content",
          "Back": "new back content"
        }
      }
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

- **addTags**

  Adds tags to notes by note ID.

  _Sample request_:

  ```json
  {
    "action": "addTags",
    "version": 5,
    "params": {
      "notes": [1483959289817, 1483959291695],
      "tags": "european-languages"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

- **removeTags**

  Remove tags from notes by note ID.

  _Sample request_:

  ```json
  {
    "action": "removeTags",
    "version": 5,
    "params": {
      "notes": [1483959289817, 1483959291695],
      "tags": "european-languages"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

- **getTags**

  Gets the complete list of tags for the current user.

  _Sample request_:

  ```json
  {
    "action": "getTags",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": ["european-languages", "idioms"],
    "error": null
  }
  ```

- **findNotes**

  Returns an array of note IDs for a given query. Same query syntax as `guiBrowse`.

  _Sample request_:

  ```json
  {
    "action": "findNotes",
    "version": 5,
    "params": {
      "query": "deck:current"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [1483959289817, 1483959291695],
    "error": null
  }
  ```

- **notesInfo**

  Returns a list of objects containing for each note ID the note fields, tags, note type and the cards belonging to
  the note.

  _Sample request_:

  ```json
  {
    "action": "notesInfo",
    "version": 5,
    "params": {
      "notes": [1502298033753]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [
      {
        "noteId": 1502298033753,
        "modelName": "Basic",
        "tags": ["tag", "another_tag"],
        "fields": {
          "Front": { "value": "front content", "order": 0 },
          "Back": { "value": "back content", "order": 1 }
        }
      }
    ],
    "error": null
  }
  ```

#### Cards

- **suspend**

  Suspend cards by card ID; returns `true` if successful (at least one card wasn't already suspended) or `false`
  otherwise.

  _Sample request_:

  ```json
  {
    "action": "suspend",
    "version": 5,
    "params": {
      "cards": [1483959291685, 1483959293217]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **unsuspend**

  Unsuspend cards by card ID; returns `true` if successful (at least one card was previously suspended) or `false`
  otherwise.

  _Sample request_:

  ```json
  {
    "action": "unsuspend",
    "version": 5,
    "params": {
      "cards": [1483959291685, 1483959293217]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **areSuspended**

  Returns an array indicating whether each of the given cards is suspended (in the same order).

  _Sample request_:

  ```json
  {
    "action": "areSuspended",
    "version": 5,
    "params": {
      "cards": [1483959291685, 1483959293217]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [false, true],
    "error": null
  }
  ```

- **areDue**

  Returns an array indicating whether each of the given cards is due (in the same order). _Note_: cards in the
  learning queue with a large interval (over 20 minutes) are treated as not due until the time of their interval has
  passed, to match the way Anki treats them when reviewing.

  _Sample request_:

  ```json
  {
    "action": "areDue",
    "version": 5,
    "params": {
      "cards": [1483959291685, 1483959293217]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [false, true],
    "error": null
  }
  ```

- **getIntervals**

  Returns an array of the most recent intervals for each given card ID, or a 2-dimensional array of all the intervals
  for each given card ID when `complete` is `true`. Negative intervals are in seconds and positive intervals in days.

  _Sample request 1_:

  ```json
  {
    "action": "getIntervals",
    "version": 5,
    "params": {
      "cards": [1502298033753, 1502298036657]
    }
  }
  ```

  _Sample result 1_:

  ```json
  {
    "result": [-14400, 3],
    "error": null
  }
  ```

  _Sample request 2_:

  ```json
  {
    "action": "getIntervals",
    "version": 5,
    "params": {
      "cards": [1502298033753, 1502298036657],
      "complete": true
    }
  }
  ```

  _Sample result 2_:

  ```json
  {
    "result": [
      [-120, -180, -240, -300, -360, -14400],
      [-120, -180, -240, -300, -360, -14400, 1, 3]
    ],
    "error": null
  }
  ```

- **findCards**

  Returns an array of card IDs for a given query. Functionally identical to `guiBrowse` but doesn't use the GUI for
  better performance.

  _Sample request_:

  ```json
  {
    "action": "findCards",
    "version": 5,
    "params": {
      "query": "deck:current"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [1494723142483, 1494703460437, 1494703479525],
    "error": null
  }
  ```

- **cardsToNotes**

  Returns an unordered array of note IDs for the given card IDs. For cards with the same note, the ID is only given
  once in the array.

  _Sample request_:

  ```json
  {
    "action": "cardsToNotes",
    "version": 5,
    "params": {
      "cards": [1502098034045, 1502098034048, 1502298033753]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [1502098029797, 1502298025183],
    "error": null
  }
  ```

- **cardsInfo**

  Returns a list of objects containing for each card ID the card fields, front and back sides including CSS, note
  type, the note that the card belongs to, and deck name, as well as ease and interval.

  _Sample request_:

  ```json
  {
    "action": "cardsInfo",
    "version": 5,
    "params": {
      "cards": [1498938915662, 1502098034048]
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [
      {
        "answer": "back content",
        "question": "front content",
        "deckName": "Default",
        "modelName": "Basic",
        "fieldOrder": 1,
        "fields": {
          "Front": { "value": "front content", "order": 0 },
          "Back": { "value": "back content", "order": 1 }
        },
        "css": "p {font-family:Arial;}",
        "cardId": 1498938915662,
        "interval": 16,
        "note": 1502298033753
      },
      {
        "answer": "back content",
        "question": "front content",
        "deckName": "Default",
        "modelName": "Basic",
        "fieldOrder": 0,
        "fields": {
          "Front": { "value": "front content", "order": 0 },
          "Back": { "value": "back content", "order": 1 }
        },
        "css": "p {font-family:Arial;}",
        "cardId": 1502098034048,
        "interval": 23,
        "note": 1502298033753
      }
    ],
    "error": null
  }
  ```

#### Media

- **storeMediaFile**

  Stores a file with the specified base64-encoded contents inside the media folder. To prevent Anki from removing
  files not used by any cards (e.g. for configuration files), prefix the filename with an underscore. These files are
  still synchronized to AnkiWeb.

  _Sample request_:

  ```json
  {
    "action": "storeMediaFile",
    "version": 5,
    "params": {
      "filename": "_hello.txt",
      "data": "SGVsbG8sIHdvcmxkIQ=="
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

  _Content of `_hello.txt`_:

  ```
  Hello world!
  ```

- **retrieveMediaFile**

  Retrieves the base64-encoded contents of the specified file, returning `false` if the file does not exist.

  _Sample request_:

  ```json
  {
    "action": "retrieveMediaFile",
    "version": 5,
    "params": {
      "filename": "_hello.txt"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": "SGVsbG8sIHdvcmxkIQ==",
    "error": null
  }
  ```

- **deleteMediaFile**

  Deletes the specified file inside the media folder.

  _Sample request_:

  ```json
  {
    "action": "deleteMediaFile",
    "version": 5,
    "params": {
      "filename": "_hello.txt"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

#### Graphical

- **guiBrowse**

  Invokes the _Card Browser_ dialog and searches for a given query. Returns an array of identifiers of the cards that
  were found.

  _Sample request_:

  ```json
  {
    "action": "guiBrowse",
    "version": 5,
    "params": {
      "query": "deck:current"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": [1494723142483, 1494703460437, 1494703479525],
    "error": null
  }
  ```

- **guiAddCards**

  Invokes the _Add Cards_ dialog.

  _Sample request_:

  ```json
  {
    "action": "guiAddCards",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

- **guiCurrentCard**

  Returns information about the current card or `null` if not in review mode.

  _Sample request_:

  ```json
  {
    "action": "guiCurrentCard",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": {
      "answer": "back content",
      "question": "front content",
      "deckName": "Default",
      "modelName": "Basic",
      "fieldOrder": 0,
      "fields": {
        "Front": { "value": "front content", "order": 0 },
        "Back": { "value": "back content", "order": 1 }
      },
      "cardId": 1498938915662,
      "buttons": [1, 2, 3]
    },
    "error": null
  }
  ```

- **guiStartCardTimer**

  Starts or resets the `timerStarted` value for the current card. This is useful for deferring the start time to when
  it is displayed via the API, allowing the recorded time taken to answer the card to be more accurate when calling
  `guiAnswerCard`.

  _Sample request_:

  ```json
  {
    "action": "guiStartCardTimer",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **guiShowQuestion**

  Shows question text for the current card; returns `true` if in review mode or `false` otherwise.

  _Sample request_:

  ```json
  {
    "action": "guiShowQuestion",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **guiShowAnswer**

  Shows answer text for the current card; returns `true` if in review mode or `false` otherwise.

  _Sample request_:

  ```json
  {
    "action": "guiShowAnswer",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **guiAnswerCard**

  Answers the current card; returns `true` if succeeded or `false` otherwise. Note that the answer for the current
  card must be displayed before before any answer can be accepted by Anki.

  _Sample request_:

  ```json
  {
    "action": "guiAnswerCard",
    "version": 5,
    "params": {
      "ease": 1
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **guiDeckOverview**

  Opens the _Deck Overview_ dialog for the deck with the given name; returns `true` if succeeded or `false` otherwise.

  _Sample request_:

  ```json
  {
    "action": "guiDeckOverview",
    "version": 5,
    "params": {
      "name": "Default"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **guiDeckBrowser**

  Opens the _Deck Browser_ dialog.

  _Sample request_:

  ```json
  {
    "action": "guiDeckBrowser",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```

- **guiDeckReview**

  Starts review for the deck with the given name; returns `true` if succeeded or `false` otherwise.

  _Sample request_:

  ```json
  {
    "action": "guiDeckReview",
    "version": 5,
    "params": {
      "name": "Default"
    }
  }
  ```

  _Sample result_:

  ```json
  {
    "result": true,
    "error": null
  }
  ```

- **guiExitAnki**

  Schedules a request to gracefully close Anki. This operation is asynchronous, so it will return immediately and
  won't wait until the Anki process actually terminates.

  _Sample request_:

  ```json
  {
    "action": "guiExitAnki",
    "version": 5
  }
  ```

  _Sample result_:

  ```json
  {
    "result": null,
    "error": null
  }
  ```
