from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

pokemonfamily_location = Table(
    "pokemonfamily_location",
    Base.metadata,
    Column("family_id", Integer, ForeignKey("pokemon_families.id"), primary_key=True),
    Column("location_id", Integer, ForeignKey("locations.id"), primary_key=True),
)

pokemonfamily_types = Table(
    "pokemonfamily_types",
    Base.metadata,
    Column("family_id", ForeignKey("pokemon_families.id"), primary_key=True),
    Column("type_id", ForeignKey("pokemon_types.id"), primary_key=True),
)

class PokemonType(Base):
    __tablename__ = "pokemon_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    families = relationship("PokemonFamily", back_populates="types")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # one-way: from location → families
    families = relationship(
        "PokemonFamily",
        secondary=pokemonfamily_location,
    )

class PokemonFamily(Base):
    __tablename__ = "pokemon_families"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer) # pas forcément unique, cf mega-évolution
    
    name = Column(String, unique=True, index=True)

    type_id = Column(Integer, ForeignKey("pokemon_types.id"))

    types = relationship("PokemonType", back_populates="families")

class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("pokemon_families.id"))
    level = Column(Integer, default=1)
    hp = Column(Integer, default=100)  # Points de vie

    # en dehors du modèle SQL, juste pour accéder facilement à la famille
    family = relationship("PokemonFamily")