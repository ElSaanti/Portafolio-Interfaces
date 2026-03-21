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

def render_row(project, index):
    num_str = str(index).zfill(2)
    desc = project.get("description", "")
    desc_html = f'<span class="row-desc">{desc}</span>' if desc else ""
    return f"""
    <a class="project-row" href="{project['url']}" target="_blank">
      <span class="row-num">{num_str}</span>
      <span class="row-title">{project['title']}</span>
      <span class="row-cat">{project.get('category', '')}</span>
      {desc_html}
      <span class="row-arrow">&#x2192;</span>
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
        rows = "".join(render_row(p, p["id"]) for p in projects)
        content = f"""
        <div class="list-header">
          <span class="lh-num">#</span>
          <span class="lh-title">Proyecto</span>
          <span class="lh-cat">Categoria</span>
          <span class="lh-arrow"></span>
        </div>
        <div class="project-list">{rows}</div>"""
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
  --line:  #e0e0e0;
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
  padding: 3rem 5rem 2.2rem;
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
main {{ padding: 0 5rem 8rem; }}

.panel-head {{
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: 3.5rem 0 2.5rem;
  border-bottom: 1px solid var(--line);
  margin-bottom: 0;
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

/* ---- LIST HEADER ---- */
.list-header {{
  display: grid;
  grid-template-columns: 3rem 1fr 14rem 2rem;
  align-items: center;
  padding: 0.7rem 1rem 0.7rem 0;
  border-bottom: 1px solid var(--black);
  gap: 1rem;
}}

.lh-num, .lh-title, .lh-cat {{
  font-size: 0.58rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--muted);
}}

/* ---- PROJECT LIST ---- */
.project-list {{
  display: flex;
  flex-direction: column;
}}

/* ---- PROJECT ROW ---- */
.project-row {{
  display: grid;
  grid-template-columns: 3rem 1fr 14rem 2rem;
  align-items: center;
  gap: 1rem;
  padding: 1.4rem 1rem 1.4rem 0;
  border-bottom: 1px solid var(--line);
  text-decoration: none;
  color: inherit;
  transition: background 0.15s, padding-left 0.15s;
  cursor: pointer;
  animation: fadeUp 0.4s ease both;
}}

.project-row:hover {{
  background: var(--grey);
  padding-left: 1rem;
}}

.project-row:hover .row-arrow {{
  transform: translateX(5px);
  color: var(--black);
}}

.row-num {{
  font-size: 0.62rem;
  color: var(--muted);
  letter-spacing: 0.18em;
  font-family: 'Noto Sans JP', monospace;
}}

.row-title {{
  font-family: 'Shippori Mincho', serif;
  font-size: 1.05rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  line-height: 1.3;
}}

.row-cat {{
  font-size: 0.58rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  background: var(--grey);
  padding: 0.22rem 0.6rem;
  border: 1px solid var(--line);
  justify-self: start;
}}

.row-desc {{
  display: none;
}}

.row-arrow {{
  font-size: 0.9rem;
  color: #ccc;
  transition: transform 0.2s, color 0.2s;
  justify-self: end;
}}

/* ---- COMING SOON ---- */
.coming-soon {{
  padding: 7rem 0;
  text-align: center;
  border: 1px solid var(--line);
  margin-top: 3rem;
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
  padding: 1.4rem 5rem;
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
  from {{ opacity: 0; transform: translateY(8px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

.project-row:nth-child(1)  {{ animation-delay: 0.03s }}
.project-row:nth-child(2)  {{ animation-delay: 0.06s }}
.project-row:nth-child(3)  {{ animation-delay: 0.09s }}
.project-row:nth-child(4)  {{ animation-delay: 0.12s }}
.project-row:nth-child(5)  {{ animation-delay: 0.15s }}
.project-row:nth-child(6)  {{ animation-delay: 0.18s }}
.project-row:nth-child(7)  {{ animation-delay: 0.21s }}
.project-row:nth-child(8)  {{ animation-delay: 0.24s }}
.project-row:nth-child(9)  {{ animation-delay: 0.27s }}
.project-row:nth-child(10) {{ animation-delay: 0.30s }}
.project-row:nth-child(11) {{ animation-delay: 0.33s }}
.project-row:nth-child(12) {{ animation-delay: 0.36s }}
.project-row:nth-child(13) {{ animation-delay: 0.39s }}

/* ---- RESPONSIVE ---- */
@media (max-width: 768px) {{
  .list-header {{ grid-template-columns: 2.5rem 1fr 2rem; }}
  .list-header .lh-cat {{ display: none; }}
  .project-row {{ grid-template-columns: 2.5rem 1fr 2rem; }}
  .row-cat {{ display: none; }}
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
  var rows = document.querySelectorAll('#panel-' + num + ' .project-row');
  rows.forEach(function(row, i) {{
    row.style.animation = 'none';
    void row.offsetHeight;
    row.style.animation = '';
    row.style.animationDelay = (i * 0.03 + 0.03) + 's';
  }});
}}
document.getElementById('panel-1').classList.add('active');
</script>

</body>
</html>"""

components.html(HTML, height=1400, scrolling=True)
