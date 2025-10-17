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
    "U18 PREMIER LEAGUE": "dbsaudiu18.xlsx"
}

CATEGORY_REPORT_FILES = {
    "PRO LEAGUE": "mreportsproleague.xlsx",
    "SAUDI U21 LEAGUE": "mreportsu21.xlsx",
    "U18 PREMIER LEAGUE": "mreportsu18.xlsx"
}

CATEGORY_ICONS = {
    "PRO LEAGUE": "Senior1DIV.png",
    "SAUDI U21 LEAGUE": "U21logo.png",
    "U18 PREMIER LEAGUE": "U18logo.png"
}

# Debug mode - Cambiar a True para ver mensajes de debug
DEBUG_MODE = False

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

# Usuarios
USERS = {
    'rafagil': 'rafagil',
    'alvarolopez': 'alvaro',
    'juangambero': 'juan'
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

# Selector de categoría
category = st.sidebar.radio(
    "Select Category",
    ["PRO LEAGUE", "SAUDI U21 LEAGUE", "U18 PREMIER LEAGUE"]
)

# Pestañas principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Create Match Report",
    "👁️ View Match Reports",
    "📋 Create Individual Report",
    "👁️ View Individual Reports",
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
            df_league = df[df['League'] == selected_league]
            teams = df_league['Team'].dropna().unique().tolist()
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
                if st.button("➕ Add Player", key="add_home", type="primary", use_container_width=True):
                    st.session_state.show_player_form = True
                    st.session_state.selected_team_for_player = home_team
            
            with col_away:
                st.subheader(f"✈️ {away_team}")
                if st.button("➕ Add Player", key="add_away", type="primary", use_container_width=True):
                    st.session_state.show_player_form = True
                    st.session_state.selected_team_for_player = away_team
            
            # Filtrar jugadores por equipos seleccionados
            df_filtered = df[df['Team'].isin([home_team, away_team])]
            
            # Mostrar formulario de jugador
            if st.session_state.get('show_player_form', False):
                st.markdown("---")
                st.subheader("Add Player to Report")
                
                # Usar el equipo seleccionado desde el botón
                player_team = st.session_state.get('selected_team_for_player', home_team)
                st.info(f"Team: {player_team}")
                
                # Filtrar por equipo seleccionado
                df_team = df_filtered[df_filtered['Team'] == player_team]
                
                if DEBUG_MODE:
                    st.info(f"🔍 DEBUG: Team={player_team}, Players found={len(df_team)}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Player Information")
                    
                    # PRO LEAGUE usa Name, U21/U18 usan Number
                    if category == "PRO LEAGUE":
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
                        nationality_val = ""
                        agent_val = ""
                        
                        # Obtener datos del jugador si se seleccionó uno
                        if selected_name and selected_name != "Select...":
                            try:
                                player_data = df_team[df_team['Name'] == selected_name].iloc[0]
                                birth_date_val = str(player_data.get('Birth Date', '')) if pd.notna(player_data.get('Birth Date')) else ""
                                height_val = str(player_data.get('Heigh', '')) if pd.notna(player_data.get('Heigh')) else ""
                                end_contract_val = str(player_data.get('End Contract', '')) if pd.notna(player_data.get('End Contract')) else ""
                                market_value_val = str(player_data.get('Market Value', '')) if pd.notna(player_data.get('Market Value')) else ""
                                position_val = str(player_data.get('Position', '')) if pd.notna(player_data.get('Position')) else ""
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
                        position = st.text_input("Position", value=position_val, key=f"position_{selected_name}")
                        
                        # Nationality como desplegable
                        nationality_index = 0
                        if nationality_val and nationality_val in COUNTRIES:
                            nationality_index = COUNTRIES.index(nationality_val) + 1
                        nationality = st.selectbox("Nationality", ["Select..."] + COUNTRIES, index=nationality_index, key="nationality")
                        
                        agent = st.text_input("Agent", value=agent_val, key="agent")
                    
                    else:  # U21 o U18
                        # Seleccionar por número
                        numbers = df_team['Number'].dropna().unique().tolist()
                        numbers = [int(n) if isinstance(n, (int, float)) and not pd.isna(n) else n for n in numbers]
                        selected_number = st.selectbox("Number", ["Select..."] + sorted(numbers, key=lambda x: (isinstance(x, str), x)), key="number_select")
                        selected_name = None
                        
                        # Inicializar valores por defecto
                        name_val = ""
                        position_val = ""
                        birth_date_val = ""
                        nationality_val = ""
                        agent_val = ""
                        
                        # Obtener datos del jugador si se seleccionó uno
                        if selected_number and selected_number != "Select...":
                            try:
                                player_data = df_team[df_team['Number'] == selected_number].iloc[0]
                                name_val = str(player_data.get('Name', '')) if pd.notna(player_data.get('Name')) else ""
                                position_val = str(player_data.get('Position', '')) if pd.notna(player_data.get('Position')) else ""
                                birth_date_val = str(player_data.get('Birth Date', '')) if pd.notna(player_data.get('Birth Date')) else ""
                                nationality_val = str(player_data.get('Nationality', '')) if pd.notna(player_data.get('Nationality')) else ""
                                agent_val = str(player_data.get('Agent', '')) if pd.notna(player_data.get('Agent')) and player_data.get('Agent') != '' else ""
                                
                                if DEBUG_MODE:
                                    st.success(f"🔍 DEBUG U21/U18: Number={selected_number}, Name={name_val}, Position={position_val}, Birth={birth_date_val}")
                            except Exception as e:
                                st.error(f"❌ Error loading player data: {e}")
                                if DEBUG_MODE:
                                    st.error(f"🔍 DEBUG: Exception details: {str(e)}")
                        
                        # Mostrar campos (todos editables) con keys únicos
                        name = st.text_input("Name", value=name_val, key=f"name_{selected_number}")
                        position = st.text_input("Position", value=position_val, key=f"position_{selected_number}")
                        birth_date = st.text_input("Birth Date", value=birth_date_val, key=f"birth_date_{selected_number}")
                        
                        # Nationality como desplegable
                        nationality_index = 0
                        if nationality_val and nationality_val in COUNTRIES:
                            nationality_index = COUNTRIES.index(nationality_val) + 1
                        nationality = st.selectbox("Nationality", ["Select..."] + COUNTRIES, index=nationality_index, key="nationality")
                        
                        agent = st.text_input("Agent", value=agent_val, key="agent")
                
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
                    
                    # Potential
                    potential = st.selectbox("Potential", [
                        "Select...",
                        "LEVEL 4 - Key player for Al Nassr team + National team",
                        "LEVEL 3 - First team - Starter",
                        "LEVEL 2 - First team - Squad player",
                        "LEVEL 1 - Valuable player up to U21"
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
                            if not selected_name or selected_name == "Select..." or performance == "Select..." or potential == "Select..." or profile == "Select..." or decision == "Select...":
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
                                    'Nationality': nationality,
                                    'Agent': agent if agent else 'N/A',
                                    'Performance': performance,
                                    'Potential': potential,
                                    'Profile': profile,
                                    'Decision': decision,
                                    'Description': description
                                }
                                st.session_state.players_list.append(player_info)
                                st.session_state.show_player_form = False
                                st.success(f"✅ {selected_name} added to report!")
                                st.rerun()
                        else:  # U21 o U18
                            if not selected_number or selected_number == "Select..." or performance == "Select..." or potential == "Select..." or decision == "Select...":
                                st.error("Please fill all required fields")
                            else:
                                # Agregar jugador a la lista (usando valores editados)
                                player_info = {
                                    'Team': player_team,
                                    'Number': selected_number,
                                    'Name': name,
                                    'Position': position,
                                    'Birth Date': birth_date,
                                    'Nationality': nationality,
                                    'Agent': agent if agent else 'N/A',
                                    'Performance': performance,
                                    'Potential': potential,
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
                                if key not in ['Performance', 'Potential', 'Profile', 'Decision']:
                                    st.write(f"**{key}:** {value}")
                        with col2:
                            st.write(f"**Performance:** {player.get('Performance', 'N/A')}")
                            st.write(f"**Potential:** {player.get('Potential', 'N/A')}")
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
                            if DEBUG_MODE:
                                st.info(f"🔍 DEBUG: Saving {len(st.session_state.players_list)} players")
                            
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
                            
                            if os.path.exists(report_file):
                                # Cargar existente y añadir
                                try:
                                    existing_df = pd.read_excel(report_file)
                                    final_df = pd.concat([existing_df, report_df], ignore_index=True)
                                except Exception as e:
                                    st.warning(f"Could not load existing file: {e}. Creating new file.")
                                    final_df = report_df
                            else:
                                final_df = report_df
                            
                            # Guardar con openpyxl
                            final_df.to_excel(report_file, index=False, engine='openpyxl')
                            
                            st.success(f"✅ Match report saved successfully!")
                            st.info(f"📁 Saved to: {report_file}")
                            st.balloons()
                            
                            # Limpiar lista
                            st.session_state.players_list = []
                            st.session_state.show_player_form = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error saving report: {str(e)}")
                            st.error(f"Please check file permissions and try again.")
                
                with col3:
                    if st.button("🗑️ Clear All", use_container_width=True):
                        st.session_state.players_list = []
                        st.session_state.show_player_form = False
                        st.rerun()

with tab2:
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
            st.header(f"View Match Reports - {category}")
    else:
        st.header(f"View Match Reports - {category}")
    
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
            st.write(f"**Total Reports:** {len(df_reports)}")
            
            # CSS personalizado con colores Al Nassr
            st.markdown("""
                <style>
                .scout-header {
                    background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%);
                    color: #d4af37;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0 10px 0;
                    font-size: 24px;
                    font-weight: bold;
                    border-left: 5px solid #d4af37;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                .player-card {
                    background: white;
                    border: 2px solid #e8e8e8;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    transition: all 0.3s ease;
                }
                .player-card:hover {
                    border-color: #d4af37;
                    box-shadow: 0 4px 12px rgba(212,175,55,0.2);
                }
                .player-name {
                    color: #1a2332;
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .info-label {
                    color: #1a2332;
                    font-weight: 600;
                    display: inline-block;
                    min-width: 120px;
                }
                .info-value {
                    color: #555;
                }
                .rating-badge {
                    background: #d4af37;
                    color: #1a2332;
                    padding: 4px 12px;
                    border-radius: 15px;
                    font-weight: bold;
                    display: inline-block;
                    margin: 2px;
                }
                /* Performance y Potential levels */
                .level-4 { background: #28a745; color: white; }
                .level-3 { background: #007bff; color: white; }
                .level-2 { background: #fd7e14; color: white; }
                .level-1 { background: transparent; color: #1a2332; border: 2px solid #6c757d; }
                
                /* Decision colors */
                .decision-A { background: #28a745; color: white; }
                .decision-B-plus { background: #007bff; color: white; }
                .decision-B { background: #ffc107; color: #1a2332; }
                .decision-P { background: #007bff; color: white; }
                .decision-C { background: #dc3545; color: white; }
                </style>
            """, unsafe_allow_html=True)
            
            # FILTROS DINÁMICOS
            st.markdown("### 🔍 Filters")
            
            # Crear columnas para filtros
            filter_cols = st.columns(4)
            filters = {}
            
            # Obtener todas las columnas del DataFrame
            all_columns = df_reports.columns.tolist()
            
            # Filtros principales en la primera fila
            with filter_cols[0]:
                if 'Scout' in all_columns:
                    scouts = ['All'] + sorted(df_reports['Scout'].dropna().unique().tolist())
                    filters['Scout'] = st.selectbox("Scout", scouts)
            
            with filter_cols[1]:
                if 'Team' in all_columns:
                    teams = df_reports['Team'].dropna().unique().tolist()
                    all_teams = ['All'] + sorted(teams)
                    filters['Team'] = st.selectbox("Team (Player)", all_teams)
            
            with filter_cols[2]:
                if 'Decision' in all_columns:
                    decisions = ['All'] + sorted(df_reports['Decision'].dropna().unique().tolist())
                    filters['Decision'] = st.selectbox("Decision", decisions)
            
            with filter_cols[3]:
                if 'Performance' in all_columns:
                    performances = ['All'] + sorted(df_reports['Performance'].dropna().unique().tolist())
                    filters['Performance'] = st.selectbox("Performance", performances)
            
            # Filtros adicionales en segunda fila
            filter_cols2 = st.columns(4)
            
            with filter_cols2[0]:
                if 'Position' in all_columns:
                    positions = ['All'] + sorted(df_reports['Position'].dropna().unique().tolist())
                    filters['Position'] = st.selectbox("Position", positions)
            
            with filter_cols2[1]:
                if 'Nationality' in all_columns:
                    nationalities = ['All'] + sorted(df_reports['Nationality'].dropna().unique().tolist())
                    filters['Nationality'] = st.selectbox("Nationality", nationalities)
            
            with filter_cols2[2]:
                if 'Potential' in all_columns:
                    potentials = ['All'] + sorted(df_reports['Potential'].dropna().unique().tolist())
                    filters['Potential'] = st.selectbox("Potential", potentials)
            
            with filter_cols2[3]:
                if 'Profile' in all_columns and category == "PRO LEAGUE":
                    profiles = ['All'] + sorted(df_reports['Profile'].dropna().unique().tolist())
                    filters['Profile'] = st.selectbox("Profile", profiles)
            
            # Aplicar filtros
            df_filtered = df_reports.copy()
            
            if filters.get('Scout') and filters['Scout'] != 'All':
                df_filtered = df_filtered[df_filtered['Scout'] == filters['Scout']]
            
            if filters.get('Team') and filters['Team'] != 'All':
                df_filtered = df_filtered[df_filtered['Team'] == filters['Team']]
            
            if filters.get('Decision') and filters['Decision'] != 'All':
                df_filtered = df_filtered[df_filtered['Decision'] == filters['Decision']]
            
            if filters.get('Performance') and filters['Performance'] != 'All':
                df_filtered = df_filtered[df_filtered['Performance'] == filters['Performance']]
            
            if filters.get('Position') and filters['Position'] != 'All':
                df_filtered = df_filtered[df_filtered['Position'] == filters['Position']]
            
            if filters.get('Nationality') and filters['Nationality'] != 'All':
                df_filtered = df_filtered[df_filtered['Nationality'] == filters['Nationality']]
            
            if filters.get('Potential') and filters['Potential'] != 'All':
                df_filtered = df_filtered[df_filtered['Potential'] == filters['Potential']]
            
            if filters.get('Profile') and filters.get('Profile') != 'All':
                df_filtered = df_filtered[df_filtered['Profile'] == filters['Profile']]
            
            st.markdown("---")
            st.write(f"**Showing {len(df_filtered)} reports**")
            
            if df_filtered.empty:
                st.info("No reports match the selected filters.")
            else:
                # Botones de descarga
                st.markdown("### 📥 Export Reports")
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    # CSV
                    csv_reports = df_filtered.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv_reports,
                        file_name=f"match_reports_{category.lower().replace(' ', '_')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col_d2:
                    # Excel
                    from io import BytesIO
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df_filtered.to_excel(writer, index=False, sheet_name='Reports')
                    buffer.seek(0)
                    
                    st.download_button(
                        label="⬇️ Download XLSX",
                        data=buffer,
                        file_name=f"match_reports_{category.lower().replace(' ', '_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                st.markdown("---")
                
                # Agrupar por Scout
                scouts_list = df_filtered['Scout'].unique()
                
                for scout in sorted(scouts_list):
                    # Header del Scout con estilo
                    st.markdown(f'<div class="scout-header">👤 {scout}</div>', unsafe_allow_html=True)
                    
                    # Obtener reportes de este scout
                    scout_reports = df_filtered[df_filtered['Scout'] == scout]
                    
                    st.write(f"*{len(scout_reports)} report(s)*")
                    
                    # Mostrar cada reporte
                    for idx, report in scout_reports.iterrows():
                        # Construir etiqueta del expander
                        player_name = report.get('Name', 'Unknown Player')
                        position = report.get('Position', 'N/A')
                        birth_date = report.get('Birth Date', 'N/A')
                        
                        # Construir partido
                        home_team = report.get('Home Team', '')
                        away_team = report.get('Away Team', '')
                        match = f"{home_team} vs {away_team}" if home_team and away_team else "N/A"
                        
                        # Fecha
                        date = report.get('Date', 'N/A')
                        
                        # Etiqueta del expander
                        expander_label = f"⚽ {player_name} | 📍 {position} | 🎂 {birth_date} | 🏟️ {match} | 📅 {date}"
                        
                        with st.expander(expander_label):
                            # Información en columnas
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("**Match Info**")
                                if 'Home Team' in report and pd.notna(report['Home Team']):
                                    st.write(f"🏠 **Home:** {report['Home Team']}")
                                if 'Away Team' in report and pd.notna(report['Away Team']):
                                    st.write(f"✈️ **Away:** {report['Away Team']}")
                                if 'Date' in report and pd.notna(report['Date']):
                                    st.write(f"📅 **Date:** {report['Date']}")
                                if 'League' in report and pd.notna(report['League']):
                                    st.write(f"🏆 **League:** {report['League']}")
                            
                            with col2:
                                st.markdown("**Player Info**")
                                if 'Team' in report and pd.notna(report['Team']):
                                    st.write(f"👕 **Team:** {report['Team']}")
                                if 'Position' in report and pd.notna(report['Position']):
                                    st.write(f"📍 **Position:** {report['Position']}")
                                if 'Birth Date' in report and pd.notna(report['Birth Date']):
                                    st.write(f"🎂 **Birth Date:** {report['Birth Date']}")
                                if 'Nationality' in report and pd.notna(report['Nationality']):
                                    st.write(f"🌍 **Nationality:** {report['Nationality']}")
                                if 'Agent' in report and pd.notna(report['Agent']) and report['Agent'] != 'N/A':
                                    st.write(f"🤝 **Agent:** {report['Agent']}")
                                
                                # Campos específicos de PRO LEAGUE
                                if category == "PRO LEAGUE":
                                    if 'Height' in report and pd.notna(report['Height']):
                                        st.write(f"📏 **Height:** {report['Height']}")
                                    if 'End Contract' in report and pd.notna(report['End Contract']):
                                        st.write(f"📄 **Contract:** {report['End Contract']}")
                                    if 'Market Value' in report and pd.notna(report['Market Value']):
                                        st.write(f"💰 **Value:** {report['Market Value']}")
                                
                                # Campo específico de U21/U18
                                if 'Number' in report and pd.notna(report['Number']):
                                    st.write(f"🔢 **Number:** {report['Number']}")
                            
                            with col3:
                                st.markdown("**Evaluation**")
                                
                                # Performance con colores
                                if 'Performance' in report and pd.notna(report['Performance']):
                                    perf_text = str(report['Performance'])
                                    # Detectar el nivel
                                    if 'LEVEL 4' in perf_text:
                                        perf_class = 'level-4'
                                    elif 'LEVEL 3' in perf_text:
                                        perf_class = 'level-3'
                                    elif 'LEVEL 2' in perf_text:
                                        perf_class = 'level-2'
                                    elif 'LEVEL 1' in perf_text:
                                        perf_class = 'level-1'
                                    else:
                                        perf_class = 'rating-badge'
                                    st.markdown(f"**Performance:** <span class='rating-badge {perf_class}'>{perf_text}</span>", unsafe_allow_html=True)
                                
                                # Potential con colores
                                if 'Potential' in report and pd.notna(report['Potential']):
                                    pot_text = str(report['Potential'])
                                    # Detectar el nivel
                                    if 'LEVEL 4' in pot_text:
                                        pot_class = 'level-4'
                                    elif 'LEVEL 3' in pot_text:
                                        pot_class = 'level-3'
                                    elif 'LEVEL 2' in pot_text:
                                        pot_class = 'level-2'
                                    elif 'LEVEL 1' in pot_text:
                                        pot_class = 'level-1'
                                    else:
                                        pot_class = 'rating-badge'
                                    st.markdown(f"**Potential:** <span class='rating-badge {pot_class}'>{pot_text}</span>", unsafe_allow_html=True)
                                
                                # Profile (solo PRO LEAGUE y si no es "-")
                                if 'Profile' in report and pd.notna(report['Profile']):
                                    profile_val = str(report['Profile']).strip()
                                    if profile_val != '-' and profile_val != '':
                                        st.write(f"**Profile:** {report['Profile']}")
                                
                                # Decision con colores
                                if 'Decision' in report and pd.notna(report['Decision']):
                                    decision = str(report['Decision'])
                                    decision_class = "decision-" + decision.split(' - ')[0].replace('+', '-plus').replace(' ', '-')
                                    st.markdown(f"**Decision:** <span class='rating-badge {decision_class}'>{decision}</span>", unsafe_allow_html=True)
                            
                            # Description
                            if 'Description' in report and pd.notna(report['Description']) and report['Description']:
                                st.markdown("**📝 Description:**")
                                st.write(report['Description'])
                            
                            # Botón para eliminar reporte
                            st.markdown("---")
                            if st.button(f"🗑️ Delete Report", key=f"delete_report_{idx}", type="secondary"):
                                # Eliminar esta fila del DataFrame
                                df_reports_updated = df_reports.drop(idx)
                                
                                # Guardar el archivo actualizado
                                try:
                                    df_reports_updated.to_excel(report_file, index=False, engine='openpyxl')
                                    st.success(f"✅ Report deleted successfully!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error deleting report: {str(e)}")

with tab3:
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
            st.header(f"Create Individual Report - {category}")
    else:
        st.header(f"Create Individual Report - {category}")
    st.info("Coming soon...")

with tab4:
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
            st.header(f"View Individual Reports - {category}")
    else:
        st.header(f"View Individual Reports - {category}")
    st.info("Coming soon...")

with tab5:
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
    db_tab1, db_tab2, db_tab3 = st.tabs(["⚽ PRO LEAGUE", "🎯 U21", "🌟 U18"])
    
    # Función para mostrar base de datos
    def show_database(db_category, db_file):
        if not os.path.exists(db_file):
            st.error(f"Database file not found: {db_file}")
            return
        
        # Cargar datos
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
                    # Obtener valores únicos del DataFrame temporal (ya filtrado)
                    unique_vals = df_temp[col].dropna().unique().tolist()
                    if len(unique_vals) > 0:
                        # Para Number y Birth Date, ordenar numéricamente
                        if col in ['Number', 'Birth Date']:
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
        filter_cols2 = st.columns(4)
        
        additional_cols = [c for c in all_cols if c not in common_filters and c not in ['Name']]
        
        for idx, col in enumerate(additional_cols[:8]):  # Máximo 8 filtros adicionales
            with filter_cols2[idx % 4]:
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
            
            # Configurar la tabla
            # Convertir todas las columnas a string para evitar errores de tipo
            df_display = df_filtered[selected_cols].copy()
            for col in df_display.columns:
                df_display[col] = df_display[col].astype(str)
            
            st.dataframe(
                df_display,
                use_container_width=True,
                height=600,
                hide_index=True
            )
            
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
        show_database("U18 PREMIER LEAGUE", CATEGORY_DB_FILES["U18 PREMIER LEAGUE"])
