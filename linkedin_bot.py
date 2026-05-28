#!/usr/bin/env python3
"""
LinkedIn Bot — Autonomous AI Agent
Powered by Koza Agent. Fully independent with AI content generation.
"""

import os
import sys
import json
import argparse
import logging
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("linkedin-bot")

load_dotenv()


# ── AI Provider ──────────────────────────────────────────────────────────────

SUPPORTED_PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
    },
    "ollama": {
        "base_url": "http://localhost:11434",
        "default_model": "llama3",
    },
    "kimi": {
        "base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-8k",
    },
    "minimax": {
        "base_url": "https://api.minimax.io/v1",
        "default_model": "abab6.5-chat",
    },
}


def get_provider_config():
    """Read provider settings from environment."""
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    api_key = os.getenv("AI_API_KEY", "")
    model = os.getenv("AI_MODEL", "")
    base_url = os.getenv("AI_BASE_URL", "")

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}. Try: {', '.join(SUPPORTED_PROVIDERS.keys())}")

    config = dict(SUPPORTED_PROVIDERS[provider])
    if api_key:
        config["api_key"] = api_key
    if model:
        config["default_model"] = model
    if base_url:
        config["base_url"] = base_url

    return provider, config


def generate_content(prompt: str, system_prompt: str = "") -> str:
    """
    Generate text using the configured AI provider (OpenAI-compatible API).
    Returns the generated content string.
    """
    provider, config = get_provider_config()
    model = config.get("default_model")
    api_key = config.get("api_key", "")
    base_url = config.get("base_url")

    headers = {
        "Content-Type": "application/json",
    }

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 500,
    }

    log.info(f"🤖 Generating content via {provider}/{model}...")

    try:
        resp = requests.post(
            f"{base_url}/chat/completions",
            json=payload,
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        log.info(f"✅ Content generated ({len(content)} chars)")
        return content
    except Exception as e:
        log.warning(f"⚠️ AI generation failed: {e}")
        raise


def auto_generate_topic() -> str:
    """Auto-generate a LinkedIn post topic."""
    return generate_content(
        "Suggest one short, engaging LinkedIn post topic about technology, productivity, or AI trends. "
        "Just give the topic title, nothing else.",
        system_prompt="You are a LinkedIn content strategist."
    )


def generate_post(topic: str = "", style: str = "professional") -> str:
    """Generate a full LinkedIn post on the given topic."""
    prompt = (
        f"Write a LinkedIn post about: {topic or 'a trending tech topic'}\n"
        f"Style: {style}\n"
        "Make it engaging, include 3-5 short paragraphs, use emojis sparingly, "
        "and end with a question to encourage comments."
    )
    return generate_content(prompt, system_prompt="You are a LinkedIn influencer with 100k+ followers.")


# ── LinkedIn API ─────────────────────────────────────────────────────────────

def post_to_linkedin(token: str, person_urn: str, message: str) -> dict:
    """
    LinkedIn v2 API (ugcPosts) ile metin paylaşımı yapar.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": message},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
        },
    }

    log.info(f"📤 Posting to LinkedIn: {message[:60]}...")

    resp = requests.post(
        "https://api.linkedin.com/v2/ugcPosts", json=payload, headers=headers
    )

    if resp.status_code in (200, 201):
        post_id = resp.json().get("id", resp.headers.get("X-RestLi-Id", "unknown"))
        log.info(f"✅ Posted! ID: {post_id}")
        return {"status": "success", "post_id": post_id}
    else:
        log.error(f"❌ Error {resp.status_code}: {resp.text}")
        return {"status": "error", "code": resp.status_code, "detail": resp.text}


def verify_token(token: str) -> dict:
    """Verify LinkedIn token and return person info."""
    r = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )
    if r.status_code == 200:
        data = r.json()
        return {"status": "success", "sub": data.get("sub", ""), "data": data}
    return {"status": "error", "code": r.status_code, "detail": r.text}


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LinkedIn Bot — Autonomous AI Agent")
    parser.add_argument("--token", help="LinkedIn access token", default=os.getenv("LINKEDIN_TOKEN"))
    parser.add_argument("--person-urn", help="LinkedIn person URN", default=os.getenv("LINKEDIN_PERSON_URN"))
    parser.add_argument("--message", help="Post message (optional if AI mode)")
    parser.add_argument("--topic", help="Topic for AI-generated post")
    parser.add_argument("--style", help="Post style: professional | casual | inspirational", default="professional")
    parser.add_argument("--ai", help="Auto-generate post with AI", action="store_true")
    parser.add_argument("--verify", help="Only verify token", action="store_true")
    parser.add_argument("--list-providers", help="List supported AI providers and exit", action="store_true")
    parser.add_argument("--provider", help="Override AI_PROVIDER env")

    args = parser.parse_args()

    # ── List providers ──
    if args.list_providers:
        print("Supported AI providers:")
        for name, cfg in SUPPORTED_PROVIDERS.items():
            print(f"  • {name} — default model: {cfg['default_model']}")
        sys.exit(0)

    # ── Token ──
    token = args.token or os.getenv("LINKEDIN_TOKEN")
    if not token:
        log.error("❌ No token. Use --token or LINKEDIN_TOKEN env.")
        sys.exit(1)

    # ── Verify ──
    if args.verify:
        result = verify_token(token)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "success" else 1)

    # ── Person URN ──
    person_urn = args.person_urn or os.getenv("LINKEDIN_PERSON_URN")
    if not person_urn:
        log.error("❌ No person URN. Use --person-urn or LINKEDIN_PERSON_URN env.")
        sys.exit(1)

    # ── Provider override ──
    if args.provider:
        os.environ["AI_PROVIDER"] = args.provider

    # ── Generate or use message ──
    if args.ai:
        topic = args.topic or auto_generate_topic()
        log.info(f"📝 Generated topic: {topic}")
        message = generate_post(topic, args.style)
        print(f"\n── Generated Post ──\n{message}\n────────────────────\n")
    elif args.message:
        message = args.message
    else:
        log.error("❌ Provide --message or use --ai for AI generation.")
        sys.exit(1)

    # ── Post ──
    result = post_to_linkedin(token, person_urn, message)

    if result["status"] == "success":
        print(json.dumps(result, indent=2))
        sys.exit(0)
    else:
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
