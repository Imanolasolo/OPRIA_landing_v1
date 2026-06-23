import streamlit as st
import sqlite3
import urllib.parse
import smtplib
from email.message import EmailMessage
from datetime import datetime


# -----------------------------
# CONFIG
# -----------------------------


def get_secret(key: str, default=None):
    return st.secrets.get(key, default)


def get_secret_bool(key: str, default: bool = False) -> bool:
    value = get_secret(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)

TEXTS = {
    "es": {
        "lang_label": "Idioma",
        "lang_current": "Idioma actual: Español",
        "hero_tag": "OpsTech para escalar sin caos",
        "hero_title": "Convierte tu operación en una máquina de crecimiento",
        "hero_p1": "Crecer no debería significar más caos.",
        "hero_p2": "Conecta operación y resultados en una sola capa.",
        "hero_point_1": "Diseña procesos que sí se ejecutan",
        "hero_point_2": "Detecta cuellos de botella en tiempo real",
        "hero_point_3": "Toma decisiones con datos accionables",
        "quick_metric_1": "Tiempo perdido",
        "quick_metric_2": "Visibilidad operativa",
        "quick_metric_3": "Decisiones reactivas",
        "quick_metric_value_1": "-35%",
        "quick_metric_value_2": "+100%",
        "quick_metric_value_3": "-60%",
        "quick_metric_delta_1": "menos retrabajo",
        "quick_metric_delta_2": "en procesos críticos",
        "quick_metric_delta_3": "con datos en vivo",
        "cta_left_title": "Más control. Menos urgencias.",
        "cta_left_l1": "Tu operación puede vender y cumplir al mismo tiempo.",
        "cta_left_l2": "OPRIA OS ordena procesos, equipos y decisiones.",
        "cta_left_l3": "Resultado: más velocidad y más margen.",
        "whatsapp_message": "Hola OPRIA OS, quiero conocer el sistema operativo empresarial",
        "whatsapp_button": "Agendar diagnóstico por WhatsApp",
        "problem_header": "Tu operación en 30 segundos",
        "problem_tab_1": "Dolor",
        "problem_tab_2": "Solución",
        "problem_tab_3": "Resultado",
        "problem_tab_1_body": "- Mucha herramienta suelta\n- Procesos que viven en chats\n- Decisiones lentas",
        "problem_tab_2_body": "- Flujo operativo único\n- Trazabilidad en tiempo real\n- Roles y procesos claros",
        "problem_tab_3_body": "- Menos retrabajo\n- Más foco comercial\n- Escalabilidad con orden",
        "opstech_header": "Bienvenido a OpsTech",
        "opstech_card_title": "Qué resuelves con OPRIA",
        "opstech_card_p1": "Centraliza procesos, equipos y datos en un flujo operativo claro.",
        "opstech_card_p2": "Menos improvisación. Más ejecución con resultados medibles.",
        "product_header": "OPRIA OS",
        "feature_people": "Personas",
        "feature_people_desc": "Roles, equipos y responsabilidades",
        "feature_processes": "Procesos",
        "feature_processes_desc": "Flujos operativos medibles",
        "feature_data": "Datos",
        "feature_data_desc": "Indicadores y visibilidad",
        "feature_decisions": "Decisiones",
        "feature_decisions_desc": "Acción basada en información",
        "partners_header": "Para pymes, empresarios y compañías",
        "partners_exp": "¿Dónde encaja OPRIA en tu empresa?",
        "partners_body": "Perfecto para empresas que quieren ordenar su operación sin añadir complejidad.\n\n- Centraliza procesos críticos\n- Gana visibilidad diaria\n- Escala con control\n\nHoy trabajamos directo con pymes, empresarios y compañías.",
        "contact_header": "¿Buscas más información? Hablemos",
        "contact_exp": "Contacta con nosotros en 1 minuto",
        "form_name": "Nombre",
        "form_company": "Empresa",
        "form_email": "Email",
        "form_interest": "Estoy interesado en:",
        "form_interest_1": "Implementar OPRIA",
        "form_interest_2": "Ser partner integrador",
        "form_interest_3": "Invertir / colaborar",
        "form_interest_4": "Más información",
        "form_message": "Cuéntanos",
        "form_submit": "Enviar",
        "form_success": "Recibido. Te contactaremos.",
        "mail_ok": "Notificación enviada correctamente al equipo comercial.",
        "mail_fail": "El lead se guardó, pero el email no pudo enviarse:",
    },
    "en": {
        "lang_label": "Language",
        "lang_current": "Current language: English",
        "hero_tag": "OpsTech to scale without chaos",
        "hero_title": "Turn your operation into a growth engine",
        "hero_p1": "Growth should not create more chaos.",
        "hero_p2": "Connect operations and outcomes in one layer.",
        "hero_point_1": "Design processes that are actually executed",
        "hero_point_2": "Detect bottlenecks in real time",
        "hero_point_3": "Make decisions with actionable data",
        "quick_metric_1": "Wasted time",
        "quick_metric_2": "Operational visibility",
        "quick_metric_3": "Reactive decisions",
        "quick_metric_value_1": "-35%",
        "quick_metric_value_2": "+100%",
        "quick_metric_value_3": "-60%",
        "quick_metric_delta_1": "less rework",
        "quick_metric_delta_2": "in critical workflows",
        "quick_metric_delta_3": "with live data",
        "cta_left_title": "More control. Fewer emergencies.",
        "cta_left_l1": "Your operation can sell and deliver at the same time.",
        "cta_left_l2": "OPRIA OS aligns processes, teams, and decisions.",
        "cta_left_l3": "Result: more speed and healthier margins.",
        "whatsapp_message": "Hello OPRIA OS, I want to learn about the business operating system",
        "whatsapp_button": "Schedule a diagnostic on WhatsApp",
        "problem_header": "Your operation in 30 seconds",
        "problem_tab_1": "Pain",
        "problem_tab_2": "Solution",
        "problem_tab_3": "Outcome",
        "problem_tab_1_body": "- Too many disconnected tools\n- Processes trapped in chats\n- Slow decisions",
        "problem_tab_2_body": "- One operating flow\n- Real-time traceability\n- Clear roles and processes",
        "problem_tab_3_body": "- Less rework\n- More commercial focus\n- Scalable operations",
        "opstech_header": "Welcome to OpsTech",
        "opstech_card_title": "What OPRIA solves for you",
        "opstech_card_p1": "Centralize processes, teams, and data into one clear operating flow.",
        "opstech_card_p2": "Less improvisation. More execution with measurable outcomes.",
        "product_header": "OPRIA OS",
        "feature_people": "People",
        "feature_people_desc": "Roles, teams, and responsibilities",
        "feature_processes": "Processes",
        "feature_processes_desc": "Measurable operating flows",
        "feature_data": "Data",
        "feature_data_desc": "Visibility and key metrics",
        "feature_decisions": "Decisions",
        "feature_decisions_desc": "Action based on information",
        "partners_header": "For SMEs, business owners, and companies",
        "partners_exp": "Where does OPRIA fit in your company?",
        "partners_body": "Perfect for companies that want to organize operations without adding complexity.\n\n- Centralize critical workflows\n- Gain daily visibility\n- Scale with control\n\nToday we focus on direct support for SMEs, business owners, and companies.",
        "contact_header": "Need more information? Let's talk",
        "contact_exp": "Contact us in 1 minute",
        "form_name": "Name",
        "form_company": "Company",
        "form_email": "Email",
        "form_interest": "I am interested in:",
        "form_interest_1": "Implement OPRIA",
        "form_interest_2": "Become an integration partner",
        "form_interest_3": "Invest / collaborate",
        "form_interest_4": "More information",
        "form_message": "Tell us",
        "form_submit": "Send",
        "form_success": "Received. We will contact you.",
        "mail_ok": "Notification sent successfully to the commercial team.",
        "mail_fail": "Lead was saved, but the email could not be sent:",
    }
}


