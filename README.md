# llm-tools-anki

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/aled1027/llm-tools-anki/blob/main/LICENSE)

Manage Anki cards with the LLM tool.

## Installation

```bash
# Install the LLM tools Anki plugin
llm install llm-tools-anki
```

## Basic Usage

```bash
# Set ChatGPT 4o as your default model (recommended)
llm models default 4o

# Create your first card
llm -T Anki "Add a card about photosynthesis to my default deck" --chain-limit 50
```

## 📚 Usage Examples

### 🎓 Creating Educational Cards

```bash
# Language learning cards
llm -T Anki "Add 5 Spanish color vocabulary cards to my default deck" --chain-limit 50

# Science concepts
llm -T Anki "Create 3 cards about the water cycle for my science deck" --chain-limit 50

# Programming concepts
llm -T Anki "Add 4 Python function cards to my coding deck" --chain-limit 50
```

### 🎵 Adding Audio to Cards

```bash
# Generate audio for existing cards
llm -T Anki "Add audio to all cards in my Spanish deck" --chain-limit 50

# Create new cards with audio
llm -T Anki "Create 3 French pronunciation cards with audio" --chain-limit 50
```

### 🖼️ Adding Images

```bash
# Add images to cards without them
llm -T Anki "Add relevant images to all cards in my geography deck" --chain-limit 50

# Create cards with images
llm -T Anki "Create 5 animal cards with images for my biology deck" --chain-limit 50
```

### Use Chain Limits for Complex Operations

```bash
# For operations involving multiple steps
llm -T Anki "complex operation..." --chain-limit 50
```

### Combine with Other LLM Tools

```bash
# Use web search for research-based cards
llm -T Anki -T web_search "Research topic and create cards" --chain-limit 50
```

### Specify HTML Formatting for Rich Content

```bash
llm -T Anki "
Create cards with HTML formatting:
- Use <b> for bold text
- Use <pre><code> for code blocks
- Use <img> for images
" --chain-limit 30
```

### Use Tags for Organization

```bash
llm -T Anki "Add cards with tags: biology, chapter1, exam-prep" --chain-limit 50
```

### More Prompts

```bash
# Evolve and improve existing cards
llm -T Anki "Take cards in my 'Evolve' deck and make them more engaging while testing the same concepts" --chain-limit 50

# Research-based cards
llm -T Anki -T web_search "Research quantum computing and create 5 cards for my tech deck" --chain-limit 50

# Bulk card creation with specific formatting
llm -T Anki "
Create 10 PyTorch cards for my 'pytorch' deck with these requirements:
- Use HTML formatting only (no markdown)
- Code blocks should use <pre><code>...</code></pre>
- Each card tests ONE atomic concept
- Include one comprehensive card at the end
" --chain-limit 50
```

## Configuration

### Setting Up Audio Generation (Gemini TTS)

1. **Get a Google Cloud API Key:**

   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Go to **APIs & Services > Credentials**
   - Create an API key
   - Enable **Text-to-Speech API**

2. **Configure the API Key:**
   ```bash
   llm keys set gemini YOUR_API_KEY_HERE
   ```

### Setting Up Image Search (Unsplash)

1. **Get an Unsplash API Key:**

   - Visit [Unsplash Developers](https://unsplash.com/developers)
   - Create an account and register your application
   - Get your Access Key

2. **Configure the API Key:**
   ```bash
   llm keys set unsplash YOUR_UNSPLASH_ACCESS_KEY
   ```

## More Example Prompts

## Development

### Local Setup

```bash
# Clone the repository
git clone https://github.com/aled1027/llm-tools-anki.git
cd llm-tools-anki

# Install dependencies with uv
uv sync --all-extras
uv run python -m pip install -e '.[test]'
```

### Running Tests

```bash
uv run pytest tests/
```

## Additional Resources

- [Simon's LLM Tools Blog Post](https://simonwillison.net/2025/May/27/llm-tools/) - Learn about LLM tools
- [LLM Tools SQLite](https://github.com/simonw/llm-tools-sqlite) - Reference implementation
- [LLM Tools Template](https://github.com/simonw/llm-plugin-tools) - Create your own tools
- [AnkiConnect Documentation](https://foosoft.net/projects/anki-connect) - API reference
- [AnkiConnect MCP](https://github.com/spacholski1225/anki-connect-mcp) - Alternative implementation

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
