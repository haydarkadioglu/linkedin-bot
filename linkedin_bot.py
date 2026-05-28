#!/usr/bin/env python3
"""
LinkedIn Bot - Bağımsız AI Agent
LinkedIn API üzerinden otomatik paylaşım yapar.
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


def post_to_linkedin(token: str, person_urn: str, message: str) -> dict:
    """
    LinkedIn v2 API (ugcPosts) ile metin paylaşımı yapar.
    
    Args:
        token: LinkedIn OAuth access token
        person_urn: Kullanıcının URN'si (örn. urn:li:person:xxx)
        message: Paylaşılacak metin
        
    Returns:
        API yanıtı (dict)
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
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    log.info(f"📤 LinkedIn'e paylaşım gönderiliyor: {message[:60]}...")

    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        json=payload,
        headers=headers
    )

    if response.status_code in (200, 201):
        post_id = response.json().get("id", response.headers.get("X-RestLi-Id", "unknown"))
        log.info(f"✅ Paylaşım başarılı! Post ID: {post_id}")
        return {"status": "success", "post_id": post_id}
    else:
        log.error(f"❌ Hata {response.status_code}: {response.text}")
        return {"status": "error", "code": response.status_code, "detail": response.text}


def verify_token(token: str) -> dict:
    """Token'ın geçerliliğini kontrol eder ve person URN döndürür."""
    headers = {
        "Authorization": f"Bearer {token}",
    }
    r = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
    if r.status_code == 200:
        data = r.json()
        sub = data.get("sub", "")
        return {"status": "success", "sub": sub, "data": data}
    return {"status": "error", "code": r.status_code, "detail": r.text}


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Bot - Otomatik Paylaşım")
    parser.add_argument("--token", help="LinkedIn access token",
                       default=os.getenv("LINKEDIN_TOKEN"))
    parser.add_argument("--person-urn", help="LinkedIn person URN",
                       default=os.getenv("LINKEDIN_PERSON_URN"))
    parser.add_argument("--message", help="Paylaşılacak mesaj", required=True)
    parser.add_argument("--verify", help="Sadece token'ı doğrula", action="store_true")

    args = parser.parse_args()

    if not args.token:
        log.error("❌ Token bulunamadı. --token argümanı veya LINKEDIN_TOKEN ortam değişkeni kullanın.")
        sys.exit(1)

    if args.verify:
        result = verify_token(args.token)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "success" else 1)

    if not args.person_urn:
        log.error("❌ Person URN bulunamadı. --person-urn argümanı veya LINKEDIN_PERSON_URN ortam değişkeni kullanın.")
        sys.exit(1)

    result = post_to_linkedin(args.token, args.person_urn, args.message)

    if result["status"] == "success":
        print(json.dumps(result, indent=2))
        sys.exit(0)
    else:
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
