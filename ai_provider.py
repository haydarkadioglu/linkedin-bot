"""
AI Provider module — OpenAI-compatible multi-provider content generation.
"""

import os
import logging
import requests

log = logging.getLogger("linkedin-bot")

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
    """Read provider settings from environment variables."""
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    api_key = os.getenv("AI_API_KEY", "")
    model = os.getenv("AI_MODEL", "")
    base_url = os.getenv("AI_BASE_URL", "")

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Try: {', '.join(SUPPORTED_PROVIDERS.keys())}"
        )

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

    Args:
        prompt: The user prompt.
        system_prompt: Optional system-level instruction.

    Returns:
        Generated text content.
    """
    provider, config = get_provider_config()
    model = config.get("default_model")
    api_key = config.get("api_key", "")
    base_url = config.get("base_url")

    headers = {"Content-Type": "application/json"}
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

    log.info("🤖 Generating content via %s/%s...", provider, model)

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
        log.info("✅ Content generated (%d chars)", len(content))
        return content
    except Exception as e:
        log.warning("⚠️ AI generation failed: %s", e)
        raise


def auto_generate_topic() -> str:
    """Auto-generate a short, engaging LinkedIn post topic."""
    return generate_content(
        "Suggest one short, engaging LinkedIn post topic about technology, "
        "productivity, or AI trends. Just give the topic title, nothing else.",
        system_prompt="You are a LinkedIn content strategist.",
    )


def generate_post(topic: str = "", style: str = "professional") -> str:
    """
    Generate a full LinkedIn post on a given topic with a specified style.

    Args:
        topic: The post topic. Auto-generated if empty.
        style: Writing style (professional, casual, inspirational).

    Returns:
        The full post text.
    """
    prompt = (
        f"Write a LinkedIn post about: {topic or 'a trending tech topic'}\n"
        f"Style: {style}\n"
        "Make it engaging, include 3-5 short paragraphs, use emojis sparingly, "
        "and end with a question to encourage comments."
    )
    return generate_content(
        prompt,
        system_prompt="You are a LinkedIn influencer with 100k+ followers.",
    )
