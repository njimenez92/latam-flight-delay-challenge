
# 🚀 **Documentación Completa del Proyecto LATAM Flight Delay Challenge**

---
# 📚 **Índice**

1. 🚀 **Migración a Poetry y Pyenv**  
2. 🐍 **Resumen de Bugs Corregidos y Soluciones**  
   - 🐛 **Bug 1.1:** Incompatibilidad de NumPy 2.x  
   - 🐛 **Bug 1.2:** Error en sns.barplot con Datos de Aerolíneas  
   - 🐛 **Bug 1.3:** Error en sns.barplot con Datos por Día  
   - 🐛 **Bug 1.4:** Error en sns.barplot con Datos por Mes  
   - 🐛 **Bug 1.5:** Error en sns.barplot con Datos por Temporada Alta  
   - 🐛 **Bug 1.6:** Error en sns.barplot con Datos por Tipo de Vuelo  
   - 🐛 **Bug 1.7:** Error en sns.barplot con Datos por Periodo del Día  
   - 🐛 **Bug 1.8:** Error al Importar xgboost  
3. 🔍 **Análisis Detallado de la Exploración y Selección de Modelos**  
   - 🏢 **Distribución de Vuelos por Aerolínea**  
   - 📅 **Distribución de Vuelos por Día**  
   - 🗓️ **Distribución de Vuelos por Mes**  
   - 📆 **Distribución de Vuelos por Día de la Semana**  
   - 🛠️ **Generación de Características**  
4. 🤖 **Selección de Modelos**  
   - 📏 **Comparación de Resultados**  
   - 🥇 **Modelo Recomendado**  
5. 📑 **Configuración de CI (Integración Continua)**  
6. 🚀 **Configuración de CD (Despliegue Continuo)**  
7. 🧠 **API y Modelo de Machine Learning**  
8. ⚡ **Pruebas de Estrés**  
9. 🛠️ **Arquitectura de Despliegue**  
10. 📋 **Comandos Makefile Sugeridos**  
11. 🔄 **Flujo de Trabajo CI/CD**  
12. 🌍 **Acceder a los Servicios Desplegados**  
13. 📡 **Probar los Endpoints de la API**  
   - ✅ **Endpoint `/health`**  
   - 📊 **Endpoint `/predict`**
---
## 🚀 1. Migración a Poetry y Pyenv
La migración de Pip + Virtualenv a Poetry + Pyenv se justifica por:

* **Gestión Unificada de Dependencias:**

    * Un solo archivo (pyproject.toml) centraliza dependencias de producción, desarrollo y pruebas.
    * Bloqueo de versiones consistente con poetry.lock.

* **Manejo de Versiones de Python:**

    * Pyenv facilita el uso de versiones específicas de Python por proyecto.
    * Evita conflictos entre entornos.

* **Simplificación del Makefile:**

    * Comandos más claros y limpios usando poetry install y poetry run.
    * Eliminación de múltiples archivos requirements-*.txt.

* **Estándar Moderno:**

    * Poetry sigue el estándar PEP 518.
    * Mejor compatibilidad con CI/CD (GitHub Actions).

* **Escalabilidad y Reproducibilidad:**

    * Instalaciones más rápidas y consistentes entre entornos.
    * Facilita la colaboración y despliegue.



### 2. 🐍 Resumen de Bugs Corregidos y Soluciones
A continuación, se presenta un resumen de los errores corregidos relacionados con el uso de las bibliotecas **NumPy**, **Seaborn** y funciones personalizadas.

---

#### 🐛 Bug 2.1: Incompatibilidad de NumPy 2.x
**❗ Problema:**
Al importar librerías como pandas o módulos que dependen de NumPy, apareció un error debido a la incompatibilidad entre la API de **NumPy 1.x** y **2.x**.

**✅ Solución Aplicada:**
Se restringió NumPy a versiones anteriores a **2.x** en el archivo `pyproject.toml`:

```toml
[tool.poetry.dev-dependencies]
numpy = "<2"
```
Esto asegura la estabilidad y compatibilidad con otras dependencias.

---

