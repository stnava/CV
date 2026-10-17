#!/usr/bin/env python3
"""
Automated Instagram Visual CV & Publication Card Generator for Brian B. Avants, Ph.D.
Generates 1080x1080 SVG & PNG slides + posts_manifest.json for the Instagram Graph API.
Also parses avantsCV.bib to auto-generate "Paper Spotlight" cards for new publications.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

POSTS = [
    {
        "id": "post_01_visual_cv",
        "pinned": True,
        "badge": "PINNED · VISUAL CV",
        "title": "BRIAN B. AVANTS, Ph.D.",
        "subtitle": "AI & Machine Learning Executive\nComputational Anatomy Pioneer",
        "metric": "57,000+ Citations · h-index: 71",
        "footer": "Founder, Cingulate LLC · Creator of ANTsX · stnava.github.io",
        "gradient": ("#0f172a", "#1d4ed8"),
        "accent": "#60a5fa",
        "bullets": [
            "Co-Creator & Lead Architect: ANTs, ANTsPy, ANTsR, ANTsPyNet, ANTsPyMM",
            "Creator of SyN, N4ITK, Eigenanatomy, SiMLR & NSA-Flow (PyTorch)",
            "Ex-Senior Director of ML (Invicro) & Biomarkers Lead (Biogen)",
            "Visiting Associate Professor of Radiology & Medical Imaging (UVA)",
        ],
        "caption": (
            "Brian B. Avants, Ph.D. — Visual Executive CV 🧠⚡\n\n"
            "For 20+ years, my focus has been translating rigorous mathematical foundations "
            "(diffeomorphisms, manifold optimization, multi-view representation learning) into "
            "open-source software and clinical trial biomarkers.\n\n"
            "🔹 57,000+ Citations · h-index: 71 · 180+ Peer-Reviewed Papers\n"
            "🔹 Co-Creator of the ANTsX Ecosystem (ANTs, ANTsPy, ANTsR, ANTsPyNet, ANTsPyMM)\n"
            "🔹 6x #1 Ranked in International Medical Imaging Benchmarks (Klein, EMPIRE10, BRATS, SATA)\n"
            "🔹 Founder & Principal @ Cingulate LLC (Portsmouth, NH)\n\n"
            "Full interactive CV & Resume at link in bio (stnava.github.io/CV).\n\n"
            "#Neuroimaging #MachineLearning #ComputationalAnatomy #ANTsX #MedicalAI #Biomarkers #PyTorch #DataScience"
        ),
    },
    {
        "id": "post_02_nature_cover",
        "pinned": True,
        "badge": "PINNED · CLINICAL TRIAL IMPACT",
        "title": "BEHIND THE NATURE COVER",
        "subtitle": "Quantitative Amyloid PET Analytics\nin the Phase 1b PRIME Trial",
        "metric": "Nature (2016) · J. Nucl. Med. (2018)",
        "footer": "Biogen Translational & Advanced Analytics · Aducanumab Program",
        "gradient": ("#31102f", "#be185d"),
        "accent": "#f472b6",
        "bullets": [
            "Lead integrative imaging data scientist for Aducanumab (Aduhelm)",
            "Confirmatory amyloid PET SUVR reference & target region optimization",
            "Created Figure 1 & primary visualization for the 2016 Nature cover story",
            "Longitudinal rs-fMRI network biomarkers in amyloid-positive cohorts",
        ],
        "caption": (
            "How rigorous reference-region math and quantitative PET analytics helped shape a landmark "
            "Nature cover story (Sevigny et al., Nature 2016; Chiao et al., J Nucl Med 2018).\n\n"
            "During my time leading Translational & Advanced Analytics (Biomarkers) at Biogen, "
            "we demonstrated how reference/target region selection in Amyloid PET SUVR directly impacts "
            "longitudinal treatment effect detection in Alzheimer's disease clinical trials.\n\n"
            "#Alzheimers #ClinicalTrials #AmyloidPET #Neuroimaging #Biotech #Biomarkers #NatureJournal #ANTsX"
        ),
    },
    {
        "id": "post_03_antsx_ecosystem",
        "pinned": True,
        "badge": "PINNED · OPEN-SOURCE ECOSYSTEM",
        "title": "THE ANTsX ECOSYSTEM",
        "subtitle": "Quantitative Biological &\nMedical Imaging at Global Scale",
        "metric": "Scientific Reports (2021, 2024)",
        "footer": "github.com/ANTsX · C++ · Python · R · Deep Learning",
        "gradient": ("#064e3b", "#059669"),
        "accent": "#34d399",
        "bullets": [
            "ANTs (C++): SyN diffeomorphic registration, N4 bias correction, Atropos, DiReCT",
            "ANTsPy & ANTsPyNet: Pre-trained 2D/3D CNNs, Deep Atropos, HippMapp3r, Brain Age",
            "ANTsPyMM: Automated multi-modal MRI phenotyping & QC for clinical trials",
            "ANTsR & subtyper: Statistical imaging, SCCAN, SiMLR & longitudinal staging",
        ],
        "caption": (
            "The ANTsX Ecosystem: 18+ years of open-source medical image registration, morphometry, "
            "and deep learning (Tustison et al., Scientific Reports 2021 & 2024).\n\n"
            "From foundational C++ diffeomorphisms (SyN) and bias correction (N4ITK) to pre-trained "
            "PyTorch/TensorFlow networks in ANTsPyNet and automated multi-modal trial QC in ANTsPyMM.\n\n"
            "Explore the code: github.com/ANTsX\n\n"
            "#OpenSource #ANTsX #ANTsPy #MedicalImaging #DeepLearning #Neuroscience #Python #RStats #ITK"
        ),
    },
    {
        "id": "post_04_nsa_flow",
        "pinned": False,
        "badge": "PYTORCH · REPRESENTATION LEARNING",
        "title": "NSA-FLOW",
        "subtitle": "Non-Negative Stiefel Approximating Flow\nfor Interpretable Embeddings",
        "metric": "arXiv:2511.06425 · github.com/stnava/nsa_flow",
        "footer": "Smooth Geometry Near the Stiefel Manifold · PyTorch",
        "gradient": ("#1e1b4b", "#6d28d9"),
        "accent": "#c084fc",
        "bullets": [
            "Unifies sparse matrix factorization, orthogonalization & manifold learning",
            "Continuous balance between reconstruction fidelity & column decorrelation",
            "Proximal non-negativity updates + adaptive gradient control in PyTorch",
            "Extracts stable, biological networks in neuroimaging, genomics & text",
        ],
        "caption": (
            "Introducing NSA-Flow (Non-Negative Stiefel Approximating Flow): Orthogonalish Matrix "
            "Optimization for Interpretable Embeddings (arXiv:2511.06425).\n\n"
            "High-dimensional biomedical data (MRI, genomics, multi-omics) demands latent features "
            "that are both sparse and non-redundant. NSA-Flow operates as a smooth flow near the "
            "Stiefel manifold with proximal updates—delivering interpretable representations that "
            "generalize across cohorts.\n\n"
            "Code: github.com/stnava/nsa_flow\n\n"
            "#PyTorch #MachineLearning #ManifoldLearning #MatrixFactorization #InterpretableAI #Genomics #Neuroimaging"
        ),
    },
    {
        "id": "post_05_simlr",
        "pinned": False,
        "badge": "NATURE COMPUTATIONAL SCIENCE",
        "title": "SiMLR MULTI-VIEW AI",
        "subtitle": "Similarity-Driven Multi-View Embeddings\nfrom High-Dimensional Biomedical Data",
        "metric": "Nature Computational Science (2021)",
        "footer": "Formulated at ICERM (Brown University) · ANTsR / ANTsX",
        "gradient": ("#172554", "#0284c7"),
        "accent": "#38bdf8",
        "bullets": [
            "Jointly embeds structural MRI, rs-fMRI, diffusion MRI & genomics",
            "Exploits inter-modality similarity across noisy, high-dimensional views",
            "Superior signal recovery vs. classical CCA, PCA & unregularized SVD",
            "Deployed in UK Biobank, depression genetics & military neurotrauma",
        ],
        "caption": (
            "How do you fuse structural MRI, functional connectivity, diffusion tensors, and genetics "
            "when every modality has thousands of dimensions?\n\n"
            "Developed during my Visiting Scholar fellowship at Brown University's ICERM and published "
            "in Nature Computational Science (Avants, Tustison & Stone, 2021), SiMLR projects "
            "multi-modal biomedical data into joint, biologically interpretable low-dimensional spaces.\n\n"
            "#NatureComputationalScience #MultiModalAI #BrainMapping #DataScience #Mathematics #ICERM #ANTsX"
        ),
    },
    {
        "id": "post_06_blast_tbi",
        "pinned": False,
        "badge": "DEFENSE & NEUROTRAUMA · UVA",
        "title": "MAPPING INVISIBLE WOUNDS",
        "subtitle": "Neuroinflammation & Network Effects of\nRepetitive Blast Exposure",
        "metric": "Journal of Neurotrauma (2020, 2022, 2024)",
        "footer": "University of Virginia · LIMBIC-CENC · Normative Neuroimaging Library",
        "gradient": ("#3f2e05", "#d97706"),
        "accent": "#fbbf24",
        "bullets": [
            "Multi-view TSPO PET + MRI analysis in Special Operations personnel",
            "Quantifies neuroinflammation & volume changes from repetitive blast exposure",
            "Co-architect of the demographically diverse Normative Neuroimaging Library",
            "Supports next-generation TBI diagnostic & therapeutic development",
        ],
        "caption": (
            "Quantifying the neurological effects of repetitive low-level blast overpressure in career "
            "breachers and Special Operations personnel (Stone, Avants, Tustison et al., Journal of "
            "Neurotrauma 2020, 2022, 2024).\n\n"
            "By combining multi-view machine learning (SiMLR) with TSPO PET neuroinflammation imaging "
            "and the Normative Neuroimaging Library, we can detect subtle, network-level brain changes "
            "invisible to conventional clinical reads.\n\n"
            "#TraumaticBrainInjury #Neurotrauma #Neuroimaging #PETImaging #MilitaryHealth #Biomarkers #UVA"
        ),
    },
    {
        "id": "post_07_biobank_scale",
        "pinned": False,
        "badge": "POPULATION NEUROSCIENCE",
        "title": "49,000+ BRAINS MAPPED",
        "subtitle": "Population-Scale Phenotyping Across\nUK Biobank, PPMI & ADNI",
        "metric": "Nature Medicine (2024) · Sci. Reports (2024)",
        "footer": "ANTsX Structural Phenotypes · Aligned-UMAP · ICLR 2023",
        "gradient": ("#0f172a", "#0d9488"),
        "accent": "#2dd4bf",
        "bullets": [
            "ANTsX structural phenotypes across the UK Biobank (Scientific Reports 2024)",
            "Brain aging patterns across 49,482 individuals (Nature Medicine 2024)",
            "Multimodal patient representation learning with missing modalities (ICLR 2023)",
            "Longitudinal Parkinson's disease subtyping via Aligned-UMAP (Patterns 2023)",
        ],
        "caption": (
            "Scaling precision neuroimaging from single-subject diffeomorphisms to 49,000+ individuals "
            "(Scientific Reports 2024; Nature Medicine 2024; ICLR 2023; Patterns 2023).\n\n"
            "Standardized, reproducible Image Derived Phenotypes (IDPs) and longitudinal manifold "
            "embeddings allow us to chart brain aging trajectories and subtype Parkinson's & "
            "Alzheimer's progression years before symptom onset.\n\n"
            "#UKBiobank #PPMI #Parkinsons #Alzheimers #PrecisionMedicine #ICLR #NatureMedicine #BigData"
        ),
    },
    {
        "id": "post_08_syn_n4",
        "pinned": False,
        "badge": "FOUNDATIONAL ALGORITHMS",
        "title": "SyN & N4ITK",
        "subtitle": "The Mathematical Foundations Behind\n13,500+ Citations",
        "metric": "Med. Image Anal. (2008) · IEEE TMI (2010)",
        "footer": "Physical Coordinate Invariance · #1 in Klein (2009) & EMPIRE10 (2010)",
        "gradient": ("#1e1b4b", "#4f46e5"),
        "accent": "#818cf8",
        "bullets": [
            "SyN: Symmetric geodesic diffeomorphic registration with cross-correlation",
            "N4ITK: Improved B-spline bias field correction for MRI intensity uniformity",
            "Strictly respects physical space orientation, spacing & direction cosines",
            "2026 evolution: Deep Computational Anatomy via Multiview Normalizing Flows",
        ],
        "caption": (
            "Why physical coordinate invariance and diffeomorphic symmetry still matter in the era of "
            "deep learning.\n\n"
            "When we introduced SyN (Avants et al., Medical Image Analysis 2008) and N4ITK (Tustison, "
            "Avants et al., IEEE TMI 2010), our goal was garantizar invertible, symmetric, physically "
            "grounded mappings across anatomy. In 2026, those same principles power Deep Computational "
            "Anatomy via Latent-Aligned Multiview Normalizing Flows.\n\n"
            "#Diffeomorphisms #ComputationalAnatomy #IEEE #MedicalImageAnalysis #ComputerVision #Math"
        ),
    },
    {
        "id": "post_09_cingulate_llc",
        "pinned": False,
        "badge": "VENTURE & ADVISORY · PORTSMOUTH, NH",
        "title": "CINGULATE LLC",
        "subtitle": "Boutique AI, Computational Anatomy &\nClinical Trial Biomarker Consultancy",
        "metric": "Founded 2018 · Portsmouth, NH",
        "footer": "antsx@antsx.com · stnava.github.io/CV",
        "gradient": ("#090d16", "#2563eb"),
        "accent": "#60a5fa",
        "bullets": [
            "Custom AI/ML architecture for biotech, pharma & defense clinical trials",
            "End-to-end multi-modal MRI/PET/CT biomarker pipelines (ANTsPyMM)",
            "Concurrent 3D super-resolution & longitudinal disease staging (subtyper)",
            "Direct principal advisory by Brian B. Avants, Ph.D.",
        ],
        "caption": (
            "Through Cingulate LLC (Portsmouth, NH), I partner with biotech, pharmaceutical, defense, "
            "and academic teams to design high-sensitivity imaging biomarkers, automated multi-modal "
            "QC pipelines, and interpretable AI architectures.\n\n"
            "📩 Reach out at antsx@antsx.com or explore my updated Executive Resume & CV at "
            "stnava.github.io/CV.\n\n"
            "#CingulateLLC #BiotechConsulting #PharmaAI #ClinicalTrials #PortsmouthNH #Neuroimaging #AIExecutive"
        ),
    },
]


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def wrap_line(text: str, width: int = 54) -> list[str]:
    words = text.split()
    lines, current = [], []
    count = 0
    for w in words:
        if count + len(w) + (1 if current else 0) > width:
            lines.append(" ".join(current))
            current = [w]
            count = len(w)
        else:
            current.append(w)
            count += len(w) + (1 if len(current) > 1 else 0)
    if current:
        lines.append(" ".join(current))
    return lines


def build_svg(post: dict) -> str:
    c1, c2 = post["gradient"]
    accent = post["accent"]
    badge = xml_escape(post["badge"])
    title = xml_escape(post["title"])
    sub_lines = [xml_escape(x) for x in post["subtitle"].split("\n")]
    metric = xml_escape(post["metric"])
    footer = xml_escape(post["footer"])

    bullet_svg = []
    y_cursor = 560
    for b in post["bullets"]:
        wrapped = wrap_line(b, width=52)
        bullet_svg.append(
            f'<rect x="88" y="{y_cursor - 18}" width="12" height="12" rx="3" fill="{accent}" />'
        )
        for idx, line in enumerate(wrapped):
            bullet_svg.append(
                f'<text x="118" y="{y_cursor}" fill="#e2e8f0" font-family="Helvetica, Arial, sans-serif" '
                f'font-size="25" font-weight="500">{xml_escape(line)}</text>'
            )
            y_cursor += 34
        y_cursor += 16

    sub_svg = []
    sy = 330
    for sline in sub_lines:
        sub_svg.append(
            f'<text x="84" y="{sy}" fill="#cbd5e1" font-family="Helvetica, Arial, sans-serif" '
            f'font-size="33" font-weight="600">{sline}</text>'
        )
        sy += 44

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}" />
      <stop offset="100%" stop-color="{c2}" />
    </linearGradient>
    <radialGradient id="glow" cx="85%" cy="15%" r="55%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.28" />
      <stop offset="100%" stop-color="{c1}" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Background -->
  <rect width="1080" height="1080" fill="url(#bg)" />
  <rect width="1080" height="1080" fill="url(#glow)" />

  <!-- Subtle Diffeomorphic Grid / Mesh Lines -->
  <g stroke="#ffffff" stroke-opacity="0.06" stroke-width="1.5" fill="none">
    <path d="M 0 180 Q 540 120 1080 200" />
    <path d="M 0 360 Q 540 300 1080 380" />
    <path d="M 0 540 Q 540 480 1080 560" />
    <path d="M 0 720 Q 540 660 1080 740" />
    <path d="M 0 900 Q 540 840 1080 920" />
    <path d="M 180 0 Q 120 540 200 1080" />
    <path d="M 540 0 Q 480 540 560 1080" />
    <path d="M 900 0 Q 840 540 920 1080" />
  </g>

  <!-- Outer Card Frame -->
  <rect x="44" y="44" width="992" height="992" rx="28" fill="#090d16" fill-opacity="0.48" stroke="#ffffff" stroke-opacity="0.16" stroke-width="2" />

  <!-- Top Badge -->
  <rect x="84" y="92" width="520" height="46" rx="23" fill="{accent}" fill-opacity="0.18" stroke="{accent}" stroke-opacity="0.6" stroke-width="1.5" />
  <text x="112" y="122" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="20" font-weight="bold">{badge}</text>

  <!-- Main Title -->
  <text x="84" y="242" fill="#ffffff" font-family="Helvetica, Arial, sans-serif" font-size="56" font-weight="bold">{title}</text>

  <!-- Subtitle -->
  {"".join(sub_svg)}

  <!-- Metric Pill -->
  <rect x="84" y="420" width="912" height="68" rx="14" fill="#ffffff" fill-opacity="0.08" stroke="{accent}" stroke-opacity="0.5" stroke-width="1.5" />
  <text x="114" y="463" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="27" font-weight="bold">{metric}</text>

  <!-- Bullets -->
  {"".join(bullet_svg)}

  <!-- Divider & Footer -->
  <line x1="84" y1="935" x2="996" y2="935" stroke="#ffffff" stroke-opacity="0.18" stroke-width="1.5" />
  <text x="84" y="982" fill="#94a3b8" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="bold">{footer}</text>
  <text x="996" y="982" text-anchor="end" fill="{accent}" font-family="Courier, monospace" font-size="22" font-weight="bold">@antsx.ai</text>
</svg>
"""


