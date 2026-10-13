def inject_styles():
    return """
    <style>
        :root {
            --bg: #07151d;
            --bg-soft: #0d1f2b;
            --panel: #112534;
            --panel-alt: #143244;
            --line: rgba(255,255,255,0.08);
            --text: #ebf5ef;
            --muted: #b9c8c2;
            --gold: #f4d68f;
            --mint: #91e7c5;
            --peach: #f7b38e;
            --shadow: rgba(0,0,0,0.35);
        }

        .main {
            background: linear-gradient(180deg, #07151d 0%, #0a1c28 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }

        .stApp > header {
            background: rgba(7,21,29,0.7);
            backdrop-filter: blur(10px);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(22,36,48,0.92), rgba(13,25,33,0.96));
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.2rem;
        }

        .stRadio {
            color: var(--text);
        }

        .stRadio > div {
            gap: 0.45rem;
        }

        .stRadio label {
            color: var(--muted);
            padding: 0.45rem 0.6rem;
            border-radius: 10px;
            transition: background 0.2s ease;
        }

        .stRadio label:hover {
            background: rgba(255,255,255,0.03);
        }

        .stRadio [data-baseweb="radio"] {
            accent-color: var(--mint);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 0.55rem 0.9rem;
            color: var(--muted);
        }

        .stTabs [data-baseweb="tab-selected"] {
            background: linear-gradient(135deg, rgba(144, 231, 197, 0.18), rgba(244, 214, 143, 0.12));
            color: var(--text);
            border-color: rgba(144, 231, 197, 0.4);
        }

        .hero {
            background: linear-gradient(135deg, rgba(19, 39, 52, 0.96), rgba(12, 26, 36, 1));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 26px;
            padding: 2rem 2rem 1.5rem;
            box-shadow: 0 18px 40px var(--shadow);
            margin-bottom: 1.5rem;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(144,231,197,0.14);
            color: var(--mint);
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            border: 1px solid rgba(144,231,197,0.25);
            font-size: 0.76rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 1.1rem;
            font-weight: 700;
        }

        .hero-title {
            font-size: clamp(2.5rem, 5vw, 4rem);
            line-height: 1.05;
            margin: 0 0 0.6rem;
            letter-spacing: -0.06em;
            font-weight: 800;
            color: var(--text);
        }

        .hero-subtitle {
            font-size: clamp(1.05rem, 2vw, 1.5rem);
            color: var(--muted);
            max-width: 62ch;
            margin: 0;
        }

        .cta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1.2rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            padding: 0.65rem 1rem;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.03);
            color: var(--text);
            font-weight: 600;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }

        .pill--accent {
            background: linear-gradient(135deg, rgba(244,214,143,0.18), rgba(144,231,197,0.18));
            border-color: rgba(244,214,143,0.2);
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }

        .card {
            background: linear-gradient(180deg, rgba(16,33,43,0.96), rgba(12,24,31,1));
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.25rem;
            box-shadow: 0 12px 28px var(--shadow);
            min-height: 180px;
        }

        .card h3 {
            color: var(--text);
            margin: 0 0 0.5rem;
            font-size: 1.2rem;
        }

        .card p {
            color: var(--muted);
            margin: 0;
            line-height: 1.6;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin: 1rem 0 2rem;
        }

        .stat {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 1rem 1.1rem;
        }

        .stat .value {
            color: var(--gold);
            font-size: 1.8rem;
            font-weight: 800;
            line-height: 1.1;
            display: block;
        }

        .stat .label {
            color: var(--muted);
            font-size: 0.9rem;
            margin-top: 0.2rem;
        }

        .example-list {
            list-style: none;
            padding: 0;
            margin: 1rem 0 0;
        }

        .example-list li {
            color: var(--text);
            font-size: 1.08rem;
            line-height: 2;
            padding-left: 0.3rem;
        }

        .example-list li::before {
            content: "•";
            color: var(--mint);
            font-weight: 700;
            margin-right: 0.7rem;
        }

        .info-box {
            background: linear-gradient(135deg, rgba(244,214,143,0.12), rgba(144,231,197,0.11));
            border: 1px solid rgba(244,214,143,0.18);
            border-radius: 18px;
            padding: 1.1rem 1.2rem;
            color: var(--text);
            margin-top: 1.3rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }

        h1, h2, h3, h4, p {
            color: var(--text);
        }

        .stAlert {
            border-radius: 16px;
            border: 1px solid rgba(244,214,143,0.25);
        }

        .stButton > button {
            border-radius: 12px;
            background: linear-gradient(135deg, #f4d68f, #91e7c5);
            color: #0d1c28;
            border: none;
            font-weight: 700;
            padding: 0.65rem 1rem;
        }

        .stButton > button:hover {
            box-shadow: 0 10px 22px rgba(144,231,197,0.2);
        }
    </style>
    """
