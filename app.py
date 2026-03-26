import streamlit as st
import streamlit.components.v1 as components
import yaml
import base64
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
  [data-testid="stAppViewContainer"] { background: #f9f7f4; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).parent

@st.cache_data
def load_projects():
    with open(BASE_DIR / "projects.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@st.cache_data
def get_image_b64(img_path_str: str) -> str:
    with open(img_path_str, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_thumb(project_id: int) -> str:
    for ext in ["png", "jpg", "jpeg", "webp"]:
        img_path = BASE_DIR / "imagenes" / f"{project_id}.{ext}"
        if img_path.exists():
            b64 = get_image_b64(str(img_path))
            mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
            return f"data:image/{mime};base64,{b64}"
    return ""

# Color palette per category — pastel accent + dark text
CATEGORY_STYLE = {
    "Computer Vision":   ("hsl(210,85%,92%)", "hsl(210,60%,35%)"),
    "Text Analysis":     ("hsl(150,65%,88%)", "hsl(150,50%,28%)"),
    "Translation":       ("hsl(280,70%,92%)", "hsl(280,50%,35%)"),
    "Machine Learning":  ("hsl(25,90%,90%)",  "hsl(25,65%,35%)"),
    "NLP":               ("hsl(185,70%,88%)", "hsl(185,55%,28%)"),
    "Sentiment Analysis":("hsl(340,75%,92%)", "hsl(340,55%,35%)"),
    "OCR":               ("hsl(55,85%,88%)",  "hsl(55,60%,30%)"),
    "Data Analysis":     ("hsl(115,65%,88%)", "hsl(115,50%,28%)"),
    "Streamlit":         ("hsl(0,75%,90%)",   "hsl(0,55%,35%)"),
}

data = load_projects()

def render_card(project, index):
    num_str = str(index).zfill(2)
    desc = project.get("description", "")
    desc_html = f'<p class="card-desc">{desc}</p>' if desc else ""
    thumb = get_thumb(project["id"])
    cat = project.get("category", "")
    bg, fg = CATEGORY_STYLE.get(cat, ("hsl(220,15%,90%)", "hsl(220,15%,35%)"))

    if thumb:
        media_html = f"""
        <div class="card-media">
          <img src="{thumb}" alt="{project['title']}" loading="lazy"/>
          <div class="card-badge" style="background:{bg};color:{fg}">{cat}</div>
        </div>"""
    else:
        media_html = f"""
        <div class="card-media no-img" style="background:{bg}">
          <span class="placeholder-num" style="color:{fg}">{num_str}</span>
          <div class="card-badge" style="background:white;color:{fg}">{cat}</div>
        </div>"""

    return f"""
    <a class="card" href="{project['url']}" target="_blank">
      {media_html}
      <div class="card-body">
        <p class="card-num">Proyecto {num_str}</p>
        <h3 class="card-title">{project['title']}</h3>
        {desc_html}
        <span class="card-cta">Ver proyecto <span class="arrow">&#x2192;</span></span>
      </div>
    </a>
    """

def render_panel(key, panel_id):
    portfolio = data.get(key, {})
    projects  = portfolio.get("projects", [])
    title     = portfolio.get("title", "")
    if not projects:
        content = '<div class="coming-soon"><p class="cs-title">Portafolio 2</p><p class="cs-sub">Proyectos proximamente...</p></div>'
        count = ""
    else:
        cards = "".join(render_card(p, p["id"]) for p in projects)
        content = f'<div class="grid">{cards}</div>'
        count = f"{len(projects)} proyectos"
    return f"""
    <div class="panel" id="{panel_id}">
      <div class="panel-head">
        <h2 class="panel-title">{title}</h2>
        {f'<span class="panel-count">{count}</span>' if count else ''}
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,700&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --cream: #f9f7f4;
  --black: #111;
  --mid:   #555;
  --line:  #e0ddd8;
  --white: #fff;
  --radius: 16px;
}}

html, body {{
  background: var(--cream);
  color: var(--black);
  font-family: 'DM Sans', sans-serif;
  font-weight: 300;
  -webkit-font-smoothing: antialiased;
}}

/* ---- HEADER ---- */
header {{
  padding: 2.8rem 5rem 2rem;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.5rem;
  border-bottom: 1.5px solid var(--line);
  background: var(--white);
}}

.header-left {{}}

.site-eyebrow {{
  font-size: 0.68rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--mid);
  margin-bottom: 0.4rem;
}}

.site-name {{
  font-family: 'Fraunces', serif;
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1;
  color: var(--black);
}}

.site-name em {{
  font-style: italic;
  font-weight: 300;
}}

/* ---- NAV ---- */
nav {{
  display: flex;
  background: var(--cream);
  border: 1.5px solid var(--line);
  border-radius: 40px;
  padding: 4px;
  gap: 4px;
}}

.nav-btn {{
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  padding: 0.5rem 1.4rem;
  cursor: pointer;
  border: none;
  background: transparent;
  color: var(--mid);
  border-radius: 30px;
  transition: all 0.22s ease;
  white-space: nowrap;
}}

.nav-btn.active {{
  background: var(--black);
  color: var(--white);
}}

.nav-btn:not(.active):hover {{
  background: var(--line);
  color: var(--black);
}}

/* ---- MAIN ---- */
main {{
  padding: 0 5rem 8rem;
  max-width: 1440px;
  margin: 0 auto;
}}

/* ---- PANEL HEAD ---- */
.panel-head {{
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: 3rem 0 2.5rem;
  border-bottom: 1.5px solid var(--line);
  margin-bottom: 3rem;
  gap: 1rem;
  flex-wrap: wrap;
}}

.panel-title {{
  font-family: 'Fraunces', serif;
  font-size: clamp(1.4rem, 2.5vw, 2rem);
  font-weight: 700;
  letter-spacing: -0.03em;
}}

.panel-count {{
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--mid);
  background: var(--line);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
}}

/* ---- GRID ---- */
.grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}}

/* ---- CARD ---- */
.card {{
  background: var(--white);
  border-radius: var(--radius);
  border: 1.5px solid var(--line);
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
  animation: fadeUp 0.5s ease both;
}}

.card:hover {{
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.1);
  border-color: #bbb;
}}

.card:hover .arrow {{
  transform: translate(3px, -3px);
}}

/* ---- CARD MEDIA ---- */
.card-media {{
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  position: relative;
  background: #f0ede8;
}}

.card-media img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top;
  display: block;
  transition: transform 0.4s ease;
}}

.card:hover .card-media img {{
  transform: scale(1.04);
}}

.card-media.no-img {{
  display: flex;
  align-items: center;
  justify-content: center;
}}

.placeholder-num {{
  font-family: 'Fraunces', serif;
  font-size: 5rem;
  font-weight: 700;
  letter-spacing: -0.05em;
  opacity: 0.25;
  line-height: 1;
}}

.card-badge {{
  position: absolute;
  bottom: 0.7rem;
  left: 0.8rem;
  font-size: 0.58rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.25rem 0.65rem;
  border-radius: 20px;
  backdrop-filter: blur(6px);
}}

/* ---- CARD BODY ---- */
.card-body {{
  padding: 1.4rem 1.6rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
}}

.card-num {{
  font-size: 0.62rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--mid);
}}

.card-title {{
  font-family: 'Fraunces', serif;
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.35;
  letter-spacing: -0.02em;
  color: var(--black);
}}

.card-desc {{
  font-size: 0.78rem;
  line-height: 1.75;
  color: var(--mid);
  margin-top: 0.2rem;
}}

.card-cta {{
  margin-top: auto;
  padding-top: 1rem;
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--black);
  display: flex;
  align-items: center;
  gap: 0.4rem;
  border-top: 1px solid var(--line);
}}

.arrow {{
  display: inline-block;
  transition: transform 0.2s ease;
}}

/* ---- COMING SOON ---- */
.coming-soon {{
  padding: 6rem 2rem;
  text-align: center;
  border: 2px dashed var(--line);
  border-radius: var(--radius);
  background: var(--white);
}}

.cs-title {{
  font-family: 'Fraunces', serif;
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 300;
  font-style: italic;
  color: var(--line);
  letter-spacing: -0.03em;
}}

.cs-sub {{
  font-size: 0.78rem;
  color: var(--mid);
  margin-top: 0.8rem;
}}

/* ---- FOOTER ---- */
footer {{
  border-top: 1.5px solid var(--line);
  padding: 1.5rem 5rem;
  display: flex;
  justify-content: space-between;
  font-size: 0.65rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--mid);
  background: var(--white);
  flex-wrap: wrap;
  gap: 0.5rem;
}}

/* ---- TOGGLE ---- */
.panel {{ display: none; }}
.panel.active {{ display: block; }}

/* ---- ANIMATION ---- */
@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(16px); }}
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

/* ---- RESPONSIVE ---- */
@media (max-width: 1100px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
@media (max-width: 640px) {{
  .grid {{ grid-template-columns: 1fr; }}
  header, main, footer {{ padding-left: 1.5rem; padding-right: 1.5rem; }}
}}

</style>
</head>
<body>

<header>
  <div class="header-left">
    <p class="site-eyebrow">Creacion de Interfaces &nbsp;&middot;&nbsp; Portafolio</p>
    <div class="site-name">Santiago Marin Vargas</div>
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

components.html(HTML, height=3200, scrolling=True)
