#!/usr/bin/env python3
"""Keep static site long-form links current without replacing older video cards."""
from __future__ import annotations

import html
import re
from pathlib import Path
from yt_dlp import YoutubeDL

CHANNEL = "https://www.youtube.com/@MarksAccidentallyObsessed/videos"
START = "<!-- BEGIN AUTO LONG-FORM VIDEOS -->"
END = "<!-- END AUTO LONG-FORM VIDEOS -->"
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
WATCH_LINK = re.compile(r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})")


def fetch_long_form():
    settings = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "extract_flat": "in_playlist",
        "playlistend": 24,
        "skip_download": True,
        "socket_timeout": 25,
        "retries": 2,
    }
    with YoutubeDL(settings) as ydl:
        response = ydl.extract_info(CHANNEL, download=False)
    if not response or not response.get("entries"):
        raise RuntimeError("YouTube returned no channel video entries; leaving site unchanged")

    results = []
    for item in response["entries"]:
        if not item:
            continue
        video_id = item.get("id", "")
        if not VIDEO_ID.fullmatch(video_id):
            continue
        duration = item.get("duration")
        # The channel /videos tab excludes Shorts. Confirm duration where
        # available rather than adding short clips to a long-form gallery.
        if duration is not None and duration < 180:
            continue
        title = (item.get("title") or "").strip()
        if not title or title in ("[Private video]", "[Deleted video]"):
            continue
        results.append((video_id, title))
        if len(results) == 8:
            break
    if not results:
        raise RuntimeError("No public long-form uploads found; leaving site unchanged")
    return results


def gallery_card(video_id, title):
    safe_title = html.escape(title, quote=True)
    return (
        '        <a class="card product" href="https://www.youtube.com/watch?v=' + video_id
        + '" target="_blank" rel="noopener">\n'
        + '          <img src="https://i.ytimg.com/vi/' + video_id
        + '/hqdefault.jpg" alt="' + safe_title + ' thumbnail" loading="lazy" />\n'
        + '          <h3>' + safe_title + '</h3>\n'
        + '          <p>Watch the full deep dive on YouTube.</p>\n'
        + '        </a>'
    )


def home_card(video_id, title):
    safe_title = html.escape(title, quote=True)
    return (
        '          <a class="video-item" href="https://www.youtube.com/watch?v='
        + video_id + '" target="_blank" rel="noopener">\n'
        + '            <img src="https://i.ytimg.com/vi/' + video_id
        + '/hqdefault.jpg" alt="' + safe_title + ' thumbnail" loading="lazy" />\n'
        + '            <div><h3>' + safe_title
        + '</h3><p>Watch the long-form video on YouTube.</p></div>\n'
        + '          </a>'
    )


def refresh_page(path, opener, videos, card_fn, limit):
    file = Path(path)
    content = file.read_text(encoding="utf-8")
    # Exclude previously generated cards from the duplicate check.
    static_only = re.sub(
        re.escape(START) + r".*?" + re.escape(END), "", content, flags=re.S
    )
    archived_ids = set(WATCH_LINK.findall(static_only))
    to_add = [(vid, title) for vid, title in videos[:limit] if vid not in archived_ids]
    auto_html = START + "\n" + "\n".join(
        card_fn(vid, title) for vid, title in to_add
    ) + "\n        " + END

    if START in content and END in content:
        content = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            lambda _match: auto_html, content, count=1, flags=re.S,
        )
    else:
        if opener not in content:
            raise RuntimeError(f"Could not locate video list in {path}")
        content = content.replace(opener, opener + "\n        " + auto_html, 1)

    # Both pages have exactly one featured YouTube player.
    content = re.sub(
        r'(iframe src="https://www\.youtube\.com/embed/)[A-Za-z0-9_-]{11}',
        lambda m: m.group(1) + videos[0][0],
        content, count=1,
    )
    if content != file.read_text(encoding="utf-8"):
        file.write_text(content, encoding="utf-8")
        print(f"Refreshed {path} with {len(to_add)} new cards")
    else:
        print(f"No changes in {path}")


def main():
    videos = fetch_long_form()
    print(f"Newest full-length upload: {videos[0][1]} ({videos[0][0]})")
    refresh_page("videos.html", '<div class="shop-grid">', videos, gallery_card, 8)
    refresh_page("index.html", '<div class="video-list">', videos, home_card, 4)


if __name__ == "__main__":
    main()
