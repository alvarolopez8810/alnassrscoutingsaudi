# Nueva vista minimalista para VIEW MATCH REPORTS
# Este código reemplazará la sección de tab2

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
                    birth_date = str(report.get('Birth Date', ''))[:4] if pd.notna(report.get('Birth Date')) else 'N/A'
                    home_team = report.get('Home Team', '')
                    away_team = report.get('Away Team', '')
                    date = str(report.get('Date', ''))[:10] if pd.notna(report.get('Date')) else 'N/A'
                    performance = report.get('Performance', 'N/A')
                    league = report.get('League', 'N/A')
                    watch = report.get('Watch', 'N/A')
                    decision = report.get('Decision', 'N/A')
                    description = report.get('Description', '')
                    
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
                    expander_label = f"#{number} {name} | {position} | 🎂 {birth_date} | ⚽ {home_team} vs {away_team} | 📅 {date} | {decision_display}"
                    
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
