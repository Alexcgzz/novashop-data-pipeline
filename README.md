# NovaShop - Data Pipeline

Pipeline de datos de punta a punta para una tienda en linea mexicana ficticia.

## Problema
Debido al alto crecimiento del negocio y por ende de los datos, estos estan dispersos por varios sistemas y vienen sucios.

## Objetivo del negocio
El objetivo sera la conclusion y visualizacion leve de los datos, mediante tablas y respuestas a las siguientes preguntas:

1. **Ingresos**: ¿cuánto vendemos por mes y por categoría de producto? ¿Vamos creciendo?
2. **Productos top**: ¿cuáles son los productos y categorías que más venden (en ingreso y en unidades)?
3. **Rentabilidad**: ¿qué categorías nos dejan más margen? (tenemos precio y costo de cada producto)
4. **Clientes**: ¿cuál es nuestro ticket promedio por pedido? ¿qué % de clientes nos vuelven a comprar vs los que compran una sola vez?
5. **Canal de adquisición**: ¿de qué canal (Google, Facebook, orgánico, referidos...) vienen los clientes que más gastan?
Devoluciones/cancelaciones: ¿qué % de pedidos se cancelan o devuelven, y cuánto ingreso representa eso?

## Arquitectura

```mermaid
flowchart LR
    A[CSV crudos | ~45K registros] --> B[pandas | Limpiezas y modelado]
    B --> C[Parquet | Tipado y comprimido]
    C --> D[AWS S3 | data lake]
    D --> E[AWS Athena | SQL]
    E --> F[5 Insights de negocio]
```

## Stack
Python | Pandas | SQL | AWS S3 | AWS Athena | Git