#### 🐛 Bug 2.2: Error en sns.barplot con Datos de Aerolíneas
**❗ Problema:**
Al intentar graficar los vuelos por aerolínea usando `sns.barplot` con argumentos posicionales:

```python
sns.barplot(flights_by_airline.index, flights_by_airline.values, alpha=0.9)
```

Se generó un error indicando que `barplot()` no acepta más de un argumento posicional.

**✅ Solución Aplicada:**
Se reestructuraron los datos en un **DataFrame** y se especificaron los parámetros `x`, `y` y `data` explícitamente:

```python
sns.barplot(x='Airline', y='Flights', data=flights_by_airline, alpha=0.9)
```

---

#### 🐛 Bug 2.3: Error en sns.barplot con Datos por Día
**❗ Problema:**
Al graficar los vuelos por día con argumentos posicionales:

```python
sns.barplot(flights_by_day.index, flights_by_day.values, alpha=0.9)
```

Se generó el mismo error por el uso de argumentos posicionales.

**✅ Solución Aplicada:**
Se convirtió en un **DataFrame** y se usaron los parámetros explícitos:

```python
sns.barplot(x='Day', y='Flights', data=flights_by_day, alpha=0.9)
```

---

#### 🐛 Bug 2.4: Error en sns.barplot con Datos por Mes
**❗ Problema:**
Al graficar vuelos por mes con argumentos posicionales:

```python
sns.barplot(flights_by_month.index, flights_by_month.values, alpha=0.9)
```

Se generó un error debido al cambio en la API de **Seaborn**.

**✅ Solución Aplicada:**
Se creó un **DataFrame** y se usaron parámetros explícitos:

```python
sns.barplot(x='Month', y='Flights', data=flights_by_month, color='lightblue', alpha=0.8)
```

---

#### 🐛 Bug 2.5: Error en sns.barplot con Datos por Temporada Alta
**❗ Problema:**
Al graficar tasas de retraso por temporada alta con listas como argumentos:

```python
sns.barplot(["no", "yes"], high_season_rate['Tasa (%)'])
```

Se generó un error debido al uso de argumentos posicionales.

**✅ Solución Aplicada:**
Se convirtió en un **DataFrame** y se usaron parámetros explícitos:

```python
sns.barplot(x='High Season', y='Tasa (%)', data=high_season_rate, color='skyblue', alpha=0.75)
```

---

#### 🐛 Bug 2.6: Error en sns.barplot con Datos por Tipo de Vuelo
**❗ Problema:**
Al graficar las tasas de retraso por tipo de vuelo usando argumentos posicionales:

```python
sns.barplot(flight_type_rate.index, flight_type_rate['Tasa (%)'])
```

Se generó un error debido a la nueva sintaxis de **Seaborn**.

**✅ Solución Aplicada:**
Se utilizó un **DataFrame** con parámetros explícitos:

```python
sns.barplot(x='Flight Type', y='Tasa (%)', data=flight_type_rate, color='skyblue', alpha=0.75)
```

---

#### 🐛 Bug 2.7: Error en sns.barplot con Datos por Periodo del Día
**❗ Problema:**
Al intentar graficar tasas de retraso por periodo del día usando listas como argumentos posicionales:

```python
sns.barplot(period_day_rate_values, period_day_rate['Tasa (%)'])
```

Se generó un error por el uso incorrecto de los parámetros.

**✅ Solución Aplicada:**
Se corrigió creando un **DataFrame** y utilizando parámetros explícitos:

```python
sns.barplot(x='Period', y='Tasa (%)', data=period_day_rate, color='skyblue', alpha=0.75)
```

---

#### 🐛 Bug 2.8: Error al Importar xgboost
**❗ Problema:**
Al intentar importar XGBoost se presentó el siguiente error:

```python
ModuleNotFoundError: No module named 'xgboost'
```

**✅ Solución Aplicada:**
Se instaló XGBoost con Poetry:

```bash
poetry add xgboost
```

**Verificación:**

```python
import xgboost as xgb
print(xgb.__version__)
```

---

#### 🛠️ Explicación General de los Cambios

