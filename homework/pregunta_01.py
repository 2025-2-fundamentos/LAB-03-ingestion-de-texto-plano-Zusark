"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
def pregunta_01():
  """
  Construya y retorne un dataframe de Pandas a partir del archivo
  'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

  - El dataframe tiene la misma estructura que el archivo original.
  - Los nombres de las columnas deben ser en minusculas, reemplazando los
    espacios por guiones bajos.
  - Las palabras clave deben estar separadas por coma y con un solo
    espacio entre palabra y palabra.


  """
  try:
    import re
    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as f:
      lines = f.readlines()

    # encontrar la línea separadora (----)
    start_idx = 0
    for i, ln in enumerate(lines):
      if set(ln.strip()) == {'-'} and len(ln.strip()) > 10:
        start_idx = i + 1
        break

    pattern = re.compile(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$')
    records = []
    current = None

    for ln in lines[start_idx:]:
      if not ln.strip():
        continue
      m = pattern.match(ln)
      if m:
        # guardar anterior
        if current:
          records.append(current)
        cluster = int(m.group(1))
        cantidad = int(m.group(2))
        porcentaje = float(m.group(3).replace(',', '.'))
        resto = m.group(4).strip()
        current = {
          'cluster': cluster,
          'cantidad_de_palabras_clave': cantidad,
          'porcentaje_de_palabras_clave': porcentaje,
          'principales_palabras_clave': resto,
        }
      else:
        # línea de continuación de keywords
        if current is not None:
          current['principales_palabras_clave'] += ' ' + ln.strip()

    if current:
      records.append(current)

    rows = []
    for r in records:
      kw = r['principales_palabras_clave'].strip()
      # quitar punto final si existe
      if kw.endswith('.'):
        kw = kw[:-1]
      # normalizar espacios
      kw = ' '.join(kw.split())
      # asegurar separación con ', '
      tokens = [t.strip() for t in kw.split(',') if t.strip()]
      kw = ', '.join(tokens)
      rows.append([
        r['cluster'],
        r['cantidad_de_palabras_clave'],
        r['porcentaje_de_palabras_clave'],
        kw,
      ])

    df = pd.DataFrame(
      rows,
      columns=['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'],
    )
    return df
  except FileNotFoundError:
    print("El archivo 'files/input/clusters_report.txt' no se encontró.")
    return None