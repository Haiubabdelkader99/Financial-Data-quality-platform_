# Tu primer proyecto en GitHub — paso a paso

## 1. Qué estás montando
`financial-data-quality-platform`: un pipeline de datos financieros con SQL, dbt y Python.
Simula tres carteras durante dos días. Valora posiciones en EUR, concilia con un custodio ficticio
y revisa concentración por instrumento. Incluye casos correctos, descuadres y pruebas que detectan errores.
Los nombres y datos son inventados. No necesitas ningún fichero del trabajo ni una cuenta cloud.

El README está en inglés para reclutadores; esta guía y la preparación de entrevista están en español.

## 2. Descarga y descomprime
Descomprime el ZIP. Entra en la carpeta `financial-data-quality-platform`.
Debes ver `README.md`, `requirements.txt`, `dbt_project.yml`, `models`, `scripts` y `seeds`.
El informe de ejemplo está en `examples/report.html`: puedes abrirlo antes de instalar nada.

## 3. Instala Python y abre una terminal
Necesitas Python 3.12: https://www.python.org/downloads/
En Windows marca «Add Python to PATH» durante la instalación.
Abre la carpeta del proyecto en VS Code: https://code.visualstudio.com/
Ve a Terminal → New Terminal. Si utilizas otro editor, abre PowerShell en la misma carpeta.

Comprueba:
```powershell
py -3.12 --version
```
Si `py` no existe pero `python --version` muestra 3.12, usa `python` en su lugar.

## 4. Prepara el entorno en Windows
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
Si PowerShell bloquea la activación, no necesitas cambiar la política del ordenador. Ejecuta directamente:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:Path = "$PWD\.venv\Scripts;" + $env:Path
.\.venv\Scripts\python.exe scripts/run_pipeline.py
.\.venv\Scripts\python.exe scripts/verify_demo.py
.\.venv\Scripts\python.exe scripts/failure_drill.py
```
El cambio de Path solo afecta a esa terminal y permite al runner encontrar `dbt`.

## 5. Ejecútalo (si has activado el entorno)
```powershell
python scripts/run_pipeline.py
python scripts/verify_demo.py
python scripts/failure_drill.py
Start-Process outputs/report.html
```
El primer comando carga CSV, construye y prueba modelos, genera documentación y exporta informes.
El segundo confirma los valores esperados. El tercero verifica tres defectos en copias temporales.
Al acabar tendrás `outputs/report.html`, tres CSV y `alerts.json`.

Resultados esperados: 18 posiciones, 6 carteras-fecha, 1 descuadre de EUR 50 y 4 excesos de concentración.
Es normal ver excepciones de negocio: están incluidas para demostrar el proceso de revisión.

Para documentación interactiva:
```powershell
dbt docs serve --profiles-dir .
```
Abre la dirección local que aparezca. Para pararlo: Ctrl+C.

macOS/Linux: sigue los comandos del README.

## 6. Crea el repositorio en GitHub
Tu captura muestra el usuario `Haiubabdelkader99`.
1. En GitHub pulsa **+ → New repository**.
2. Nombre: **financial-data-quality-platform**.
3. Descripción: **Tested financial data pipelines with dbt, SQL and Python: valuation, reconciliation and risk controls.**
4. Selecciona **Public** para que lo puedan revisar los reclutadores.
5. Si vas a subir por Git, no inicialices README, licencia ni .gitignore: ya están incluidos.
6. Pulsa **Create repository**.

### Opción recomendada: Git (conserva carpetas y CI)
Instala Git si hace falta: https://git-scm.com/downloads
Abre una terminal nueva en la carpeta del proyecto y ejecuta:
```powershell
git init
git branch -M main
git add .
git status
git commit -m "Add tested financial data quality platform"
git remote add origin https://github.com/Haiubabdelkader99/financial-data-quality-platform.git
git push -u origin main
```
Si Git pide identidad, establece tu nombre y el email que quieras asociar al commit
(puedes usar el email privado noreply que muestra GitHub en Settings → Emails):
```powershell
git config user.name "Haiub Abdelkader Mohamed"
git config user.email "TU_EMAIL_DE_COMMIT"
```
Vuelve a ejecutar el commit y el push. Sigue el inicio de sesión que te ofrezca Git;
no escribas tu contraseña ni tokens en los archivos del proyecto.

Antes del commit comprueba con `git status` que no se incluyen `.venv`, `outputs`, `target`, `logs` ni la base de datos.
La carpeta `examples` sí se incluye: contiene resultados sintéticos para que el reclutador vea la salida.

### Alternativa: subir desde la web
Usa «uploading an existing file» / Add file → Upload files y arrastra el contenido del proyecto descomprimido.
No subas el ZIP como único archivo: el código debe quedar visible en carpetas.
Comprueba que se ha subido `.github/workflows/ci.yml`; algunos selectores ocultan carpetas con punto.
Si falta, créalo con Add file → Create new file y pega el contenido usando esa ruta como nombre.
Si has ejecutado localmente, NO arrastres `.venv`, `target`, `logs`, `outputs` ni `finance.duckdb`.

## 7. Comprueba GitHub Actions
Entra en la pestaña **Actions**. Tras el push a main debe arrancar «Financial data quality».
Espera a que termine y revisa los pasos y el artefacto `financial-data-evidence`.
El workflow está validado localmente en cuanto a comandos; su primera ejecución real en GitHub
solo ocurrirá cuando publiques. Una cuenta nueva puede pedir habilitar Actions.

## 8. Haz tu primera mejora con un PR
1. Entiende los modelos leyendo `docs/architecture.md` y ejecutando los ejemplos.
2. Crea una rama: `git switch -c feature/my-first-control`.
3. Añade o mejora un control y documenta su motivo. Ejecuta todas las comprobaciones.
4. Haz commit y push: `git push -u origin feature/my-first-control`.
5. En GitHub pulsa Compare & pull request; completa la plantilla y revisa Actions.
6. Explica qué aprendiste en el README antes de fusionar.

## 9. Presentación en tu perfil y CV
Fija el repositorio en tu perfil con «Customize your pins».
Bio sugerida: **Financial Data & Analytics | Risk Controls | SQL · dbt · Python | Asset Management**.
Cuando el repositorio sea público y pase CI, enlázalo en el CV.
Perfil: https://github.com/Haiubabdelkader99
Repositorio previsto: https://github.com/Haiubabdelkader99/financial-data-quality-platform
Estas URLs corresponden al usuario visible y al nombre propuesto; este paquete no crea ni publica el repositorio.

No presentes el proyecto como experiencia productiva ni como trabajo de CaixaBank.
Explica la asistencia de IA con naturalidad y demuestra que has revisado, ejecutado y mejorado el código.
