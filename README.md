
# 📁 Conexión a OneDrive Empresarial con Microsoft Graph API (Como usuario)

Este proyecto permite conectarse a OneDrive (cuenta empresarial), acceder a carpetas compartidas (como `datacampus`), y realizar operaciones básicas con archivos como crear, leer y eliminar archivos Excel mediante Microsoft Graph API y autenticación con `msal` en Python.

## ✅ Requisitos

- Cuenta de Microsoft con permisos sobre los recursos de OneDrive.
- Cliente registrado en [Azure Portal](https://portal.azure.com/).
- Permisos delegados:
  - `Files.ReadWrite.All`
  - `Sites.ReadWrite.All`
  - `User.Read`
- Python 3.8 o superior
- Librerías:
  - `requests`
  - `msal`
  - `pandas`
  - `openpyxl`
  - `python-dotenv`

## 🧠 Arquitectura

```
main.py ─────► OD_manager.py
              └─ Autenticación
              └─ Navegación entre carpetas
              └─ Creación/lectura/borrado de archivos
```

---

## ⚙️ Configuración Inicial

1. Crea un archivo `.env` con las siguientes variables:

```env
TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

2. Instala las dependencias:

```bash
pip install msal requests pandas openpyxl python-dotenv
```

---

## 🚀 ¿Qué hace este proyecto?

### 1. Autenticación con Microsoft

Se usa `msal` con flujo `device_code` para iniciar sesión desde navegador. Esto evita necesitar permisos de administrador global.

```python
token = autenticar()
```

### 2. Acceso a carpetas compartidas

Se lista el contenido compartido con el usuario y se localiza la carpeta `datacampus`:

```python
drive_id, root_id = encontrar_carpeta_datacampus(token)
```

### 3. Buscar subcarpeta `Documentos`

```python
documentos_id = buscar_subcarpeta(token, drive_id, root_id, "Documentos")
```

### 4. Crear un archivo Excel

```python
crear_excel_en_carpeta(token, drive_id, documentos_id, "test.xlsx")
```

Se guarda un `DataFrame` de ejemplo en memoria y se sube como archivo Excel.

### 5. Leer archivos Excel existentes

```python
df = descargar_y_convertir_excel(token, drive_id, archivo_id, archivo_nombre)
```

### 6. Eliminar un archivo

```python
eliminar_archivo(token, drive_id, archivo_id)
```

---

## 🧪 Comandos disponibles (`main.py`)

Al ejecutar:

```bash
python main.py
```

Se muestran 2 opciones:

- `2`: Crear y opcionalmente eliminar un archivo `test.xlsx`.
- `3`: Leer todos los archivos `.xlsx` en la carpeta `Documentos`.

---

## 🧩 Escalabilidad

Este sistema está pensado para proyectos futuros donde se necesite automatizar la interacción con archivos de OneDrive:

- Centralización de reportes en carpetas compartidas.
- Extracción de datos empresariales desde Excel.
- Automatización de flujos de lectura/escritura en equipo.

---

## 🛡️ Seguridad

- No se almacenan tokens de acceso.
- Se usa flujo de autenticación delegado.
- Toda autenticación requiere acción del usuario y se revoca automáticamente tras el cierre de sesión o expiración del token.

---


