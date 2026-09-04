CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY,
    google_sub TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    nombre TEXT NOT NULL,
    picture_url TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ultimo_acceso_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_usuarios_email_lower
    ON usuarios (LOWER(email));

CREATE TABLE IF NOT EXISTS obras (
    id UUID PRIMARY KEY,
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre TEXT NOT NULL,
    numero_contrato TEXT,
    ente TEXT,
    contratista TEXT,
    ejercicio INTEGER CHECK (ejercicio IS NULL OR ejercicio BETWEEN 2000 AND 2100),
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'ACTIVA'
        CHECK (estado IN ('ACTIVA', 'ARCHIVADA')),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_obras_usuario_estado_actualizado
    ON obras (usuario_id, estado, actualizado_en DESC);
