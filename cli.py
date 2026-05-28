"""
CLI entry point — argument parsing and orchestration for LinkedIn Bot.
"""

import os
import sys
import json
import argparse
import logging

from dotenv import load_dotenv

from ai_provider import (
    SUPPORTED_PROVIDERS,
    auto_generate_topic,
    generate_post,
)
from linkedin_api import post_to_linkedin, verify_token

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("linkedin-bot")

load_dotenv()


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(description="LinkedIn Bot — Autonomous AI Agent")
    parser.add_argument(
        "--token",
        help="LinkedIn access token",
        default=os.getenv("LINKEDIN_TOKEN"),
    )
    parser.add_argument(
        "--person-urn",
        help="LinkedIn person URN",
        default=os.getenv("LINKEDIN_PERSON_URN"),
    )
    parser.add_argument(
        "--message",
        help="Post message (optional if --ai is used)",
    )
    parser.add_argument("--topic", help="Topic for AI-generated post")
    parser.add_argument(
        "--style",
        help="Post style: professional | casual | inspirational",
        default="professional",
    )
    parser.add_argument(
        "--ai",
        help="Auto-generate post with AI",
        action="store_true",
    )
    parser.add_argument(
        "--verify",
        help="Only verify the token",
        action="store_true",
    )
    parser.add_argument(
        "--list-providers",
        help="List supported AI providers and exit",
        action="store_true",
    )
    parser.add_argument(
        "--provider",
        help="Override AI_PROVIDER env variable",
    )
    return parser


def main():
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # List supported providers
    if args.list_providers:
        print("Supported AI providers:")
        for name, cfg in SUPPORTED_PROVIDERS.items():
            print(f"  \u2022 {name} — default model: {cfg['default_model']}")
        sys.exit(0)

    # Token
    token = args.token or os.getenv("LINKEDIN_TOKEN")
    if not token:
        log.error("No token. Use --token or LINKEDIN_TOKEN env.")
        sys.exit(1)

    # Verify-only mode
    if args.verify:
        result = verify_token(token)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "success" else 1)

    # Person URN
    person_urn = args.person_urn or os.getenv("LINKEDIN_PERSON_URN")
    if not person_urn:
        log.error("No person URN. Use --person-urn or LINKEDIN_PERSON_URN env.")
        sys.exit(1)

    # Provider override
    if args.provider:
        os.environ["AI_PROVIDER"] = args.provider

    # Generate or use provided message
    if args.ai:
        topic = args.topic or auto_generate_topic()
        log.info("Generated topic: %s", topic)
        message = generate_post(topic, args.style)
        print(f"\n--- Generated Post ---\n{message}\n---------------------\n")
    elif args.message:
        message = args.message
    else:
        log.error("Provide --message or use --ai for AI generation.")
        sys.exit(1)

    # Post to LinkedIn
    result = post_to_linkedin(token, person_urn, message)

    if result["status"] == "success":
        print(json.dumps(result, indent=2))
        sys.exit(0)
    else:
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
