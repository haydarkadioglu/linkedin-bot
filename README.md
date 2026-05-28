# LinkedIn Bot

> 🤖 Created and managed by **Koza Agent** — [github.com/haydarkadioglu/koza-agent](https://github.com/haydarkadioglu/koza-agent)  
> An autonomous AI agent system that builds and manages other agents.

An independent AI agent designed to automate LinkedIn posting via the official LinkedIn API.  
Comes with built-in **AI content generation** via multiple providers.

## Features
- ✅ LinkedIn API v2 (ugcPosts) integration
- ✅ OAuth 2.0 token management & verification
- ✅ **AI-powered post generation** — 5 supported providers
- ✅ Auto topic suggestion
- ✅ Multiple post styles: professional, casual, inspirational
- ✅ CLI & environment variable support

## Supported AI Providers

| Provider   | Default Model         | Env Value   |
|------------|----------------------|-------------|
| OpenAI     | `gpt-4`              | `openai`    |
| DeepSeek   | `deepseek-chat`      | `deepseek`  |
| Ollama     | `llama3`             | `ollama`    |
| Kimi       | `moonshot-v1-8k`     | `kimi`      |
| MiniMax    | `abab6.5-chat`       | `minimax`   |

All providers use the OpenAI-compatible `/chat/completions` API.

## Installation

```bash
git clone https://github.com/haydarkadioglu/linkedin-bot.git
cd linkedin-bot

python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

### List supported providers
```bash
python linkedin_bot.py --list-providers
```

### Verify your LinkedIn token
```bash
python linkedin_bot.py --token "YOUR_TOKEN" --verify
```

### Post a custom message
```bash
python linkedin_bot.py \
  --token "YOUR_TOKEN" \
  --person-urn "urn:li:person:xxx" \
  --message "Hello LinkedIn! 🚀"
```

### AI-powered auto posting 🧠
```bash
# Let AI generate a topic + post (default: OpenAI)
python linkedin_bot.py \
  --token "YOUR_TOKEN" \
  --person-urn "urn:li:person:xxx" \
  --ai

# Use DeepSeek instead
python linkedin_bot.py \
  --token "YOUR_TOKEN" \
  --person-urn "urn:li:person:xxx" \
  --ai --provider deepseek

# Specify a custom topic
python linkedin_bot.py \
  --token "YOUR_TOKEN" \
  --person-urn "urn:li:person:xxx" \
  --ai --topic "The future of autonomous agents"

# Casual style
python linkedin_bot.py \
  --token "YOUR_TOKEN" \
  --person-urn "urn:li:person:xxx" \
  --ai --style casual
```

### Using environment variables
Create a `.env` file:
```env
LINKEDIN_TOKEN=your_token_here
LINKEDIN_PERSON_URN=urn:li:person:xxx
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxxxxxxxxxxx
```

Then just run:
```bash
python linkedin_bot.py --message "Your post"
# or
python linkedin_bot.py --ai
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LINKEDIN_TOKEN` | LinkedIn OAuth 2.0 access token |
| `LINKEDIN_PERSON_URN` | Your LinkedIn person URN |
| `AI_PROVIDER` | AI provider name (`openai`, `deepseek`, `ollama`, `kimi`, `minimax`) |
| `AI_API_KEY` | API key for your chosen provider |
| `AI_MODEL` | Override the default model (optional) |
| `AI_BASE_URL` | Override API base URL (optional) |

## License

MIT
