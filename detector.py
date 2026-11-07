import time

def analizar_logs():
    inicio_deteccion = time.time()
    
    with open("eventos.log", "r") as log:
        lineas = log.readlines()
        
    alertas = [linea for linea in lineas if "WARNING" in linea or "ERROR" in linea]
    
    fin_deteccion = time.time()
    mttd = fin_deteccion - inicio_deteccion
    mttr = mttd + 0.05  # Simulación de tiempo de mitigación
    
    print("--- INFORME DE INCIDENTES DE SEGURIDAD ---")
    print(f"Total de eventos analizados: {len(lineas)}")
    print(f"Alertas de seguridad detectadas: {len(alertas)}")
    print(f"MTTD (Mean Time to Detect): {mttd:.4f} segundos")
    print(f"MTTR (Mean Time to Respond): {mttr:.4f} segundos")
    print("------------------------------------------")

if __name__ == "__main__":
    analizar_logs()