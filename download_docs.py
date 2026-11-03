import ssl
import urllib.request
from pathlib import Path

DOCS = {
    "AI": {
        "attention_is_all_you_need.pdf": "https://arxiv.org/pdf/1706.03762",
        "mit_6.7960_lec01.pdf": "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/mit6_7960_f24_lec1.pdf",
        "mit_6.7960_lec02.pdf": "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/mit6_7960_f24_lec2.pdf",
        "mit_6.7960_lec21.pdf": "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/mit6_7960_f24_lec21.pdf",
    },
    "QuantFinance": {
        "mit_18.S096_lecnote10.pdf": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/0d3edf3e95c22b1b217a0ec8b59d8ecc_MIT18_S096F13_lecnote10.pdf",
        "mit_18.S096_lecnote14.pdf": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/bba02164ba6642f7d516df35347aec01_MIT18_S096F13_lecnote14.pdf",
        "mit_18.S096_lecnote19.pdf": "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/d19208c017ada04f9261cfb41ab8d702_MIT18_S096F13_lecnote19.pdf",
        "frey_continuous_time_finance.pdf": "https://www.wu.ac.at/fileadmin/wu/d/i/statmath/Publications/Publications_Frey/Lecture_notes/CTF-lecture-notes.pdf",
    },
    "SoftwareArchitecture": {
        "isaqb_curriculum_foundation.pdf": "https://public.isaqb.org/curriculum-foundation/curriculum-foundation-en.pdf",
        "mit_6.170_lec18.pdf": "https://www.ocw.mit.edu/courses/6-170-laboratory-in-software-engineering-fall-2005/fa369ca6db4b5e3d7833fbf362c59962_lec18.pdf",
        "ait_patterns.pdf": "https://www.cs.ait.ac.th/~mdailey/class/sw-arch/07-Patternsx2.pdf",
    },
}

for category, files in DOCS.items():
    folder = Path("documents") / category
    folder.mkdir(parents=True, exist_ok=True)
    for name, url in files.items():
        target = folder / name
        if target.exists():
            print(f"schon da: {category}/{name}")
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            # Zertifikatsprüfung nur für den WU-Server abschalten
            ctx = ssl._create_unverified_context() if "wu.ac.at" in url else None
            with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                data = r.read()
            if not data.startswith(b"%PDF"):
                raise ValueError("Antwort ist kein PDF")
            target.write_bytes(data)
            print(f"OK:       {category}/{name} ({len(data) // 1024} KB)")
        except Exception as e:
            print(f"FEHLER:   {category}/{name} -> {e}")