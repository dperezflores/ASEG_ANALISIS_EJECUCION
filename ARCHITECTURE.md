# Arquitectura de ASEG | Análisis de Ejecución

## Objetivo

Mantener una aplicación pequeña, modular y extensible sin introducir sobreingeniería. La estructura sigue principios de Clean Architecture / Ports and Adapters de forma ligera.

## Capas

### `domain/`
Contiene conceptos y modelos propios del negocio. No debe depender de Streamlit, Gemini, OpenAI, Neon ni de infraestructura externa.

### `application/`
Contiene los casos de uso y los puertos (interfaces) que necesita la aplicación. Aquí viven el analizador documental, el servicio de análisis y los contratos para proveedores de IA y repositorios de prompts.

### `infrastructure/`
Implementa los puertos definidos por la capa de aplicación. Actualmente contiene Gemini y la lectura de prompts desde archivos. Posteriormente alojará OpenAI, Neon y otros servicios externos.

### `presentation/`
Contiene exclusivamente la interfaz Streamlit y sus componentes. No debe implementar reglas de extracción ni llamadas directas a proveedores externos.

### `reports/`
Contiene generación y transformación de reportes Excel. Se mantiene separada porque son transformaciones deterministas e independientes del proveedor de IA.

### `resources/prompts/`
Contiene los prompts de auditoría como archivos independientes y versionables. Modificar un prompt no requiere modificar código Python.

### `assets/`
Contiene recursos visuales, como CSS específico de tablas.

### `config/`
Centraliza configuración general y acceso controlado a secretos o variables de entorno.

## Composition Root

`composition.py` es el único punto encargado de ensamblar implementaciones concretas con los casos de uso. La presentación solicita un `AnalysisService` sin conocer cómo se construye Gemini ni cómo se cargan los prompts.

## Paradigma

Se utiliza un enfoque híbrido:

- POO para servicios con dependencias y componentes intercambiables (`AnalysisService`, `DocumentAnalyzer`, proveedores y repositorios).
- Protocolos para inversión de dependencias (`AIProvider`, `PromptRepository`).
- Funciones puras para generación de reportes y transformaciones deterministas.
- Streamlit queda limitado a la capa de presentación y sesión temporal.

## Reglas de dependencia

Las dependencias deben apuntar hacia adentro:

`presentation -> composition -> application -> domain`

`infrastructure -> application/domain`

La capa `domain` no conoce ninguna tecnología externa.

## Evolución prevista

La incorporación de OpenAI se realizará mediante una nueva implementación de `AIProvider`. Neon se incorporará mediante puertos de repositorio en `application/ports/` e implementaciones concretas en `infrastructure/database/`, sin introducir SQL en la presentación.
