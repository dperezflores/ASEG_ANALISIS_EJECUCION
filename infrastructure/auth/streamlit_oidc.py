from __future__ import annotations

from domain.users import UserIdentity


def identity_from_streamlit_user(user) -> UserIdentity:
    subject = str(getattr(user, "sub", "") or "").strip()
    email = str(getattr(user, "email", "") or "").strip()
    name = str(getattr(user, "name", "") or email or "Usuario").strip()
    picture = str(getattr(user, "picture", "") or "").strip() or None

    if not subject:
        raise ValueError("Google no devolvió un identificador OIDC válido (sub).")
    if not email:
        raise ValueError("Google no devolvió el correo electrónico del usuario.")

    return UserIdentity(
        subject=subject,
        email=email,
        name=name,
        picture_url=picture,
    )
