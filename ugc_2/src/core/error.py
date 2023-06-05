from dataclasses import dataclass


@dataclass
class DocumentExistsException(Exception):
    message: str = "Document already exist"
