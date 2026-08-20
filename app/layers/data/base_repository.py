from sqlmodel import Session


class BaseRepository:
    """
    Repositorio base con operaciones comunes reutilizables.
    """

    @staticmethod
    def guardar(db: Session, objeto):
        db.add(objeto)
        db.commit()
        db.refresh(objeto)
        return objeto

    @staticmethod
    def actualizar(db: Session, objeto):
        db.add(objeto)
        db.commit()
        db.refresh(objeto)
        return objeto

    @staticmethod
    def eliminar_logico(db: Session, objeto):
        objeto.activo = False
        db.add(objeto)
        db.commit()
        db.refresh(objeto)
        return objeto

    @staticmethod
    def obtener_por_id(db: Session, modelo, id_objeto):
        return db.get(modelo, id_objeto)