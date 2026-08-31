# Mark's Accidentally Obsessed

Official site for the YouTube channel [Mark's Accidentally Obsessed](https://www.youtube.com/@MarkAccidentallyObsessed).

Rabbit holes. Hobbies. Hyperfixations.

- YouTube: https://www.youtube.com/@MarkAccidentallyObsessed
- TikTok: https://www.tiktok.com/@marksobsessed
- Amazon Associates tag: `markcurrently-20`

## Pages

- `index.html` — home, latest videos, about
- `videos.html` — featured uploads
- `shop.html` — Amazon affiliate shelves using store ID `markcurrently-20`

Channel art lives in `assets/`.

## GitHub Pages

Repo **Settings → Pages → Build and deployment**

- Source: **Deploy from a branch**
- Branch: `main` / `/ (root)`

After that the live URL should be:

https://markymark5127.github.io/MarksAccidentallyObssessed/

If a custom domain is set on the user site, it may appear as:

https://www.markmaynejr.com/MarksAccidentallyObssessed/

## Local preview

```bash
python3 -m http.server 8080
```

Then open http://localhost:8080

## Notes

- Affiliate disclosure is in the footer on every page.
- Shop cards use Amazon search links with `tag=markcurrently-20`. Replace a search URL with a specific ASIN anytime (`https://www.amazon.com/dp/ASIN?tag=markcurrently-20`).
- Featured video IDs can be updated in `index.html` and `videos.html` as new episodes drop.
