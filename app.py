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

def render_card(project, index):
    num_str = str(index).zfill(2)
    url = project["url"]
    thumb = f"https://shot.screenshotapi.net/screenshot?token=free&url={url}&width=800&height=450&output=image&file_type=jpeg&delay=0&retina=false&quality=60"
    desc = project.get("description", "")
    desc_html = f'<div class="card-desc">{desc}</div>' if desc else ""
    return f"""
    <a class="card" href="{url}" target="_blank">
      <div class="card-thumb">
        <img src="{thumb}" alt="{project['title']}" loading="lazy"
             onerror="this.parentElement.classList.add('thumb-error'); this.style.display='none'"/>
        <div class="thumb-fallback"><span>{project.get('category','')}</span></div>
        <div class="card-num-overlay">{num_str}</div>
      </div>
      <div class="card-body">
        <div class="card-top">
          <span class="card-cat">{project.get('category', '')}</span>
        </div>
        <div class="card-title">{project['title']}</div>
        {desc_html}
        <div class="card-bottom">
          <span class="card-link">Ver proyecto &nbsp;&#x2192;</span>
        </div>
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
.grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
}}
.card {{
  display: flex;
  flex-direction: column;
  background: var(--white);
  text-decoration: none;
  color: inherit;
  transition: background 0.2s;
  animation: fadeUp 0.5s ease both;
  overflow: hidden;
}}
.card:hover {{ background: var(--grey); }}
.card:hover .card-thumb img {{ transform: scale(1.03); }}
.card-thumb {{
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #efefef;
  position: relative;
  border-bottom: 1px solid var(--line);
}}
.card-thumb img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}}
.thumb-fallback {{
  position: absolute;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  background: #efefef;
  font-size: var(--small);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
}}
.card-thumb.thumb-error .thumb-fallback {{ display: flex; }}
.card-num-overlay {{
  position: absolute;
  top: 0.7rem;
  left: 0.8rem;
  font-size: 0.58rem;
  letter-spacing: 0.2em;
  color: var(--white);
  background: rgba(0,0,0,0.45);
  padding: 0.2rem 0.5rem;
  backdrop-filter: blur(4px);
}}
.card-body {{
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1.8rem 1.4rem;
  gap: 0.6rem;
  flex: 1;
}}
.card-top {{ display: flex; justify-content: flex-end; }}
.card-cat {{
  font-size: 0.55rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  background: var(--grey);
  padding: 0.18rem 0.5rem;
  border: 1px solid var(--line);
}}
.card-title {{
  font-family: 'Shippori Mincho', serif;
  font-size: 1.05rem;
  font-weight: 500;
  line-height: 1.35;
  letter-spacing: -0.01em;
}}
.card-desc {{
  font-size: 0.73rem;
  line-height: 1.85;
  color: #777;
}}
.card-bottom {{
  margin-top: auto;
  padding-top: 0.9rem;
  border-top: 1px solid var(--line);
}}
.card-link {{
  font-size: 0.6rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--black);
}}
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
.panel {{ display: none; }}
.panel.active {{ display: block; }}
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

components.html(HTML, height=3200, scrolling=True)
