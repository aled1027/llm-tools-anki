# llm-tools-anki

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/aled1027/llm-tools-anki/blob/main/LICENSE)

Manage Anki cards with the LLM tool

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-tools-anki
```

## Usage

```bash
llm -T anki "4444 * 233423" --td
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
