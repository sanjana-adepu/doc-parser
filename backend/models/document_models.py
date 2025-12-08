from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from config.db import Base

class ValidationSeverity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ValidationResult(BaseModel):
    field: str
    severity: ValidationSeverity
    message: str

class ExtractedData(BaseModel):
    order_id: Optional[str] = None
    customer_name: Optional[str] = None
    date: Optional[str] = None
    amount: Optional[float] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None
    email: Optional[str] = None

class DocumentMetadata(BaseModel):
    document_id: str
    file_name: str
    file_size: int
    file_type: str
    uploaded_at: datetime
    status: ProcessingStatus

class ProcessingResult(BaseModel):
    document_id: str
    status: ProcessingStatus
    extracted_data: Optional[ExtractedData] = None
    validations: List[ValidationResult] = []
    is_valid: bool
    error_count: int
    warning_count: int
    processed_at: Optional[datetime] = None

class DocumentResponse(BaseModel):
    metadata: DocumentMetadata
    result: Optional[ProcessingResult] = None

class ExportReport(BaseModel):
    total_files: int
    successful: int
    failed: int
    warnings: int
    errors: int
    documents: List[ProcessingResult]
    generated_at: datetime