"""
LinkedIn API module — post and token verification via LinkedIn v2 API.
"""

import logging
import requests

log = logging.getLogger("linkedin-bot")


def post_to_linkedin(token: str, person_urn: str, message: str) -> dict:
    """
    Post a text update to LinkedIn via the v2 ugcPosts API.

    Args:
        token: LinkedIn OAuth access token.
        person_urn: The author's LinkedIn URN (e.g. urn:li:person:xxx).
        message: The post content.

    Returns:
        API response dict with status and post_id on success.
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

    log.info("📤 Posting to LinkedIn: %s...", message[:60])

    resp = requests.post(
        "https://api.linkedin.com/v2/ugcPosts", json=payload, headers=headers
    )

    if resp.status_code in (200, 201):
        post_id = resp.json().get("id", resp.headers.get("X-RestLi-Id", "unknown"))
        log.info("✅ Posted! ID: %s", post_id)
        return {"status": "success", "post_id": post_id}
    else:
        log.error("❌ Error %s: %s", resp.status_code, resp.text)
        return {"status": "error", "code": resp.status_code, "detail": resp.text}


def verify_token(token: str) -> dict:
    """Verify a LinkedIn access token and return user info."""
    r = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )
    if r.status_code == 200:
        data = r.json()
        return {"status": "success", "sub": data.get("sub", ""), "data": data}
    return {"status": "error", "code": r.status_code, "detail": r.text}
