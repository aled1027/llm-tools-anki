# llm-tools-anki

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/aled1027/llm-tools-anki/blob/main/LICENSE)

Manage Anki cards with the LLM tool.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-tools-anki
```

## Usage

I've primarily used the tool with Chatgpt's 4o which can be set to the default llm model with:

```bash
llm models default 4o
```

```bash
llm -T Anki "my friend miguel loves learning about languages. find a cool card that I can share with him that I've been studying." --td
```

```bash
llm -T Anki "Add 5 new cards to the default deck. The five cards should ask about the colors in spanish for a language learning student" --td --chain-limit 25
```

```bash
llm -T Anki "Take the cards in the Evolve deck and adjust them. Make the cards similar, basically testing the same ideas, but make them different to keep the learning interesting and engaging for the learner. Remove any cards that you evolve" --td --chain-limit 50
```

```bash
llm -T Anki "My friend catdog thinks I don't know big words. Add 5 to 10 cards of big words that I should know so I'm not embarrassed. Add these to the default deck." --td --chain-limit 50
```

The follow prompt also requires [llm-tools-exa](https://github.com/daturkel/llm-tools-exa/tree/main) to be installed.

```bash
llm -T Anki -T web_search "I'm interviewing with Miguel Conner for a data science position in a few hours. Research him and create a few anki cards in my default deck for me to study." --td --chain-limit 50
```

An unsplash access key needs to be set for the following prompt with `llm keys set unsplash`. Access keys can be generate on the unsplash website.

```bash
llm -T Anki "For each anki card in the evolve deck without an image (ignore cards with images), use Anki_get_image_url to add an image. Make it visible in the front or back of the card, whichever makes more sense for that card. Make sure that the card is formatted as HTML (not markdown) or the image won't render correctly. The goal of the image is to increase visual appeal and improve memory retention." --td --chain-limit 50
```

The next prompt comes from [Miguel Conner](https://substack.com/@miguelconner/posts). It's a good example of informing the llm how to format code in cards:

```bash
llm -T Anki "
Create Anki flashcards for my 'pytorch' deck with these requirements:
- Use HTML formatting only (no markdown). Code blocks should use <pre><code>...</code></pre>
- Each card should test ONE atomic concept
- Include one comprehensive card at the end that tests understanding of the complete structure

Topic: PyTorch fundamentals and boilerplate code

Focus areas:
1. Basic neural network class structure
2. Essential imports and setup
3. Forward pass implementation
4. Training loop components

Create cards that help memorize the fundamental patterns and syntax needed to build PyTorch models from scratch.
" --chain-limit 50

llm -T Anki "
Replace the front of the card in the evolve deck with an audio version of its current front text.
" --chain-limit 50 --td

llm -T Anki "Create a new card in the evolve deck based on the existing card. This new card should have the front of the card replaced with audio speaking the same content. If audio was generated, pass to add_note with use_front_from_file. When you call generate audio, try to pass the appropriate language code. If passing audio to add_note, dont include it in front, just use use_front_from_file." --chain-limit 50 --td
```

## Development

To set up this plugin locally, first checkout the code. Then use [uv](https://astral.sh/)

```bash
uv sync --all-extras
uv run python -m pip install -e '.[test]'
```

## Additional Resources

- [Simon's blog post llm tools](https://simonwillison.net/2025/May/27/llm-tools/)
- [llm-tools-sqlite](https://github.com/simonw/llm-tools-sqlite/tree/main) (for reference code)
- [llm tools cookiecutter template](https://github.com/simonw/llm-plugin-tools)
- [discord message on --chain-limit](https://discord.com/channels/823971286308356157/1128504153841336370/1388261616583442502)
- [Homepage for AnkiConnect](https://foosoft.net/projects/anki-connect)
- [anki-connect-mcp](https://github.com/spacholski1225/anki-connect-mcp)

## Text-to-Speech (TTS) Support

This plugin supports multiple TTS providers for generating audio content for Anki cards:

### Gemini TTS (Google Text-to-Speech)

To use Gemini TTS, you need to:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to API & Services > Credentials, generate an API key
4. Give the API key access to all services
5. Enable the [Text-to-Speech API](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
6. Set the API key: `llm keys set gemini`
