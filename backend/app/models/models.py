from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association tables
pokemonfamily_location = Table(
    "pokemonfamily_location",
    Base.metadata,
    Column("family_id", Integer, ForeignKey("pokemon_families.id"), primary_key=True),
    Column("location_id", Integer, ForeignKey("locations.id"), primary_key=True),
)

pokemonfamily_types = Table(
    "pokemonfamily_types",
    Base.metadata,
    Column("family_id", Integer, ForeignKey("pokemon_families.id"), primary_key=True),
    Column("type_id", Integer, ForeignKey("pokemon_types.id"), primary_key=True),
)

pokemon_instance_moves = Table(
    "pokemon_instance_moves",
    Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id"), primary_key=True),
    Column("move_id", Integer, ForeignKey("pokemon_move.id"), primary_key=True),
)

default_moves = Table(
    "default_moves",
    Base.metadata,
    Column("type_id", Integer, ForeignKey("pokemon_types.id"), primary_key=True),
    Column("move_id", Integer, ForeignKey("base_move.id"), primary_key=True),
)

# Evolution table
class PokemonEvolution(Base):
    __tablename__ = "pokemon_evolutions"

    id = Column(Integer, primary_key=True, index=True)
    from_type = Column(Integer, ForeignKey("pokemon_families.id"))
    to_type = Column(Integer, ForeignKey("pokemon_families.id"))
    level = Column(Integer, default=0)

    from_family = relationship("PokemonFamily", foreign_keys=[from_type])
    to_family = relationship("PokemonFamily", foreign_keys=[to_type])

# Pokémon type
class PokemonType(Base):
    __tablename__ = "pokemon_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# Pokémon family
class PokemonFamily(Base):
    __tablename__ = "pokemon_families"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)  # Not necessarily unique
    name = Column(String, unique=True, index=True)
    base_hp = Column(Integer, default=15)

    # Many-to-many relationships
    types = relationship("PokemonType", secondary=pokemonfamily_types)
    locations = relationship("Location", secondary=pokemonfamily_location)

# Locations
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    families = relationship("PokemonFamily", secondary=pokemonfamily_location)

# Pokémon instance
class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("pokemon_families.id"))
    level = Column(Integer, default=1)
    hp = Column(Integer, default=100)

    family = relationship("PokemonFamily")
    moves = relationship("Move", secondary=pokemon_instance_moves)

# Base move (move definition)
class BaseMove(Base):
    __tablename__ = "base_move"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type_id = Column(Integer, ForeignKey("pokemon_types.id"))
    description = Column(String)
    minimal_power = Column(String, nullable=True)
    type = relationship("PokemonType")

# Pokémon-specific move instance
class Move(Base):
    __tablename__ = "pokemon_move"

    id = Column(Integer, primary_key=True, index=True)
    move_id = Column(Integer, ForeignKey("base_move.id"))
    additional_power = Column(String, nullable=True)


