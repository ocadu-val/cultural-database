from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, func
import time

class DataFormat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class DataFormatLink(SQLModel, table=True):
    metadata_id: int = Field(default=None, foreign_key="metadata.id", primary_key=True)
    data_format_id: int = Field(default=None, foreign_key="dataformat.id", primary_key=True)

class DataType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class DataTypeLink(SQLModel, table=True):
    metadata_id: int = Field(default=None, foreign_key="metadata.id", primary_key=True)
    data_type_id: int = Field(default=None, foreign_key="datatype.id", primary_key=True)

class Language(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class LanguageLink(SQLModel, table=True):
    metadata_id: Optional[int] = Field(default=None, foreign_key="metadata.id", primary_key=True)
    language_id: Optional[int] = Field(default=None, foreign_key="language.id", primary_key=True)

class ContactURL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_id: Optional[int] = Field(default=None, foreign_key="contactpoint.id")
    url: str

class ContactPoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: Optional[str]
    phone: Optional[str]
    type: str # individual, organization
    # address: str
    # city: Optional[str]
    # province: Optional[str]

class ContactRelation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str # owner, host, admin, sponsor
    name: str
    role: Optional[str]
    org: str
    contact_id: Optional[int] = Field(default=None, foreign_key="contactpoint.id")

class Entity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    org: Optional[str] = None # univeristy, government, comoany

class Theme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Discipline(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    parent_id: Optional[int] = Field(default=None, foreign_key="discipline.id")
    level: int

class Metadata(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: str
    province_code: str
    created_at: int = Field(default_factory=func.current_timestamp)
    updated_at: int = Field(default_factory=func.current_timestamp)
    description: str
    valid_from: Optional[int]
    valid_to: Optional[int]
    usage_url: str
    visibility: Optional[str]
    access_type: str
    license: Optional[str]
    usage_limit: str
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    data_formats: list[DataFormat] = Relationship(link_model=DataFormatLink)
    data_types: list[DataType] = Relationship(link_model=DataTypeLink)
    languages: list[Language] = Relationship(link_model=LanguageLink)
    contact_id: Optional[int] = Field(default=None, foreign_key="contactpoint.id")
    admin_id: Optional[int] = Field(default=None, foreign_key="entity.id")
    owner_id: Optional[int] = Field(default=None, foreign_key="entity.id")
    host_id: Optional[int] = Field(default=None, foreign_key="contactrelation.id")
    sponsor_id: Optional[int] = Field(default=None, foreign_key="entity.id")
    theme_id: Optional[int] = Field(default=None, foreign_key="theme.id")
    discipline_id: Optional[int] = Field(default=None, foreign_key="discipline.id")


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    country: str
    province: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
