import streamlit as st
import random

# ╔══════════════════════════════════════════════════════════════════╗
# ║                     YOUR ORIGINAL CLASSES                       ║
# ╚══════════════════════════════════════════════════════════════════╝

# ─── Guide Class (Mohammed Alzubaidi) ─────────────────────────────────────────
class Guide:
    def __init__(s, name, guide_id):
        s.name = name
        s.guide_id = guide_id
        s.assigned_sites = []

    def login(s, entered_id):  # checks if the entered ID belongs to this guide
        if s.guide_id == entered_id:
            return True
        return False

    def view_my_assigned_site(s): # shows all sites this guide is assigned to
        if not s.assigned_sites:
            print("You are not currently assigned to any site.")
        else:
            print("Your assigned sites:")
            for site in s.assigned_sites:
                print(f"- {site}")


# ─── Visitor Class (Meshari & Mohamed) ───────────────────────────────────────
class Visitor:
    def __init__(s, name, nationality, username, password):
        s.name = name
        s.nationality = nationality
        s.username = username
        s.password = password
        s.bookings = []  # list of dicts: [{booking_id, site_name}]

    def login(s, entered_username, entered_password):
        if s.username == entered_username and s.password == entered_password:
            return True
        return False

# ─── Manager Class (Saleh & Riyadh) ──────────────────────────────────────────
class Manager:
# Initializes lists for sites, guides dictionary, and unique booking IDs.
    def __init__(s):
        s.sites = []
        s.guide = {}
        s.visitors = {}       # username → Visitor object
        s.booking_ids = set()
 # Creates a new site dictionary and links it to a guide if provided.
    def add_site(s, name, site_type, capacity, guide_id=None):
        site = {
            "name": name,
            "type": site_type,
            "capacity": capacity,
            "guide_id": guide_id,
            "visitors": 0,
            "visitor_names": [],   # list of registered visitor names
            "status": "Open"
        }
        s.sites.append(site)
        if guide_id:
            s.guide[guide_id].assigned_sites.append(name)
 # Loops through and prints full details and status of all registered sites.
    def view_all_sites(s):
        if not s.sites:
            print("No sites available.")
            return
        for site in s.sites:
            print(f"Name: {site['name']} | Type: {site['type']} | "
                  f"Visitors: {site['visitors']} | Capacity: {site['capacity']} | "
                  f"Guide: {s.guide[site['guide_id']].name if site['guide_id'] and site['guide_id'] in s.guide else 'N/A'} | Status: {site['status']}")
# Filters and returns a list of all sites that currently have an "Open" status.
    def view_open_sites(s):
        open_sites = []
        for site in s.sites:
            if site["status"] == "Open":
                open_sites.append(site)
        return open_sites
# Finds the specified site by name and changes its status to "Closed".
    def close_site(s, site_name):
        for site in s.sites:
            if site["name"] == site_name:
                site["status"] = "Closed"
                print(f"Site '{site_name}' is now closed.")
                return
        print(f"Site '{site_name}' not found.")
# Finds the specified site by name and changes its status back to "Open".
    def reopen_site(s, site_name):
        for site in s.sites:
            if site["name"] == site_name:
                site["status"] = "Open"
                print(f"Site '{site_name}' is now open.")
                return
        print(f"Site '{site_name}' not found.")
 # Calculates and displays total sites, overall visitors, and the most visited site.
    def view_summary(s):
        total_sites = len(s.sites)
        total_visitors = sum(site["visitors"] for site in s.sites)
        most_visited = max(s.sites, key=lambda site: site["visitors"], default=None)
        print(f"Total sites: {total_sites}")
        print(f"Total registered visitors: {total_visitors}")
        if most_visited:
            print(f"Most visited site: {most_visited['name']} ({most_visited['visitors']} visitors)")
        else:
            print("No sites yet.")

    # ---------- Helper Methods ----------

    def site_exists(s, name):
        for site in s.sites:
            if site["name"] == name:
                return True
        return False

    # -------------------------- Guide Methods -----------------------------

    def add_new_Guide(s, name): # creates a guide with a unique random ID and stores it
        while True:
            guide_id = random.randint(1000, 9999)
            if guide_id not in s.guide:
                break
        new_guide = Guide(name, guide_id)
        s.guide[guide_id] = new_guide
        print(f"Guide '{name}' added with ID: {guide_id}")
        return guide_id

    def assign_guide(s, site_name, guide_id): # links an existing guide to a site (updates both sides)
        if guide_id not in s.guide:
            print(f"Guide with ID '{guide_id}' is not registered.")
            return
        for site in s.sites:
            if site["name"] == site_name:
                site["guide_id"] = guide_id
                s.guide[guide_id].assigned_sites.append(site_name)
                print(f"Guide '{s.guide[guide_id].name}' assigned to '{site_name}'.")
                return
        print(f"Site '{site_name}' not found.")

    def view_visitors_by_guide(s, guide_id): # collects each of the guide's sites with its visitor names
        result = []
        for site in s.sites:
            if site["guide_id"] == guide_id:
                result.append({"site": site["name"], "names": site["visitor_names"]})
        return result

 # ---------- Helper Methods ----------

    def guide_exists(s, guide_id):
        return guide_id in s.guide


# -------------------------- visitor Methods -----------------------------
    # Adds a new visitor to the system if the username is unique.
    def add_new_visitor(s, name, nationality, username, password):
        if username in s.visitors:
            return False
        new_visitor = Visitor(name, nationality, username, password)
        s.visitors[username] = new_visitor
        return True
    # Book a capacity-available, open site for a visitor who hasn't registered yet.
    def register_visitor(s, visitor, site_name):
        for site in s.sites:
            if site["name"] == site_name:
                if site["status"] != "Open":
                    return False, "Site is closed."
                if site["visitors"] >= site["capacity"]:
                    return False, "Site is full."
                for b in visitor.bookings:
                    if b["site_name"] == site_name:
                        return False, "You already registered for this site."
                site["visitors"] += 1
                site["visitor_names"].append(visitor.name)
                booking_id = s.generate_booking_id()
                visitor.bookings.append({"booking_id": booking_id, "site_name": site_name})
                return True, booking_id
        return False, "Site not found."
   # Cancel an active booking, free up site space, and remove records.
    def cancel_registration(s, visitor, booking_id):
        for b in visitor.bookings:
            if b["booking_id"] == booking_id:
                site_name = b["site_name"]
                for site in s.sites:
                    if site["name"] == site_name:
                        site["visitors"] -= 1
                        if visitor.name in site["visitor_names"]:
                            site["visitor_names"].remove(visitor.name)
                        break
                s.booking_ids.remove(booking_id)
                visitor.bookings.remove(b)
                return True, f"Booking {booking_id} cancelled."
        return False, "Booking ID not found."

 # ---------- Helper Methods ----------
    # Check if a specific username already exists in the system.
    def visitor_exists(s, username):
        return username in s.visitors
    # Generate a unique 4-digit booking ID not currently in use.
    def generate_booking_id(s):
        while True:
            booking_id = random.randint(1000, 9999)
            if booking_id not in s.booking_ids:
                s.booking_ids.add(booking_id)
                return booking_id


   # ------------------------------ Reflection ------------------------------

#==================== Riyad ahmed ====================

#1.Most Challenging Part:
#Tracing and reading the code because it was constantly changing,
#so I had to go back and re-read everything from the beginning many times.

#2.Most Enjoyable Concept:
#Relying on OOP concepts. The project idea became very easy because we divided
#it into three clear classes: Manager, Guide, and Visitor, which made everything simple.

#3.Improvements for More Time:
#I would expand the application's scope to support managing small festivals and
#local events, adding features like ticket pricing and event scheduling.
#====================================================
   #--------------------------------------------
  #  Meshari
  # Q1)Managing data consistency across nested data structures.
  # Q2)Efficient uniqueness check in the ID generator.
  # Q3)Improve UX-UI

    #--------------------------------------------
  #  Mohammed alzubaidi
  # Q1) The trickiest part is the relationship between guides and sites : (one guide can have many sites ) but (each site has only one guide) so "assigned_sites" is a list inside the Guide and "guide_id" is stores in the site
  # Q2) I liked using two concepts and how it  work together "random" creates the number, the "set" checks uniqueness
  # Q3) a lot of things like add "Guide passwords" and "Guide editing"

    #--------------------------------------------
  #  Mohammed Alhejaili
  # Q1)The most challenging part was getting the booking checks in order: that the site is open, then has space, then that the visitor hasn't already registered. I solved it with sequential if statements and an early return that stops the code at the first condition that fails.
  # Q2)The concept I enjoyed the most was using dictionaries and objects together, since it made organizing and looking up the data easy.
  # Q3)If I had more time, I would improve how the program searches for sites,and save the data to a file.

      #--------------------------------------------
  #  saleh
  # Q1)# Use while True in methods.
  # Q2)Connect classes and methods.
  # Q3)Add all Saudi tourist cities to the code.

# ╔══════════════════════════════════════════════════════════════════╗
# ║                  STREAMLIT APP (added for web UI)               ║
# ╚══════════════════════════════════════════════════════════════════╝

st.set_page_config(
    page_title="AlUla Tourism System",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── Theme tokens ─────────────────────────────────────────────────────────────
if st.session_state.get("theme", "dark") == "dark":
    T = {
        "app_bg": "#17120A", "sidebar_bg": "#100C06", "card_bg": "#251B0E",
        "input_bg": "#251B0E", "receipt_bg": "#0E0A05", "pill_bg": "#2E2210",
        "text": "#E8D5A0", "muted": "#C8A870", "gold": "#E8B84B", "gold_btn": "#C8922A",
        "border": "#C8922A44", "btn_text": "#17120A", "info_bg": "#14243A",
        "info_border": "#5A8AB8", "info_text": "#C0DCFF",
    }
else:
    T = {
        "app_bg": "#FBF7EE", "sidebar_bg": "#F3ECDC", "card_bg": "#FFFFFF",
        "input_bg": "#FFFFFF", "receipt_bg": "#FFFDF8", "pill_bg": "#F3E9D2",
        "text": "#3A2E16", "muted": "#7A6A45", "gold": "#A8741A", "gold_btn": "#C8922A",
        "border": "#C8922A55", "btn_text": "#FFFFFF", "info_bg": "#E6F0FA",
        "info_border": "#5A8AB8", "info_text": "#1A4A78",
    }

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{ background: {T["app_bg"]}; }}
[data-testid="stSidebar"] {{ background: {T["sidebar_bg"]} !important; border-right: 1px solid {T["border"]}; }}
[data-testid="stSidebar"] * {{ color: {T["text"]} !important; }}
.main .block-container {{ padding-top: 2.5rem; max-width: 800px; }}

h1, h2, h3, h4 {{ color: {T["gold"]} !important; font-weight: 600 !important; }}
p, div, span, label {{ color: {T["text"]} !important; }}

input {{ background: {T["input_bg"]} !important; color: {T["text"]} !important; border: 1px solid {T["border"]} !important; border-radius: 8px !important; }}
.stTextInput label, .stNumberInput label, .stSelectbox label {{ color: {T["muted"]} !important; font-weight: 500 !important; font-size: 13px !important; }}

.stButton > button {{ background: {T["gold_btn"]} !important; color: {T["btn_text"]} !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 14px !important; padding: 0.5rem 1.3rem !important; }}
.stButton > button:hover {{ background: {T["gold"]} !important; }}

.stSelectbox > div > div {{ background: {T["input_bg"]} !important; color: {T["text"]} !important; border: 1px solid {T["border"]} !important; }}
.stTabs [data-baseweb="tab"] {{ color: {T["muted"]} !important; }}
.stTabs [aria-selected="true"] {{ color: {T["gold"]} !important; border-bottom: 2px solid {T["gold"]} !important; }}

[data-testid="metric-container"] {{ background: {T["card_bg"]} !important; border: 1px solid {T["border"]} !important; border-radius: 10px !important; padding: 1rem !important; }}
[data-testid="stMetricValue"] {{ color: {T["gold"]} !important; }}
[data-testid="stMetricLabel"] {{ color: {T["muted"]} !important; }}

.stInfo > div {{ background: {T["info_bg"]} !important; border: 1px solid {T["info_border"]} !important; color: {T["info_text"]} !important; border-radius: 8px !important; }}
hr {{ border-color: {T["border"]} !important; }}

.alula-card {{ background: {T["card_bg"]}; border: 1px solid {T["border"]}; border-radius: 12px; padding: 1.1rem 1.3rem; margin-bottom: 10px; }}
.alula-card h4 {{ color: {T["gold"]} !important; margin: 0 0 5px; font-size: 15px; }}
.alula-card p {{ color: {T["muted"]} !important; margin: 0; font-size: 13px; }}

.role-card {{ background: {T["card_bg"]}; border: 1px solid {T["border"]}; border-radius: 14px; padding: 1.5rem 1rem; text-align: center; margin-bottom: 10px; }}
.role-card .role-icon {{ font-size: 34px; }}
.role-card h3 {{ color: {T["gold"]} !important; margin: 0.4rem 0 0.3rem; font-size: 18px; }}
.role-card p {{ color: {T["muted"]} !important; font-size: 12px; margin: 0; }}

.receipt-box {{ background: {T["receipt_bg"]}; border: 1px solid {T["gold_btn"]}; border-radius: 12px; padding: 1rem 1.3rem; margin-bottom: 8px; }}
.receipt-row {{ display: flex; justify-content: space-between; padding: 5px 0; }}
.receipt-label {{ color: {T["muted"]} !important; font-size: 13px; }}
.receipt-value {{ color: {T["text"]} !important; font-size: 13px; font-weight: 500; }}
.receipt-id {{ color: {T["gold"]} !important; font-size: 18px !important; font-weight: 700 !important; }}

.name-pill {{ display:inline-block; background:{T["pill_bg"]}; border:1px solid {T["border"]}; color:{T["text"]}; padding:3px 10px; border-radius:14px; font-size:12px; margin:3px 4px 0 0; }}
</style>
""", unsafe_allow_html=True)

# ─── Session state ────────────────────────────────────────────────────────────
# Bump this number whenever the Manager/Visitor/Guide data shape changes,
# so a fresh Manager is rebuilt instead of reusing an old incompatible one.
SCHEMA_VERSION = 3

def seed_example_data(m):
    """Adds 4 example sites with 2 guides so the app isn't empty on first load."""
    g1 = m.add_new_Guide("Ahmed")
    g2 = m.add_new_Guide("Sara")
    m.add_site("AlUla Old Town", "Historical", 50, g1)
    m.add_site("Hegra", "Archaeological", 30, g2)
    m.add_site("Dadan", "Historical", 20, g1)
    m.add_site("Jabal Ikmah", "Rock Art", 15, None)

if st.session_state.get("schema_version") != SCHEMA_VERSION:
    st.session_state.manager = Manager()
    seed_example_data(st.session_state.manager)   # ← seed the 4 example sites
    st.session_state.schema_version = SCHEMA_VERSION
    st.session_state.role = None
    st.session_state.logged_in_guide = None
    st.session_state.logged_in_visitor = None

if "manager" not in st.session_state:
    st.session_state.manager = Manager()
if "role" not in st.session_state:
    st.session_state.role = None
if "logged_in_guide" not in st.session_state:
    st.session_state.logged_in_guide = None
if "logged_in_visitor" not in st.session_state:
    st.session_state.logged_in_visitor = None
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "pending_toast" not in st.session_state:
    st.session_state.pending_toast = None

manager = st.session_state.manager

# Show any toast queued from before the last rerun
if st.session_state.pending_toast:
    st.toast(st.session_state.pending_toast)
    st.session_state.pending_toast = None

def notify(msg):
    """Queue a toast that survives the next st.rerun()."""
    st.session_state.pending_toast = msg

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ AlUla Tourism")
    theme_label = "🌙 Dark mode" if st.session_state.theme == "light" else "☀️ Light mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()
    st.markdown("---")
    if st.session_state.role is None:
        st.caption("Pick a role to begin")
    else:
        st.markdown(f"### {st.session_state.role.capitalize()}")
        st.markdown("---")
        if st.session_state.role == "manager":
            if st.button("📊  Summary", use_container_width=True):
                st.session_state.manager_page = "summary"; st.rerun()
            if st.button("🗺️  Sites", use_container_width=True):
                st.session_state.manager_page = "sites"; st.rerun()
            if st.button("🧭  Guides", use_container_width=True):
                st.session_state.manager_page = "guides"; st.rerun()
        elif st.session_state.role == "guide":
            if st.session_state.logged_in_guide:
                st.markdown(f"**{st.session_state.logged_in_guide.name}**")
                st.markdown("---")
                if st.button("🗺️  My sites", use_container_width=True):
                    st.session_state.guide_page = "sites"; st.rerun()
                if st.button("👥  My visitors", use_container_width=True):
                    st.session_state.guide_page = "visitors"; st.rerun()
        elif st.session_state.role == "visitor":
            if st.session_state.logged_in_visitor:
                st.markdown(f"**{st.session_state.logged_in_visitor.name}**")
                st.markdown("---")
                if st.button("🔍  Browse sites", use_container_width=True):
                    st.session_state.visitor_page = "browse"; st.rerun()
                if st.button("🎟️  My bookings", use_container_width=True):
                    st.session_state.visitor_page = "bookings"; st.rerun()
        st.markdown("---")
        if st.button("🔙  Back to home", use_container_width=True):
            st.session_state.role = None
            st.session_state.logged_in_guide = None
            st.session_state.logged_in_visitor = None
            st.rerun()

# ─── Home ─────────────────────────────────────────────────────────────────────
if st.session_state.role is None:
    st.markdown("# 🏛️ AlUla Tourism System")
    st.caption("Select your role to get started")
    st.markdown("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="role-card"><div class="role-icon">🏢</div><h3>Manager</h3><p>Sites, guides & summary</p></div>', unsafe_allow_html=True)
        if st.button("Enter", use_container_width=True, key="h_m"):
            st.session_state.role = "manager"; st.session_state.manager_page = "summary"; st.rerun()
    with col2:
        st.markdown('<div class="role-card"><div class="role-icon">🧭</div><h3>Guide</h3><p>Your sites & visitors</p></div>', unsafe_allow_html=True)
        if st.button("Enter", use_container_width=True, key="h_g"):
            st.session_state.role = "guide"; st.rerun()
    with col3:
        st.markdown('<div class="role-card"><div class="role-icon">🎟️</div><h3>Visitor</h3><p>Browse & register</p></div>', unsafe_allow_html=True)
        if st.button("Enter", use_container_width=True, key="h_v"):
            st.session_state.role = "visitor"; st.rerun()

# ─── Manager ──────────────────────────────────────────────────────────────────
elif st.session_state.role == "manager":
    if "manager_page" not in st.session_state:
        st.session_state.manager_page = "summary"
    page = st.session_state.manager_page

    if page == "summary":
        st.markdown("# 📊 Summary")
        total_sites = len(manager.sites)
        total_visitors = sum(site["visitors"] for site in manager.sites)
        most_visited = max(manager.sites, key=lambda site: site["visitors"], default=None)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total sites", total_sites)
        c2.metric("Total visitors", total_visitors)
        c3.metric("Most visited", most_visited["name"] if most_visited and most_visited["visitors"] > 0 else "—")
        st.markdown("---")
        st.markdown("#### Guides")
        if manager.guide:
            for g in manager.guide.values():
                st.markdown(f"- **{g.name}** — ID `{g.guide_id}` — {len(g.assigned_sites)} site(s)")
        else:
            st.info("No guides yet.")

    elif page == "sites":
        st.markdown("# 🗺️ Sites")
        tab1, tab2, tab3 = st.tabs(["All sites", "Add site", "Manage"])
        with tab1:
            if not manager.sites:
                st.info("No sites yet.")
            for site in manager.sites:
                gname = manager.guide[site["guide_id"]].name if site["guide_id"] and site["guide_id"] in manager.guide else "N/A"
                badge = "🟢 Open" if site["status"] == "Open" else "🔴 Closed"
                st.markdown(f'<div class="alula-card"><h4>{site["name"]} &nbsp; {badge}</h4><p>{site["type"]} · {site["visitors"]}/{site["capacity"]} visitors · Guide: {gname}</p></div>', unsafe_allow_html=True)
        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                site_name = st.text_input("Site name")
                site_type = st.text_input("Site type")
            with c2:
                capacity = st.number_input("Max capacity", min_value=1, value=50)
                gopts = ["None"] + [f"{g.name} (ID: {gid})" for gid, g in manager.guide.items()]
                gchoice = st.selectbox("Guide (optional)", gopts)
            if st.button("Add site"):
                if not site_name:
                    st.toast("❌ Enter a site name.")
                elif manager.site_exists(site_name):
                    st.toast(f"❌ '{site_name}' already exists.")
                else:
                    gid = None
                    if gchoice != "None":
                        gid = int(gchoice.split("ID: ")[1].replace(")", ""))
                    manager.add_site(site_name, site_type, capacity, gid)
                    notify(f"✅ Site '{site_name}' added!")
                    st.rerun()
        with tab3:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Assign guide**")
                if manager.sites and manager.guide:
                    asite = st.selectbox("Site", [s["name"] for s in manager.sites], key="asite")
                    aguide = st.selectbox("Guide", [f"{g.name} (ID: {gid})" for gid, g in manager.guide.items()], key="aguide")
                    if st.button("Assign"):
                        gid = int(aguide.split("ID: ")[1].replace(")", ""))
                        manager.assign_guide(asite, gid)
                        notify(f"✅ Guide assigned to '{asite}'!")
                        st.rerun()
                else:
                    st.info("Need a site and a guide.")
            with c2:
                st.markdown("**Open / Close site**")
                if manager.sites:
                    csite = st.selectbox("Site", [s["name"] for s in manager.sites], key="csite")
                    cur = next((s for s in manager.sites if s["name"] == csite), None)
                    if cur and cur["status"] == "Open":
                        if st.button("🔴 Close site"):
                            manager.close_site(csite)
                            notify(f"✅ '{csite}' closed.")
                            st.rerun()
                    elif cur:
                        if st.button("🟢 Reopen site"):
                            manager.reopen_site(csite)
                            notify(f"✅ '{csite}' reopened.")
                            st.rerun()
                else:
                    st.info("No sites yet.")

    elif page == "guides":
        st.markdown("# 🧭 Guides")
        tab1, tab2 = st.tabs(["All guides", "Add guide"])
        with tab1:
            if not manager.guide:
                st.info("No guides yet.")
            for gid, g in manager.guide.items():
                sites_str = ", ".join(g.assigned_sites) if g.assigned_sites else "None"
                st.markdown(f'<div class="alula-card"><h4>{g.name} &nbsp; <small style="color:#C8A870">ID {gid}</small></h4><p>Sites: {sites_str}</p></div>', unsafe_allow_html=True)
        with tab2:
            st.info("ℹ️ Guide ID is generated automatically.")
            gname = st.text_input("Guide name")
            if st.button("Add guide"):
                if not gname:
                    st.toast("❌ Enter a guide name.")
                else:
                    nid = manager.add_new_Guide(gname)
                    notify(f"✅ '{gname}' added — ID {nid}")
                    st.rerun()

# ─── Guide ────────────────────────────────────────────────────────────────────
elif st.session_state.role == "guide":
    if not st.session_state.logged_in_guide:
        st.markdown("# 🧭 Guide Login")
        gid_text = st.text_input("Enter your Guide ID")
        if st.button("Login"):
            if not gid_text.isdigit():
                st.toast("❌ ID must be a number.")
            else:
                found = None
                for g in manager.guide.values():
                    if g.login(int(gid_text)):
                        found = g
                        break
                if found:
                    st.session_state.logged_in_guide = found
                    st.session_state.guide_page = "sites"
                    notify(f"✅ Welcome, {found.name}!")
                    st.rerun()
                else:
                    st.toast("❌ Guide ID not found.")
    else:
        guide = st.session_state.logged_in_guide
        if "guide_page" not in st.session_state:
            st.session_state.guide_page = "sites"
        if st.session_state.guide_page == "sites":
            st.markdown("# 🗺️ My assigned sites")
            if not guide.assigned_sites:
                st.info("No sites assigned yet.")
            for sname in guide.assigned_sites:
                for site in manager.sites:
                    if site["name"] == sname:
                        badge = "🟢 Open" if site["status"] == "Open" else "🔴 Closed"
                        st.markdown(f'<div class="alula-card"><h4>{site["name"]} &nbsp; {badge}</h4><p>{site["type"]} · {site["visitors"]}/{site["capacity"]} visitors</p></div>', unsafe_allow_html=True)
        elif st.session_state.guide_page == "visitors":
            st.markdown("# 👥 My visitors")
            results = manager.view_visitors_by_guide(guide.guide_id)
            if not results:
                st.info("No sites assigned yet.")
            for r in results:
                names_html = ""
                if r["names"]:
                    names_html = "".join([f'<span class="name-pill">{n}</span>' for n in r["names"]])
                else:
                    names_html = '<span style="color:#9A8B72; font-size:12px;">No visitors yet</span>'
                st.markdown(f'<div class="alula-card"><h4>{r["site"]}</h4><div style="margin-top:6px;">{names_html}</div></div>', unsafe_allow_html=True)

# ─── Visitor ──────────────────────────────────────────────────────────────────
elif st.session_state.role == "visitor":
    if not st.session_state.logged_in_visitor:
        st.markdown("# 🎟️ Visitor")
        tab1, tab2 = st.tabs(["Login", "Create account"])
        with tab1:
            u = st.text_input("Username", key="lu")
            p = st.text_input("Password", type="password", key="lp")
            if st.button("Login"):
                if not u or not p:
                    st.toast("❌ Fill in all fields.")
                elif not manager.visitor_exists(u):
                    st.toast("❌ Username not found.")
                else:
                    v = manager.visitors[u]
                    if v.login(u, p):
                        st.session_state.logged_in_visitor = v
                        st.session_state.visitor_page = "browse"
                        notify(f"✅ Welcome back, {v.name}!")
                        st.rerun()
                    else:
                        st.toast("❌ Incorrect password.")
        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                nn = st.text_input("Full name", key="rn")
                nu = st.text_input("Username", key="ru")
            with c2:
                nat = st.text_input("Nationality", key="rnat")
                npw = st.text_input("Password", type="password", key="rp")
            if st.button("Create account"):
                if not nn or not nu or not nat or not npw:
                    st.toast("❌ Fill in all fields.")
                elif manager.visitor_exists(nu):
                    st.toast(f"❌ Username '{nu}' taken.")
                else:
                    manager.add_new_visitor(nn, nat, nu, npw)
                    st.toast(f"✅ Account created! You can login now.")
    else:
        visitor = st.session_state.logged_in_visitor
        if "visitor_page" not in st.session_state:
            st.session_state.visitor_page = "browse"
        if st.session_state.visitor_page == "browse":
            st.markdown("# 🔍 Open sites")
            open_sites = manager.view_open_sites()
            if not open_sites:
                st.info("No open sites right now.")
            for site in open_sites:
                gname = manager.guide[site["guide_id"]].name if site["guide_id"] and site["guide_id"] in manager.guide else "N/A"
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f'<div class="alula-card"><h4>{site["name"]}</h4><p>{site["type"]} · Guide: {gname} · {site["visitors"]}/{site["capacity"]}</p></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown("<div style='padding-top:12px'>", unsafe_allow_html=True)
                    if st.button("Register", key=f"reg_{site['name']}"):
                        ok, res = manager.register_visitor(visitor, site["name"])
                        if ok:
                            notify(f"✅ Registered! Booking ID {res}")
                            st.rerun()
                        else:
                            st.toast(f"❌ {res}")
                    st.markdown("</div>", unsafe_allow_html=True)
        elif st.session_state.visitor_page == "bookings":
            st.markdown("# 🎟️ My bookings")
            if not visitor.bookings:
                st.info("No active bookings.")
            for b in visitor.bookings:
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f'<div class="receipt-box"><div class="receipt-row"><span class="receipt-label">Site</span><span class="receipt-value">{b["site_name"]}</span></div><div class="receipt-row"><span class="receipt-label">Booking ID</span><span class="receipt-id">{b["booking_id"]}</span></div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown("<div style='padding-top:18px'>", unsafe_allow_html=True)
                    if st.button("Cancel", key=f"c_{b['booking_id']}"):
                        ok, msg = manager.cancel_registration(visitor, b["booking_id"])
                        if ok:
                            notify(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.toast(f"❌ {msg}")
                    st.markdown("</div>", unsafe_allow_html=True)
