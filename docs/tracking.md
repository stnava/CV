# Project Tracking — Brian B. Avants CV & Executive Portfolio (`stnava/CV`)

| Field | Value |
| :--- | :--- |
| **Current Version** | `v2026.10.0` |
| **Current Phase** | Phase 2 — Multi-Format Executive CV/Resume & Social Automation Complete |
| **Next Work Package** | WP-04 — Optional YouTube / Shorts Automated Video Pipeline |
| **Blockers** | None (Meta Graph API tokens optional for live Instagram scheduling) |
| **Last Updated** | 2026-10-17 |

---

## Work Packages

| ID | Work Package | Status | Deliverables |
| :--- | :--- | :--- | :--- |
| **WP-01** | **Executive 2-Page Resume Modernization** | `done` | `src/avants_resume.tex`, `src/avants_resume.pdf`, `BrianAvants_Resume.pdf`, `BrianAvants_Resume.docx`, `BrianAvants_Resume.md`, `resume.html` |
| **WP-02** | **Comprehensive 11-Page CV Update (2018–2026)** | `done` | `src/BrianAvants_CV.tex`, `src/BrianAvants_CV.pdf`, `BrianAvants_CV.pdf`, `BrianAvants_CV.docx`, `BrianAvants_CV.md`, `index.html`, `indexbase.html`, `avantsCV.bib`, `compile` |
| **WP-03** | **Instagram Visual CV & Automated Publishing Suite** | `done` | `instagram_cv_concept.html`, `instagram/generate_posts.py`, `instagram/publish_instagram.py`, `instagram/posts/*`, `.github/workflows/instagram_publish.yml` |
| **WP-04** | **Social Media & YouTube Automation Strategy Docs** | `done` | `docs/social_media_and_youtube_strategy.md`, `README.md` |

---

## Session Log

### 2026-10-17 — Release `v2026.10.0`: Multi-Format Executive Portfolio & Instagram Visual CV Suite
- **Summary**: Completed comprehensive modernization of Dr. Brian B. Avants' CV (11 pages) and Executive Resume (2 pages) across LaTeX, PDF, Word (`.docx`), Markdown (`.md`), and responsive HTML (`index.html`, `resume.html`). Added 2018–2026 publications (`avantsCV.bib`), grant funding, and executive roles (Cingulate LLC, UVA, Invicro). Built automated Instagram Visual CV slide generator (`instagram/generate_posts.py`), Meta Graph API publisher (`instagram/publish_instagram.py`), GitHub Actions workflow (`.github/workflows/instagram_publish.yml`), interactive preview (`instagram_cv_concept.html`), and social/YouTube automation strategy documentation (`docs/social_media_and_youtube_strategy.md`).
- **Verification**:
  - LaTeX builds (`src/avants_resume.tex` -> 2 pages, `src/BrianAvants_CV.tex` -> 11 pages) verified with zero errors.
  - Instagram slide generator verified (`9/9` 1080×1080 PNG/SVG slides and `posts_manifest.json` rendered cleanly).
  - Meta Graph API publisher CLI (`--list`, `--dry-run`) verified.
