## Tecnologías Utilizadas

Lista las principales tecnologías y librerías utilizadas:

* Python
* Django
* Django REST Framework (DRF)
* django-filter (Para filtrado)
* reportlab (Para generación de PDF - o la librería que uses)
* (Otras librerías importantes que hayas añadido)

## Configuración e Instalación

Instrucciones paso a paso para configurar el proyecto localmente.

1.  **Clonar el Repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO_BACKEND>
    cd <nombre_de_la_carpeta_del_backend>
    ```

2.  **Crear y Activar Entorno Virtual:**

    Es altamente recomendado usar un entorno virtual.

    * Linux/macOS:
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```
    * Windows (CMD):
        ```bash
        python -m venv venv
        venv\Scripts\activate.bat
        ```
    * Windows (PowerShell):
        ```bash
        python -m venv venv
        venv\Scripts\Activate.ps1
        ```

3.  **Instalar Dependencias:**

    Con el entorno virtual activado, instala las librerías necesarias desde el archivo `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno:**

    Crea un archivo `.env` en la raíz del proyecto backend (si no existe) para las variables de configuración sensibles y específicas del entorno. Este archivo NO está incluido en el repositorio por seguridad (ver `.gitignore`).

    Puedes basarte en un archivo de ejemplo (si lo proporcionas) o listar aquí las variables mínimas necesarias:

    ```
    # Ejemplo de contenido para .env
    SECRET_KEY='<tu_clave_secreta>' # Cambia esto por una clave única y segura
    DEBUG=True # O False para producción
    DATABASE_URL='sqlite:///db.sqlite3' # O la URL de tu base de datos (PostgreSQL, etc.)
    # Otras variables de configuración...
    ```
    Asegúrate de que `SECRET_KEY` sea única y secreta. Para bases de datos diferentes a SQLite, necesitarás configurar la conexión en `settings.py` y las variables correspondientes aquí.

5.  **Aplicar Migraciones de Base de Datos:**

    Configura la base de datos aplicando las migraciones.

    ```bash
    python manage.py migrate
    ```

6.  **(Opcional) Crear Superusuario:**

    Si necesitas acceder al panel de administración de Django:

    ```bash
    python manage.py createsuperuser
    ```
    Sigue las instrucciones en pantalla.

7.  **Iniciar el Servidor de Desarrollo:**

    ```bash
    python manage.py runserver
    ```
    El backend estará disponible en `http://127.0.0.1:8000/` por defecto. La API RESTful estará bajo el prefijo `/api/`.
