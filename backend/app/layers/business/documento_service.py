import os
import shutil
from fastapi import UploadFile, HTTPException, status
from sqlmodel import Session
from app.layers.models.documento import Documento
from app.layers.data.documento_repository import DocumentoRepository
from app.layers.models.auth import User

# Asegurarnos de que la carpeta física exista en tu PC
UPLOAD_DIR = "app/static/documentos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DocumentoService:
    @staticmethod
    def subir_documento(db: Session, usuario_actual: User, tipo_doc: str, archivo: UploadFile, id_sp: int = None):
        # Validar tipo de archivo
        if not archivo.filename.lower().endswith(('.pdf', '.jpg', '.png', '.jpeg')):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF o Imágenes.")

        # Generar un nombre único para evitar que dos usuarios suban un "cedula.pdf" y se sobreescriba
        nombre_unico = f"user_{usuario_actual.id_usu}_{archivo.filename}"
        ruta_fisica = os.path.join(UPLOAD_DIR, nombre_unico)

        # Copiar el archivo desde la memoria de FastAPI al disco duro de tu PC
        with open(ruta_fisica, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)

        # Crear la ruta URL que el Frontend usará para mostrar el archivo
        ruta_url = f"/static/documentos/{nombre_unico}"

        # Guardar en Base de Datos
        nuevo_doc = Documento(
            id_usu=usuario_actual.id_usu,
            id_sp=id_sp,
            tipo_doc=tipo_doc,
            nom_archivo=archivo.filename,
            ruta_archivo=ruta_url,
            estado="PENDIENTE"
        )
        
        return DocumentoRepository.crear(db, nuevo_doc)

    @staticmethod
    def obtener_mis_documentos(db: Session, usuario_actual: User):
        return DocumentoRepository.obtener_por_usuario(db, usuario_actual.id_usu)