def get_lang():
    lang = st.session_state.get("landing_opstech_lang", "es")
    if lang not in TEXTS:
        lang = "es"
        st.session_state["landing_opstech_lang"] = lang
    return lang


def set_lang(lang):
    if lang in TEXTS:
        st.session_state["landing_opstech_lang"] = lang


def tr(key: str) -> str:
    lang = get_lang()
    return str(TEXTS.get(lang, {}).get(key, key))


st.set_page_config(
    page_title="OPRIA OS | OpsTech",
    page_icon="⚙️",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;700&display=swap');

:root {
    --op-bg: #fff8ef;
    --op-surface: rgba(255, 255, 255, 0.86);
    --op-border: rgba(219, 96, 48, 0.28);
    --op-primary: #d45d2f;
    --op-primary-strong: #bc4b22;
    --op-secondary: #123e54;
    --op-text: #16222f;
    --op-muted: #3e5667;
    --op-shadow: 0 18px 40px rgba(18, 62, 84, 0.14);
}

.stApp {
    background:
        radial-gradient(950px 430px at 95% -5%, rgba(18, 62, 84, 0.2), transparent 58%),
        radial-gradient(760px 420px at 5% 2%, rgba(212, 93, 47, 0.18), transparent 64%),
        var(--op-bg);
}

h1,h2,h3 {
    color: var(--op-secondary);
    font-family: "Outfit", "Segoe UI", sans-serif;
    letter-spacing: -0.02em;
}

p,li {
    color: var(--op-text);
    font-family: "Plus Jakarta Sans", "Segoe UI", sans-serif;
    font-size: 17px;
    line-height: 1.6;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 2.4rem;
    border-radius: 26px;
    background: linear-gradient(138deg, rgba(255, 255, 255, 0.96), rgba(255, 242, 231, 0.92));
    border: 1px solid var(--op-border);
    box-shadow: var(--op-shadow);
    margin-bottom: 0.75rem;
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.45fr) minmax(0, 1fr);
    gap: 1rem;
    align-items: start;
}