🔹 **Reestructuración de Datos:**
- Se usaron **DataFrames** en lugar de listas o series.

🔹 **Parámetros Explícitos en `sns.barplot`:**
- **`x`:** Define la columna del eje X.
- **`y`:** Define la columna del eje Y.
- **`data`:** Define el **DataFrame** fuente.

🔹 **Instalación de Dependencias:**
- Se utilizó **Poetry** para gestionar las dependencias.

🔹 **Mejoras Visuales:**
- Se ajustaron etiquetas: `plt.xticks(rotation=90)`
- Se ajustaron límites: `plt.ylim()`

🔹 **Compatibilidad con Nuevas Versiones:**
- Todas las soluciones son compatibles con **Seaborn 0.11.0+**.

---
## 3. 🔍 Análisis Detallado de la Exploración y Selección de Modelos para la Predicción de Retrasos en Vuelos ✈️


#### 3.1 🏢 Distribución de Vuelos por Aerolínea
Se realizó un análisis para determinar la cantidad de vuelos operados por cada aerolínea. Se utilizó un gráfico de barras donde se observó que unas pocas aerolíneas concentran la mayoría de los vuelos, mientras que otras tienen una participación mucho menor.

**🔑 Observaciones Clave:**
- **🏆 Aerolíneas Dominantes:** LATAM Airlines, Sky Airline y JetSmart concentran la mayor parte de los vuelos operados en el aeropuerto SCL.
- 🛫 Aerolíneas con baja frecuencia de vuelos, como American Airlines y Delta Airlines, tienen una participación marginal en comparación.
- ⚖️ Estas diferencias deben considerarse al ajustar los pesos en el modelo predictivo.

#### 3.2 📅 Distribución de Vuelos por Día
Se analizó la distribución diaria de los vuelos para identificar patrones específicos en días del mes.

**🔑 Observaciones Clave:**
- 📈 Se identifican días con picos de actividad, posiblemente relacionados con periodos de alta demanda, como fines de semana y festivos.
- 📉 Algunos días, especialmente a mitad de semana, tienen un número consistentemente bajo de vuelos.
- ⚠️ Estos patrones pueden indicar días críticos donde los retrasos son más frecuentes.

#### 3.3 🗓️ Distribución de Vuelos por Mes
Se realizó un análisis mensual para identificar tendencias estacionales.

**🔑 Observaciones Clave:**
- 🎄 Los meses de diciembre, enero y julio muestran un aumento significativo en el tráfico aéreo debido a vacaciones y festividades.
- 🍂 Los meses de abril y septiembre presentan una disminución relativa.
- 📊 Las tendencias estacionales son un factor clave a considerar en el modelo.

#### 3.4 📆 Distribución de Vuelos por Día de la Semana
Se evaluó la distribución semanal de los vuelos.

**🔑 Observaciones Clave:**
- 📅 Los viernes y lunes son los días con mayor actividad aérea.
- 🛬 Los fines de semana, en particular los domingos, presentan variabilidad en función de las aerolíneas.
- 📉 Los martes y miércoles suelen ser los días con menor actividad.

#### 🛠️ Generación de Características
Se crearon las siguientes columnas para mejorar la capacidad predictiva del modelo:
- **🌟 high_season:** Indica si el vuelo pertenece a una temporada alta.
- **⏱️ min_diff:** Diferencia en minutos entre la hora programada y la hora real del vuelo.
- **🌅 period_day:** Clasifica el vuelo en mañana, tarde o noche.
- **⚠️ delay:** Variable objetivo que indica si hubo un retraso mayor a 15 minutos.

Estas características resultaron ser relevantes para el análisis y modelado.

---
## 4. 🤖 Selección de Modelos

Se entrenaron y evaluaron dos modelos principales:
- **🚀 XGBoost**
- **📊 Logistic Regression**

