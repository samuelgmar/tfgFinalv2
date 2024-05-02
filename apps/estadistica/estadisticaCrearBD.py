import sqlite3
conexion = sqlite3.connect("estadistica.db")
cursor = conexion.cursor()
##Euromillones
# Crear tabla para los números de Euromillones
cursor.execute('''CREATE TABLE IF NOT EXISTS euromillones (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para El Millón
cursor.execute('''CREATE TABLE IF NOT EXISTS el_millon (
                    id INTEGER PRIMARY KEY,
                    numero TEXT NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para las estrellas
cursor.execute('''CREATE TABLE IF NOT EXISTS estrellas (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

##Primitiva
# Crear tabla para los números de la Primitiva
cursor.execute('''CREATE TABLE IF NOT EXISTS primitiva (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para el Complementario de la Primitiva
cursor.execute('''CREATE TABLE IF NOT EXISTS complementario_pr (
                    id INTEGER PRIMARY KEY,
                    numero TEXT NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para el Reintegro de la Primitiva
cursor.execute('''CREATE TABLE IF NOT EXISTS reintegro_pr (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para el Joker
cursor.execute('''CREATE TABLE IF NOT EXISTS joker (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

#Bonoloto
# Crear tabla para los números de la Bonoloto
cursor.execute('''CREATE TABLE IF NOT EXISTS bonoloto (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para el Complementario de la Bonoloto
cursor.execute('''CREATE TABLE IF NOT EXISTS complementario_bo (
                    id INTEGER PRIMARY KEY,
                    numero TEXT NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para el Reintegro de la Bonoloto
cursor.execute('''CREATE TABLE IF NOT EXISTS reintegro_bo (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

#ELGORDO
# Crear tabla para los números del Gordo de la Primitiva
cursor.execute('''CREATE TABLE IF NOT EXISTS gordo (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para la clave del Gordo de la Primitiva
cursor.execute('''CREATE TABLE IF NOT EXISTS clave (
                    id INTEGER PRIMARY KEY,
                    numero TEXT NOT NULL,
                    fecha DATE NOT NULL
                )''')

#Eurodreams
# Crear tabla para los números de Eurodreams
cursor.execute('''CREATE TABLE IF NOT EXISTS eurodreams (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

# Crear tabla para los sueños
cursor.execute('''CREATE TABLE IF NOT EXISTS sueño (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')

#LoteriaNacional
# Crear tabla para los números de la Lotería Nacional
cursor.execute('''CREATE TABLE IF NOT EXISTS LN (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    fecha DATE NOT NULL,
                    premio REAL
                )''')

# Crear tabla para los reintegros de la Lotería Nacional
cursor.execute('''CREATE TABLE IF NOT EXISTS reintegroLN (
                    id INTEGER PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    posicion INTEGER NOT NULL,
                    fecha DATE NOT NULL
                )''')



# Datos de la Bonoloto
datos_bonoloto = [
    ["2024-01-01", [10, 15, 21, 28, 29, 36]],
    ["2024-01-02", [3, 10, 15, 32, 35, 41]],
    ["2024-01-03", [11, 15, 22, 38, 43, 47]],
    ["2024-01-04", [4, 14, 27, 32, 43, 49]],
    ["2024-01-05", [7, 27, 32, 34, 35, 36]],
    ["2024-01-06", [31, 37, 39, 43, 44, 46]],
    ["2024-01-07", [20, 31, 35, 36, 40, 41]],
    ["2024-01-08", [10, 29, 39, 41, 44, 48]],
    ["2024-01-09", [6, 33, 36, 43, 44, 47]],
    ["2024-01-10", [18, 19, 27, 40, 48, 49]],
    ["2024-01-11", [5, 18, 19, 23, 42, 45]],
    ["2024-01-12", [11, 12, 16, 18, 30, 47]],
    ["2024-01-13", [4, 23, 27, 28, 34, 49]],
    ["2024-01-14", [16, 19, 35, 40, 47, 49]],
    ["2024-01-15", [9, 10, 20, 24, 27, 31]],
    ["2024-01-16", [1, 3, 9, 13, 26, 38]],
    ["2024-01-17", [11, 13, 18, 23, 43, 49]],
    ["2024-01-18", [25, 26, 32, 33, 44, 45]],
    ["2024-01-19", [1, 2, 9, 26, 38, 43]],
    ["2024-01-20", [7, 12, 20, 23, 35, 41]],
    ["2024-01-21", [4, 10, 22, 34, 41, 44]],
    ["2024-01-22", [11, 12, 16, 24, 31, 46]],
    ["2024-01-23", [10, 16, 29, 33, 46, 48]],
    ["2024-01-24", [3, 17, 23, 25, 34, 48]],
    ["2024-01-25", [6, 13, 16, 21, 27, 32]],
    ["2024-01-26", [5, 7, 29, 30, 39, 41]],
    ["2024-01-27", [2, 4, 37, 39, 44, 46]],
    ["2024-01-28", [4, 25, 29, 31, 37, 41]],
    ["2024-01-29", [3, 5, 10, 37, 47, 49]],
    ["2024-01-30", [13, 15, 16, 25, 31, 34]],
    ["2024-01-31", [6, 14, 16, 36, 43, 46]],
    ["2024-02-01", [7, 10, 14, 38, 43, 47]],
    ["2024-02-02", [1, 10, 16, 31, 39, 45]],
    ["2024-02-03", [1, 6, 10, 18, 22, 26]],
    ["2024-02-04", [22, 23, 34, 42, 44, 47]],
    ["2024-02-05", [10, 20, 28, 29, 30, 34]],
    ["2024-02-06", [3, 7, 22, 39, 40, 45]],
    ["2024-02-07", [1, 13, 16, 19, 25, 39]],
    ["2024-02-08", [1, 6, 17, 36, 40, 43]],
    ["2024-02-09", [7, 16, 17, 24, 27, 37]],
    ["2024-02-10", [1, 5, 12, 22, 23, 28]],
    ["2024-02-11", [24, 30, 34, 39, 45, 46]],
    ["2024-02-12", [13, 23, 24, 25, 42, 47]],
    ["2024-02-13", [3, 10, 33, 36, 38, 39]],
    ["2024-02-14", [14, 16, 26, 31, 34, 40]],
    ["2024-02-15", [8, 18, 28, 32, 41, 48]],
    ["2024-02-16", [5, 9, 16, 17, 22, 32]],
    ["2024-02-17", [5, 6, 7, 15, 25, 28]],
    ["2024-02-18", [17, 24, 28, 31, 41, 45]],
    ["2024-02-19", [6, 9, 19, 23, 25, 37]],
    ["2024-02-20", [2, 6, 9, 22, 31, 46]],
    ["2024-02-21", [2, 14, 19, 27, 31, 40]],
    ["2024-02-22", [5, 8, 11, 19, 44, 45]],
    ["2024-02-23", [1, 12, 20, 27, 36, 39]],
    ["2024-02-24", [2, 11, 15, 20, 34, 48]],
    ["2024-02-25", [6, 9, 25, 39, 42, 47]],
    ["2024-02-26", [6, 11, 25, 33, 34, 35]],
    ["2024-02-27", [7, 9, 14, 17, 32, 33]],
    ["2024-02-28", [1, 5, 6, 16, 28, 30]],
    ["2024-02-29", [4, 7, 25, 26, 40, 47]],
    ["2024-03-01", [8, 9, 16, 18, 41, 48]],
    ["2024-03-02", [8, 19, 29, 33, 35, 49]],
    ["2024-03-03", [7, 16, 19, 33, 48, 49]]
]

# Insertar datos en la tabla de Bonoloto
for fecha, numeros in datos_bonoloto:
    numeros_str = ' '.join(map(str, numeros))  # Convertir la lista de números a una cadena de texto
    cursor.execute("INSERT INTO bonoloto (numero, fecha) VALUES (?, ?)", (numeros_str, fecha))

# Datos del Complementario de la Bonoloto
datos_complementario_bo = [
    ["2024-01-01", 25], ["2024-01-02", 48], ["2024-01-03", 8], ["2024-01-04", 31], ["2024-01-05", 29],
    ["2024-01-06", 33], ["2024-01-07", 37], ["2024-01-08", 16], ["2024-01-09", 41], ["2024-01-10", 9],
    ["2024-01-11", 36], ["2024-01-12", 36], ["2024-01-13", 42], ["2024-01-14", 38], ["2024-01-15", 34],
    ["2024-01-16", 31], ["2024-01-17", 14], ["2024-01-18", 29], ["2024-01-19", 44], ["2024-01-20", 49],
    ["2024-01-21", 46], ["2024-01-22", 34], ["2024-01-23", 40], ["2024-01-24", 21], ["2024-01-25", 14],
    ["2024-01-26", 46], ["2024-01-27", 16], ["2024-01-28", 38], ["2024-01-29", 18], ["2024-01-30", 35],
    ["2024-01-31", 12], ["2024-02-01", 30], ["2024-02-02", 17], ["2024-02-03", 11], ["2024-02-04", 36],
    ["2024-02-05", 0], ["2024-02-06", 17], ["2024-02-07", 21], ["2024-02-08", 27], ["2024-02-09", 42],
    ["2024-02-10", 47], ["2024-02-11", 26], ["2024-02-12", 12], ["2024-02-13", 8], ["2024-02-14", 10],
    ["2024-02-15", 45], ["2024-02-16", 21], ["2024-02-17", 49], ["2024-02-18", 22], ["2024-02-19", 20],
    ["2024-02-20", 8], ["2024-02-21", 34], ["2024-02-22", 9], ["2024-02-23", 40], ["2024-02-24", 31],
    ["2024-02-25", 38], ["2024-02-26", 38], ["2024-02-27", 6], ["2024-02-28", 46], ["2024-02-29", 20],
    ["2024-03-01", 23], ["2024-03-02", 34], ["2024-03-03", 15]
]

# Insertar datos en la tabla de Complementario de la Bonoloto
for fecha, numero in datos_complementario_bo:
    cursor.execute("INSERT INTO complementario_bo (numero, fecha) VALUES (?, ?)", (numero, fecha))

# Datos del Reintegro de la Bonoloto
datos_reintegro_bo = [
    ["2024-01-01", 6], ["2024-01-02", 5], ["2024-01-03", 8], ["2024-01-04", 6], ["2024-01-05", 6],
    ["2024-01-06", 6], ["2024-01-07", 7], ["2024-01-08", 5], ["2024-01-09", 8], ["2024-01-10", 8],
    ["2024-01-11", 7], ["2024-01-12", 1], ["2024-01-13", 1], ["2024-01-14", 2], ["2024-01-15", 7],
    ["2024-01-16", 8], ["2024-01-17", 1], ["2024-01-18", 4], ["2024-01-19", 0], ["2024-01-20", 7],
    ["2024-01-21", 2], ["2024-01-22", 2], ["2024-01-23", 0], ["2024-01-24", 4], ["2024-01-25", 6],
    ["2024-01-26", 3], ["2024-01-27", 7], ["2024-01-28", 6], ["2024-01-29", 3], ["2024-01-30", 5],
    ["2024-01-31", 5], ["2024-02-01", 9], ["2024-02-02", 5], ["2024-02-03", 0], ["2024-02-04", 0],
    ["2024-02-05", 3], ["2024-02-06", 5], ["2024-02-07", 0], ["2024-02-08", 8], ["2024-02-09", 6],
    ["2024-02-10", 7], ["2024-02-11", 1], ["2024-02-12", 9], ["2024-02-13", 7], ["2024-02-14", 9],
    ["2024-02-15", 4], ["2024-02-16", 7], ["2024-02-17", 1], ["2024-02-18", 7], ["2024-02-19", 7],
    ["2024-02-20", 2], ["2024-02-21", 0], ["2024-02-22", 4], ["2024-02-23", 7], ["2024-02-24", 2],
    ["2024-02-25", 3], ["2024-02-26", 3], ["2024-02-27", 4], ["2024-02-28", 6], ["2024-02-29", 3],
    ["2024-03-01", 8], ["2024-03-02", 2], ["2024-03-03", 3]
]

# Insertar datos en la tabla de Reintegro de la Bonoloto
for fecha, numero in datos_reintegro_bo:
    cursor.execute("INSERT INTO reintegro_bo (numero, fecha) VALUES (?, ?)", (numero, fecha))

# Datos del Gordo de la Primitiva
datos_gordo = [
    ["2024-01-07", [6, 18, 20, 31, 49]],
    ["2024-01-14", [1, 26, 28, 40, 45]],
    ["2024-01-21", [6, 10, 23, 24, 49]],
    ["2024-01-28", [10, 19, 23, 26, 39]],
    ["2024-02-04", [9, 26, 28, 43, 51]],
    ["2024-02-11", [2, 3, 8, 21, 36]],
    ["2024-02-18", [5, 6, 19, 34, 44]],
    ["2024-02-25", [1, 19, 20, 21, 39]],
    ["2024-03-03", [8, 17, 24, 26, 32]]
]

# Insertar datos en la tabla del Gordo de la Primitiva
for fecha, numeros in datos_gordo:
    numeros_str = ' '.join(map(str, numeros))  # Convertir la lista de números a una cadena de texto
    cursor.execute("INSERT INTO gordo (numero, fecha) VALUES (?, ?)", (numeros_str, fecha))


# Datos de la clave del Gordo de la Primitiva
datos_clave = [
    ["2024-01-07", "1"],
    ["2024-01-14", "8"],
    ["2024-01-21", "6"],
    ["2024-01-28", "1"],
    ["2024-02-04", "9"],
    ["2024-02-11", "9"],
    ["2024-02-18", "6"],
    ["2024-02-25", "2"],
    ["2024-03-03", "1"]
]

# Insertar datos en la tabla de la clave del Gordo de la Primitiva
for fecha, clave in datos_clave:
    cursor.execute("INSERT INTO clave (numero, fecha) VALUES (?, ?)", (clave, fecha))


# Datos de los sorteos de Eurodreams
datos_eurodreams = [
    ["2024-03-07", [13, 15, 23, 31, 35, 39]],
    ["2024-02-29", [10, 11, 21, 31, 38, 40]],
    ["2024-02-22", [2, 8, 10, 20, 24, 39]],
    ["2024-02-15", [3, 5, 8, 14, 16, 21]],
    ["2024-02-08", [2, 19, 22, 26, 36, 40]],
    ["2024-02-01", [6, 12, 15, 28, 33, 35]],
    ["2024-01-25", [1, 2, 3, 22, 26, 27]],
    ["2024-01-18", [8, 16, 19, 23, 30, 40]],
    ["2024-01-11", [5, 7, 24, 29, 31, 38]],
    ["2024-01-04", [15, 21, 22, 29, 30, 39]],
    ["2024-01-01", [2, 5, 18, 24, 28, 39]]
]

# Insertar datos en la tabla de Eurodreams
for fecha, numeros in datos_eurodreams:
    for numero in numeros:
        cursor.execute("INSERT INTO eurodreams (numero, fecha) VALUES (?, ?)", (numero, fecha))


# Datos de los sueños asociados a los sorteos de Eurodreams
datos_suenos = [
    ["2024-03-07", 1],
    ["2024-02-29", 1],
    ["2024-02-22", 4],
    ["2024-02-15", 1],
    ["2024-02-08", 4],
    ["2024-02-01", 3],
    ["2024-01-25", 1],
    ["2024-01-18", 5],
    ["2024-01-11", 2],
    ["2024-01-04", 1],
    ["2024-01-01", 4]
]

# Insertar datos en la tabla de sueños
for fecha, sueno in datos_suenos:
    cursor.execute("INSERT INTO sueño (numero, fecha) VALUES (?, ?)", (sueno, fecha))


# Datos de los sorteos de la Lotería Nacional
datos_ln = [
    ["2024-03-09", 10235, 53616, [2, 4, 5]],
    ["2024-03-07", 86709, 21260, [0, 7, 9]],
    ["2024-03-02", 32609, 20739, [2, 7, 9]],
    ["2024-02-29", 78863, 29479, [0, 3, 9]],
    ["2024-02-24", 76850, 24768, [0, 3, 8]],
    ["2024-02-22", 41701, 45034, [1, 5, 6]],
    ["2024-02-17", 72246, 72530, [2, 5, 6]],
    ["2024-02-15", 11568, 28569, [2, 4, 8]],
    ["2024-02-10", 60407, 67981, [3, 7, 8]],
    ["2024-02-08", 19156, 65772, [2, 4, 6]],
    ["2024-02-03", 7709, 7592, [2, 5, 9]],
    ["2024-02-01", 86015, 61520, [1, 5, 8]],
    ["2024-01-27", 10186, 20085, [3, 5, 6]],
    ["2024-01-25", 2344, 74455, [2, 4, 8]],
    ["2024-01-20", 56859, 84343, [2, 5, 9]],
    ["2024-01-18", 45849, 29536, [0, 5, 9]],
    ["2024-01-13", 43422, 31142, [0, 2, 9]],
    ["2024-01-11", 60859, 49296, [0, 4, 9]],
    ["2024-01-04", 80260, 57393, [0, 2, 9]]
]

# Insertar datos en la tabla de la Lotería Nacional
for fecha, primer_premio, segundo_premio, reintegros in datos_ln:
    cursor.execute("INSERT INTO LN (numero, fecha) VALUES (?, ?)", (primer_premio, fecha))
    cursor.execute("INSERT INTO LN (numero, fecha) VALUES (?, ?)", (segundo_premio, fecha))
    for reintegro in reintegros:
        cursor.execute("INSERT INTO reintegroLN (numero, posicion, fecha) VALUES (?, ?, ?)", (reintegro, reintegros.index(reintegro) + 1, fecha))

conexion.commit()
conexion.close()