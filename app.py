import streamlit as st
import pandas as pd
import os
from PIL import Image
import datetime

# Configuración de la página
st.set_page_config(
    page_title="Al Nassr Scouting System",
    page_icon="alnassr.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mapeo de categorías a archivos
CATEGORY_DB_FILES = {
    "PRO LEAGUE": "dbproleague.xlsx",
    "SAUDI U21 LEAGUE": "dbsaudiu21.xlsx",
    "U18 & U17 PREMIER LEAGUE": "dbu18_dbu17.xlsx"  # Nuevo archivo con sheets
}

CATEGORY_REPORT_FILES = {
    "PRO LEAGUE": "mreportsproleague.xlsx",
    "SAUDI U21 LEAGUE": "mreportsu21.xlsx",
    "U18 & U17 PREMIER LEAGUE": "mreportsu18.xlsx"
}

CATEGORY_ANALYTICS_FILES = {
    "PRO LEAGUE": "analyticsproleague.xlsx",
    "SAUDI U21 LEAGUE": "analyticsu21.xlsx",
    "U18 & U17 PREMIER LEAGUE": "analyticsu18u17.xlsx"
}

CATEGORY_ICONS = {
    "PRO LEAGUE": "Senior1DIV.png",
    "SAUDI U21 LEAGUE": "U21logo.png",
    "U18 & U17 PREMIER LEAGUE": "U18logo.png"
}

# Debug mode - Cambiar a True para ver mensajes de debug
DEBUG_MODE = False

# Lista de posiciones
POSITIONS = [
    "Goalkeeper",
    "Left Back",
    "Left Center Back",
    "Right Center Back",
    "Right Back",
    "Defensive Midfielder (6)",
    "Central Midfielder (8)",
    "Attacking Midfielder (10)",
    "Right Winger",
    "Left Winger",
    "Striker",
    "Second Striker"
]

# Lista de países del mundo
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo, Dem. Rep. of the", "Congo, Rep. of the", "Costa Rica", "Croatia",
    "Cuba", "Cyprus", "Czechia", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador",
    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (Swaziland)", "Ethiopia", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran",
    "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
    "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "North Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives",
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand",
    "Nicaragua", "Niger", "Nigeria", "North Korea", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
    "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "São Tomé and Príncipe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
    "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain",
    "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania",
    "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",
    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu",
    "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Credenciales de usuarios
USERS = {
    'rafagil': 'rafagil123',
    'alvarolopez': 'alvarolopez',
    'juangambero': 'juan123'
}

# Mapeo username a nombre completo
SCOUT_NAMES = {
    'rafagil': 'Rafa Gil',
    'alvarolopez': 'Alvaro Lopez',
    'juangambero': 'Juan Gambero'
}

# Inicializar session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# PANTALLA DE LOGIN
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Logo
        try:
            logo = Image.open('alnassr.png')
            st.image(logo, width=150)
        except:
            st.write("⚽")
        
        st.markdown("# AL NASSR SCOUTING SYSTEM")
        st.markdown("---")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    
    st.stop()

# APLICACIÓN PRINCIPAL (después del login)
st.sidebar.image('alnassr.png', width=100)
st.sidebar.markdown(f"### Welcome, {SCOUT_NAMES[st.session_state.username]}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")

# Selector de categoría con session state para evitar reinicios
if 'current_category' not in st.session_state:
    st.session_state.current_category = "PRO LEAGUE"

category = st.sidebar.radio(
    "Select Category",
    ["PRO LEAGUE", "SAUDI U21 LEAGUE", "U18 & U17 PREMIER LEAGUE"],
    index=["PRO LEAGUE", "SAUDI U21 LEAGUE", "U18 & U17 PREMIER LEAGUE"].index(st.session_state.current_category),
    key="category_selector"
)

# Detectar cambio de categoría y limpiar estados relacionados
if category != st.session_state.current_category:
    st.session_state.current_category = category
    # Limpiar estados que pueden causar conflictos
    keys_to_clear = [k for k in st.session_state.keys() if k.startswith(('show_player_form', 'selected_team_for_player', 'players_list'))]
    for key in keys_to_clear:
        del st.session_state[key]

# Pestañas principales
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Create Match Report",
    "👁️ View Match Reports",
    "📊 Analytics - Reports",
    "💾 Database"
])