#### 4.1 📏 Comparación de Resultados
Se evaluaron los modelos utilizando métricas clave:
- **✅ Precisión:** Indica la proporción de predicciones positivas correctas respecto al total de predicciones positivas realizadas por el modelo.
- **🔄 Recall:** Mide la capacidad del modelo para detectar todos los casos positivos reales. Es especialmente relevante en este caso, ya que perder un retraso importante puede tener consecuencias significativas.
- **⚖️ F1-Score:** Es la media armónica entre precisión y recall, proporcionando una métrica balanceada.
- **📈 ROC-AUC:** Representa la capacidad del modelo para distinguir entre clases positivas y negativas.

**🔑 Hallazgos Clave:**
1. ⚖️ No se encontraron diferencias significativas entre XGBoost y Logistic Regression en términos de rendimiento global.
2. 🔄 El equilibrio de clases mejoró el rendimiento, especialmente en la métrica de **Recall**, lo que sugiere que el modelo puede identificar mejor los vuelos retrasados.
3. 🛠️ La reducción de características a las 10 más importantes no afectó negativamente el rendimiento.
4. 🥇 **Recall** es la métrica más importante en este contexto, ya que es preferible capturar más vuelos retrasados aunque aumenten los falsos positivos.

#### 4.2 🥇 Modelo Recomendado
Se recomienda utilizar **🚀 XGBoost con balanceo de clases y reducción a las 10 características más importantes** debido a:
- ⚙️ Su capacidad para manejar datos tabulares.
- 🚀 Su eficiencia en entornos productivos.
- 📊 Su estabilidad en los resultados obtenidos.
- 🥇 Su rendimiento superior en términos de **Recall** y **F1-Score**.

#### Conclusiones Finales
- 📅 La temporada alta, el periodo del día y la diferencia en minutos son variables clave para la predicción de retrasos.
- 🌐 Se recomienda implementar el modelo **XGBoost** optimizado en una API para consultas en tiempo real.
- 📊 Se deben monitorear las métricas del modelo periódicamente para ajustes futuros.
- 🥇 **Recall** debe ser priorizado como la métrica principal para la evaluación continua del modelo.
---
## 📑 **5. Configuración de CI (Integración Continua)**

