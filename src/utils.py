from sqlmodel import Session, select
from .database import engine
from .models import *
import re

def extract_phone_numbers(text):
    pattern = re.compile(r'''
        # Match optional country code +1 or 1
        (?:\+?1[\s.-]?)?

        # Match area code (optional parentheses)
        \(?(\d{3})\)?[\s.-]?

        # Match first 3 digits of phone number
        (\d{3})[\s.-]?

        # Match last 4 digits of phone number
        (\d{4})
    ''', re.VERBOSE)
    matches = pattern.findall(text)
    formatted_numbers = ['-'.join(match) for match in matches]
    return formatted_numbers

def extract_emails(text):
    pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    matches = pattern.findall(text)
    return matches

def find_or_create_data_format(name: str):
    with Session(engine) as session:
        data_format = session.exec(select(DataFormat).where(DataFormat.name == name)).first()
        if (data_format is not None):
            return data_format
        data_format = DataFormat(name=name)
        session.add(data_format)
        session.commit()
        session.refresh(data_format)
        return data_format

def find_or_create_data_type(name: str):
    with Session(engine) as session:
        data_type = session.exec(select(DataType).where(DataType.name == name)).first()
        if (data_type is not None):
            return data_type
        data_type = DataType(name=name)
        session.add(data_type)
        session.commit()
        session.refresh(data_type)
        return data_type

def find_or_create_language(name: str):
    with Session(engine) as session:
        language = session.exec(select(Language).where(Language.name == name)).first()
        if (language  is not None):
            return language
        language = Language(name=name)
        session.add(language)
        session.commit()
        session.refresh(language)
        return language

def find_or_create_theme(name: str):
    with Session(engine) as session:
        theme = session.exec(select(Theme).where(Theme.name == name)).first()
        if (theme  is not None):
            return theme
        theme = Theme(name=name)
        session.add(theme)
        session.commit()
        session.refresh(theme)
        return theme

def create_metadata(metadata: Metadata):
    with Session(engine) as session:
        session.add(metadata)
        session.commit()
        session.refresh(metadata)

def find_or_create_discipline(name: str, level: int, parent_id: Optional[int] = None):
    with Session(engine) as session:
        discipline = session.exec(select(Discipline).where(Discipline.name == name, Discipline.level == level)).first()
        if (discipline is not None):
            return discipline
        discipline = Discipline(name=name, level=level, parent_id=parent_id)
        session.add(discipline)
        session.commit()
        session.refresh(discipline)
        return discipline

def process_discipline(discipline: dict[str, str]):
    primary, secondary, tertiary = discipline['primary_discipline'], discipline['secondary_discipline'], discipline['tertiary_discipline']
    discipline_ref = None

    if primary is not None:
        primary_discipline = find_or_create_discipline(primary, level=1)
        discipline_ref = primary_discipline
        if secondary is not None:
            secondary_discipline = find_or_create_discipline(
                secondary,
                level=2,
                parent_id=primary_discipline.id
            )
            discipline_ref = secondary_discipline

            if tertiary is not None:
                tertiary_discipline = find_or_create_discipline(
                    tertiary,
                    level=3,
                    parent_id=secondary_discipline.id
                )
                discipline_ref = tertiary_discipline
    return discipline_ref

def find_or_create_location(country: str, province: Optional[str] = None, city: Optional[str] = None, region: Optional[str] = None):
    with Session(engine) as session:
        location = session.exec(select(Location).where(Location.country == country, Location.province == province, Location.city == city, Location.region == region)).first()
        if (location is not None):
            return location
        location = Location(country=country, province=province, city=city, region=region)
        session.add(location)
        session.commit()
        session.refresh(location)
        return location

def process_location(location_relevance: str):
    if location_relevance in ['Canada', 'Newfoundland and Labrador']:
        location = find_or_create_location('CA', 'NL')
        return location
    location = Location(country='CA', province='NL', region=location_relevance)
    return location

def process_contact(type: Optional[str], details:Optional[str] = None):
    with Session(engine) as session:
        if type is None:
            return None
        phone = ','.join(extract_phone_numbers(details)) if details is not None else None
        email = '\n'.join(extract_emails(details)) if details is not None else None
        contact = session.exec(select(ContactPoint).where(ContactPoint.type == type, ContactPoint.email == email, ContactPoint.phone == phone)).first()
        if (contact is not None):
            return contact
        contact = ContactPoint(type=type, email=email, phone=phone)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return contact

def process_entity(name: str):
    with Session(engine) as session:
        entity = session.exec(select(Entity).where(Entity.name == name)).first()
        if (entity is not None):
            return entity
        entity = Entity(name=name)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

def process_entity_sponsor(name: str, type: str):
    with Session(engine) as session:
        entity = session.exec(select(Entity).where(Entity.name == name)).first()
        if (entity is None):
            entity = Entity(name=name, org=type)
        else:
            entity.org = type
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity
