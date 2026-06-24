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
        s.assigned_sites = []  # list: one guide can have many sites

    def login(s, entered_id):
        if s.guide_id == entered_id:
            return True
        return False

    def view_my_assigned_site(s):
        if not s.assigned_sites:
            print("You are not currently assigned to any site.")
        else:
            print("Your assigned sites:")
            for site in s.assigned_sites:
                print(f"- {site}")


# ─── Visitor Class (Meshari & Mohamed) ───────────────────────────────────────
class Visitor:
    def __init__(s, name, nationality):
        s.name = name
        s.nationality = nationality
        s.booking_id = None   # assigned later by system
        s.booked_site = None  # assigned later by system

    def register_in_system(s):
        print(f"You are now registered as {s.name} and your nationality is {s.nationality}. Welcome!")


# ─── Manager Class (Saleh & Riyadh) ──────────────────────────────────────────
class Manager:
    def __init__(s):
        s.sites = []         # list of site dicts
        s.guide = {}         # guide_id → Guide object
        s.booking_ids = set() # unique booking IDs

    def site_exists(s, name):
        for site in s.sites:
            if site["name"] == name:
                return True
        return False

    def guide_exists(s, guide_id):
        return guide_id in s.guide

    def add_site(s, name, site_type, capacity, guide_id=None):
        site = {
            "name": name,
            "type": site_type,
            "capacity": capacity,
            "guide_id": guide_id,
            "visitors": 0,
            "status": "Open"
        }
        s.sites.append(site)
        if guide_id:
            s.guide[guide_id].assigned_sites.append(name)

    def view_all_sites(s):
        if not s.sites:
            print("No sites available.")
            return
        for site in s.sites:
            print(f"Name: {site['name']} | Type: {site['type']} | "
                  f"Visitors: {site['visitors']} | Capacity: {site['capacity']} | "
                  f"Guide: {s.guide[site['guide_id']].name if site['guide_id'] and site['guide_id'] in s.guide else 'N/A'} | Status: {site['status']}")

    def view_open_sites(s):
        # lambda requirement: filter open sites using lambda
        return list(filter(lambda site: site["status"] == "Open", s.sites))

    def add_new_Guide(s, name, guide_id):
        if guide_id in s.guide:
            print(f"Guide with ID '{guide_id}' named {s.guide[guide_id].name} already exists.")
        else:
            new_guide = Guide(name, guide_id)
            s.guide[guide_id] = new_guide
            print(f"Guide '{name}' (ID: {guide_id}) added to available guides.")

    def assign_guide(s, site_name, guide_id):
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

    def close_site(s, site_name):
        for site in s.sites:
            if site["name"] == site_name:
                site["status"] = "Closed"
                print(f"Site '{site_name}' is now closed.")
                return
        print(f"Site '{site_name}' not found.")

    def view_summary(s):
        total_sites = len(s.sites)
        total_visitors = sum(site["visitors"] for site in s.sites)
        # lambda requirement: used as key for max()
        most_visited = max(s.sites, key=lambda site: site["visitors"], default=None)
        print(f"Total sites: {total_sites}")
        print(f"Total registered visitors: {total_visitors}")
        if most_visited:
            print(f"Most visited site: {most_visited['name']} ({most_visited['visitors']} visitors)")
        else:
            print("No sites yet.")
        print(f"Available Guides: {', '.join([f'{g.name} (ID: {g.guide_id})' for g in s.guide.values()]) if s.guide else 'None'}")

    def generate_booking_id(s):
        while True:
            booking_id = random.randint(1000, 9999)
            if booking_id not in s.booking_ids:
                s.booking_ids.add(booking_id)
                return booking_id

    def register_visitor(s, visitor, site_name):
        for site in s.sites:
            if site["name"] == site_name:
                if site["status"] != "Open":
                    return False, "Site is closed."
                if site["visitors"] >= site["capacity"]:
                    return False, "Site is full."
                site["visitors"] += 1
                visitor.booking_id = s.generate_booking_id()
                visitor.booked_site = site_name
                return True, visitor.booking_id
        return False, "Site not found."

    def cancel_registration(s, booking_id, site_name):
        if booking_id not in s.booking_ids:
            return False, "Booking ID not found."
        for site in s.sites:
            if site["name"] == site_name:
                site["visitors"] -= 1
                s.booking_ids.remove(booking_id)
                return True, "Booking cancelled."
        return False, "Site not found."

    def view_visitors_by_guide(s, guide_id):
        result = []
        for site in s.sites:
            if site["guide_id"] == guide_id:
                result.append({"site": site["name"], "visitors": site["visitors"]})
        return result