def parse_recent_bib_entries(bib_path: Path, min_year: int = 2024) -> list[dict]:
    if not bib_path.exists():
        return []
    content = bib_path.read_text(encoding="utf-8", errors="ignore")
    entries = re.findall(r"@\w+\s*\{([^,]+),([\s\S]*?)\n\}", content)
    results = []
    for key, body in entries:
        year_m = re.search(r"year\s*=\s*\{?(\d{4})\}?", body, re.IGNORECASE)
        if not year_m or int(year_m.group(1)) < min_year:
            continue
        title_m = re.search(r"title\s*=\s*\{([^\}]+)\}", body, re.IGNORECASE)
        journal_m = re.search(r"(?:journal|booktitle)\s*=\s*\{([^\}]+)\}", body, re.IGNORECASE)
        results.append(
            {
                "key": key.strip(),
                "year": int(year_m.group(1)),
                "title": title_m.group(1).strip() if title_m else key,
                "venue": journal_m.group(1).strip() if journal_m else "Preprint / Journal",
            }
        )
    return results


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "posts"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for post in POSTS:
        svg_path = out_dir / f"{post['id']}.svg"
        png_path = out_dir / f"{post['id']}.png"
        if png_path.exists():
            png_path.unlink()
        svg_content = build_svg(post)
        svg_path.write_text(svg_content, encoding="utf-8")

        # Convert SVG to 1080x1080 PNG using macOS CoreGraphics (qlmanage) or ImageMagick
        converted = False
        for cmd in [
            ["/usr/bin/qlmanage", "-t", "-s", "1080", "-o", str(out_dir), str(svg_path)],
            ["/opt/homebrew/bin/magick", str(svg_path), str(png_path)],
        ]:
            try:
                subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                ql_png = out_dir / f"{svg_path.name}.png"
                if ql_png.exists():
                    ql_png.rename(png_path)
                    converted = True
                    break
                if png_path.exists():
                    converted = True
                    break
            except Exception:
                pass

        manifest.append(
            {
                "id": post["id"],
                "pinned": post["pinned"],
                "title": post["title"],
                "svg": f"posts/{svg_path.name}",
                "png": f"posts/{png_path.name}" if converted else None,
                "caption": post["caption"],
            }
        )

    bib_path = Path(__file__).resolve().parent.parent / "avantsCV.bib"
    recent_papers = parse_recent_bib_entries(bib_path, min_year=2024)

    manifest_data = {
        "account_recommendations": ["@antsx.ai", "@cingulate.ai", "@brianavants.ai", "@diffeomorphic"],
        "public_gh_pages_base_url": "https://stnava.github.io/CV/instagram/",
        "posts": manifest,
        "auto_detected_recent_bib_entries": recent_papers,
    }

    manifest_path = out_dir / "posts_manifest.json"
    manifest_path.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    print(f"Generated {len(manifest)} Instagram posts and {len(recent_papers)} BibTeX spotlight records in {out_dir}")


if __name__ == "__main__":
    main()