with tab1:
    # Mostrar icono de categoría
    icon_file = CATEGORY_ICONS.get(category)
    if icon_file and os.path.exists(icon_file):
        col_icon, col_title = st.columns([1, 9])
        with col_icon:
            try:
                icon = Image.open(icon_file)
                st.image(icon, width=80)
            except:
                pass
        with col_title:
            st.header(f"Create Match Report - {category}")
    else:
        st.header(f"Create Match Report - {category}")
    
    # Cargar base de datos según categoría
    db_file = CATEGORY_DB_FILES.get(category)
    if not db_file or not os.path.exists(db_file):
        st.error(f"Database file not found: {db_file}")
    else:
        # Para U18 & U17, cargar ambas sheets y combinarlas
        if category == "U18 & U17 PREMIER LEAGUE":
            df_u18 = pd.read_excel(db_file, sheet_name="dbu18league")
            df_u17 = pd.read_excel(db_file, sheet_name="dbu17league")
            df = pd.concat([df_u18, df_u17], ignore_index=True)
        else:
            df = pd.read_excel(db_file)
        
        # Inicializar session state para jugadores
        if 'players_list' not in st.session_state:
            st.session_state.players_list = []
        
        # Selector de Scout
        scout = st.selectbox("Scout", list(SCOUT_NAMES.values()))
        
        # Liga
        if 'League' in df.columns:
            leagues = df['League'].dropna().unique().tolist()
            selected_league = st.selectbox("Liga", ["Select..."] + sorted(leagues))
        else:
            selected_league = category
            st.info(f"Liga: {category}")
        
        # Filtrar equipos por liga seleccionada
        if selected_league and selected_league != "Select...":
            if 'League' in df.columns:
                df_league = df[df['League'] == selected_league]
                teams = df_league['Team'].dropna().unique().tolist()
            else:
                teams = df['Team'].dropna().unique().tolist() if 'Team' in df.columns else []
        else:
            teams = []
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Home Team
            if teams:
                home_team = st.selectbox("Home Team", ["Select..."] + sorted(teams))
            else:
                home_team = "Select..."
        
        with col2:
            # Away Team
            if teams:
                away_team = st.selectbox("Away Team", ["Select..."] + sorted(teams))
            else:
                away_team = "Select..."
        
        # Solo mostrar formulario si se han seleccionado ambos equipos
        if home_team and home_team != "Select..." and away_team and away_team != "Select...":
            st.markdown("---")
            
            # Dos columnas para los equipos
            col_home, col_away = st.columns(2)
            
            with col_home:
                st.subheader(f"🏠 {home_team}")
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    if st.button("➕ Add Player", key="add_home", type="primary", use_container_width=True):
                        st.session_state.show_player_form = True
                        st.session_state.selected_team_for_player = home_team
                        st.session_state.add_new_player = False
                with col_h2:
                    if st.button("👤 Add New Player", key="add_new_home", use_container_width=True):
                        st.session_state.show_player_form = True
                        st.session_state.selected_team_for_player = home_team
                        st.session_state.add_new_player = True
            
            with col_away:
                st.subheader(f"✈️ {away_team}")
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    if st.button("➕ Add Player", key="add_away", type="primary", use_container_width=True):
                        st.session_state.show_player_form = True
                        st.session_state.selected_team_for_player = away_team
                        st.session_state.add_new_player = False
                with col_a2:
                    if st.button("👤 Add New Player", key="add_new_away", use_container_width=True):
                        st.session_state.show_player_form = True
                        st.session_state.selected_team_for_player = away_team
                        st.session_state.add_new_player = True
            
            # Filtrar jugadores por equipos seleccionados (desde df_league si existe, sino desde df)
            if selected_league and selected_league != "Select..." and 'League' in df.columns:
                df_filtered = df_league[df_league['Team'].isin([home_team, away_team])]
            else:
                df_filtered = df[df['Team'].isin([home_team, away_team])]
            
            # Mostrar formulario de jugador
            if st.session_state.get('show_player_form', False):
                st.markdown("---")
                
                # Detectar si es nuevo jugador
                is_new_player = st.session_state.get('add_new_player', False)
                
                if is_new_player:
                    st.subheader("👤 Add New Player to Database & Report")
                    st.warning("⚠️ This will create a new player in the database and add a match report")
                else:
                    st.subheader("Add Player to Report")
                
                # Usar el equipo seleccionado desde el botón
                player_team = st.session_state.get('selected_team_for_player', home_team)
                st.info(f"Team: {player_team}")
                
                # Filtrar por equipo seleccionado
                df_team = df_filtered[df_filtered['Team'] == player_team]
                
                if DEBUG_MODE:
                    st.info(f"🔍 DEBUG: Team={player_team}, Players found={len(df_team)}, New Player={is_new_player}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Player Information")
                    
                    # PRO LEAGUE usa Name, U21/U18 usan Number
                    if category == "PRO LEAGUE":
                        if is_new_player:
                            # Campo de texto para nuevo jugador
                            selected_name = st.text_input("Player Name *", key="new_player_name", placeholder="Enter full name")
                            selected_number = None
                        else:
                            # Seleccionar por nombre
                            player_names = df_team['Name'].dropna().unique().tolist()
                            selected_name = st.selectbox("Player Name", ["Select..."] + sorted(player_names), key="player_select")
                            selected_number = None
                        
                        # Inicializar valores por defecto
                        birth_date_val = ""
                        height_val = ""
                        end_contract_val = ""
                        market_value_val = ""
                        position_val = ""
                        sec_position_val = ""
                        nationality_val = ""
                        agent_val = ""
                        
                        # Obtener datos del jugador si se seleccionó uno (solo si NO es nuevo jugador)
                        if not is_new_player and selected_name and selected_name != "Select...":
                            try:
                                player_data = df_team[df_team['Name'] == selected_name].iloc[0]
                                birth_date_val = str(player_data.get('Birth Date', '')) if pd.notna(player_data.get('Birth Date')) else ""
                                height_val = str(player_data.get('Heigh', '')) if pd.notna(player_data.get('Heigh')) else ""
                                end_contract_val = str(player_data.get('End Contract', '')) if pd.notna(player_data.get('End Contract')) else ""
                                market_value_val = str(player_data.get('Market Value', '')) if pd.notna(player_data.get('Market Value')) else ""
                                position_val = str(player_data.get('Position', '')) if pd.notna(player_data.get('Position')) else ""
                                sec_position_val = str(player_data.get('Sec. Position', '')) if pd.notna(player_data.get('Sec. Position')) else ""
                                nationality_val = str(player_data.get('Nationality', '')) if pd.notna(player_data.get('Nationality')) else ""
                                agent_val = str(player_data.get('Agent', '')) if pd.notna(player_data.get('Agent')) and player_data.get('Agent') != '' else ""
                                
                                if DEBUG_MODE:
                                    st.success(f"🔍 DEBUG PRO: Loaded {selected_name} - Position={position_val}, Birth={birth_date_val}")
                            except Exception as e:
                                st.error(f"❌ Error loading player data: {e}")
                                if DEBUG_MODE:
                                    st.error(f"🔍 DEBUG: Exception details: {str(e)}")
                        
                        # Mostrar campos (todos editables) con valores únicos en keys
                        birth_date = st.text_input("Birth Date", value=birth_date_val, key=f"birth_date_{selected_name}")
                        height = st.text_input("Height", value=height_val, key=f"height_{selected_name}")
                        end_contract = st.text_input("End Contract", value=end_contract_val, key=f"end_contract_{selected_name}")
                        market_value = st.text_input("Market Value", value=market_value_val, key=f"market_value_{selected_name}")
                        
                        # Position como desplegable editable
                        position_index = 0
                        if position_val and position_val in POSITIONS:
                            position_index = POSITIONS.index(position_val) + 1
                        position = st.selectbox("Position", ["Select..."] + POSITIONS, index=position_index, key=f"position_{selected_name}")
                        
                        # Sec. Position como desplegable editable
                        sec_position_index = 0
                        if sec_position_val and sec_position_val in POSITIONS:
                            sec_position_index = POSITIONS.index(sec_position_val) + 1
                        sec_position = st.selectbox("Sec. Position", ["Select..."] + POSITIONS, index=sec_position_index, key=f"sec_position_{selected_name}")
                        
                        # Nationality como desplegable
                        nationality_index = 0
                        if nationality_val and nationality_val in COUNTRIES:
                            nationality_index = COUNTRIES.index(nationality_val) + 1
                        nationality = st.selectbox("Nationality", ["Select..."] + COUNTRIES, index=nationality_index, key=f"nationality_{selected_name}")
                        
                        agent = st.text_input("Agent", value=agent_val, key=f"agent_{selected_name}")
                    
                    else:  # U21 o U18
                        if is_new_player:
                            # Campo numérico para nuevo jugador
                            selected_number = st.number_input("Number *", min_value=1, max_value=99, step=1, key="new_player_number")
                            selected_name = None
                        else:
                            # Seleccionar por número
                            numbers = df_team['Number'].dropna().unique().tolist()
                            numbers = [int(n) if isinstance(n, (int, float)) and not pd.isna(n) else n for n in numbers]
                            selected_number = st.selectbox("Number", ["Select..."] + sorted(numbers, key=lambda x: (isinstance(x, str), x)), key="number_select")
                            selected_name = None
                        
                        # Inicializar valores por defecto
                        name_val = ""
                        position_val = ""
                        sec_position_val = ""
                        birth_date_val = ""
                        nationality_val = ""
                        agent_val = ""
                        
                        # Obtener datos del jugador si se seleccionó uno (solo si NO es nuevo jugador)
                        if not is_new_player and selected_number and selected_number != "Select...":
                            try:
                                if DEBUG_MODE:
                                    st.info(f"🔍 DEBUG: Columns in df_team: {df_team.columns.tolist()}")
                                    st.info(f"🔍 DEBUG: Looking for Number={selected_number}")
                                
                                player_data = df_team[df_team['Number'] == selected_number].iloc[0]
                                
                                if DEBUG_MODE:
                                    st.info(f"🔍 DEBUG: Player data found: {player_data.to_dict()}")
                                
                                name_val = str(player_data.get('Name', '')) if pd.notna(player_data.get('Name')) else ""
                                position_val = str(player_data.get('Position', '')) if pd.notna(player_data.get('Position')) else ""
                                sec_position_val = str(player_data.get('Sec. Position', '')) if pd.notna(player_data.get('Sec. Position')) else ""
                                birth_date_val = str(player_data.get('Birth Date', '')) if pd.notna(player_data.get('Birth Date')) else ""
                                nationality_val = str(player_data.get('Nationality', '')) if pd.notna(player_data.get('Nationality')) else ""
                                agent_val = str(player_data.get('Agent', '')) if pd.notna(player_data.get('Agent')) and player_data.get('Agent') != '' else ""
                                
                                if DEBUG_MODE:
                                    st.success(f"🔍 DEBUG U21/U18: Number={selected_number}, Name={name_val}, Position={position_val}, Nationality={nationality_val}, Birth={birth_date_val}")
                            except Exception as e:
                                st.error(f"❌ Error loading player data: {e}")
                                if DEBUG_MODE:
                                    st.error(f"🔍 DEBUG: Exception details: {str(e)}")
                        
                        # Mostrar campos (todos editables) con keys únicos
                        name = st.text_input("Name", value=name_val, key=f"name_{selected_number}")
                        
                        # Position como desplegable editable
                        position_index = 0
                        if position_val and position_val in POSITIONS:
                            position_index = POSITIONS.index(position_val) + 1
                        position = st.selectbox("Position", ["Select..."] + POSITIONS, index=position_index, key=f"position_{selected_number}")
                        
                        # Sec. Position como desplegable editable
                        sec_position_index = 0
                        if sec_position_val and sec_position_val in POSITIONS:
                            sec_position_index = POSITIONS.index(sec_position_val) + 1
                        sec_position = st.selectbox("Sec. Position", ["Select..."] + POSITIONS, index=sec_position_index, key=f"sec_position_{selected_number}")
                        
                        birth_date = st.text_input("Birth Date", value=birth_date_val, key=f"birth_date_{selected_number}")
                        
                        # Nationality como desplegable
                        nationality_index = 0
                        if nationality_val and nationality_val in COUNTRIES:
                            nationality_index = COUNTRIES.index(nationality_val) + 1
                        nationality = st.selectbox("Nationality", ["Select..."] + COUNTRIES, index=nationality_index, key=f"nationality_{selected_number}")
                        
                        agent = st.text_input("Agent", value=agent_val, key=f"agent_{selected_number}")
                
                with col2:
                    st.markdown("### Evaluation")
                    
                    # Performance
                    performance = st.selectbox("Performance", [
                        "Select...",
                        "LEVEL 4 - One of the best in the match",
                        "LEVEL 3 - Consistent and standout performance",
                        "LEVEL 2 - Performance above average",
                        "LEVEL 1 - Contributes but doesn't stand out especially"
                    ])
                    
                    # Watch
                    watch = st.selectbox("Watch", [
                        "Select...",
                        "LIVE - STADIUM",
                        "TV - SAFF+"
                    ])
                    
                    # Profile (solo para PRO LEAGUE)
                    if category == "PRO LEAGUE":
                        profile = st.selectbox("Profile", [
                            "Select...",
                            "6 – TOP MUNDIAL EN SU POSICIÓN",
                            "5 – UEFA Champions League Player",
                            "4 – First Pro Level",
                            "3 – Stand Out SPL - TOP4",
                            "2 – Starter SPL - TOP4",
                            "1 – Backup SPL - TOP4"
                        ])
                    else:
                        profile = None
                    
                    # Decision
                    decision = st.selectbox("Decision", [
                        "Select...",
                        "A - FICHAR",
                        "B+ - INTERESANTE",
                        "B - SEGUIR",
                        "P - PROSPECT",
                        "C - DESCARTAR"
                    ])
                
                # Description (campo de texto largo)
                st.markdown("### Description")
                description = st.text_area("Notes / Description", height=150, placeholder="Write your observations about the player...")
                
                # Botones
                col1, col2 = st.columns(2)
                with col1:
                    submit_btn = st.button("Add to Report", use_container_width=True, type="primary", key="submit_player")
                with col2:
                    cancel_btn = st.button("Cancel", use_container_width=True, key="cancel_player")
                
                if cancel_btn:
                    st.session_state.show_player_form = False
                    st.rerun()
                
                if submit_btn:
                        # Validar que se hayan seleccionado todos los campos
                        if category == "PRO LEAGUE":
                            if is_new_player:
                                # Validación para nuevo jugador
                                if not selected_name or position == "Select..." or nationality == "Select..." or performance == "Select..." or watch == "Select..." or profile == "Select..." or decision == "Select...":
                                    st.error("Please fill all required fields (Name, Position, Nationality, Performance, Watch, Profile, Decision)")
                                else:
                                    # Guardar nuevo jugador en la base de datos
                                    try:
                                        new_player_data = {
                                            'Team': player_team,
                                            'Name': selected_name,
                                            'Birth Date': birth_date,
                                            'Heigh': height,
                                            'End Contract': end_contract,
                                            'Market Value': market_value,
                                            'Position': position,
                                            'Sec. Position': sec_position if sec_position != "Select..." else '',
                                            'Nationality': nationality if nationality != "Select..." else '',
                                            'Agent': agent if agent else '',
                                            'League': selected_league if selected_league != "Select..." else category
                                        }
                                        
                                        # Cargar base de datos y añadir jugador
                                        df_db = pd.read_excel(db_file)
                                        df_db = pd.concat([df_db, pd.DataFrame([new_player_data])], ignore_index=True)
                                        df_db.to_excel(db_file, index=False, engine='openpyxl')
                                        
                                        st.success(f"✅ {selected_name} added to database!")
                                        
                                        # Ahora agregar al reporte
                                        player_info = {
                                            'Team': player_team,
                                            'Name': selected_name,
                                            'Birth Date': birth_date,
                                            'Height': height,
                                            'End Contract': end_contract,
                                            'Market Value': market_value,
                                            'Position': position,
                                            'Sec. Position': sec_position if sec_position != "Select..." else '',
                                            'Nationality': nationality,
                                            'Agent': agent if agent else 'N/A',
                                            'Performance': performance,
                                            'Watch': watch,
                                            'Profile': profile,
                                            'Decision': decision,
                                            'Description': description
                                        }
                                        st.session_state.players_list.append(player_info)
                                        st.session_state.show_player_form = False
                                        st.success(f"✅ {selected_name} added to report!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error saving to database: {str(e)}")
                            else:
                                # Jugador existente
                                if not selected_name or selected_name == "Select..." or performance == "Select..." or watch == "Select..." or profile == "Select..." or decision == "Select...":
                                    st.error("Please fill all required fields")
                                else:
                                    # Agregar jugador a la lista (usando valores editados)
                                    player_info = {
                                        'Team': player_team,
                                        'Name': selected_name,
                                        'Birth Date': birth_date,
                                        'Height': height,
                                        'End Contract': end_contract,
                                        'Market Value': market_value,
                                        'Position': position,
                                        'Sec. Position': sec_position if sec_position != "Select..." else '',
                                        'Nationality': nationality,
                                        'Agent': agent if agent else 'N/A',
                                        'Performance': performance,
                                        'Watch': watch,
                                        'Profile': profile,
                                        'Decision': decision,
                                        'Description': description
                                    }
                                    st.session_state.players_list.append(player_info)
                                    st.session_state.show_player_form = False
                                    st.success(f"✅ {selected_name} added to report!")
                                    st.rerun()
                        else:  # U21 o U18
                            if is_new_player:
                                # Validación para nuevo jugador
                                if not selected_number or not name or position == "Select..." or nationality == "Select..." or performance == "Select..." or watch == "Select..." or decision == "Select...":
                                    st.error("Please fill all required fields (Number, Name, Position, Nationality, Performance, Watch, Decision)")
                                else:
                                    # Guardar nuevo jugador en la base de datos
                                    try:
                                        new_player_data = {
                                            'Team': player_team,
                                            'Number': int(selected_number),
                                            'Name': name,
                                            'Position': position,
                                            'Sec. Position': sec_position if sec_position != "Select..." else '',
                                            'Birth Date': birth_date,
                                            'Nationality': nationality if nationality != "Select..." else '',
                                            'Agent': agent if agent else '',
                                            'League': selected_league if selected_league != "Select..." else category
                                        }
                                        
                                        # Cargar base de datos y añadir jugador
                                        if category == "U18 & U17 PREMIER LEAGUE":
                                            # Determinar sheet según la liga
                                            sheet_name = "dbu18league" if "U18" in str(selected_league) else "dbu17league"
                                            df_db = pd.read_excel(db_file, sheet_name=sheet_name)
                                            df_db = pd.concat([df_db, pd.DataFrame([new_player_data])], ignore_index=True)
                                            with pd.ExcelWriter(db_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                                                df_db.to_excel(writer, sheet_name=sheet_name, index=False)
                                        else:
                                            df_db = pd.read_excel(db_file)
                                            df_db = pd.concat([df_db, pd.DataFrame([new_player_data])], ignore_index=True)
                                            df_db.to_excel(db_file, index=False, engine='openpyxl')
                                        
                                        st.success(f"✅ {name} added to database!")
                                        
                                        # Ahora agregar al reporte
                                        player_info = {
                                            'Team': player_team,
                                            'Number': selected_number,
                                            'Name': name,
                                            'Position': position,
                                            'Sec. Position': sec_position if sec_position != "Select..." else '',
                                            'Birth Date': birth_date,
                                            'Nationality': nationality,
                                            'Agent': agent if agent else 'N/A',
                                            'Performance': performance,
                                            'Watch': watch,
                                            'Decision': decision,
                                            'Description': description
                                        }
                                        st.session_state.players_list.append(player_info)
                                        st.session_state.show_player_form = False
                                        st.success(f"✅ {name} added to report!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error saving to database: {str(e)}")
                            else:
                                # Jugador existente
                                if not selected_number or selected_number == "Select..." or performance == "Select..." or watch == "Select..." or decision == "Select...":
                                    st.error("Please fill all required fields")
                                else:
                                    # Agregar jugador a la lista (usando valores editados)
                                    player_info = {
                                        'Team': player_team,
                                        'Number': selected_number,
                                        'Name': name,
                                        'Position': position,
                                        'Sec. Position': sec_position if sec_position != "Select..." else '',
                                        'Birth Date': birth_date,
                                        'Nationality': nationality,
                                        'Agent': agent if agent else 'N/A',
                                        'Performance': performance,
                                        'Watch': watch,
                                        'Decision': decision,
                                        'Description': description
                                    }
                                    st.session_state.players_list.append(player_info)
                                    st.session_state.show_player_form = False
                                    st.success(f"✅ {name} added to report!")
                                    st.rerun()
            
            # Mostrar lista de jugadores añadidos
            if st.session_state.players_list:
                st.markdown("---")
                st.subheader(f"Players in Report ({len(st.session_state.players_list)})")
                
                for idx, player in enumerate(st.session_state.players_list):
                    with st.expander(f"👤 {player.get('Name', 'N/A')} - {player.get('Team', '')} - {player.get('Position', '')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            for key, value in player.items():
                                if key not in ['Performance', 'Watch', 'Profile', 'Decision']:
                                    st.write(f"**{key}:** {value}")
                        with col2:
                            st.write(f"**Performance:** {player.get('Performance', 'N/A')}")
                            st.write(f"**Watch:** {player.get('Watch', 'N/A')}")
                            if 'Profile' in player and player['Profile']:
                                st.write(f"**Profile:** {player.get('Profile', 'N/A')}")
                            st.write(f"**Decision:** {player.get('Decision', 'N/A')}")
                        
                        if st.button(f"🗑️ Remove", key=f"remove_{idx}"):
                            st.session_state.players_list.pop(idx)
                            st.rerun()
                
                # Botón para guardar informe
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("💾 Save Match Report", type="primary", use_container_width=True):
                        try:
                            st.info(f"🔄 Saving report for user: {scout}")
                            st.info(f"📊 Players to save: {len(st.session_state.players_list)}")
                            
                            # Crear DataFrame con los jugadores
                            report_df = pd.DataFrame(st.session_state.players_list)
                            
                            # Añadir información del partido
                            report_df.insert(0, 'Scout', scout)
                            report_df.insert(1, 'Date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            report_df.insert(2, 'League', selected_league if selected_league != "Select..." else category)
                            report_df.insert(3, 'Home Team', home_team)
                            report_df.insert(4, 'Away Team', away_team)
                            
                            # Guardar en Excel
                            report_file = CATEGORY_REPORT_FILES.get(category)
                            st.info(f"📁 Target file: {report_file}")
                            
                            # Verificar si el archivo existe y es accesible
                            if os.path.exists(report_file):
                                st.info(f"✅ File exists, loading existing data...")
                                # Cargar existente y añadir
                                try:
                                    existing_df = pd.read_excel(report_file)
                                    st.info(f"📊 Existing reports: {len(existing_df)}")
                                    final_df = pd.concat([existing_df, report_df], ignore_index=True)
                                    st.info(f"📊 Total reports after merge: {len(final_df)}")
                                except Exception as e:
                                    st.warning(f"⚠️ Could not load existing file: {e}. Creating new file.")
                                    final_df = report_df
                            else:
                                st.info(f"📄 File does not exist, creating new file...")
                                final_df = report_df
                            
                            # Guardar con openpyxl
                            st.info(f"💾 Saving to Excel...")
                            final_df.to_excel(report_file, index=False, engine='openpyxl')
                            
                            # Verificar que se guardó correctamente
                            if os.path.exists(report_file):
                                verify_df = pd.read_excel(report_file)
                                st.success(f"✅ Match report saved successfully!")
                                st.success(f"✅ Verified: {len(verify_df)} total reports in file")
                                st.info(f"📁 Saved to: {report_file}")
                                st.balloons()
                                
                                # Limpiar lista
                                st.session_state.players_list = []
                                st.session_state.show_player_form = False
                                st.rerun()
                            else:
                                st.error(f"❌ File was not created. Check permissions.")
                        except PermissionError as e:
                            st.error(f"❌ Permission Error: {str(e)}")
                            st.error(f"🔒 The file may be open in another program (Excel). Please close it and try again.")
                        except Exception as e:
                            st.error(f"❌ Error saving report: {str(e)}")
                            st.error(f"📋 Error type: {type(e).__name__}")
                            import traceback
                            st.error(f"🔍 Full error: {traceback.format_exc()}")
                
                with col3:
                    if st.button("🗑️ Clear All", use_container_width=True):
                        st.session_state.players_list = []
                        st.session_state.show_player_form = False
                        st.rerun()

with tab2:
    st.header(f"📊 Match Reports - {category}")
    
    # Cargar archivo de reportes según categoría
    report_file = CATEGORY_REPORT_FILES.get(category)
    
    if not os.path.exists(report_file):
        st.info(f"No match reports found for {category}. Create your first report in the 'Create Match Report' tab!")
    else:
        # Cargar datos
        df_reports = pd.read_excel(report_file)
        
        if df_reports.empty:
            st.info("No reports available yet.")
        else:
            # CSS minimalista y moderno
            st.markdown("""
                <style>
                /* Contenedor principal */
                .report-container {
                    background: #f5f5f5;
                    padding: 20px;
                    border-radius: 12px;
                    margin: 10px 0;
                }
                
                /* Tarjeta de reporte */
                .report-card {
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    margin-bottom: 16px;
                    overflow: hidden;
                    transition: all 0.3s ease;
                }
                
                .report-card:hover {
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                }
                
                /* Header del reporte */
                .report-header {
                    padding: 20px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    flex-wrap: wrap;
                    transition: background 0.2s;
                }
                
                .report-header:hover {
                    background: #fafafa;
                }
                
                /* Chevron */
                .chevron {
                    font-size: 20px;
                    transition: transform 0.4s;
                    color: #666;
                }
                
                .chevron.expanded {
                    transform: rotate(180deg);
                }
                
                /* Dorsal */
                .player-number {
                    font-size: 24px;
                    font-weight: bold;
                    color: #1a2332;
                    min-width: 50px;
                }
                
                /* Nombre del jugador */
                .player-name {
                    font-size: 18px;
                    font-weight: 600;
                    color: #1a2332;
                    flex: 1;
                    min-width: 150px;
                }
                
                /* Badges */
                .badge {
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: 600;
                    display: inline-block;
                }
                
                .badge-position {
                    background: #ff4444;
                    color: white;
                }
                
                .badge-birth {
                    background: #f0f0f0;
                    color: #666;
                }
                
                .badge-decision-green {
                    background: #2ecc71;
                    color: white;
                }
                
                .badge-decision-blue {
                    background: #007bff;
                    color: white;
                }
                
                .badge-decision-yellow {
                    background: #ffc107;
                    color: #1a2332;
                }
                
                .badge-decision-red {
                    background: #dc3545;
                    color: white;
                }
                
                /* Match info */
                .match-info {
                    color: #666;
                    font-size: 14px;
                    margin: 0 8px;
                }
                
                /* Botón Follow Closer */
                .btn-follow {
                    background: #2ecc71;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                    border: none;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s;
                    margin-left: auto;
                }
                
                .btn-follow:hover {
                    background: #27ae60;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(46,204,113,0.3);
                }
                
                /* Contenido colapsable */
                .report-content {
                    padding: 0 20px 20px 20px;
                    display: none;
                    animation: slideDown 0.4s ease;
                }
                
                .report-content.show {
                    display: block;
                }
                
                @keyframes slideDown {
                    from {
                        opacity: 0;
                        transform: translateY(-10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                /* Grid de 4 columnas */
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 1px;
                    background: #e0e0e0;
                    border-radius: 8px;
                    overflow: hidden;
                    margin-bottom: 20px;
                }
                
                .stat-item {
                    background: white;
                    padding: 20px;
                    text-align: center;
                }
                
                .stat-value {
                    font-size: 32px;
                    font-weight: bold;
                    color: #1976d2;
                    margin-bottom: 8px;
                }
                
                .stat-label {
                    font-size: 12px;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                
                .stat-desc {
                    font-size: 14px;
                    color: #333;
                    margin-top: 8px;
                }
                
                /* Informe del partido */
                .match-report {
                    background: #fafafa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #1976d2;
                }
                
                .match-report-title {
                    font-size: 16px;
                    font-weight: 600;
                    color: #1a2332;
                    margin-bottom: 12px;
                }
                
                .match-report-text {
                    font-size: 14px;
                    line-height: 1.6;
                    color: #333;
                }
                
                /* Responsive */
                @media (max-width: 768px) {
                    .stats-grid {
                        grid-template-columns: 1fr;
                    }
                }
                </style>
            """, unsafe_allow_html=True)
            
            st.write(f"**Total Reports:** {len(df_reports)}")
            
            # Filtros básicos
            st.markdown("### 🔍 Filters")
            filter_cols = st.columns(3)
            
            with filter_cols[0]:
                if 'League' in df_reports.columns:
                    leagues = ['All'] + sorted(df_reports['League'].dropna().unique().tolist())
                    filter_league = st.selectbox("League", leagues, key="filter_league_view")
                else:
                    filter_league = 'All'
            
            with filter_cols[1]:
                if 'Decision' in df_reports.columns:
                    decisions = ['All'] + sorted(df_reports['Decision'].dropna().unique().tolist())
                    filter_decision = st.selectbox("Decision", decisions, key="filter_decision_view")
                else:
                    filter_decision = 'All'
            
            with filter_cols[2]:
                if 'Scout' in df_reports.columns:
                    scouts = ['All'] + sorted(df_reports['Scout'].dropna().unique().tolist())
                    filter_scout = st.selectbox("Scout", scouts, key="filter_scout_view")
                else:
                    filter_scout = 'All'
            
            # Aplicar filtros
            df_filtered = df_reports.copy()
            
            if filter_league != 'All':
                df_filtered = df_filtered[df_filtered['League'] == filter_league]
            
            if filter_decision != 'All':
                df_filtered = df_filtered[df_filtered['Decision'] == filter_decision]
            
            if filter_scout != 'All':
                df_filtered = df_filtered[df_filtered['Scout'] == filter_scout]
            
            st.markdown("---")
            st.write(f"**Showing {len(df_filtered)} of {len(df_reports)} reports**")
            
            # Agrupar por Scout
            scouts_list = df_filtered['Scout'].unique() if 'Scout' in df_filtered.columns else ['Unknown']
            
            for scout in sorted(scouts_list):
                # Header del Scout
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%); 
                            color: #d4af37; 
                            padding: 20px; 
                            border-radius: 10px; 
                            margin: 20px 0 10px 0; 
                            font-size: 24px; 
                            font-weight: bold; 
                            border-left: 5px solid #d4af37; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    👤 {scout}
                </div>
                """, unsafe_allow_html=True)
                
                # Filtrar reportes de este scout
                scout_reports = df_filtered[df_filtered['Scout'] == scout] if 'Scout' in df_filtered.columns else df_filtered
                
                st.write(f"*{len(scout_reports)} report(s)*")
                
                # Mostrar reportes de este scout
                for idx, report in scout_reports.iterrows():
                    # Extraer datos
                    number = report.get('Number', '')
                    name = report.get('Name', 'Unknown Player')
                    position = report.get('Position', 'N/A')
                    sec_position = report.get('Sec. Position', '')
                    birth_date = str(report.get('Birth Date', ''))[:4] if pd.notna(report.get('Birth Date')) else 'N/A'
                    home_team = report.get('Home Team', '')
                    away_team = report.get('Away Team', '')
                    date = str(report.get('Date', ''))[:10] if pd.notna(report.get('Date')) else 'N/A'
                    performance = report.get('Performance', 'N/A')
                    league = report.get('League', 'N/A')
                    watch = report.get('Watch', 'N/A')
                    decision = report.get('Decision', 'N/A')
                    description = report.get('Description', '')
                    
                    # Construir display de posición
                    position_display = position
                    if sec_position and str(sec_position).strip() and str(sec_position) != 'nan':
                        position_display = f"{position} ({sec_position})"
                    
                    # Extraer nivel de performance
                    perf_level = '?'
                    perf_desc = performance
                    if 'LEVEL' in str(performance):
                        parts = str(performance).split(' - ')
                        if len(parts) >= 2:
                            perf_level = parts[0].replace('LEVEL ', '')
                            perf_desc = parts[1]
                    
                    # Extraer texto de decision para el botón y determinar color
                    decision_text = str(decision)
                    decision_display = decision_text
                    
                    # Determinar color según decisión
                    decision_color = '#2ecc71'  # Verde por defecto (A)
                    if 'B+' in decision_text or 'INTERESANTE' in decision_text.upper():
                        decision_color = '#007bff'  # Azul
                    elif 'B' in decision_text and 'B+' not in decision_text:
                        decision_color = '#ffc107'  # Amarillo
                    elif 'C' in decision_text or 'DESCARTAR' in decision_text.upper():
                        decision_color = '#dc3545'  # Rojo
                    
                    # Crear label para el expander
                    expander_label = f"#{number} {name} | {position_display} | 🎂 {birth_date} | ⚽ {home_team} vs {away_team} | 📅 {date} | {decision_display}"
                    
                    with st.expander(expander_label, expanded=False):
                        # Grid de 4 columnas usando Streamlit nativo
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 20px; background: white; border-radius: 8px;">
                                <div style="font-size: 48px; font-weight: bold; color: #1976d2; margin-bottom: 8px;">{perf_level}</div>
                                <div style="font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">Performance in the match</div>
                                <div style="font-size: 14px; color: #333; margin-top: 8px;">{perf_desc}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 20px; background: white; border-radius: 8px;">
                                <div style="font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">🏆 League</div>
                                <div style="font-size: 14px; color: #333; margin-top: 20px;">{league}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 20px; background: white; border-radius: 8px;">
                                <div style="font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">📺 Watch</div>
                                <div style="font-size: 14px; color: #333; margin-top: 20px;">{watch}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col4:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 20px; background: white; border-radius: 8px;">
                                <div style="font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">Decision</div>
                                <div style="margin-top: 20px;">
                                    <span style="background: {decision_color}; color: {'white' if decision_color != '#ffc107' else '#1a2332'}; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 600;">{decision_display}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Informe del partido
                        st.markdown("---")
                        st.markdown(f"""
                        <div style="background: #fafafa; padding: 20px; border-radius: 8px; border-left: 4px solid #1976d2; margin-top: 20px;">
                            <div style="font-size: 16px; font-weight: 600; color: #1a2332; margin-bottom: 12px;">📝 Informe del partido</div>
                            <div style="font-size: 14px; line-height: 1.6; color: #333;">{description if description else 'No description available.'}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Botones de acción
                        st.markdown("---")
                        col_edit, col_delete = st.columns(2)
                        
                        with col_edit:
                            if st.button("✏️ Edit Report", key=f"edit_report_{idx}", use_container_width=True):
                                st.session_state[f'editing_report_{idx}'] = True
                                st.rerun()
                        
                        with col_delete:
                            if st.button("🗑️ Delete Report", key=f"delete_report_{idx}", use_container_width=True, type="secondary"):
                                # Eliminar el reporte
                                try:
                                    df_reports_updated = df_filtered.drop(idx)
                                    # Guardar
                                    df_reports_updated.to_excel(report_file, index=False, engine='openpyxl')
                                    st.success("✅ Report deleted successfully!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error deleting report: {str(e)}")
                        
                        # Modo edición
                        if st.session_state.get(f'editing_report_{idx}', False):
                            st.markdown("---")
                            st.markdown("### ✏️ Edit Report")
                            
                            # Obtener datos actuales
                            current_position = report.get('Position', '')
                            current_sec_position = report.get('Sec. Position', '')
                            current_date = report.get('Date', '')
                            current_home = report.get('Home Team', '')
                            current_away = report.get('Away Team', '')
                            
                            # Obtener equipos disponibles
                            all_teams = []
                            if 'Home Team' in df_reports.columns:
                                all_teams.extend(df_reports['Home Team'].dropna().unique().tolist())
                            if 'Away Team' in df_reports.columns:
                                all_teams.extend(df_reports['Away Team'].dropna().unique().tolist())
                            all_teams = sorted(list(set(all_teams)))
                            
                            # Position y Sec. Position
                            col_pos1, col_pos2 = st.columns(2)
                            with col_pos1:
                                position_options = [
                                    "Goalkeeper", "Left Back", "Left Center Back", "Right Center Back", "Right Back",
                                    "Defensive Midfielder (6)", "Central Midfielder (8)", "Attacking Midfielder (10)",
                                    "Right Winger", "Left Winger", "Striker", "Second Striker"
                                ]
                                current_pos_idx = position_options.index(current_position) if current_position in position_options else 0
                                edit_position = st.selectbox("Position", position_options, index=current_pos_idx, key=f"edit_pos_{idx}")
                            
                            with col_pos2:
                                sec_position_options = ["None"] + position_options
                                current_sec_idx = sec_position_options.index(current_sec_position) if current_sec_position in sec_position_options else 0
                                edit_sec_position = st.selectbox("Sec. Position", sec_position_options, index=current_sec_idx, key=f"edit_sec_pos_{idx}")
                                if edit_sec_position == "None":
                                    edit_sec_position = ""
                            
                            # Fecha
                            import datetime
                            if pd.notna(current_date):
                                try:
                                    date_value = pd.to_datetime(current_date).date()
                                except:
                                    date_value = datetime.date.today()
                            else:
                                date_value = datetime.date.today()
                            
                            edit_date = st.date_input("Date", value=date_value, key=f"edit_date_{idx}")
                            
                            # Partido (Home vs Away)
                            col_home, col_away = st.columns(2)
                            with col_home:
                                if current_home in all_teams:
                                    home_idx = all_teams.index(current_home)
                                else:
                                    home_idx = 0
                                edit_home = st.selectbox("Home Team", all_teams, index=home_idx, key=f"edit_home_{idx}")
                            
                            with col_away:
                                if current_away in all_teams:
                                    away_idx = all_teams.index(current_away)
                                else:
                                    away_idx = 0
                                edit_away = st.selectbox("Away Team", all_teams, index=away_idx, key=f"edit_away_{idx}")
                            
                            # Performance
                            perf_options = [
                                "LEVEL 4 - One of the best in the match",
                                "LEVEL 3 - Consistent and standout performance",
                                "LEVEL 2 - Performance above average",
                                "LEVEL 1 - Contributes but doesn't stand out especially"
                            ]
                            current_perf_idx = 0
                            for i, opt in enumerate(perf_options):
                                if performance in opt:
                                    current_perf_idx = i
                                    break
                            
                            edit_performance = st.selectbox("Performance", perf_options, index=current_perf_idx, key=f"edit_perf_{idx}")
                            
                            # Watch
                            watch_options = ["LIVE - STADIUM", "TV - SAFF+"]
                            current_watch_idx = 0 if "LIVE" in str(watch) else 1
                            edit_watch = st.selectbox("Watch", watch_options, index=current_watch_idx, key=f"edit_watch_{idx}")
                            
                            # Decision
                            decision_options = [
                                "A+ - FICHAR YA",
                                "A - FICHAR",
                                "B+ - INTERESANTE",
                                "B - SEGUIR",
                                "C - DESCARTAR"
                            ]
                            current_decision_idx = 0
                            for i, opt in enumerate(decision_options):
                                if decision in opt:
                                    current_decision_idx = i
                                    break
                            
                            edit_decision = st.selectbox("Decision", decision_options, index=current_decision_idx, key=f"edit_decision_{idx}")
                            
                            # Description
                            edit_description = st.text_area("Description", value=description, height=150, key=f"edit_desc_{idx}")
                            
                            # Botones
                            col_cancel, col_save = st.columns(2)
                            
                            with col_cancel:
                                if st.button("❌ Cancel", key=f"cancel_edit_{idx}", use_container_width=True):
                                    del st.session_state[f'editing_report_{idx}']
                                    st.rerun()
                            
                            with col_save:
                                if st.button("💾 Save Changes", key=f"save_edit_{idx}", type="primary", use_container_width=True):
                                    try:
                                        # Actualizar el reporte
                                        df_reports.at[idx, 'Position'] = edit_position
                                        df_reports.at[idx, 'Sec. Position'] = edit_sec_position
                                        df_reports.at[idx, 'Date'] = edit_date
                                        df_reports.at[idx, 'Home Team'] = edit_home
                                        df_reports.at[idx, 'Away Team'] = edit_away
                                        df_reports.at[idx, 'Performance'] = edit_performance
                                        df_reports.at[idx, 'Watch'] = edit_watch
                                        df_reports.at[idx, 'Decision'] = edit_decision
                                        df_reports.at[idx, 'Description'] = edit_description
                                        
                                        # Guardar
                                        df_reports.to_excel(report_file, index=False, engine='openpyxl')
                                        st.success("✅ Report updated successfully!")
                                        del st.session_state[f'editing_report_{idx}']
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error updating report: {str(e)}")
with tab3:
    st.header(f"📊 Analytics - Reports - {category}")
    
    # Cargar archivo de reportes según categoría
    report_file = CATEGORY_REPORT_FILES.get(category)
    
    if not os.path.exists(report_file):
        st.info(f"No match reports found for {category}. Create reports first in the 'Create Match Report' tab!")
    else:
        # Cargar datos
        df_reports = pd.read_excel(report_file)
        
        if df_reports.empty:
            st.info("No reports available yet.")
        else:
            # Agrupar por jugador (Name o Number + Name)
            if 'Name' in df_reports.columns:
                # Obtener lista única de jugadores
                players_list = df_reports['Name'].dropna().unique().tolist()
                
                if not players_list:
                    st.info("No players found in reports.")
                else:
                    # Botón de descarga de Analytics
                    analytics_file = CATEGORY_ANALYTICS_FILES.get(category)
                    if os.path.exists(analytics_file):
                        df_analytics_download = pd.read_excel(analytics_file)
                        if not df_analytics_download.empty:
                            st.markdown("### 📥 Download Analytics Data")
                            col_csv, col_json, col_excel = st.columns(3)
                            
                            with col_csv:
                                csv_data = df_analytics_download.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="📄 Download CSV",
                                    data=csv_data,
                                    file_name=f"analytics_{category.lower().replace(' ', '_')}.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            
                            with col_json:
                                json_data = df_analytics_download.to_json(orient='records', indent=2).encode('utf-8')
                                st.download_button(
                                    label="📋 Download JSON",
                                    data=json_data,
                                    file_name=f"analytics_{category.lower().replace(' ', '_')}.json",
                                    mime="application/json",
                                    use_container_width=True
                                )
                            
                            with col_excel:
                                from io import BytesIO
                                buffer = BytesIO()
                                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                    df_analytics_download.to_excel(writer, index=False, sheet_name='Analytics')
                                buffer.seek(0)
                                st.download_button(
                                    label="📊 Download Excel",
                                    data=buffer,
                                    file_name=f"analytics_{category.lower().replace(' ', '_')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                            
                            st.markdown("---")
                    
                    # Selector de jugador
                    st.markdown("### 🔍 Select Player")
                    selected_player = st.selectbox("Player", ["Select..."] + sorted(players_list), key="analytics_player_select")
                    
                    if selected_player and selected_player != "Select...":
                        # Cargar perfil guardado si existe
                        analytics_file = CATEGORY_ANALYTICS_FILES.get(category)
                        saved_profile = None
                        
                        if os.path.exists(analytics_file):
                            df_analytics = pd.read_excel(analytics_file)
                            saved_profiles = df_analytics[df_analytics['Name'] == selected_player]
                            if not saved_profiles.empty:
                                saved_profile = saved_profiles.iloc[0]
                        
                        # Filtrar todos los reportes de este jugador
                        player_reports = df_reports[df_reports['Name'] == selected_player]
                        
                        # Obtener datos del jugador (del primer reporte)
                        first_report = player_reports.iloc[0]
                        player_name = first_report.get('Name', 'Unknown')
                        player_team = first_report.get('Team', 'N/A')
                        player_position = first_report.get('Position', 'N/A')
                        player_sec_position = first_report.get('Sec. Position', '')
                        player_birth = str(first_report.get('Birth Date', ''))[:4] if pd.notna(first_report.get('Birth Date')) else 'N/A'
                        
                        # Nationality con manejo robusto
                        nationality_value = first_report.get('Nationality', 'N/A')
                        if pd.isna(nationality_value) or str(nationality_value).strip() == '' or str(nationality_value) == 'nan':
                            player_nationality = 'N/A'
                        else:
                            player_nationality = str(nationality_value)
                        
                        player_number = first_report.get('Number', '')
                        
                        # HEADER CON FOTO
                        st.markdown("---")
                        col_photo, col_info = st.columns([1, 3])
                        
                        with col_photo:
                            # Opción para subir foto
                            uploaded_photo = st.file_uploader("Upload Player Photo", type=['jpg', 'jpeg', 'png'], key=f"photo_{selected_player}")
                            if uploaded_photo:
                                st.image(uploaded_photo, width=150)
                            else:
                                st.markdown(f"""
                                <div style="width: 150px; height: 150px; border-radius: 50%; background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%); 
                                            display: flex; align-items: center; justify-content: center; border: 4px solid #d4af37;">
                                    <span style="font-size: 48px; color: #d4af37; font-weight: bold;">{player_name[0] if player_name else '?'}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with col_info:
                            st.markdown(f"## {player_name}")
                            st.markdown(f"**Team:** {player_team}")
                            if player_number:
                                st.markdown(f"**Number:** #{player_number}")
                            position_display = f"{player_position}" + (f" / {player_sec_position}" if player_sec_position else "")
                            st.markdown(f"**Position:** {position_display}")
                            st.markdown(f"**🎂 Birth Year:** {player_birth}")
                            st.markdown(f"**🌍 Nationality:** {player_nationality}")
                        
                        st.markdown("---")
                        
                        # RATINGS (3 columnas)
                        st.markdown("### 📊 Aggregated Statistics")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            # Calcular promedio de Performance
                            performance_levels = []
                            for perf in player_reports['Performance'].dropna():
                                if 'LEVEL' in str(perf):
                                    level = str(perf).split(' - ')[0].replace('LEVEL ', '')
                                    try:
                                        performance_levels.append(float(level))
                                    except:
                                        pass
                            
                            if performance_levels:
                                avg_performance = sum(performance_levels) / len(performance_levels)
                                
                                # Determinar categoría
                                if avg_performance > 3.5:
                                    perf_category = "⭐ STANDOUT PLAYER"
                                    perf_color = "#2ecc71"
                                elif avg_performance >= 3:
                                    perf_category = "🌟 GOOD & INTERESTING"
                                    perf_color = "#007bff"
                                elif avg_performance >= 2.5:
                                    perf_category = "📈 ABOVE AVERAGE"
                                    perf_color = "#17a2b8"
                                elif avg_performance >= 2:
                                    perf_category = "➡️ AVERAGE"
                                    perf_color = "#ffc107"
                                else:
                                    perf_category = "📉 BELOW AVERAGE"
                                    perf_color = "#dc3545"
                                
                                st.markdown(f"""
                                <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;">
                                    <div style="font-size: 48px; font-weight: bold; color: {perf_color};">{avg_performance:.2f}</div>
                                    <div style="font-size: 12px; color: #666; text-transform: uppercase; margin: 10px 0;">Performance Average</div>
                                    <div style="background: #f0f0f0; border-radius: 10px; height: 10px; margin: 10px 0;">
                                        <div style="background: {perf_color}; width: {(avg_performance/4)*100}%; height: 100%; border-radius: 10px;"></div>
                                    </div>
                                    <div style="font-size: 14px; font-weight: 600; color: {perf_color};">{perf_category}</div>
                                    <div style="font-size: 12px; color: #999; margin-top: 5px;">Based on {len(performance_levels)} report(s)</div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.info("No performance data available")
                        
                        with col2:
                            # Calcular moda de Decision
                            decisions = player_reports['Decision'].dropna().tolist()
                            if decisions:
                                from collections import Counter
                                decision_counts = Counter(decisions)
                                mode_decision = decision_counts.most_common(1)[0][0]
                                mode_count = decision_counts.most_common(1)[0][1]
                                
                                # Determinar color
                                if 'B+' in mode_decision or 'INTERESANTE' in mode_decision.upper():
                                    decision_color = '#007bff'
                                elif 'B' in mode_decision and 'B+' not in mode_decision:
                                    decision_color = '#ffc107'
                                elif 'C' in mode_decision or 'DESCARTAR' in mode_decision.upper():
                                    decision_color = '#dc3545'
                                else:
                                    decision_color = '#2ecc71'
                                
                                st.markdown(f"""
                                <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;">
                                    <div style="font-size: 12px; color: #666; text-transform: uppercase; margin-bottom: 15px;">Decision (Mode)</div>
                                    <div style="background: {decision_color}; color: {'white' if decision_color != '#ffc107' else '#1a2332'}; 
                                                padding: 15px 20px; border-radius: 8px; font-size: 16px; font-weight: 600; margin: 15px 0;">
                                        {mode_decision}
                                    </div>
                                    <div style="font-size: 12px; color: #999; margin-top: 10px;">
                                        Appears {mode_count} time(s) out of {len(decisions)}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.info("No decision data available")
                        
                        with col3:
                            # Conteo de Watch
                            watch_data = player_reports['Watch'].dropna().tolist()
                            if watch_data:
                                from collections import Counter
                                watch_counts = Counter(watch_data)
                                
                                watch_html = '<div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
                                watch_html += '<div style="font-size: 12px; color: #666; text-transform: uppercase; margin-bottom: 15px; text-align: center;">Watch Methods</div>'
                                
                                for method, count in watch_counts.items():
                                    icon = "📺" if "TV" in str(method) else "🏟️"
                                    watch_html += f'<div style="padding: 10px; margin: 5px 0; background: #f8f9fa; border-radius: 6px; border-left: 3px solid #1976d2;">'
                                    watch_html += f'<div style="font-size: 18px;">{icon} <strong>{count}</strong> time(s)</div>'
                                    watch_html += f'<div style="font-size: 12px; color: #666; margin-top: 3px;">{method}</div>'
                                    watch_html += '</div>'
                                
                                watch_html += '</div>'
                                st.markdown(watch_html, unsafe_allow_html=True)
                            else:
                                st.info("No watch data available")
                        
                        st.markdown("---")
                        
                        # SCOUT REPORTS
                        st.markdown(f"### 📝 Scout Reports ({len(player_reports)})")
                        
                        for idx, report in player_reports.iterrows():
                            scout_name = report.get('Scout', 'Unknown Scout')
                            description = report.get('Description', 'No description')
                            date = str(report.get('Date', ''))[:10] if pd.notna(report.get('Date')) else 'N/A'
                            match_info = f"{report.get('Home Team', '')} vs {report.get('Away Team', '')}"
                            watch_method = report.get('Watch', 'N/A')
                            watch_icon = "📺" if "TV" in str(watch_method) else "🏟️"
                            
                            # Extraer Performance
                            performance = report.get('Performance', 'N/A')
                            perf_level = '?'
                            if 'LEVEL' in str(performance):
                                perf_level = str(performance).split(' - ')[0].replace('LEVEL ', '')
                            
                            # Iniciales del scout
                            initials = ''.join([word[0].upper() for word in scout_name.split()[:2]])
                            
                            st.markdown(f"""
                            <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 10px 0;">
                                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                    <div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%); 
                                                display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                                        <span style="color: #d4af37; font-weight: bold; font-size: 18px;">{initials}</span>
                                    </div>
                                    <div>
                                        <div style="font-weight: 600; font-size: 16px; color: #1a2332;">{scout_name}</div>
                                        <div style="font-size: 12px; color: #666;">{match_info} • {date} • {watch_icon} {watch_method} • ⭐ Performance: {perf_level}</div>
                                    </div>
                                </div>
                                <div style="font-size: 14px; line-height: 1.6; color: #333; padding-left: 65px;">
                                    {description}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        # SECCIÓN: POTENTIAL & DECISION FINAL
                        st.markdown("### ⭐ Final Evaluation")
                        
                        # Verificar si hay perfil guardado
                        if saved_profile is not None:
                            # Mostrar perfil guardado
                            saved_potential = saved_profile.get('Potential Level', 'N/A')
                            saved_prof = saved_profile.get('Actual Profile', saved_profile.get('Profile', ''))  # Compatibilidad con datos antiguos
                            saved_decision = saved_profile.get('Decision Final', 'N/A')
                            
                            # Determinar color del potential
                            if '🔴' in str(saved_potential) or '1' in str(saved_potential):
                                pot_color = '#dc3545'
                            elif '🟠' in str(saved_potential) or '2' in str(saved_potential):
                                pot_color = '#fd7e14'
                            elif '🔵' in str(saved_potential) or '3' in str(saved_potential):
                                pot_color = '#007bff'
                            else:
                                pot_color = '#28a745'
                            
                            # Determinar color del profile (para PRO LEAGUE)
                            if '1' in str(saved_prof):
                                prof_color = '#6c757d'
                            elif '2' in str(saved_prof):
                                prof_color = '#17a2b8'
                            elif '3' in str(saved_prof):
                                prof_color = '#007bff'
                            elif '4' in str(saved_prof):
                                prof_color = '#28a745'
                            elif '5' in str(saved_prof):
                                prof_color = '#fd7e14'
                            else:
                                prof_color = '#dc3545'
                            
                            # HTML según categoría
                            if category == "PRO LEAGUE":
                                st.markdown(f"""
                                <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 10px 0;">
                                    <div style="margin-bottom: 20px;">
                                        <div style="font-size: 12px; color: #666; text-transform: uppercase; margin-bottom: 8px;">Potential Level</div>
                                        <div style="background: {pot_color}; color: white; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: 600; display: inline-block;">
                                            {saved_potential}
                                        </div>
                                    </div>
                                    <div style="margin-bottom: 20px;">
                                        <div style="font-size: 12px; color: #666; text-transform: uppercase; margin-bottom: 8px;">Actual Profile</div>
                                        <div style="background: {prof_color}; color: white; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: 600; display: inline-block;">
                                            {saved_prof}
                                        </div>
                                    </div>
                                    <div>
                                        <div style="font-size: 12px; color: #666; text-transform: uppercase; margin-bottom: 8px;">Decision Final - Fit with Al Nassr</div>
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #1976d2;">
                                            <div style="font-size: 14px; line-height: 1.6; color: #333;">{saved_decision}</div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 10px 0;">
                                    <div style="margin-bottom: 20px;">
                                        <div style="font-size: 12px; color: #666; text-transform: uppercase; margin-bottom: 8px;">Potential Level</div>
                                        <div style="background: {pot_color}; color: white; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: 600; display: inline-block;">
                                            {saved_potential}
                                        </div>
                                    </div>
                                    <div>
                                        <div style="font-size: 12px; color: #666; text-transform: uppercase; margin-bottom: 8px;">Decision Final - Fit with Al Nassr</div>
                                        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #1976d2;">
                                            <div style="font-size: 14px; line-height: 1.6; color: #333;">{saved_decision}</div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Botón para editar
                            if st.button("✏️ Edit Analytics", type="primary", use_container_width=True, key=f"edit_{selected_player}"):
                                st.session_state[f'editing_{selected_player}'] = True
                                st.rerun()
                        
                        # Modo edición (si no hay perfil guardado o si se presionó editar)
                        if saved_profile is None or st.session_state.get(f'editing_{selected_player}', False):
                            with st.expander("📝 Edit Final Evaluation", expanded=True):
                                # Valores por defecto si existe perfil
                                default_potential_index = 0
                                default_profile_index = 0
                                default_decision = ""
                                
                                if saved_profile is not None:
                                    saved_pot = str(saved_profile.get('Potential Level', ''))
                                    saved_prof = str(saved_profile.get('Actual Profile', saved_profile.get('Profile', '')))  # Compatibilidad
                                    default_decision = str(saved_profile.get('Decision Final', ''))
                                
                                # Diferentes opciones según categoría
                                if category == "PRO LEAGUE":
                                    # Para PRO LEAGUE: Potential Level y Actual Profile (ambos con 6 opciones)
                                    
                                    level_options = [
                                        "Select...",
                                        "1 - BACKUP AL NASSR PLAYER",
                                        "2 - SQUAD AL NASSR PLAYER",
                                        "3 - STARTER AL NASSR PLAYER",
                                        "4 - STANDOUT AL NASSR PLAYER",
                                        "5 - ELITE CHAMPIONS LEAGUE",
                                        "6 - TOP WORLD CLASS"
                                    ]
                                    
                                    # Encontrar índice del potential guardado
                                    if saved_profile is not None:
                                        for i, opt in enumerate(level_options):
                                            if saved_pot in opt or any(x in saved_pot for x in ['1', '2', '3', '4', '5', '6'] if x in opt):
                                                default_potential_index = i
                                                break
                                    
                                    # Dropdown de Potential Level
                                    potential_level = st.selectbox(
                                        "Potential Level",
                                        level_options,
                                        index=default_potential_index,
                                        key=f"potential_{selected_player}"
                                    )
                                    
                                    # Encontrar índice del profile guardado
                                    if saved_profile is not None:
                                        for i, opt in enumerate(level_options):
                                            if saved_prof in opt or any(x in saved_prof for x in ['1', '2', '3', '4', '5', '6'] if x in opt):
                                                default_profile_index = i
                                                break
                                    
                                    # Dropdown de Actual Profile
                                    profile = st.selectbox(
                                        "Actual Profile",
                                        level_options,
                                        index=default_profile_index,
                                        key=f"profile_{selected_player}"
                                    )
                                else:
                                    # Para U21/U18: Solo Potential
                                    
                                    # Encontrar índice del potential guardado
                                    potential_options = [
                                        "Select...",
                                        "🔴 1 - Ceiling till U21",
                                        "🟠 2 - First Team Squad Player",
                                        "🔵 3 - First Team Starter Player",
                                        "🟢 4 - First Team & National Team Key Player"
                                    ]
                                    if saved_profile is not None:
                                        for i, opt in enumerate(potential_options):
                                            if saved_pot in opt or any(x in saved_pot for x in ['1', '2', '3', '4'] if x in opt):
                                                default_potential_index = i
                                                break
                                    
                                    # Dropdown de Potential Level
                                    potential_level = st.selectbox(
                                        "Potential Level",
                                        potential_options,
                                        index=default_potential_index,
                                        key=f"potential_{selected_player}"
                                    )
                                    profile = None
                                
                                # Text-area para Decision Final
                                decision_final = st.text_area(
                                    "Decision Final - Fit with Al Nassr",
                                    value=default_decision,
                                    placeholder="Provide a comprehensive analysis of how this player fits with Al Nassr's needs, playing style, and long-term strategy...",
                                    height=200,
                                    key=f"decision_final_{selected_player}"
                                )
                                
                                # Botones de acción
                                col_cancel, col_save = st.columns([1, 1])
                                
                                with col_cancel:
                                    if st.button("❌ Cancel", use_container_width=True, key=f"cancel_{selected_player}"):
                                        if f'editing_{selected_player}' in st.session_state:
                                            del st.session_state[f'editing_{selected_player}']
                                        st.rerun()
                                
                                with col_save:
                                    if st.button("💾 Save Profile", type="primary", use_container_width=True, key=f"save_{selected_player}"):
                                        # Validación según categoría
                                        if category == "PRO LEAGUE":
                                            if potential_level is None or potential_level == "Select...":
                                                st.error("Please select a Potential Level")
                                            elif profile is None or profile == "Select...":
                                                st.error("Please select an Actual Profile")
                                            elif not decision_final:
                                                st.error("Please provide a Decision Final")
                                            else:
                                                valid = True
                                        else:
                                            if potential_level == "Select...":
                                                st.error("Please select a Potential Level")
                                                valid = False
                                            elif not decision_final:
                                                st.error("Please provide a Decision Final")
                                                valid = False
                                            else:
                                                valid = True
                                        
                                        if 'valid' in locals() and valid:
                                            # Guardar en Excel
                                            analytics_data = {
                                                'Name': player_name,
                                                'Team': player_team,
                                                'Position': player_position,
                                                'Sec. Position': player_sec_position,
                                                'Birth Date': player_birth,
                                                'Nationality': player_nationality,
                                                'Potential Level': potential_level,
                                                'Actual Profile': profile if category == "PRO LEAGUE" else '',
                                                'Decision Final': decision_final,
                                                'Category': category,
                                                'Last Updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                                            }
                                            
                                            analytics_df = pd.DataFrame([analytics_data])
                                            
                                            if os.path.exists(analytics_file):
                                                # Cargar y actualizar
                                                existing_df = pd.read_excel(analytics_file)
                                                # Eliminar perfil anterior si existe
                                                existing_df = existing_df[existing_df['Name'] != player_name]
                                                # Añadir nuevo
                                                analytics_df = pd.concat([existing_df, analytics_df], ignore_index=True)
                                            
                                            # Guardar
                                            try:
                                                analytics_df.to_excel(analytics_file, index=False, engine='openpyxl')
                                                st.success(f"✅ Profile saved for {player_name}!")
                                                if f'editing_{selected_player}' in st.session_state:
                                                    del st.session_state[f'editing_{selected_player}']
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"❌ Error saving profile: {str(e)}")
            else:
                st.error("Invalid report format: 'Name' column not found.")

with tab4:
    st.header("📊 Player Database")
    
    # CSS personalizado para la tabla
    st.markdown("""
        <style>
        .database-header {
            background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%);
            color: #d4af37;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }
        .stats-box {
            background: #f8f9fa;
            border-left: 4px solid #d4af37;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sub-pestañas para las categorías
    db_tab1, db_tab2, db_tab3, db_tab4, db_tab5 = st.tabs(["⚽ PRO LEAGUE", "🎯 U21", "🌟 U18", "⭐ U17", "🔄 U18-U17 Combined"])
    
    # Función para mostrar base de datos
    def show_database(db_category, db_file, sheet_name=None, combine_sheets=False):
        if not os.path.exists(db_file):
            st.error(f"Database file not found: {db_file}")
            return
        
        # Cargar datos (con sheet si se especifica)
        if combine_sheets:
            # Combinar ambas sheets
            df_u18 = pd.read_excel(db_file, sheet_name="dbu18league")
            df_u17 = pd.read_excel(db_file, sheet_name="dbu17league")
            df_db = pd.concat([df_u18, df_u17], ignore_index=True)
        elif sheet_name:
            df_db = pd.read_excel(db_file, sheet_name=sheet_name)
        else:
            df_db = pd.read_excel(db_file)
        
        if df_db.empty:
            st.info("No players in database.")
            return
        
        # Header con categoría
        st.markdown(f'<div class="database-header">🗂️ {db_category} DATABASE</div>', unsafe_allow_html=True)
        
        # Estadísticas
        total_players = len(df_db)
        st.markdown(f'<div class="stats-box">📊 <b>Total Players:</b> {total_players}</div>', unsafe_allow_html=True)
        
        # FILTROS DINÁMICOS
        st.markdown("### 🔍 Filters")
        
        # Buscador general
        search_term = st.text_input("🔎 Search (Name, Team, Position...)", "", key=f"search_{db_category}")
        
        # Obtener todas las columnas
        all_cols = df_db.columns.tolist()
        
        # Crear filtros dinámicos en columnas
        filter_cols = st.columns(4)
        filters = {}
        
        col_idx = 0
        # Filtros para columnas categóricas más comunes (orden importante: League primero)
        common_filters = ['League', 'Position', 'Team', 'Nationality', 'Number', 'Birth Date']
        
        # DataFrame temporal para filtros dependientes
        df_temp = df_db.copy()
        
        for col in common_filters:
            if col in all_cols:
                with filter_cols[col_idx % 4]:
                    # Birth Date como slider de años
                    if col == 'Birth Date':
                        # Extraer años (primeros 4 dígitos)
                        years = []
                        for val in df_temp[col].dropna():
                            year_str = str(val)[:4]
                            if year_str.isdigit():
                                years.append(int(year_str))
                        
                        if years:
                            min_year = min(years)
                            max_year = max(years)
                            selected_range = st.slider(
                                "Birth Year",
                                min_value=min_year,
                                max_value=max_year,
                                value=(min_year, max_year),
                                key=f"filter_{db_category}_birth_year"
                            )
                            filters['Birth Date'] = selected_range
                            
                            # Aplicar filtro de rango de años
                            df_temp = df_temp[df_temp[col].apply(
                                lambda x: selected_range[0] <= int(str(x)[:4]) <= selected_range[1] 
                                if pd.notna(x) and str(x)[:4].isdigit() else False
                            )]
                    else:
                        # Obtener valores únicos del DataFrame temporal (ya filtrado)
                        unique_vals = df_temp[col].dropna().unique().tolist()
                        if len(unique_vals) > 0:
                            # Para Number, ordenar numéricamente
                            if col == 'Number':
                                try:
                                    sorted_vals = sorted(unique_vals, key=lambda x: int(x) if str(x).isdigit() else 0)
                                except:
                                    sorted_vals = sorted(unique_vals)
                            else:
                                sorted_vals = sorted(unique_vals)
                            filters[col] = st.selectbox(f"{col}", ["All"] + sorted_vals, key=f"filter_{db_category}_{col}")
                            
                            # Aplicar filtro inmediatamente para que afecte a los siguientes
                            if filters[col] != "All":
                                df_temp = df_temp[df_temp[col].astype(str) == str(filters[col])]
                col_idx += 1
        
        # Filtros adicionales
        st.markdown("#### Additional Filters")
        
        # Slider de Minutes (si existe)
        if 'Minutes' in all_cols:
            minutes_vals = df_db['Minutes'].dropna()
            if len(minutes_vals) > 0:
                try:
                    minutes_vals = [float(x) for x in minutes_vals if str(x).replace('.','').replace('-','').isdigit()]
                    if minutes_vals:
                        min_minutes = int(min(minutes_vals))
                        max_minutes = int(max(minutes_vals))
                        selected_minutes = st.slider(
                            "Minutes",
                            min_value=min_minutes,
                            max_value=max_minutes,
                            value=(min_minutes, max_minutes),
                            key=f"filter_{db_category}_minutes"
                        )
                        filters['Minutes'] = selected_minutes
                except:
                    pass
        
        filter_cols2 = st.columns(5)
        
        # Filtros específicos para U18/U17
        priority_filters = ['M_Played', 'M_Starter', 'M_Sub', 'Goals', 'Cards']
        
        col_idx2 = 0
        for col in priority_filters:
            if col in all_cols:
                with filter_cols2[col_idx2 % 5]:
                    unique_vals = df_db[col].dropna().unique().tolist()
                    if len(unique_vals) > 0:
                        try:
                            # Ordenar numéricamente
                            sorted_vals = sorted(unique_vals, key=lambda x: float(x) if str(x).replace('.','').isdigit() else 0)
                        except:
                            sorted_vals = sorted(unique_vals)
                        filters[col] = st.selectbox(f"{col}", ["All"] + [str(v) for v in sorted_vals], key=f"filter_{db_category}_{col}_priority")
                col_idx2 += 1
        
        # Otros filtros adicionales (excluyendo los ya mostrados)
        additional_cols = [c for c in all_cols if c not in common_filters and c not in priority_filters and c not in ['Name']]
        
        if additional_cols:
            st.markdown("#### Other Filters")
            filter_cols3 = st.columns(4)
            
            for idx, col in enumerate(additional_cols[:8]):  # Máximo 8 filtros adicionales
                with filter_cols3[idx % 4]:
                    if df_db[col].dtype in ['object', 'string']:
                        unique_vals = df_db[col].dropna().unique().tolist()
                        if len(unique_vals) > 0 and len(unique_vals) < 50:  # Solo si hay menos de 50 valores únicos
                            filters[col] = st.selectbox(f"{col}", ["All"] + sorted([str(v) for v in unique_vals]), key=f"filter_{db_category}_{col}_add")
        
        # Aplicar filtros
        df_filtered = df_db.copy()
        
        # Filtro de búsqueda general
        if search_term:
            mask = df_filtered.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            df_filtered = df_filtered[mask]
        
        # Aplicar filtros específicos
        for col, value in filters.items():
            if value and value != "All":
                # Si es un rango (tuple), aplicar filtro de rango
                if isinstance(value, tuple):
                    if col == 'Birth Date':
                        # Filtro de año de nacimiento
                        df_filtered = df_filtered[df_filtered[col].apply(
                            lambda x: value[0] <= int(str(x)[:4]) <= value[1] 
                            if pd.notna(x) and str(x)[:4].isdigit() else False
                        )]
                    elif col == 'Minutes':
                        # Filtro de minutos
                        df_filtered = df_filtered[df_filtered[col].apply(
                            lambda x: value[0] <= float(x) <= value[1] 
                            if pd.notna(x) and str(x).replace('.','').replace('-','').isdigit() else False
                        )]
                else:
                    # Filtro normal
                    df_filtered = df_filtered[df_filtered[col].astype(str) == str(value)]
        
        # Mostrar resultados
        st.markdown("---")
        st.write(f"**Showing {len(df_filtered)} of {total_players} players**")
        
        if df_filtered.empty:
            st.info("No players match the selected filters.")
        else:
            # Selector de columnas a mostrar
            with st.expander("⚙️ Customize Columns"):
                all_columns = df_filtered.columns.tolist()
                default_cols = all_columns[:10] if len(all_columns) > 10 else all_columns
                selected_cols = st.multiselect(
                    "Select columns to display:",
                    all_columns,
                    default=default_cols,
                    key=f"cols_{db_category}"
                )
            
            # Si no hay columnas seleccionadas, mostrar todas
            if not selected_cols:
                selected_cols = all_columns
            
            # Configurar la tabla EDITABLE
            df_display = df_filtered[selected_cols].copy()
            
            # Usar data_editor para hacer la tabla editable
            edited_df = st.data_editor(
                df_display,
                use_container_width=True,
                height=600,
                hide_index=True,
                num_rows="dynamic",  # Permite añadir/eliminar filas
                key=f"editor_{db_category}"
            )
            
            # Botón para guardar cambios
            if st.button("💾 Save Changes to Database", type="primary", use_container_width=True, key=f"save_{db_category}"):
                try:
                    # Actualizar el DataFrame original con los cambios
                    for col in selected_cols:
                        if col in df_filtered.columns and col in edited_df.columns:
                            df_filtered[col] = edited_df[col]
                    
                    # Actualizar el DataFrame completo
                    for idx in df_filtered.index:
                        if idx in df_db.index:
                            for col in selected_cols:
                                if col in df_filtered.columns:
                                    df_db.at[idx, col] = df_filtered.at[idx, col]
                    
                    # Guardar en Excel
                    if combine_sheets:
                        # Para U18-U17 Combined, necesitamos separar y guardar en ambas sheets
                        st.warning("Cannot save combined view. Please edit U18 or U17 separately.")
                    elif sheet_name:
                        # Guardar en sheet específica
                        with pd.ExcelWriter(db_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            df_db.to_excel(writer, sheet_name=sheet_name, index=False)
                        st.success(f"✅ Changes saved to {sheet_name}!")
                        st.rerun()
                    else:
                        # Guardar archivo completo
                        df_db.to_excel(db_file, index=False, engine='openpyxl')
                        st.success(f"✅ Changes saved to database!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving changes: {str(e)}")
            
            # Botones de descarga
            st.markdown("### 📥 Export Data")
            
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                # CSV
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"{db_category.lower().replace(' ', '_')}_filtered.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_d2:
                # Excel
                from io import BytesIO
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_filtered.to_excel(writer, index=False, sheet_name='Players')
                buffer.seek(0)
                
                st.download_button(
                    label="⬇️ Download XLSX",
                    data=buffer,
                    file_name=f"{db_category.lower().replace(' ', '_')}_filtered.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
    # Mostrar cada categoría en su tab
    with db_tab1:
        show_database("PRO LEAGUE", CATEGORY_DB_FILES["PRO LEAGUE"])
    
    with db_tab2:
        show_database("SAUDI U21 LEAGUE", CATEGORY_DB_FILES["SAUDI U21 LEAGUE"])
    
    with db_tab3:
        show_database("U18 PREMIER LEAGUE", CATEGORY_DB_FILES["U18 & U17 PREMIER LEAGUE"], sheet_name="dbu18league")
    
    with db_tab4:
        show_database("U17 PREMIER LEAGUE", CATEGORY_DB_FILES["U18 & U17 PREMIER LEAGUE"], sheet_name="dbu17league")
    
    with db_tab5:
        show_database("U18-U17 COMBINED", CATEGORY_DB_FILES["U18 & U17 PREMIER LEAGUE"], sheet_name="Ambas_Ligas")
