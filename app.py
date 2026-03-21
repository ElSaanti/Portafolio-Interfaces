import streamlit as st
import streamlit.components.v1 as components
import yaml
from pathlib import Path

st.set_page_config(
    page_title="SMV - Portafolio",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  [data-testid="stAppViewContainer"] { background: #fff; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).parent

@st.cache_data
def load_projects():
    with open(BASE_DIR / "projects.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

data = load_projects()

# Color por categoria
CATEGORY_COLORS = {
    "Computer Vision":  "#1a1a1a",
    "Text Analysis":    "#2d4a3e",
    "Translation":      "#3a2d4a",
    "Machine Learning": "#4a2d2d",
    "NLP":              "#2d3a4a",
    "Sentiment Analysis":"#4a3a2d",
    "OCR":              "#2d4a4a",
    "Data Analysis":    "#3a4a2d",
    "Streamlit":        "#4a2d3a",
}

def get_color(category):
    return CATEGORY_COLORS.get(category, "#1a1a1a")

def render_card(project, index):
    num_str = str(index).zfill(2)
    desc = project.get("description", "")
    desc_html = f'<p class="card-desc">{desc}</p>' if desc else ""
    color = get_color(project.get("category", ""))
    return f"""
    <a class="card" href="{project['url']}" target="_blank" style="--card-color: {color};">
      <div class="card-header">
        <span class="card-num">{num_str}</span>
        <span class="card-cat">{project.get('category', '')}</span>
      </div>
      <div class="card-content">
        <div class="card-num-bg">{num_str}</div>
        <h3 class="card-title">{project['title']}</h3>
        {desc_html}
      </div>
      <div class="card-footer-row">
        <span class="card-link">Ver proyecto &nbsp;&#x2192;</span>
      </div>
    </a>
    """

def render_panel(key, panel_id):
    portfolio = data.get(key, {})
    projects  = portfolio.get("projects", [])
    title     = portfolio.get("title", "")
    if not projects:
        content = """
        <div class="coming-soon">
          <p class="cs-label">proximamente</p>
          <p class="cs-title">Portafolio 2</p>
          <p class="cs-sub">Los proyectos se agregaran durante el semestre.</p>
        </div>"""
        count = "sin proyectos aun"
    else:
        cards = "".join(render_card(p, p["id"]) for p in projects)
        content = f'<div class="grid">{cards}</div>'
        count = f"{len(projects)} proyectos"
    return f"""
    <div class="panel" id="{panel_id}">
      <div class="panel-head">
        <h2 class="panel-title">{title}</h2>
        <span class="panel-count">{count}</span>
      </div>
      {content}
    </div>"""

p1 = render_panel("portfolio_1", "panel-1")
p2 = render_panel("portfolio_2", "panel-2")

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;600&family=Noto+Sans+JP:wght@300;400&display=swap" rel="stylesheet">
<style>

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --white: #ffffff;
  --black: #0d0d0d;
  --grey:  #f5f5f5;
  --line:  #c8c8c8;
  --muted: #999999;
  --small: 0.67rem;
}}

html, body {{
  background: var(--white);
  color: var(--black);
  font-family: 'Noto Sans JP', sans-serif;
  font-weight: 300;
  -webkit-font-smoothing: antialiased;
}}

/* ---- HEADER ---- */
header {{
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 3rem 4rem 2.2rem;
  border-bottom: 2px solid var(--black);
  flex-wrap: wrap;
  gap: 1.5rem;
}}

.site-name {{
  font-family: 'Shippori Mincho', serif;
  font-size: clamp(1.8rem, 3vw, 2.8rem);
  font-weight: 500;
  letter-spacing: -0.03em;
  line-height: 1;
}}

.site-sub {{
  font-size: var(--small);
  color: var(--muted);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-top: 0.5rem;
}}

nav {{ display: flex; }}

.nav-btn {{
  font-family: 'Noto Sans JP', sans-serif;
  font-size: var(--small);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  padding: 0.55rem 1.6rem;
  cursor: pointer;
  border: 1px solid var(--black);
  background: var(--white);
  color: var(--black);
  transition: all 0.2s;
  margin-left: -1px;
}}
.nav-btn.active {{ background: var(--black); color: var(--white); }}
.nav-btn:not(.active):hover {{ background: var(--grey); }}

/* ---- MAIN ---- */
main {{ padding: 0 4rem 8rem; }}

.panel-head {{
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: 3.5rem 0 2.5rem;
  border-bottom: 1px solid var(--line);
  margin-bottom: 3rem;
  flex-wrap: wrap;
  gap: 1rem;
}}

.panel-title {{
  font-family: 'Shippori Mincho', serif;
  font-size: clamp(1.3rem, 2vw, 1.8rem);
  font-weight: 500;
  letter-spacing: -0.02em;
}}

.panel-count {{
  font-size: var(--small);
  color: var(--muted);
  letter-spacing: 0.15em;
}}

/* ---- GRID ---- */
.grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
}}

/* ---- CARD ---- */
.card {{
  display: flex;
  flex-direction: column;
  background: var(--white);
  text-decoration: none;
  color: inherit;
  overflow: hidden;
  animation: fadeUp 0.5s ease both;
  transition: background 0.2s;
  min-height: 240px;
}}

.card:hover {{
  background: var(--card-color, #1a1a1a);
}}

.card:hover .card-num,
.card:hover .card-cat,
.card:hover .card-title,
.card:hover .card-link,
.card:hover .card-desc {{
  color: rgba(255,255,255,0.9);
}}

.card:hover .card-num-bg {{
  color: rgba(255,255,255,0.06);
}}

.card:hover .card-cat {{
  border-color: rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.08);
}}

