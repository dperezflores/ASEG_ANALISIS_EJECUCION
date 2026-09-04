# Arquitectura de ASEG | Análisis de Ejecución

## Objetivo

Mantener una aplicación pequeña, modular y extensible sin introducir sobreingeniería. La estructura sigue principios de Clean Architecture / Ports and Adapters de forma ligera.

## Capas

### `domain/`
Contiene conceptos y modelos propios del negocio. No depende de Streamlit, Gemini, OpenAI, Neon ni de infraestructura externa.

Modelos actuales principales:
- Usuario e identidad externa.
- Obra/Contrato y su estado.
- Estimación, Factura, Comprobante de Pago y Póliza.

### `application/`
Contiene casos de uso y puertos (interfaces). Actualmente incluye:
- análisis documental;
- sincronización de usuarios;
- administración de obras;
- contratos para proveedores de IA;
- contratos para repositorios de prompts, usuarios y obras.

### `infrastructure/`
Implementa los puertos definidos por la aplicación. Actualmente contiene:
- Gemini;
- lectura de prompts desde archivos;
- autenticación OIDC de Streamlit/Google;
- conexión PostgreSQL;
- repositorios Neon de usuarios y obras.

### `presentation/`
Contiene exclusivamente la interfaz Streamlit. Incluye login, selección/registro de obras, sidebar, centro de análisis y resultados. No contiene SQL ni llamadas directas a Gemini.

### `reports/`
Generación y transformación determinista de reportes Excel.

### `resources/prompts/`
Prompts de auditoría como archivos independientes y versionables.

### `assets/`
Recursos visuales, incluido CSS específico de tablas.

### `config/`
Configuración general y acceso controlado a secretos o variables de entorno.

### `sql/`
Migraciones versionadas del esquema PostgreSQL/Neon.

## Composition Root

`composition.py` ensambla implementaciones concretas con los casos de uso. La presentación solicita servicios y no conoce cómo se construye Gemini ni cómo se conecta Neon.

## Paradigma

Se utiliza un enfoque híbrido:

- POO para servicios con dependencias y componentes intercambiables (`AnalysisService`, `DocumentAnalyzer`, `AuthService`, `WorkService`, proveedores y repositorios).
- Protocolos para inversión de dependencias (`AIProvider`, `PromptRepository`, `UserRepository`, `WorkRepository`).
- Funciones puras para generación de reportes y transformaciones deterministas.
- Streamlit queda limitado a presentación y estado temporal de sesión.

## Reglas de dependencia

Las dependencias deben apuntar hacia adentro:

`presentation -> composition -> application -> domain`

`infrastructure -> application/domain`

La capa `domain` no conoce ninguna tecnología externa.

## Seguridad multiusuario

Toda operación sobre una obra debe validar simultáneamente:
- `obra_id`;
- `usuario_id` autenticado.

La interfaz nunca se considera una frontera de seguridad suficiente. Los repositorios aplican la pertenencia del recurso en sus consultas.

Las API keys de IA y las credenciales OIDC/Neon no se almacenan en GitHub. Los secretos de infraestructura viven en Streamlit Secrets.

## Persistencia

La jerarquía objetivo es:

`Usuario -> Obra/Contrato -> Documento -> Resultado de análisis`

La fase actual implementa `Usuario -> Obra/Contrato`. La persistencia de documentos y resultados se añadirá en la siguiente etapa sin cambiar el motor de análisis existente.

## Evolución prevista

OpenAI se incorporará mediante una nueva implementación de `AIProvider`. La persistencia de documentos y resultados utilizará nuevos puertos en `application/ports/` e implementaciones Neon en `infrastructure/database/` sin introducir SQL en la presentación.
