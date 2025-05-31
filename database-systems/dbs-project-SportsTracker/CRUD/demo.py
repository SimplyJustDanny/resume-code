import psycopg2


# pip install psycopg2-binary==2.9.9
# pip install Flask
# pip install flask-cours
pg_config = {
    'user' : 'dbsuer',
    'password' : 'pass',
    'host' : 'localhost',
    'port' : '8999'
}


url = "dbname = %s password=%s host=%s port=%s user=%s" % \
    (pg_config['database'],
     pg_config['password'],
     pg_config['host'],
     pg_config['port'],
     pg_config['user'])

# abre coneccion con el url
conn = psycopg2.connect(url)
# el cursor manda los query a la coneccion
cur = conn.cursor()
# se esribre query como se hacia en datagrip
query = "select pid, pname, pcolor, pmaterial, pweight, pprice from part;"
# manda a que el cursor ejecuta el query que esta en el parametro
cur.execute(query)
# ejecuta el query para cada row 
for row in cur:
    print(row)

# cierra el cursor, se deben cerrar los cursoser cuando ya se paren de usar para evitar errores
cur.close()

# cierra la coneccion con el url
# no hace falta cerrar la coneccion porque va estar corriendo en un servidor
# conn.close()