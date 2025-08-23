# 📚 Proyecto Django Empresarial

Una aplicación web moderna en Django con una estructura limpia y organizada.

## 📋 Descripción General

Este proyecto sigue una estructura personalizada:
- `src/`: Directorio principal del código
  - `config/`: Configuración del proyecto
  - `core/`: Aplicación principal
- `venv/`: Entorno virtual (no incluido en git)

## ✨ Características

- 📱 Estructura limpia y organizada con Django 5
- 🛠️ Separación de configuración y código de aplicación
- 📦 Listo para usar con frameworks frontend
- 🔒 Interfaz de administración para gestión de contenido

## 🔧 Instalación


1. Clona este repositorio
2. Crea un entorno virtual:
   ```bash
   python3 -m venv venv
   ```

3. Activa el entorno virtual:
   - **En Linux/MacOS:**
     ```bash
     source venv/bin/activate
     ```
   - **En Windows (CMD):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **En Windows (PowerShell):**
     ```powershell
     venv\Scripts\Activate.ps1
     ```

3. Instala las dependencias:
   ```bash
   cd src
   pip install -r requirements.txt
   ```

4. Aplica las migraciones:
   ```bash
   python3 manage.py migrate
   ```

5. Crea un superusuario:
   ```bash
   python3 manage.py createsuperuser
   ```

## 🚀 Ejecución del Proyecto

```bash
cd src
python3 manage.py runserver
```

Accede al sitio en http://127.0.0.1:8000/ y al admin en http://127.0.0.1:8000/admin/

## 🛠️ Desarrollo

- Agrega modelos en `core/models.py`
- Crea vistas en `core/views.py`
- Añade rutas en `core/urls.py`
- Crea plantillas en `core/templates/`

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 👥 Integrantes

- Bautista Aguilera Jefferson
- Medina Mallqui Ailyn
- Moya Condori Maria Fernanda
- Toledo La Fuente Luis Miguel
