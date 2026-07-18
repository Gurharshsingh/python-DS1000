"""
Streamlit Frontend - Student Management UI
HOW TO RUN: streamlit run frontend.py
Backend must be running: uvicorn backend:app --reload
"""

import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Student Manager",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def api_get(endpoint):
    try:
        r = requests.get(f"{API_URL}{endpoint}", timeout=5)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return None, 503


def api_post(endpoint, data):
    try:
        r = requests.post(f"{API_URL}{endpoint}", json=data, timeout=5)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return None, 503


def api_put(endpoint, data):
    try:
        r = requests.put(f"{API_URL}{endpoint}", json=data, timeout=5)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return None, 503


def api_delete(endpoint):
    try:
        r = requests.delete(f"{API_URL}{endpoint}", timeout=5)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return None, 503


def backend_online():
    d, c = api_get("/")
    return d is not None and c == 200


# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
st.sidebar.title("🎓 Student Manager")
st.sidebar.markdown("---")

# Backend status
if backend_online():
    st.sidebar.success("✅ Backend Online")
else:
    st.sidebar.error("❌ Backend Offline")
    st.sidebar.info("Run:\n`uvicorn backend:app --reload`")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Dashboard",
        "➕ Add Student",
        "📋 View All Students",
        "✏️ Update Student",
        "🗑️ Delete Student",
        "🧪 API Explorer",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**📡 API Base URL:**")
st.sidebar.code(API_URL)
st.sidebar.markdown(f"[📖 Swagger Docs]({API_URL}/docs)")


