from sqlmodel import Session


class BaseRepository:
    """
    Repositorio base seguro con soporte para transacciones atómicas.
    - commit=True: Para operaciones de un solo paso (guarda de inmediato).
    - commit=False: Para operaciones de múltiples pasos (se confirma al final en el servicio).
    """

    @staticmethod
    def guardar(db: Session, objeto, commit: bool = True):
        db.add(objeto)
        if commit:
            db.commit()
            db.refresh(objeto)
        else:
            db.flush()  # Valida y asigna el ID primario sin cerrar la transacción
        return objeto

    @staticmethod
    def actualizar(db: Session, objeto, commit: bool = True):
        db.add(objeto)
        if commit:
            db.commit()
            db.refresh(objeto)
        else:
            db.flush()
        return objeto

    @staticmethod
    def eliminar_logico(db: Session, objeto, commit: bool = True):
        objeto.activo = False
        db.add(objeto)
        if commit:
            db.commit()
            db.refresh(objeto)
        else:
            db.flush()
        return objeto

    @staticmethod
    def obtener_por_id(db: Session, modelo, id_objeto):
        return db.get(modelo, id_objeto)