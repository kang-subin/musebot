from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar("T")

class BaseResponse(GenericModel, Generic[T]):
    success: bool = Field(default=True, description="요청 성공 여부")
    message: Optional[str] = Field(default="요청이 성공적으로 처리되었습니다.", description="응답 메시지")
    data: Optional[T] = Field(default=None, description="실제 응답 데이터 (도메인별 DTO)")
