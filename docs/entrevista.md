# Cómo explicar el proyecto en una entrevista

## Presentación de 45 segundos
«He preparado un proyecto de portfolio con datos sintéticos que reproduce un problema de mi ámbito:
convertir posiciones, precios y divisas en reporting financiero fiable. Uso SQL y dbt para transformar
y documentar los datos, concilio los resultados con una fuente de referencia y genero excepciones de riesgo.
Además de comprobar el caso correcto, introduzco duplicados, un FX ausente y una referencia desconocida
para demostrar que las pruebas bloquean resultados incorrectos. Lo ejecuto localmente con DuckDB y he
definido un workflow de GitHub Actions para validar los cambios.»

Di que has ejecutado/modificado el proyecto cuando lo hayas hecho. No presentes este código como
un sistema de CaixaBank, una implementación productiva o experiencia en Snowflake.

## Preguntas que debes poder responder
1. ¿Cuál es la granularidad de cada tabla y cómo evitas duplicar una valoración al hacer joins?
2. ¿Por qué un LEFT JOIN es más seguro que perder posiciones con un INNER JOIN?
3. ¿Cómo conviertes USD a EUR? ¿Qué significa la dirección del FX?
4. ¿Por qué usas DECIMAL y redondeas tras agregar?
5. ¿Por qué un descuadre de conciliación no hace fallar necesariamente el pipeline?
6. ¿Qué prueba detecta cada uno de los tres fallos introducidos?
7. ¿Qué se revisa en el PR y qué hace realmente el CI?
8. ¿Qué cambiarías para trabajar con Snowflake y millones de registros?

## Mapeo con Affirm
- Modelos y datasets → staging, valoración y marts dbt.
- Reliability → pruebas, casos negativos, bloqueo de publicación y alertas locales.
- Pipelines/lineage → ref(), documentación dbt, contratos de granularidad y runbook.
- Incidencias → simulación, identificación del test y solución de la causa.
- Stakeholders → requisitos/tolerancias/documentación del control.
- GitHub workflows → pipeline CI y plantilla PR; demuestra un PR real tras publicar.
- Python/BI → exports y reporte HTML. No se atribuye experiencia Power BI a este código.
- Accounting/Snowflake → áreas por ampliar; valoración de carteras no es libro mayor contable.

## Primera mejora personal
Ejecuta el proyecto, modifica un dato sintético, investiga qué cambia y escribe tus conclusiones.
Después crea una rama y añade un control pequeño con prueba. Este cambio propio será evidencia
mucho más convincente que limitarte a subir el ZIP generado.
