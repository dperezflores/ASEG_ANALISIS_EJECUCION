# ASEG | Análisis de Ejecución

Aplicación independiente extraída del módulo de Ejecución de `aseg_auditor_IA`.

## Fase 1

Esta versión contiene exclusivamente:

- Estimaciones.
- Facturas.
- Comprobantes de pago.
- Pólizas (Devengo / Pago).
- Gemini como proveedor inicial.
- Esquemas estructurados con Pydantic.
- Reportes Excel con el orden institucional utilizado en el proyecto de origen.
- Interfaz Streamlit y estilo institucional base.

Esta fase **no comparte ejecución ni persistencia** con Auditor IA y no modifica el repositorio original.

## Seguridad

Las API keys no deben incorporarse al repositorio. La clave puede capturarse en la interfaz y vive únicamente durante la sesión. `.streamlit/secrets.toml` está excluido mediante `.gitignore`.

## Ejecución local

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Arquitectura prevista

La siguiente fase incorporará:

1. Inicio de sesión con Google mediante OIDC.
2. Neon PostgreSQL.
3. Usuarios y obras/contratos.
4. Persistencia de resultados por obra.
5. Recuperación de análisis en sesiones posteriores.
6. Proveedor OpenAI además de Gemini.
7. Aislamiento y pruebas de concurrencia para el equipo auditor.

Los PDF originales no se almacenarán inicialmente en Neon; se conservarán metadatos, huella SHA-256 y resultados estructurados.
