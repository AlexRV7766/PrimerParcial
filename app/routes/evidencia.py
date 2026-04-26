from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

import cloudinary.uploader
import cloudinary

from app.core.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.models.evidencia import Evidencia

router = APIRouter(prefix="/evidencias", tags=["Evidencias"])


@router.post("/upload")
async def subir_archivo(
    emergencia_id: int,
    tipo: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        resultado = cloudinary.uploader.upload(
            archivo.file,
            resource_type="auto",
            timestamp="auto"
        )

        url = resultado["secure_url"]

        evidencia = Evidencia(
            emergencia_id=emergencia_id,
            tipo=tipo,
            url=url
        )

        db.add(evidencia)
        db.commit()
        db.refresh(evidencia)

        return {"mensaje": "Archivo subido", "url": url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{evidencia_id}")
def eliminar(
    evidencia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    evidencia = db.query(Evidencia).filter(Evidencia.id == evidencia_id).first()
    if not evidencia:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")
    
    # Podría requerirse borrar de Cloudinary si tuviéramos el public_id, 
    # por ahora solo la borramos de la BD
    db.delete(evidencia)
    db.commit()
    return {"mensaje": "Evidencia eliminada"}