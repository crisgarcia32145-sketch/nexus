
import streamlit as st

from database import (
    initialize_db,
    add_task,
    get_tasks,
    toggle_task,
    delete_task,
)

st.set_page_config(
    page_title="NEXUS | Control Center",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- ESTILOS ----------

st.markdown("""
<style>
    .stApp {
        background: #0b0a12;
        color: #f4efff;
    }

    [data-testid="stSidebar"] {
        background: #12101c;
        border-right: 1px solid #302641;
    }

    .hero {
        padding: 30px;
        border: 1px solid #392750;
        border-radius: 20px;
        background: linear-gradient(120deg, #28183c, #11101b);
        margin-bottom: 24px;
    }

    .eyebrow {
        color: #c4a5fd;
        letter-spacing: 4px;
        font-size: 12px;
        font-weight: 700;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 42px;
        margin: 12px 0;
    }

    .hero p {
        color: #c4bad7;
    }

    div[data-testid="stMetric"] {
        background: #15121f;
        border: 1px solid #302641;
        padding: 18px;
        border-radius: 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #c4a5fd;
    }

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #493660;
    }

    div[data-testid="stForm"] {
        background: #12101b;
        padding: 20px;
        border: 1px solid #302641;
        border-radius: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- BASE DE DATOS ----------

initialize_db()

# ---------- BARRA LATERAL ----------

with st.sidebar:
    st.markdown("## ✦ NEXUS")
    st.caption("PERSONAL CONTROL CENTER")
    st.divider()

    page = st.radio(
        "NAVEGACIÓN",
        ["Dashboard", "Mis tareas", "Acerca de"],
    )

    st.divider()
    st.caption("NEXUS v0.1")
    st.caption("Construido con Python 💜")

# ---------- OBTENER DATOS ----------

tasks = get_tasks()

total = len(tasks)
completed = sum(task[4] for task in tasks)
pending = total - completed
progress = completed / total if total else 0

# ---------- DASHBOARD ----------

if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">N E X U S / WORKSPACE</div>
        <h1>Tu centro de control.</h1>
        <p>Organizá tus ideas. Construí tus proyectos.
        Convertí tus planes en resultados.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Tu actividad")

    col1, col2, col3 = st.columns(3)

    col1.metric("Tareas totales", total)
    col2.metric("Pendientes", pending)
    col3.metric("Completadas", completed)

    st.subheader("Progreso general")
    st.progress(progress, text=f"{progress:.0%} completado")

    st.divider()

    st.subheader("⚡ Acceso rápido")

    if st.button("＋ Crear una tarea", type="primary"):
        st.session_state["quick_add"] = True

    if st.session_state.get("quick_add", False):
        with st.form("quick_task_form", clear_on_submit=True):
            quick_title = st.text_input("Nombre de la tarea")
            quick_category = st.selectbox(
                "Categoría",
                ["Personal", "Estudios", "Programación", "Ideas"],
            )

            save_quick = st.form_submit_button("Guardar tarea")

            if save_quick:
                if quick_title.strip():
                    add_task(quick_title, quick_category)
                    st.session_state["quick_add"] = False
                    st.rerun()
                else:
                    st.warning("Escribí un nombre para la tarea.")

    st.subheader("Actividad reciente")

    if not tasks:
        st.info(
            "Todavía no hay tareas. "
            "¡Este es el momento de crear la primera!"
        )
    else:
        for task in tasks[:5]:
            task_id, title, category, created_at, is_done = task

            with st.container(border=True):
                symbol = "✅" if is_done else "◉"
                st.markdown(f"{symbol} **{title}**")
                st.caption(f"{category} · {created_at}")

# ---------- MIS TAREAS ----------

elif page == "Mis tareas":
    st.title("Mis tareas")
    st.caption("Administrá tus pendientes desde un solo lugar.")

    with st.form("create_task", clear_on_submit=True):
        title = st.text_input(
            "Nombre",
            placeholder="Ej. Crear mi primera aplicación con IA",
        )

        category = st.selectbox(
            "Categoría",
            ["Personal", "Estudios", "Programación", "Ideas"],
        )

        submitted = st.form_submit_button(
            "＋ Crear tarea",
            type="primary",
        )

        if submitted:
            if title.strip():
                add_task(title, category)
                st.rerun()
            else:
                st.warning("El nombre no puede estar vacío.")

    st.divider()

    filter_option = st.selectbox(
        "Mostrar",
        ["Todas", "Pendientes", "Completadas"],
    )

    visible_tasks = tasks

    if filter_option == "Pendientes":
        visible_tasks = [t for t in tasks if not t[4]]
    elif filter_option == "Completadas":
        visible_tasks = [t for t in tasks if t[4]]

    if not visible_tasks:
        st.info("No hay tareas en esta categoría.")

    for task in visible_tasks:
        task_id, title, category, created_at, is_done = task

        with st.container(border=True):
            col1, col2, col3 = st.columns(
                [0.10, 0.68, 0.22],
                vertical_alignment="center",
            )

            with col1:
                checked = st.checkbox(
                    "Completar",
                    value=bool(is_done),
                    key=f"task_done_{task_id}",
                    label_visibility="collapsed",
                )

            if checked != bool(is_done):
                toggle_task(task_id, checked)
                st.rerun()

            with col2:
                if is_done:
                    st.markdown(f"~~**{title}**~~")
                else:
                    st.markdown(f"**{title}**")

                st.caption(f"{category} · {created_at}")

            with col3:
                if st.button(
                    "Eliminar",
                    key=f"delete_{task_id}",
                    use_container_width=True,
                ):
                    delete_task(task_id)
                    st.rerun()

# ---------- ACERCA DE ----------

elif page == "Acerca de":
    st.title("Acerca de NEXUS")

    st.markdown("""
    NEXUS es un proyecto personal creado para aprender
    desarrollo de software con Python.

    **Tecnologías**
    - Python: lógica de la aplicación.
    - Streamlit: interfaz web.
    - SQLite: almacenamiento de datos.
    - Pytest: pruebas automatizadas.

    **Próximas mejoras**
    - Calendario y fechas límite.
    - Buscador de tareas.
    - Estadísticas de productividad.
    - Asistente de inteligencia artificial.
    """)