El archivo **ci.yml** automatiza los siguientes pasos cada vez que se realiza un *push* o un *pull request* en las ramas configuradas (**main**, **develop**, **feature/**, **release/** y **hotfix/**).

### 🔧 **Pasos Principales:**
1. **Checkout del código:** Descarga el código fuente.
2. **Configuración de Python:** Usa Python 3.11.
3. **Instalación de Dependencias:** Usa Poetry para gestionar dependencias.
4. **Linter:** Se ejecuta **flake8** para analizar la calidad del código.
5. **Pruebas Unitarias:** Se ejecutan los siguientes comandos:
   - `make model-test`
   - `make api-test`
   - `make utils-test`
6. **Reporte de Cobertura:** Se genera un informe usando `pytest --cov`.

📄 **Archivo ci.yml:** `ci.yml`

---

## 🚀 **6. Configuración de CD (Despliegue Continuo)**

El archivo **cd.yml** realiza el despliegue del modelo y la API en **Google Cloud Run** utilizando Docker.

### 🔧 **Pasos Principales:**
1. **Checkout del código:** Descarga el repositorio.
2. **Instalación de Dependencias:** Usa Poetry para instalar dependencias sin las de desarrollo.
3. **Autenticación en Google Cloud:** Se utiliza `google-github-actions/auth`.
4. **Construcción de Imagen Docker:** Se construye y etiqueta la imagen Docker.
5. **Empuje de Imagen Docker:** Se sube la imagen al Artifact Registry de GCP.
6. **Despliegue en Cloud Run:** Dependiendo de la rama (`main`, `develop`, `release/**`), se selecciona el entorno:
   - **Producción:** `latam-flight-delay-challenge-prod`
   - **Staging:** `latam-flight-delay-challenge-staging`

📄 **Archivo cd.yml:** `cd.yml`

---

## 🧠 **7. API y Modelo de Machine Learning**

### 🌐 **API con FastAPI:**
- **Endpoint `/predict`:** Permite realizar predicciones.
- **Endpoint `/health`:** Verifica el estado de la API.

📄 **Código de la API:** `api.py`

---

## ⚡ **8. Pruebas de Estrés**

Se utilizó **Locust** para simular múltiples usuarios consultando la API de predicción.

### 🔧 **Configuración:**
- **Escenario:** Simulación de múltiples peticiones concurrentes al endpoint `/predict`.
- **Parámetros:** Número de usuarios, tasa de crecimiento, tiempo de prueba.

📄 **Reporte de Pruebas de Estrés:** `stress-test.html`

---

## 🛠️ **9. Arquitectura de Despliegue**

```scss
┌────────────────────┐
│    GitHub Repo     │
│  (Public, main y   │
│  ramas de feature) │
└────────────────────┘
          │
          │ 1) Push/PR
          ▼
┌───────────────────────────┐
│       GitHub Actions      │  <-- CI/CD (ci.yml y cd.yml)
│  (Integración Continua y  │
│   Despliegue Continuo)    │
└───────────────────────────┘
          │
          │ 2) Test (CI)
          │    - make model-test
          │    - make api-test
          │    - Linter & QA
          │
          └───────► OK?
                    │
                    │ 3) Build & Deploy (CD)
                    │
                    ▼
             ┌─────────────────┐
             │   Docker Image  │
             │(Contenedor con  │
             │  model.py y     │
             │  api.py dentro) │
             └─────────────────┘
                    │
                    │ 4) Deploy
                    ▼
        ┌───────────────────────────┐
        │        Cloud Run         │
        │    (o tu servicio de     │
        │     preferencia en GCP)  │
        └───────────────────────────┘
                    │
                    │ 5) API URL
                    ▼
         ┌────────────────────────┐
         │   API (FastAPI)       │
         │   Endpoint de /predict │
         │   Endpoint de /health  │
         └────────────────────────┘
                    │
                    │ 6) make stress-test (Local/Remoto)
                    ▼
            ┌───────────────────┐
            │   Usuarios/DS    │
            │   consumen la     │
            │   predicción de   │
            │   demoras         │
            └───────────────────┘

```

---

## 📋 **10. Comandos Makefile Sugeridos**

```makefile
install:
	poetry install

model-test:
	poetry run pytest tests/model

api-test:
	poetry run pytest tests/api

utils-test:
	poetry run pytest tests/utils

stress-test:
	locust -f tests/stress/api_stress.py --host=https://api-url
```

---

## 🔄 **11. Flujo de Trabajo CI/CD**

### 🛠️ **Integración Continua (CI)**
1. **Push/PR a ramas específicas.**
2. **Ejecución de pruebas:**
   - `make model-test`
   - `make api-test`
   - `make utils-test`
3. **Linter:** flake8 analiza el código.
4. **Generación de reportes de cobertura.**

### 🚀 **Despliegue Continuo (CD)**
1. **Autenticación en Google Cloud.**
2. **Construcción de Imagen Docker.**
3. **Empuje a Artifact Registry.**
4. **Despliegue en Cloud Run.**

---

## 🌍 **12. Acceder a los Servicios Desplegados**

- **Staging:** [https://latam-flight-delay-challenge-staging-591005290668.us-central1.run.app](https://latam-flight-delay-challenge-staging-591005290668.us-central1.run.app)  
- **Producción:** [https://latam-flight-delay-challenge-prod-591005290668.us-central1.run.app](https://latam-flight-delay-challenge-prod-591005290668.us-central1.run.app)

---

## 📡 **13. Probar los Endpoints de la API**

### ✅ **Endpoint `/health`**
- **Descripción:** Verifica si la API está activa.
- **Método:** `GET`
- **Ejemplo de Respuesta:**  
```json
{
  "status": "OK",
  "detail": "your request was received"
}
```

### 📊 **Endpoint `/predict`**
- **Descripción:** Realiza predicciones basadas en los datos de entrada.
- **Método:** `POST`
- **Cuerpo de la Solicitud:**  
```json
{
  "flights": [
    {
      "OPERA": "Aerolineas Argentinas",
      "TIPOVUELO": "N",
      "MES": 3
    }
  ]
}
```
- **Respuesta Esperada:**  
```json
{
  "predict": [0]
}
```

---