# ╔══════════════════════════════════════════════════════════════════╗
# ║                  STREAMLIT APP (added for web UI)               ║
# ╚══════════════════════════════════════════════════════════════════╝

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AlUla Tourism System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Desert dark theme CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #1A1208; }
[data-testid="stSidebar"] { background: #120D05 !important; border-right: 1px solid #3A2A10; }
[data-testid="stSidebar"] * { color: #C8A870 !important; }
.main .block-container { padding-top: 2rem; }
h1, h2, h3 { color: #E8B84B !important; }
p, label, .stMarkdown { color: #C8A870 !important; }
input, textarea, select { background: #2A1E0F !important; color: #C8A870 !important; border: 1px solid #3A2A10 !important; border-radius: 8px !important; }
.stTextInput input, .stNumberInput input { background: #2A1E0F !important; color: #E8B84B !important; }
.stButton > button { background: #C8922A !important; color: #1A1208 !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; padding: 0.5rem 1.2rem !important; }
.stButton > button:hover { background: #E8B84B !important; }
.stSelectbox > div > div { background: #2A1E0F !important; color: #C8A870 !important; border: 1px solid #3A2A10 !important; }
[data-testid="metric-container"] { background: #2A1E0F !important; border: 1px solid #3A2A10 !important; border-radius: 10px !important; padding: 1rem !important; }
[data-testid="stMetricValue"] { color: #E8B84B !important; }
[data-testid="stMetricLabel"] { color: #7A6A4A !important; }
hr { border-color: #3A2A10 !important; }
.alula-card { background: #2A1E0F; border: 1px solid #3A2A10; border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 12px; }
.alula-card h4 { color: #E8B84B !important; margin: 0 0 4px; font-size: 15px; }
.alula-card p { color: #7A6A4A !important; margin: 0; font-size: 12px; }
.receipt-box { background: #0F0A05; border: 1px solid #C8922A; border-radius: 12px; padding: 1.5rem; max-width: 400px; }
.receipt-box h3 { color: #E8B84B !important; text-align: center; margin-bottom: 1rem; }
.receipt-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2A1E0F; }
.receipt-label { color: #7A6A4A !important; font-size: 13px; }
.receipt-value { color: #C8A870 !important; font-size: 13px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ─── Session state — keeps data alive between Streamlit reruns ────────────────
if "manager" not in st.session_state:
    st.session_state.manager = Manager()
if "role" not in st.session_state:
    st.session_state.role = None
if "logged_in_guide" not in st.session_state:
    st.session_state.logged_in_guide = None
if "current_visitor" not in st.session_state:
    st.session_state.current_visitor = None

manager = st.session_state.manager

# ─── Sidebar navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ AlUla Tourism")
    st.markdown("---")

    if st.session_state.role is None:
        st.markdown("### Select your role")
        if st.button("🏢  Manager", use_container_width=True):
            st.session_state.role = "manager"
            st.rerun()
        if st.button("🧭  Guide", use_container_width=True):
            st.session_state.role = "guide"
            st.rerun()
        if st.button("🎟️  Visitor", use_container_width=True):
            st.session_state.role = "visitor"
            st.rerun()
    else:
        st.markdown(f"### {st.session_state.role.capitalize()}")
        st.markdown("---")

        if st.session_state.role == "manager":
            if st.button("📊  Summary", use_container_width=True):
                st.session_state.manager_page = "summary"
                st.rerun()
            if st.button("🗺️  Sites", use_container_width=True):
                st.session_state.manager_page = "sites"
                st.rerun()
            if st.button("🧭  Guides", use_container_width=True):
                st.session_state.manager_page = "guides"
                st.rerun()

        elif st.session_state.role == "guide":
            if st.session_state.logged_in_guide:
                st.markdown(f"**Welcome, {st.session_state.logged_in_guide.name}!**")
                st.markdown("---")
                if st.button("🗺️  My sites", use_container_width=True):
                    st.session_state.guide_page = "sites"
                    st.rerun()
                if st.button("👥  My visitors", use_container_width=True):
                    st.session_state.guide_page = "visitors"
                    st.rerun()

        elif st.session_state.role == "visitor":
            if st.session_state.current_visitor:
                st.markdown(f"**{st.session_state.current_visitor.name}**")
                st.markdown("---")
                if st.button("🔍  Browse sites", use_container_width=True):
                    st.session_state.visitor_page = "browse"
                    st.rerun()
                if st.button("🎟️  My booking", use_container_width=True):
                    st.session_state.visitor_page = "booking"
                    st.rerun()
                if st.button("❌  Cancel booking", use_container_width=True):
                    st.session_state.visitor_page = "cancel"
                    st.rerun()

        st.markdown("---")
        if st.button("🔙  Back to home", use_container_width=True):
            st.session_state.role = None
            st.session_state.logged_in_guide = None
            st.session_state.current_visitor = None
            st.rerun()

# ─── Home page ────────────────────────────────────────────────────────────────
if st.session_state.role is None:
    st.markdown("# 🏛️ AlUla Tourism System")
    st.markdown("##### Welcome — select your role from the sidebar to get started")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="alula-card"><h4>🏢 Manager</h4><p>Manage sites, assign guides, view system summary and close sites.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="alula-card"><h4>🧭 Guide</h4><p>Login with your ID to view your assigned sites and registered visitors.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="alula-card"><h4>🎟️ Visitor</h4><p>Browse open sites, register for a visit and get your booking confirmation.</p></div>', unsafe_allow_html=True)

# ─── Manager pages ────────────────────────────────────────────────────────────
elif st.session_state.role == "manager":
    if "manager_page" not in st.session_state:
        st.session_state.manager_page = "summary"
    page = st.session_state.manager_page

    if page == "summary":
        st.markdown("# 📊 Summary")
        total_sites = len(manager.sites)
        total_visitors = sum(site["visitors"] for site in manager.sites)
        most_visited = max(manager.sites, key=lambda site: site["visitors"], default=None)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total sites", total_sites)
        col2.metric("Total visitors", total_visitors)
        col3.metric("Most visited", most_visited["name"] if most_visited and most_visited["visitors"] > 0 else "—")
        st.markdown("---")
        st.markdown("#### Available guides")
        if manager.guide:
            for g in manager.guide.values():
                st.markdown(f"- **{g.name}** (ID: `{g.guide_id}`) — {len(g.assigned_sites)} site(s)")
        else:
            st.info("No guides added yet.")

    elif page == "sites":
        st.markdown("# 🗺️ Sites")
        tab1, tab2, tab3 = st.tabs(["All sites", "Add site", "Assign / Close"])

        with tab1:
            if not manager.sites:
                st.info("No sites added yet.")
            else:
                for site in manager.sites:
                    guide_name = manager.guide[site["guide_id"]].name if site["guide_id"] and site["guide_id"] in manager.guide else "N/A"
                    badge = "🟢 Open" if site["status"] == "Open" else "🔴 Closed"
                    st.markdown(f'<div class="alula-card"><h4>{site["name"]} &nbsp; <small>{badge}</small></h4><p>Type: {site["type"]} &nbsp;|&nbsp; Visitors: {site["visitors"]}/{site["capacity"]} &nbsp;|&nbsp; Guide: {guide_name}</p></div>', unsafe_allow_html=True)

        with tab2:
            st.markdown("#### Add a new site")
            col1, col2 = st.columns(2)
            with col1:
                site_name = st.text_input("Site name")
                site_type = st.text_input("Site type")
            with col2:
                capacity = st.number_input("Max capacity", min_value=1, value=50)
                guide_options = ["None"] + [f"{g.name} (ID: {gid})" for gid, g in manager.guide.items()]
                guide_choice = st.selectbox("Assign guide (optional)", guide_options)
            if st.button("Add site"):
                if not site_name:
                    st.error("Please enter a site name.")
                elif manager.site_exists(site_name):
                    st.error(f"Site '{site_name}' already exists.")
                else:
                    guide_id = None
                    if guide_choice != "None":
                        guide_id = int(guide_choice.split("ID: ")[1].replace(")", ""))
                    manager.add_site(site_name, site_type, capacity, guide_id)
                    st.success(f"Site '{site_name}' added successfully!")
                    st.rerun()

        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Assign a guide")
                if manager.sites and manager.guide:
                    sel_site = st.selectbox("Select site", [s["name"] for s in manager.sites], key="assign_site")
                    sel_guide = st.selectbox("Select guide", [f"{g.name} (ID: {gid})" for gid, g in manager.guide.items()], key="assign_guide")
                    if st.button("Assign guide"):
                        guide_id = int(sel_guide.split("ID: ")[1].replace(")", ""))
                        manager.assign_guide(sel_site, guide_id)
                        st.success(f"Guide assigned to '{sel_site}'!")
                        st.rerun()
                else:
                    st.info("Need at least one site and one guide.")
            with col2:
                st.markdown("#### Close a site")
                open_sites = [s["name"] for s in manager.sites if s["status"] == "Open"]
                if open_sites:
                    sel_close = st.selectbox("Select site to close", open_sites, key="close_site")
                    if st.button("Close site"):
                        manager.close_site(sel_close)
                        st.success(f"'{sel_close}' is now closed.")
                        st.rerun()
                else:
                    st.info("No open sites to close.")

    elif page == "guides":
        st.markdown("# 🧭 Guides")
        tab1, tab2 = st.tabs(["All guides", "Add guide"])
        with tab1:
            if not manager.guide:
                st.info("No guides added yet.")
            else:
                for gid, g in manager.guide.items():
                    sites_str = ", ".join(g.assigned_sites) if g.assigned_sites else "None"
                    st.markdown(f'<div class="alula-card"><h4>{g.name} &nbsp; <small style="color:#7A6A4A">ID: {gid}</small></h4><p>Assigned sites: {sites_str}</p></div>', unsafe_allow_html=True)
        with tab2:
            st.markdown("#### Add a new guide")
            col1, col2 = st.columns(2)
            with col1:
                guide_name = st.text_input("Guide name")
            with col2:
                guide_id = st.number_input("Guide ID", min_value=1000, max_value=99999, value=1000)
            if st.button("Add guide"):
                if not guide_name:
                    st.error("Please enter a guide name.")
                elif manager.guide_exists(int(guide_id)):
                    st.error(f"Guide with ID {guide_id} already exists.")
                else:
                    manager.add_new_Guide(guide_name, int(guide_id))
                    st.success(f"Guide '{guide_name}' added with ID {guide_id}!")
                    st.rerun()

# ─── Guide pages ──────────────────────────────────────────────────────────────
elif st.session_state.role == "guide":
    if not st.session_state.logged_in_guide:
        st.markdown("# 🧭 Guide Login")
        st.markdown("Enter your guide ID to continue.")
        guide_id_input = st.number_input("Guide ID", min_value=1000, max_value=99999, value=1000)
        if st.button("Login"):
            found = None
            for g in manager.guide.values():
                if g.login(int(guide_id_input)):
                    found = g
                    break
            if found:
                st.session_state.logged_in_guide = found
                st.session_state.guide_page = "sites"
                st.rerun()
            else:
                st.error("Guide ID not found. Please try again.")
    else:
        guide = st.session_state.logged_in_guide
        if "guide_page" not in st.session_state:
            st.session_state.guide_page = "sites"

        if st.session_state.guide_page == "sites":
            st.markdown("# 🗺️ My assigned sites")
            if not guide.assigned_sites:
                st.info("You are not assigned to any sites yet.")
            else:
                for site_name in guide.assigned_sites:
                    for site in manager.sites:
                        if site["name"] == site_name:
                            st.markdown(f'<div class="alula-card"><h4>{site["name"]}</h4><p>Type: {site["type"]} &nbsp;|&nbsp; Visitors: {site["visitors"]}/{site["capacity"]} &nbsp;|&nbsp; Status: {site["status"]}</p></div>', unsafe_allow_html=True)

        elif st.session_state.guide_page == "visitors":
            st.markdown("# 👥 My visitors")
            results = manager.view_visitors_by_guide(guide.guide_id)
            if not results:
                st.info("No visitors registered for your sites.")
            else:
                for r in results:
                    st.markdown(f'<div class="alula-card"><h4>{r["site"]}</h4><p>Registered visitors: {r["visitors"]}</p></div>', unsafe_allow_html=True)

# ─── Visitor pages ────────────────────────────────────────────────────────────
elif st.session_state.role == "visitor":
    if not st.session_state.current_visitor:
        st.markdown("# 🎟️ Visitor Registration")
        st.markdown("Enter your details to get started.")
        col1, col2 = st.columns(2)
        with col1:
            v_name = st.text_input("Your name")
        with col2:
            v_nationality = st.text_input("Your nationality")
        if st.button("Continue"):
            if not v_name or not v_nationality:
                st.error("Please fill in all fields.")
            else:
                st.session_state.current_visitor = Visitor(v_name, v_nationality)
                st.session_state.visitor_page = "browse"
                st.rerun()
    else:
        visitor = st.session_state.current_visitor
        if "visitor_page" not in st.session_state:
            st.session_state.visitor_page = "browse"

        if st.session_state.visitor_page == "browse":
            st.markdown("# 🔍 Open sites")
            open_sites = manager.view_open_sites()
            if not open_sites:
                st.info("No open sites available right now.")
            else:
                for site in open_sites:
                    guide_name = manager.guide[site["guide_id"]].name if site["guide_id"] and site["guide_id"] in manager.guide else "N/A"
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f'<div class="alula-card"><h4>{site["name"]}</h4><p>Type: {site["type"]} &nbsp;|&nbsp; Guide: {guide_name} &nbsp;|&nbsp; Visitors: {site["visitors"]}/{site["capacity"]}</p></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown("<div style='padding-top:12px'>", unsafe_allow_html=True)
                        if st.button("Register", key=f"reg_{site['name']}"):
                            if visitor.booked_site:
                                st.error("You already have an active booking.")
                            else:
                                success, result = manager.register_visitor(visitor, site["name"])
                                if success:
                                    st.session_state.visitor_page = "booking"
                                    st.rerun()
                                else:
                                    st.error(result)
                        st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.visitor_page == "booking":
            st.markdown("# 🎟️ My booking")
            if visitor.booking_id is None:
                st.info("You have no active booking. Browse sites to register.")
            else:
                st.markdown(f"""
                <div class="receipt-box">
                    <h3>Booking Confirmation</h3>
                    <div class="receipt-row"><span class="receipt-label">Name</span><span class="receipt-value">{visitor.name}</span></div>
                    <div class="receipt-row"><span class="receipt-label">Nationality</span><span class="receipt-value">{visitor.nationality}</span></div>
                    <div class="receipt-row"><span class="receipt-label">Site</span><span class="receipt-value">{visitor.booked_site}</span></div>
                    <div class="receipt-row"><span class="receipt-label">Booking ID</span><span class="receipt-value" style="color:#E8B84B; font-size:16px; font-weight:600;">{visitor.booking_id}</span></div>
                </div>
                <p style="margin-top:12px; font-size:12px; color:#5A4A2A !important;">Save your Booking ID to cancel later.</p>
                """, unsafe_allow_html=True)

        elif st.session_state.visitor_page == "cancel":
            st.markdown("# ❌ Cancel booking")
            if visitor.booking_id is None:
                st.info("You have no active booking to cancel.")
            else:
                st.markdown(f"Your current booking: **{visitor.booked_site}** (ID: `{visitor.booking_id}`)")
                st.warning("This action cannot be undone.")
                if st.button("Confirm cancellation"):
                    success, msg = manager.cancel_registration(visitor.booking_id, visitor.booked_site)
                    if success:
                        visitor.booking_id = None
                        visitor.booked_site = None
                        st.success("Booking cancelled successfully!")
                        st.session_state.visitor_page = "browse"
                        st.rerun()
                    else:
                        st.error(msg)
