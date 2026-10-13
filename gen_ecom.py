import csv, random, os
from datetime import date, timedelta
from faker import Faker

fake = Faker('es_MX')
Faker.seed(11); random.seed(11)

OUT = '/home/claude/ecom_out'
os.makedirs(OUT, exist_ok=True)

N_CUST, N_PROD, N_ORDERS = 4000, 300, 15000

estados = ['Nuevo León','CDMX','Jalisco','Puebla','Yucatán','Coahuila',
           'Guanajuato','Querétaro','Baja California','Sonora']

cat_variants = {
    'Electrónica': ['Electrónica','electronica','ELECTRÓNICA','Electronica'],
    'Hogar':       ['Hogar','hogar','HOGAR','Casa'],
    'Ropa':        ['Ropa','ropa','ROPA','Moda'],
    'Deportes':    ['Deportes','deportes','DEPORTES','Deporte'],
    'Juguetes':    ['Juguetes','juguetes','JUGUETES','Juguetería'],
    'Belleza':     ['Belleza','belleza','BELLEZA','Cuidado Personal'],
}
canal_adq_variants = {
    'Google Ads':['Google Ads','google ads','Google','SEM'],
    'Facebook':  ['Facebook','facebook','FB','Meta'],
    'Instagram': ['Instagram','instagram','IG'],
    'Orgánico':  ['Orgánico','organico','ORGANICO','Búsqueda orgánica'],
    'Referido':  ['Referido','referido','Referral','Recomendación'],
}
estatus_variants = {
    'Completado':['Completado','completado','COMPLETE','Entregado'],
    'Cancelado': ['Cancelado','cancelado','CANCELLED','cancelada'],
    'Devuelto':  ['Devuelto','devuelto','RETURNED','devolución'],
    'Pendiente': ['Pendiente','pendiente','PENDING','en proceso'],
}
canal_variants = {'web':['web','Web','WEB','sitio web'],'app':['app','App','APP','aplicación']}
pago_variants = ['Tarjeta','TARJETA','PayPal','paypal','Transferencia','OXXO','oxxo','']

tipos = {
    'Electrónica':['Audífonos','Bocina','Smartwatch','Cargador','Cámara','Tablet','Mouse','Teclado'],
    'Hogar':['Licuadora','Sartén','Juego de Sábanas','Lámpara','Cafetera','Organizador'],
    'Ropa':['Playera','Jeans','Sudadera','Chamarra','Tenis','Gorra'],
    'Deportes':['Balón','Mancuernas','Tapete de Yoga','Botella Térmica','Guantes'],
    'Juguetes':['Rompecabezas','Set de Bloques','Muñeca','Carro de Control','Peluche'],
    'Belleza':['Shampoo','Crema Facial','Perfume','Set de Maquillaje','Secadora'],
}
marcas = ['Nova','Zentro','Aimex','BrightLine','Kairo','Lumen','Vortex','Celestia']
precio_rango = {'Electrónica':(300,9000),'Hogar':(200,4000),'Ropa':(150,2000),
                'Deportes':(100,3000),'Juguetes':(80,1500),'Belleza':(90,1800)}

def maybe_null(v,p=0.07): return '' if random.random()<p else v
def rand_date(y0,y1):
    s,e=date(y0,1,1),date(y1,10,1); return s+timedelta(days=random.randint(0,(e-s).days))
def fmt(d): return d.strftime(random.choice(['%Y-%m-%d','%d/%m/%Y','%m-%d-%Y']))
def w(name,header,rows):
    with open(os.path.join(OUT,name),'w',newline='',encoding='utf-8') as f:
        wr=csv.writer(f); wr.writerow(header); wr.writerows(rows)
    print(f'{name}: {len(rows)} filas')

# CUSTOMERS
customers=[]
for i in range(1,N_CUST+1):
    ac=random.choice(list(canal_adq_variants))
    city=fake.city(); city=random.choice([city,city.lower(),city.upper(),' '+city+' '])
    customers.append([f'C{i:05d}',fake.name(),maybe_null(fake.email(),0.05),
        fmt(rand_date(2023,2026)),city,random.choice(estados),
        random.choice(canal_adq_variants[ac])])
for _ in range(30): customers.append(list(random.choice(customers)))  # duplicados
w('customers.csv',['customer_id','nombre','email','fecha_registro','ciudad','estado','canal_adquisicion'],customers)

# PRODUCTS
products=[]
for i in range(1,N_PROD+1):
    cat=random.choice(list(cat_variants))
    lo,hi=precio_rango[cat]; precio=round(random.uniform(lo,hi),2)
    if random.random()<0.01: precio=-precio
    if random.random()<0.02: precio=''
    costo = round(precio*random.uniform(0.4,0.7),2) if precio not in ('',) and precio>0 else ''
    costo = maybe_null(costo,0.05)
    products.append([f'P{i:04d}',f'{random.choice(marcas)} {random.choice(tipos[cat])}',
        random.choice(cat_variants[cat]),random.choice(marcas),precio,costo])
w('products.csv',['product_id','nombre','categoria','marca','precio','costo'],products)

# ORDERS
cust_ids=[c[0] for c in customers]
orders=[]
for i in range(1,N_ORDERS+1):
    sc=random.choices(['Completado','Pendiente','Cancelado','Devuelto'],weights=[0.72,0.1,0.1,0.08])[0]
    cc=random.choice(list(canal_variants))
    orders.append([f'O{i:06d}',random.choice(cust_ids),fmt(rand_date(2024,2026)),
        random.choice(estatus_variants[sc]),random.choice(canal_variants[cc]),
        random.choice(pago_variants)])
w('orders.csv',['order_id','customer_id','fecha_pedido','estatus','canal','metodo_pago'],orders)

# ORDER ITEMS
prod_list=[(p[0], p[4]) for p in products]  # (id, precio)
items=[]; seq=1
for o in orders:
    for _ in range(random.randint(1,5)):
        pid,precio=random.choice(prod_list)
        try: base=float(precio)
        except: base=random.uniform(100,2000)
        base=abs(base) if base else random.uniform(100,2000)
        pu=round(base*random.uniform(0.9,1.0),2)  # precio al momento (con descuentillo)
        items.append([f'IT{seq:07d}',o[0],pid,random.randint(1,4),pu]); seq+=1
w('order_items.csv',['item_id','order_id','product_id','cantidad','precio_unitario'],items)
print('\nListo.')
