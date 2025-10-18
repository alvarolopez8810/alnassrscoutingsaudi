#!/usr/bin/env python3
# Script para reemplazar la sección de tab2 en app.py

# Leer el archivo original
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Leer el nuevo contenido
with open('view_match_reports_new.py', 'r', encoding='utf-8') as f:
    new_content = f.readlines()

# Encontrar las líneas de inicio y fin
start_line = None
end_line = None

for i, line in enumerate(lines):
    if line.strip() == 'with tab2:':
        start_line = i
    if line.strip() == 'with tab3:' and start_line is not None:
        end_line = i
        break

if start_line is not None and end_line is not None:
    print(f"Encontrado tab2 desde línea {start_line + 1} hasta {end_line}")
    
    # Crear el nuevo archivo
    new_lines = lines[:start_line] + new_content[3:] + lines[end_line:]
    
    # Guardar
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ Reemplazo completado!")
else:
    print("❌ No se encontraron las secciones")
