#!/usr/bin/env python3
"""
Official Meta Instagram Graph API Publisher for Brian B. Avants, Ph.D. (@antsx.ai / @cingulate.ai)
Supports single-image posts, multi-image carousels, dry-run inspection, and cron/GitHub Actions automation.

Prerequisites (One-Time 5-Minute Meta Setup):
1. Create your Instagram account (e.g. @antsx.ai or @cingulate.ai) in the mobile app.
2. In Instagram Settings -> Account Type and Tools -> Switch to a free "Creator" or "Business" account.
3. Link it to a Facebook Page & generate a token at https://developers.facebook.com/tools/explorer/
   with permissions: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`.
4. Export environment variables:
   export IG_USER_ID="178414..."
   export IG_ACCESS_TOKEN="EAAB..."
   export IG_PUBLIC_BASE_URL="https://stnava.github.io/CV/instagram/"
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

GRAPH_API_BASE = "https://graph.facebook.com/v21.0"


def graph_post(endpoint: str, params: dict) -> dict:
    url = f"{GRAPH_API_BASE}/{endpoint.lstrip('/')}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def publish_single_image(ig_user_id: str, access_token: str, image_url: str, caption: str, dry_run: bool = False) -> dict:
    if dry_run:
        print(f"[DRY-RUN] Would create container for image_url={image_url}")
        print(f"[DRY-RUN] Caption ({len(caption)} chars):\n{caption}\n" + "-" * 60)
        return {"id": "dry_run_media_id", "status": "DRY_RUN_OK"}

    # Step 1: Create media container
    container = graph_post(
        f"{ig_user_id}/media",
        {
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token,
        },
    )
    creation_id = container["id"]
    print(f"Created media container: {creation_id}. Waiting 5s for processing...")
    time.sleep(5)

    # Step 2: Publish container
    published = graph_post(
        f"{ig_user_id}/media_publish",
        {
            "creation_id": creation_id,
            "access_token": access_token,
        },
    )
    print(f"Successfully published Instagram post! Media ID: {published['id']}")
    return published


def publish_carousel(ig_user_id: str, access_token: str, image_urls: list[str], caption: str, dry_run: bool = False) -> dict:
    if dry_run:
        print(f"[DRY-RUN] Would create {len(image_urls)}-slide CAROUSEL:")
        for idx, u in enumerate(image_urls, 1):
            print(f"  Slide {idx}: {u}")
        print(f"[DRY-RUN] Caption ({len(caption)} chars):\n{caption}\n" + "-" * 60)
        return {"id": "dry_run_carousel_id", "status": "DRY_RUN_OK"}

    child_ids = []
    for url in image_urls:
        item = graph_post(
            f"{ig_user_id}/media",
            {
                "image_url": url,
                "is_carousel_item": "true",
                "access_token": access_token,
            },
        )
        child_ids.append(item["id"])
        time.sleep(2)

    carousel_container = graph_post(
        f"{ig_user_id}/media",
        {
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "caption": caption,
            "access_token": access_token,
        },
    )
    creation_id = carousel_container["id"]
    time.sleep(5)

    published = graph_post(
        f"{ig_user_id}/media_publish",
        {
            "creation_id": creation_id,
            "access_token": access_token,
        },
    )
    print(f"Successfully published Instagram Carousel! Media ID: {published['id']}")
    return published


def main():
    parser = argparse.ArgumentParser(description="Publish Visual CV posts to Instagram via Official Meta Graph API.")
    parser.add_argument("--manifest", default=str(Path(__file__).parent / "posts" / "posts_manifest.json"))
    parser.add_argument("--post-id", help="Specific post id to publish (e.g. post_01_visual_cv), or 'all' for full launch grid.")
    parser.add_argument("--carousel", action="store_true", help="Publish selected posts as a multi-slide carousel.")
    parser.add_argument("--list", action="store_true", help="List available post IDs in the manifest.")
    parser.add_argument("--dry-run", action="store_true", help="Preview API payloads without sending to Meta.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Manifest not found at {manifest_path}. Run generate_posts.py first.", file=sys.stderr)
        sys.exit(1)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    posts = manifest["posts"]
    if args.list:
        for idx, p in enumerate(posts, 1):
            print(f"{idx:02d}. {p['id']} — {p.get('png') or p.get('svg')}")
        return

    ig_user_id = os.environ.get("IG_USER_ID", "YOUR_IG_USER_ID")
    access_token = os.environ.get("IG_ACCESS_TOKEN", "YOUR_IG_ACCESS_TOKEN")
    base_url = os.environ.get("IG_PUBLIC_BASE_URL", manifest.get("public_gh_pages_base_url", "https://stnava.github.io/CV/instagram/"))

    dry_run = args.dry_run or (ig_user_id == "YOUR_IG_USER_ID" or access_token == "YOUR_IG_ACCESS_TOKEN")
    if dry_run and not args.dry_run:
        print("Note: IG_USER_ID / IG_ACCESS_TOKEN not set in environment; running in --dry-run preview mode.\n")

    if args.post_id and args.post_id != "all":
        posts = [p for p in posts if p["id"] == args.post_id]
        if not posts:
            print(f"No post matching --post-id {args.post_id}", file=sys.stderr)
            sys.exit(1)

    if args.carousel:
        urls = [urllib.parse.urljoin(base_url, p.get("png") or p.get("svg")) for p in posts]
        publish_carousel(ig_user_id, access_token, urls, posts[0]["caption"], dry_run=dry_run)
        return

    for post in posts:
        rel_img = post.get("png") or post.get("svg")
        public_img_url = urllib.parse.urljoin(base_url, rel_img)
        publish_single_image(ig_user_id, access_token, public_img_url, post["caption"], dry_run=dry_run)


if __name__ == "__main__":
    main()