.card:hover .card-footer-row {{
  border-top-color: rgba(255,255,255,0.15);
}}

/* ---- CARD HEADER ---- */
.card-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.6rem 0;
}}

.card-num {{
  font-size: 0.6rem;
  letter-spacing: 0.22em;
  color: var(--muted);
  transition: color 0.2s;
}}

.card-cat {{
  font-size: 0.54rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  background: var(--grey);
  padding: 0.18rem 0.5rem;
  border: 1px solid var(--line);
  transition: color 0.2s, background 0.2s, border-color 0.2s;
}}

/* ---- CARD CONTENT ---- */
.card-content {{
  flex: 1;
  padding: 0.8rem 1.6rem 1rem;
  position: relative;
  overflow: hidden;
}}

.card-num-bg {{
  position: absolute;
  bottom: -1.5rem;
  right: -0.5rem;
  font-family: 'Shippori Mincho', serif;
  font-size: 7rem;
  font-weight: 600;
  color: rgba(0,0,0,0.04);
  line-height: 1;
  pointer-events: none;
  transition: color 0.2s;
  user-select: none;
}}

.card-title {{
  font-family: 'Shippori Mincho', serif;
  font-size: 1.1rem;
  font-weight: 500;
  line-height: 1.4;
  letter-spacing: -0.01em;
  position: relative;
  z-index: 1;
  transition: color 0.2s;
}}

.card-desc {{
  font-size: 0.73rem;
  line-height: 1.85;
  color: #777;
  margin-top: 0.5rem;
  position: relative;
  z-index: 1;
  transition: color 0.2s;
}}

/* ---- CARD FOOTER ---- */
.card-footer-row {{
  padding: 0.9rem 1.6rem 1.2rem;
  border-top: 1px solid var(--line);
  transition: border-color 0.2s;
}}

.card-link {{
  font-size: 0.6rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--black);
  transition: color 0.2s;
}}

/* ---- COMING SOON ---- */
.coming-soon {{
  padding: 7rem 0;
  text-align: center;
  border: 1px solid var(--line);
}}
.cs-label {{
  font-size: var(--small);
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 1.2rem;
}}
.cs-title {{
  font-family: 'Shippori Mincho', serif;
  font-size: clamp(2.5rem, 6vw, 5rem);
  color: var(--line);
  letter-spacing: -0.03em;
}}
.cs-sub {{
  font-size: 0.74rem;
  color: var(--muted);
  margin-top: 0.8rem;
}}

/* ---- FOOTER ---- */
footer {{
  border-top: 2px solid var(--black);
  padding: 1.4rem 4rem;
  display: flex;
  justify-content: space-between;
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
  flex-wrap: wrap;
  gap: 0.5rem;
}}

/* ---- TOGGLE ---- */
.panel {{ display: none; }}
.panel.active {{ display: block; }}

/* ---- ANIMATION ---- */
@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(12px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
.card:nth-child(1)  {{ animation-delay: 0.03s }}
.card:nth-child(2)  {{ animation-delay: 0.07s }}
.card:nth-child(3)  {{ animation-delay: 0.11s }}
.card:nth-child(4)  {{ animation-delay: 0.15s }}
.card:nth-child(5)  {{ animation-delay: 0.19s }}
.card:nth-child(6)  {{ animation-delay: 0.23s }}
.card:nth-child(7)  {{ animation-delay: 0.27s }}
.card:nth-child(8)  {{ animation-delay: 0.31s }}
.card:nth-child(9)  {{ animation-delay: 0.35s }}
.card:nth-child(10) {{ animation-delay: 0.39s }}
.card:nth-child(11) {{ animation-delay: 0.43s }}
.card:nth-child(12) {{ animation-delay: 0.47s }}
.card:nth-child(13) {{ animation-delay: 0.51s }}

@media (max-width: 1100px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
@media (max-width: 640px) {{
  .grid {{ grid-template-columns: 1fr; }}
  header, main, footer {{ padding-left: 1.5rem; padding-right: 1.5rem; }}
}}

</style>
</head>
<body>

<header>
  <div>
    <div class="site-name">Santiago Marin Vargas</div>
    <div class="site-sub">Creacion de Interfaces &nbsp;&middot;&nbsp; Portafolio</div>
  </div>
  <nav>
    <button class="nav-btn active" onclick="switchPanel(1, this)">Portafolio 1</button>
    <button class="nav-btn"       onclick="switchPanel(2, this)">Portafolio 2</button>
  </nav>
</header>

<main>
  {p1}
  {p2}
</main>

<footer>
  <span>Santiago Marin Vargas</span>
  <span>Creacion de Interfaces &nbsp;&middot;&nbsp; 2025</span>
</footer>

<script>
function switchPanel(num, btn) {{
  document.querySelectorAll('.panel').forEach(function(p) {{ p.classList.remove('active'); }});
  document.querySelectorAll('.nav-btn').forEach(function(b) {{ b.classList.remove('active'); }});
  var panel = document.getElementById('panel-' + num);
  if (panel) panel.classList.add('active');
  btn.classList.add('active');
  var cards = document.querySelectorAll('#panel-' + num + ' .card');
  cards.forEach(function(card, i) {{
    card.style.animation = 'none';
    void card.offsetHeight;
    card.style.animation = '';
    card.style.animationDelay = (i * 0.04 + 0.03) + 's';
  }});
}}
document.getElementById('panel-1').classList.add('active');
</script>

</body>
</html>"""

components.html(HTML, height=3000, scrolling=True)