.hero-side {
    padding-top: 0;
}

.hero-main-copy h2,
.hero-side h2 {
    margin: 0;
    font-size: clamp(1.1rem, 1.7vw, 1.5rem);
    color: var(--op-primary-strong);
}

.hero-main-copy p,
.hero-side p {
    margin: 0.55rem 0 0;
    color: var(--op-muted);
}

.hero::after {
    content: "";
    position: absolute;
    right: -30px;
    top: -48px;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(18, 62, 84, 0.24), rgba(18, 62, 84, 0));
    pointer-events: none;
}

.hero-tag {
    display: inline-block;
    margin-bottom: 0.75rem;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    border: 1px solid var(--op-border);
    background: rgba(255, 255, 255, 0.78);
    color: var(--op-primary-strong);
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.hero h1 {
    margin: 0.15rem 0 0.45rem;
    font-size: clamp(2rem, 3.2vw, 3.2rem);
}

.hero h2 {
    margin-top: 0;
    margin-bottom: 0.85rem;
    font-size: clamp(1.2rem, 2vw, 1.7rem);
    color: var(--op-primary-strong);
}

.hero p {
    max-width: 810px;
    margin: 0.35rem 0;
    color: var(--op-muted);
}

.hero-points {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 1.55rem;
    width: 100%;
}

.hero-point {
    background: var(--op-surface);
    border: 1px solid var(--op-border);
    border-radius: 12px;
    padding: 0.65rem 0.75rem;
    color: var(--op-secondary);
    font-weight: 600;
}

.card {
    background: var(--op-surface);
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 18px;
    border: 1px solid var(--op-border);
    box-shadow: 0 10px 24px rgba(18, 62, 84, 0.09);
}

.cta {
    background: linear-gradient(145deg, var(--op-secondary), #1f617c);
    color: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(18, 62, 84, 0.28);
}

div[data-testid="stButton"] > button {
    background: linear-gradient(145deg, var(--op-primary), var(--op-primary-strong));
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    padding: 0.6rem 1rem;
}

div[data-testid="stButton"] > button:hover {
    filter: brightness(1.05);
}

@media (max-width: 768px) {
    .hero {
        padding: 1.45rem;
    }

    .hero-grid {
        grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
    }

    .hero-points {
        grid-template-columns: 1fr;
    }
}

</style>
""", unsafe_allow_html=True)



# -----------------------------
# DATABASE
# -----------------------------

def init_db():

    conn = sqlite3.connect("opria_leads.db")

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        company TEXT,
        interest TEXT,
        message TEXT,
        created TEXT
    )
    """)

    conn.commit()
    conn.close()



def save_lead(data):

    conn = sqlite3.connect("opria_leads.db")

    c = conn.cursor()

    c.execute("""
    INSERT INTO leads
    (name,email,company,interest,message,created)
    VALUES (?,?,?,?,?,?)
    """,
    (
        data["name"],
        data["email"],
        data["company"],
        data["interest"],
        data["message"],
        datetime.now()
    ))

    conn.commit()
    conn.close()


def send_lead_email(data):

    smtp_host = get_secret("OPRIA_SMTP_HOST")
    smtp_port = int(get_secret("OPRIA_SMTP_PORT", 587))
    smtp_user = get_secret("OPRIA_SMTP_USER")
    smtp_password = get_secret("OPRIA_SMTP_PASSWORD")
    smtp_from = get_secret("OPRIA_SMTP_FROM", smtp_user or "no-reply@opria.local")
    smtp_use_ssl = get_secret_bool("OPRIA_SMTP_USE_SSL", False)
    smtp_use_tls = get_secret_bool("OPRIA_SMTP_USE_TLS", True)

    if not smtp_host or not smtp_user or not smtp_password:
        return False, "Falta configurar secrets SMTP (OPRIA_SMTP_HOST, OPRIA_SMTP_USER, OPRIA_SMTP_PASSWORD)."

    email_to = str(get_secret("OPRIA_LEAD_EMAIL_TO", "jjusturi@gmail.com")).strip()

    if not email_to:
        return False, "Falta configurar OPRIA_LEAD_EMAIL_TO para el destinatario de leads."

    msg = EmailMessage()
    msg["Subject"] = "Nuevo lead - Programa fundador OPRIA OS"
    msg["From"] = smtp_from
    msg["To"] = email_to
    msg["Reply-To"] = (data.get("email") or "").strip()
    msg.set_content(
        "Se recibió una nueva solicitud al programa fundador.\n\n"
        f"Nombre: {data.get('name', '').strip()}\n"
        f"Empresa: {data.get('company', '').strip()}\n"
        f"Email: {data.get('email', '').strip()}\n"
        f"Interés: {data.get('interest', '').strip()}\n\n"
        "Mensaje:\n"
        f"{data.get('message', '').strip()}\n\n"
        f"Fecha: {datetime.now().isoformat(timespec='seconds')}"
    )

    try:
        if smtp_use_ssl:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                if smtp_use_tls:
                    server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
    except Exception as exc:
        return False, str(exc)

    return True, ""



init_db()


lang_col_1, lang_col_2, lang_col_3 = st.columns([1, 1, 5])

with lang_col_1:
    if st.button("ES", use_container_width=True):
        set_lang("es")

with lang_col_2:
    if st.button("EN", use_container_width=True):
        set_lang("en")

with lang_col_3:
    st.caption(tr("lang_current"))



# -----------------------------
# HEADER
# -----------------------------
st.markdown(f"""
<div class="hero">

<span class="hero-tag">{tr('hero_tag')}</span>

<h1>OPRIA OS</h1>

<div class="hero-grid">

<div class="hero-main-copy">

<h2>
{tr('hero_title')}
</h2>

<p>
{tr('hero_p1')}
</p>

<p>
{tr('hero_p2')}
</p>

</div>

<div class="hero-side">

<h2>{tr('opstech_card_title')}</h2>

<p>{tr('opstech_card_p1')}</p>

<p>{tr('opstech_card_p2')}</p>

</div>

</div>

<div class="hero-points">
    <div class="hero-point">{tr('hero_point_1')}</div>
    <div class="hero-point">{tr('hero_point_2')}</div>
    <div class="hero-point">{tr('hero_point_3')}</div>
</div>

</div>
""",
unsafe_allow_html=True)



st.divider()


metric_col_1, metric_col_2, metric_col_3 = st.columns(3)

with metric_col_1:
    st.metric(tr("quick_metric_1"), tr("quick_metric_value_1"), tr("quick_metric_delta_1"))

with metric_col_2:
    st.metric(tr("quick_metric_2"), tr("quick_metric_value_2"), tr("quick_metric_delta_2"))

with metric_col_3:
    st.metric(tr("quick_metric_3"), tr("quick_metric_value_3"), tr("quick_metric_delta_3"))



# -----------------------------
# DECISION BLOCK
# -----------------------------


decision_col, action_col = st.columns([1.25, 1], gap="large")

with decision_col:
    st.header(tr("problem_header"))

    problem_tab_1, problem_tab_2, problem_tab_3 = st.tabs([
        tr("problem_tab_1"),
        tr("problem_tab_2"),
        tr("problem_tab_3")
    ])

    with problem_tab_1:
        st.markdown(tr("problem_tab_1_body"))

    with problem_tab_2:
        st.markdown(tr("problem_tab_2_body"))

    with problem_tab_3:
        st.markdown(tr("problem_tab_3_body"))

with action_col:
    st.markdown(
        f"""
### {tr('cta_left_title')}

{tr('cta_left_l1')}

{tr('cta_left_l2')}

{tr('cta_left_l3')}
"""
    )

    msg = urllib.parse.quote(tr("whatsapp_message"))
    st.link_button(
        tr("whatsapp_button"),
        f"https://wa.me/?text={msg}",
        use_container_width=True
    )



# -----------------------------
# PRODUCT
# -----------------------------


st.header(tr("product_header"))


cols = st.columns(4)


features = [
    ("👥", tr("feature_people"), tr("feature_people_desc")),
    ("⚙️", tr("feature_processes"), tr("feature_processes_desc")),
    ("📊", tr("feature_data"), tr("feature_data_desc")),
    ("🎯", tr("feature_decisions"), tr("feature_decisions_desc"))
]


for col,item in zip(cols,features):

    with col:

        st.markdown(f"""
        <div class="card">

        <h2>{item[0]}</h2>

        <h3>{item[1]}</h3>

        <p>{item[2]}</p>

        </div>
        """,
        unsafe_allow_html=True)



# -----------------------------
# AUDIENCE + CONTACT
# -----------------------------


audience_col, contact_col = st.columns([1, 1], gap="large")

with audience_col:
    st.header(tr("partners_header"))

    with st.expander(tr("partners_exp"), expanded=True):
        st.write(tr("partners_body"))


with contact_col:
    st.header(tr("contact_header"))

    with st.expander(tr("contact_exp"), expanded=False):

        with st.form("contact"):


            name = st.text_input(tr("form_name"))

            company = st.text_input(tr("form_company"))

            email = st.text_input(tr("form_email"))

            interest = st.selectbox(
                tr("form_interest"),
                [
                    tr("form_interest_1"),
                    tr("form_interest_2"),
                    tr("form_interest_3"),
                    tr("form_interest_4")
                ]
            )


            message = st.text_area(
                tr("form_message")
            )


            submit = st.form_submit_button(
                tr("form_submit")
            )


            if submit:

                lead_data = {
                    "name":name,
                    "email":email,
                    "company":company,
                    "interest":interest,
                    "message":message
                }

                save_lead(lead_data)

                email_sent, email_error = send_lead_email(lead_data)


                st.success(
                    tr("form_success")
                )

                if email_sent:
                    st.info(tr("mail_ok"))
                else:
                    st.warning(f"{tr('mail_fail')} {email_error}")


# -----------------------------
# FOOTER
# -----------------------------


st.divider()

st.markdown("""
<center>

<b>OPRIA OS</b><br>

The Operating System for Business Operations

<br>

OpsTech

</center>
""",
unsafe_allow_html=True)