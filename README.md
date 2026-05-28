# LinkedIn Bot

> 🤖 Created and managed by **Koza Agent** — Autonomous AI Agent System

An independent AI agent designed to automate LinkedIn posting via the official LinkedIn API.

## Features
- LinkedIn API v2 (ugcPosts) integration
- OAuth 2.0 token management
- Automatic text sharing (PUBLIC visibility)
- Token verification utility
- CLI & environment variable support

## Installation

```bash
# Clone the repo
git clone https://github.com/haydarkadioglu/linkedin-bot.git
cd linkedin-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Verify your token
```bash
python linkedin_bot.py --token "YOUR_TOKEN" --verify
```

### Post to LinkedIn
```bash
python linkedin_bot.py \
  --token "YOUR_TOKEN" \
  --person-urn "urn:li:person:xxx" \
  --message "Hello LinkedIn! 🚀"
```

### Using environment variables
Create a `.env` file:
```env
LINKEDIN_TOKEN=your_token_here
LINKEDIN_PERSON_URN=urn:li:person:xxx
```

Then just run:
```bash
python linkedin_bot.py --message "Your post content"
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LINKEDIN_TOKEN` | LinkedIn OAuth 2.0 access token |
| `LINKEDIN_PERSON_URN` | Your LinkedIn person URN (e.g. `urn:li:person:abc123`) |

## License

MIT
