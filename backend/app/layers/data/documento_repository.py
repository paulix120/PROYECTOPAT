from typing import List
from sqlmodel import Session, select
from app.layers.models.documento import Documento

class DocumentoRepository:
    @staticmethod
    def crear(db: Session, documento: Documento) -> Documento:
        db.add(documento)
        db.commit()
        db.refresh(documento)
        return documento

    @staticmethod
    def obtener_por_usuario(db: Session, id_usu: int) -> List[Documento]:
        return db.exec(select(Documento).where(Documento.id_usu == id_usu)).all()