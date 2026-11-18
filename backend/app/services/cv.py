import uuid
from pathlib import Path

from pypdf import PdfReader

CV_DIR = Path("/tmp/cvs")
CV_DIR.mkdir(exist_ok=True)


def save_cv(data: bytes) -> str:
    cv_id = uuid.uuid4().hex
    (CV_DIR / f"{cv_id}.pdf").write_bytes(data)
    return cv_id


def read_cv_text(cv_id: str) -> str:
    path = CV_DIR / f"{uuid.UUID(cv_id).hex}.pdf"  # parsing the id blocks path traversal
    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


def delete_cv(cv_id: str) -> None:
    (CV_DIR / f"{cv_id}.pdf").unlink(missing_ok=True)