# ─────────────────────────────────────────────
# PAGE 1 — DASHBOARD
# ─────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.title("🎓 Student Management System")
    st.caption("FastAPI backend + Streamlit frontend")
    st.divider()

    data, code = api_get("/students")

    if data is None:
        st.error("❌ Cannot connect to the backend. Is it running?")
        st.code("uvicorn backend:app --reload", language="bash")
        st.stop()

    students_list = data.get("students", [])
    total = data.get("total", 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Students", total)
    col2.metric("✅ Active", sum(1 for s in students_list if s.get("is_active", True)))
    col3.metric(
        "📈 Avg Marks",
        f"{round(sum(s['marks'] for s in students_list)/len(students_list),1)}%"
        if students_list else "N/A",
    )
    col4.metric("📚 Grades", len(set(s["grade"] for s in students_list)))

    st.divider()

    if students_list:
        st.subheader("📊 Student Records")
        df = pd.DataFrame(students_list)
        cols = [c for c in ["id", "name", "age", "grade", "marks", "is_active"] if c in df.columns]
        df = df[cols]
        df.columns = [c.upper() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No students yet. Use **➕ Add Student** from the sidebar to add one!")


# ─────────────────────────────────────────────
# PAGE 2 — ADD STUDENT
# ─────────────────────────────────────────────
elif page == "➕ Add Student":
    st.title("➕ Add New Student")
    st.divider()

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name  = st.text_input("👤 Name", placeholder="e.g. Rahul Sharma")
            age   = st.number_input("🎂 Age", min_value=5, max_value=60, value=18, step=1)
        with col2:
            grade = st.selectbox("📚 Grade", ["A", "B", "C", "D", "F", "10th", "11th", "12th", "UG", "PG"])
            marks = st.slider("📈 Marks (%)", 0.0, 100.0, 75.0, step=0.5)

        is_active = st.checkbox("Active Student", value=True)
        submitted = st.form_submit_button("🎓 Add Student", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter a student name!")
        else:
            payload = {"name": name.strip(), "age": int(age),
                       "grade": grade, "marks": float(marks), "is_active": is_active}
            data, code = api_post("/students", payload)
            if data is None:
                st.error("❌ Backend offline!")
            elif code == 201:
                st.success(f"✅ {data.get('message')}")
                st.json(data.get("student", {}))
            else:
                st.error(f"Error {code}: {data.get('detail')}")


# ─────────────────────────────────────────────
# PAGE 3 — VIEW ALL STUDENTS
# ─────────────────────────────────────────────
elif page == "📋 View All Students":
    st.title("📋 All Students")
    st.divider()

    col_a, col_b = st.columns([5, 1])
    with col_b:
        if st.button("🔄 Refresh"):
            st.rerun()

    data, code = api_get("/students")
    if data is None:
        st.error("❌ Cannot connect to backend.")
        st.stop()

    students_list = data.get("students", [])
    st.write(f"**Total students:** {data.get('total', 0)}")

    if not students_list:
        st.info("No students found. Add some from the sidebar.")
    else:
        search = st.text_input("🔍 Search by name")
        if search:
            students_list = [s for s in students_list if search.lower() in s["name"].lower()]

        for s in students_list:
            icon = "🟢" if s.get("is_active") else "🔴"
            with st.expander(f"{icon} {s['name']}  |  Grade: {s['grade']}  |  Marks: {s['marks']}%  |  ID: {s['id']}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("ID", s["id"])
                c2.metric("Age", s["age"])
                c3.metric("Marks", f"{s['marks']}%")
                st.write(f"**Grade:** {s['grade']}  |  **Status:** {'Active ✅' if s.get('is_active') else 'Inactive ❌'}")


# ─────────────────────────────────────────────
# PAGE 4 — UPDATE STUDENT
# ─────────────────────────────────────────────
elif page == "✏️ Update Student":
    st.title("✏️ Update Student")
    st.divider()

    data, _ = api_get("/students")
    students_list = data.get("students", []) if data else []

    if not students_list:
        st.info("No students in the database yet.")
        st.stop()

    options = {f"#{s['id']} — {s['name']} (Grade {s['grade']})": s["id"] for s in students_list}
    selected = st.selectbox("Select a student to edit:", list(options.keys()))
    sid = options[selected]

    existing, code = api_get(f"/students/{sid}")
    if not existing or code != 200:
        st.error("Could not load student.")
        st.stop()

    st.info(f"Editing: **{existing['name']}** (ID #{sid})")

    with st.form("update_form"):
        col1, col2 = st.columns(2)
        with col1:
            name  = st.text_input("👤 Name", value=existing["name"])
            age   = st.number_input("🎂 Age", min_value=5, max_value=60, value=existing["age"], step=1)
        with col2:
            grade_opts = ["A", "B", "C", "D", "F", "10th", "11th", "12th", "UG", "PG"]
            g_idx = grade_opts.index(existing["grade"]) if existing["grade"] in grade_opts else 0
            grade = st.selectbox("📚 Grade", grade_opts, index=g_idx)
            marks = st.slider("📈 Marks (%)", 0.0, 100.0, float(existing["marks"]), step=0.5)

        is_active = st.checkbox("Active Student", value=existing.get("is_active", True))
        submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Name cannot be empty!")
        else:
            payload = {"name": name.strip(), "age": int(age),
                       "grade": grade, "marks": float(marks), "is_active": is_active}
            result, status = api_put(f"/students/{sid}", payload)
            if result is None:
                st.error("❌ Backend offline.")
            elif status == 200:
                st.success(f"✅ {result.get('message')}")
                st.json(result.get("student", {}))
            else:
                st.error(f"Error: {result.get('detail')}")


# ─────────────────────────────────────────────
# PAGE 5 — DELETE STUDENT
# ─────────────────────────────────────────────
elif page == "🗑️ Delete Student":
    st.title("🗑️ Delete Student")
    st.divider()

    data, _ = api_get("/students")
    students_list = data.get("students", []) if data else []

    if not students_list:
        st.info("No students to delete.")
        st.stop()

    options = {f"#{s['id']} — {s['name']} (Grade {s['grade']})": s["id"] for s in students_list}
    selected = st.selectbox("Select student to delete:", list(options.keys()))
    sid = options[selected]

    existing, _ = api_get(f"/students/{sid}")
    if existing:
        c1, c2, c3 = st.columns(3)
        c1.metric("Name", existing["name"])
        c2.metric("Grade", existing["grade"])
        c3.metric("Marks", f"{existing['marks']}%")

    st.warning("⚠️ This action is permanent and cannot be undone!")
    confirm = st.checkbox(f"I confirm I want to delete **{existing.get('name', 'this student')}**")

    if confirm:
        if st.button("🗑️ Delete Student", type="primary"):
            result, code = api_delete(f"/students/{sid}")
            if result is None:
                st.error("❌ Backend offline.")
            elif code == 200:
                st.success(f"✅ {result.get('message')}")
                st.rerun()
            else:
                st.error(f"Error: {result.get('detail')}")


# ─────────────────────────────────────────────
# PAGE 6 — API EXPLORER
# ─────────────────────────────────────────────
elif page == "🧪 API Explorer":
    st.title("🧪 API Explorer")
    st.caption("Test mainn.py concepts live")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📌 Path Params", "🔎 Query Params", "💡 Quick Tests"])

    with tab1:
        st.subheader("Path Parameter — `/greet/{name}`")
        st.markdown("**STEP 3 from `mainn.py`**: The `{name}` is a variable in the URL path.")
        name_in = st.text_input("Enter a name:", value="Alice", key="greet_k")
        if st.button("▶ GET /greet/{name}"):
            d, c = api_get(f"/greet/{name_in}")
            if d:
                st.success(d.get("message", ""))
                st.code(f"GET {API_URL}/greet/{name_in}\nStatus: {c}\nResponse: {d}")
            else:
                st.error("❌ Backend offline!")

    with tab2:
        st.subheader("Query Parameters — `/add?a=...&b=...`")
        st.markdown("**STEP 4 from `mainn.py`**: Params come after `?` in the URL.")
        ca, cb = st.columns(2)
        with ca:
            a = st.number_input("a =", value=10, key="qa", step=1)
        with cb:
            b = st.number_input("b =", value=20, key="qb", step=1)
        if st.button("▶ GET /add?a=...&b=..."):
            d, c = api_get(f"/add?a={int(a)}&b={int(b)}")
            if d:
                st.success(f"{int(a)} + {int(b)} = **{d['result']}**")
                st.code(f"GET {API_URL}/add?a={int(a)}&b={int(b)}\nStatus: {c}\nResponse: {d}")
            else:
                st.error("❌ Backend offline!")

    with tab3:
        st.subheader("Quick Endpoint Tests")
        endpoints = {
            "GET /  → Home": "/",
            "GET /hello  → Optional param (default = 'Raj')": "/hello",
            "GET /hello?name=Priya  → Optional param with value": "/hello?name=Priya",
            "GET /greet/FastAPI  → Path param": "/greet/FastAPI",
            "GET /add?a=5&b=7  → Query params": "/add?a=5&b=7",
            "GET /students  → All students": "/students",
        }
        choice = st.selectbox("Pick an endpoint:", list(endpoints.keys()))
        if st.button("🚀 Send Request"):
            path = endpoints[choice]
            d, c = api_get(path)
            if d is None:
                st.error("❌ Backend offline!")
            else:
                st.code(f"GET {API_URL}{path}\nStatus: {c}")
                st.json(d)
