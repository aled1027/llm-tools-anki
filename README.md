# llm-tools-anki

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/aled1027/llm-tools-anki/blob/main/LICENSE)

Manage Anki cards with the LLM tool.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-tools-anki
```

## Usage

```bash
llm -T Anki "4444 * 233423" --td
```

```bash
llm -T Anki "my friend miguel loves learning about languages. find a cool card that I can share with him that I've been studying." --td
```

```bash
llm -T Anki "Add 5 new cards to the default deck. The five cards should ask about the colors in spanish for a language learning student" --td --chain-limit 25
```

```bash
llm -T Anki -T web_search "I'm interviewing with Miguel Conner for a data science position in a few hours. Research him and create a few anki cards in my default deck for me to study." --td --chain-limit 50
```

## Development

To set up this plugin locally, first checkout the code. Then use [uv](https://astral.sh/)

```bash
uv sync --all-extras
uv run python -m pip install -e '.[test]'
```

## How It Works

[AnkiConnect](https://ankiweb.net/shared/info/2055492159) enables external applications to interact with Anki. With it, we can read cards, update cards, add cards, delete cards and manage decks.j

Also: https://foosoft.net/projects/anki-connect

Docs adapted from README in https://github.com/amikey/anki-connect.

## Additional Resources

- [Simon's blog post llm tools](https://simonwillison.net/2025/May/27/llm-tools/)
- [llm-tools-sqlite](https://github.com/simonw/llm-tools-sqlite/tree/main) (for reference code)
- [llm tools cookiecutter template](https://github.com/simonw/llm-plugin-tools)
- [discord message on --chain-limit](https://discord.com/channels/823971286308356157/1128504153841336370/1388261616583442502)
- [Homepage for AnkiConnect](https://foosoft.net/projects/anki-connect)
- [anki-connect-mcp](https://github.com/spacholski1225/anki-connect-mcp)

test change
