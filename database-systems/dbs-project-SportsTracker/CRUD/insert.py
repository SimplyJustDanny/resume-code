import psycopg2

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
pname ="piston"
pcolor = "gray"
pmaterial = "iron"
pweight = "weight"
pprice = "3.99"
query = "inset into part(pname, pcolor, pmaterial, pweight, pprice) values(%s,%s,%s,%s,%s)"
# manda a que el cursor ejecuta el query que esta en el parametro, el segundo parametro es el prepare statement; este previene los sql injection
cur.execute(query, (pname, pcolor, pmaterial, pweight, pprice))
# coge un row de la tabla
pid = cur.fetchone()[0]
# graba el record en el db; si esto no se hace no se vera ningun cambio en el db
conn.commit()
print("pid = ", pid)

# cierra el cursor, se deben cerrar los cursoser cuando ya se paren de usar para evitar errores
cur.close()

# cierra la coneccion con el url
# no hace falta cerrar la coneccion porque va estar corriendo en un servidor
# conn.close()