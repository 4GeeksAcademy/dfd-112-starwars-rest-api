from flask_sqlalchemy import SQLAlchemy
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.orm import DeclarativeBase, declarative_base ### ---> SIN USAR
from datetime import datetime, timezone


#########################################################################################
#########################################################################################
#############                            TABLES                             #############
#############                        Star Wars Blog                         #############
#############                       with SQL Alchemy                        #############
#############                         and classes                           #############
#########################################################################################
#########################################################################################
"""
TO-DOs:

[x] Create tables for STAR WARS Database Model:

Create user and category tables:
    [x] User
    [x] People
    [x] Planet
    [x] Vehicle


Create Favorite handling tables:
    [x] People  favorites
    [x] Planet  favorites
    [x] Vehicle favorites
"""


db = SQLAlchemy()


############################################
###########         USER         ###########
############################################
"""
TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Attributes:
    [x] id
    [x] email
    [x] username
    [x] name
    [x] password
    [x] is_active
    [x] creation

[x] Create Relations
    [x] with FavoriteCharacters
    [x] with FavoritePlanets
    [x] with FavoriteVehicles

[x] Create serialization

[x] Create "__repr__" method
"""
class User(db.Model):
    __tablename__ = 'user'
    
    ### ATTRIBUTES ###
    id:         Mapped[int]      = mapped_column(              primary_key=True)
    email:      Mapped[str]      = mapped_column( String(40),  unique=True,      nullable=False)
    username:   Mapped[str]      = mapped_column( String(40),  unique=True,      nullable=False)
    name:       Mapped[str]      = mapped_column( String(60),                    nullable=False)
    password:   Mapped[str]      = mapped_column( String(255),                   nullable=False)
    is_active:  Mapped[bool]     = mapped_column( Boolean(),   default=True,     nullable=False)
    creation:   Mapped[datetime] = mapped_column( DateTime(timezone=True), default=func.now(), nullable=False)


    ### RELATIONS ###

    # One-to-many relationship with FavoriteCharacters - shows all characters this user has favorited
    favorite_people: Mapped[List["FavoritePeople"]] = relationship(
        back_populates='user', 
        cascade='all, delete-orphan',
        lazy='select'
    )

    # One-to-many relationship with FavoritePlanets - shows all planets this user has favorited
    favorite_planets: Mapped[List["FavoritePlanets"]] = relationship(
        back_populates='user', 
        cascade='all, delete-orphan',
        lazy='select'
    )

    # One-to-many relationship with FavoriteVehicles - shows all vehicles this user has favorited
    favorite_vehicles: Mapped[List["FavoriteVehicles"]] = relationship(
        back_populates='user', 
        cascade='all, delete-orphan',
        lazy='select'
    )


    ### SERIALIZATION ###
    def serialize(self):
        return {
            "id":            self.id,
            "is_active":     self.is_active,
            "email":         self.email,
            "username":      self.username,
            "name":          self.name,
            "creation_date": self.creation.isoformat() if self.creation else None,
            "favorite_characters": [fav.serialize() for fav in self.favorite_people],
            "favorite_planets":    [fav.serialize() for fav in self.favorite_planets],
            "favorite_vehicles":   [fav.serialize() for fav in self.favorite_vehicles],
            # do not serialize the password, its a security breach !!!
        }
    
    ### __repr__ METHOD ###

    def __repr__(self):
        return f"<User {self.id} - {self.username} - {self.email} - {self.name}>"

############################################
##########         People         ##########
############################################
"""
TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Attributes:
    [x] id
    [x] name
    [x] birth_year
    [x] eye_color
    [x] gender
    [x] hair_color
    [x] height
    [x] mass
    [x] skin_color
    [x] homeworld
    [x] url
    [x] created
    [x] edited

[x] Create Relations
    [x] with FavoritePeople

[x] Create serialization

[x] Create "__repr__" method
"""
class People(db.Model):
    __tablename__ = 'people'

    ### ATTRIBUTES ###

    id:          Mapped[int] = mapped_column(              primary_key=True)
    name:        Mapped[str] = mapped_column( String(100),                   nullable=False)
    birth_year:  Mapped[str] = mapped_column( String(100),                   nullable=False)
    eye_color:   Mapped[str] = mapped_column( String(100),                   nullable=False)
    gender:      Mapped[str] = mapped_column( String(100),                   nullable=False)
    hair_color:  Mapped[str] = mapped_column( String(100),                   nullable=False)
    height:      Mapped[str] = mapped_column( String(20),                    nullable=False)
    mass:        Mapped[str] = mapped_column( String(40),                    nullable=False)
    skin_color:  Mapped[str] = mapped_column( String(20),                    nullable=False)
    homeworld:   Mapped[str] = mapped_column( String(40),                    nullable=False)
    url:         Mapped[str] = mapped_column( String(100), unique=True,      nullable=False)
    created:     Mapped[datetime] = mapped_column( DateTime(timezone=True), default=func.now(), nullable=False)
    edited:      Mapped[Optional[datetime]] = mapped_column( DateTime(timezone=True), default=func.now(), onupdate=func.now())


    ### RELATIONS ###

    # One-to-many relationship with FavoriteCharacters - shows which users have favorited this character
    favorite_by: Mapped[List["FavoritePeople"]] = relationship(
        back_populates='people', 
        cascade='all, delete-orphan',
        lazy='select'
    )

    ### SERIALIZATION ###
    def serialize(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "birth_year":  self.birth_year,
            "eye_color":   self.eye_color,
            "gender":      self.gender,
            "hair_color":  self.hair_color,
            "height":      self.height,
            "mass":        self.mass,
            "skin_color":  self.skin_color,
            "homeworld":   self.homeworld,
            "url":         self.url,
            "created":     self.created.isoformat()  if self.created else None,
            "edited":      self.edited.isoformat()   if self.edited  else None
        }
    

    ### __repr__ METHOD ###

    def __repr__(self): 
        return f"<People {self.id} - {self.name}>"


#######################################
#######    FavoritePeople    ##########
#######################################
"""
Represents which people/characters each user has marked as favorites.

TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Attributes:
    [x] id
    [x] user_id     (Foreign Key)
    [x] people_id   (Foreign Key)
    [x] created_at  (tracking when favorite was added)

[x] Create Relations
    [x] with User
    [x] with People

[x] Create serialization

[x] Create "__repr__" method

[x] Add unique constraint to prevent duplicate favorites
"""
class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'

    ### ATTRIBUTES ###
    id:         Mapped[int]      = mapped_column( primary_key=True)
    user_id:    Mapped[int]      = mapped_column( ForeignKey('user.id'),   nullable=False)
    people_id:  Mapped[int]      = mapped_column( ForeignKey('people.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), default=func.now(), nullable=False)

    ### TABLE CONSTRAINTS ###
    __table_args__ = (
        UniqueConstraint('user_id', 'people_id', name='unique_user_character_favorite'),
    )

    ### RELATIONS ###

    # Many-to-one relationship with User - the user who favorited this character
    user: Mapped["User"] = relationship(
        back_populates='favorite_people'
        )
    
    # Many-to-one relationship with People - the character being favorited
    people: Mapped["People"] = relationship(
        back_populates='favorite_by'
        )

    ### SERIALIZATION ###
    def serialize(self):
        return {
            "id":           self.id,
            "user_id":      self.user_id,
            "people_id":    self.people_id,
            "character":    self.people.serialize(),
            "created_at":   self.created_at.isoformat() if self.created_at else None
        }


    ### __repr__ METHOD ###

    def __repr__(self):
        return f'<FavoritePeople ... User:{self.user_id} --> Character:{self.people_id}>'



############################################
##########         Planet         ##########
############################################
"""
TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Attributes:
    [x] id
    [x] name
    [x] diameter
    [x] rotation_period
    [x] orbital_period
    [x] gravity
    [x] population
    [x] climate
    [x] terrain
    [x] surface_water
    [x] created
    [x] edited

[x] Create Relations
    [x] with FavoritePlanets

[x] Create serialization

[x] Create "__repr__" method
"""
class Planet(db.Model):
    __tablename__ = 'planet'

    ### ATTRIBUTES ###
    id:              Mapped[int] = mapped_column(              primary_key=True)
    name:            Mapped[str] = mapped_column( String(100),                   nullable=False)
    diameter:        Mapped[str] = mapped_column( String(100),                   nullable=False)
    rotation_period: Mapped[str] = mapped_column( String(100),                   nullable=False)
    orbital_period:  Mapped[str] = mapped_column( String(100),                   nullable=False)
    gravity:         Mapped[str] = mapped_column( String(100),                   nullable=False)
    population:      Mapped[str] = mapped_column( String(100),                   nullable=False)
    climate:         Mapped[str] = mapped_column( String(100),                   nullable=False)
    terrain:         Mapped[str] = mapped_column( String(100),                   nullable=False)
    surface_water:   Mapped[str] = mapped_column( String(100),                   nullable=False)
    url:             Mapped[str] = mapped_column( String(100), unique=True,      nullable=False)
    created:         Mapped[datetime] = mapped_column( DateTime(timezone=True), default=func.now(), nullable=False)
    edited:          Mapped[Optional[datetime]] = mapped_column( DateTime(timezone=True), default=func.now(), onupdate=func.now())


    ### RELATIONS ###

    # One-to-many relationship with FavoritePlanets - shows which users have favorited this planet
    favorite_by: Mapped[List["FavoritePlanets"]] = relationship(
        back_populates='planet', 
        cascade='all, delete-orphan',
        lazy='select'
    )


    ### SERIALIZATION ###
    def serialize(self):
        return {
            "id":              self.id,
            "name":            self.name,
            "diameter":        self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period":  self.orbital_period,
            "gravity":         self.gravity,
            "population":      self.population,
            "climate":         self.climate,
            "terrain":         self.terrain,
            "surface_water":   self.surface_water,
            "url":             self.url,
            "created":         self.created.isoformat()  if self.created else None,
            "edited":          self.edited.isoformat()   if self.edited  else None
        }
    

    ### __repr__ METHOD ###

    def __repr__(self):
        return f"<Planet {self.id} - {self.name}>"



############################################
#########     FavoritePlanets    ###########
############################################
"""
Represents which planets each user has marked as favorites.

TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Attributes:
    [x] id
    [x] user_id    (Foreign Key)
    [x] planet_id  (Foreign Key)
    [x] created_at (added for tracking when favorite was added)

[x] Create Relations
    [x] with User
    [x] with Planet

[x] Create serialization

[x] Create "__repr__" method

[x] Add unique constraint to prevent duplicate favorites
"""
class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'

    ### ATTRIBUTES ###
    
    id:         Mapped[int]      = mapped_column( primary_key=True)
    user_id:    Mapped[int]      = mapped_column( ForeignKey('user.id'),   nullable=False)
    planet_id:  Mapped[int]      = mapped_column( ForeignKey('planet.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), default=func.now(), nullable=False)

    ### TABLE CONSTRAINTS ###
    __table_args__ = (
        UniqueConstraint('user_id', 'planet_id', name='unique_user_planet_favorite'),
    )

    ### RELATIONS ###

    # Many-to-one relationship with User - the user who favorited this planet
    user: Mapped["User"] = relationship(
        back_populates='favorite_planets'
        )

    # Many-to-one relationship with Planet - the planet being favorited
    planet: Mapped["Planet"] = relationship(
        back_populates='favorite_by'
        )

    ### SERIALIZATION ###
    def serialize(self):
        return {
            "id":         self.id,
            "user_id":    self.user_id,
            "planet_id":  self.planet_id,
            "planet":     self.planet.serialize(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    ### __repr__ METHOD ###

    def __repr__(self):
        return f'<FavoritePlanet ... User:{self.user_id} --> Planet:{self.planet_id}>'


############################################
##########         Vehicle         #########
############################################
"""
TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Attributes:
    [x] id
    [x] name
    [x] model
    [x] vehicle_class
    [x] manufacturer
    [x] length
    [x] cost_in_credits
    [x] crew
    [x] passengers
    [x] max_atmos_speed
    [x] cargo_capacity
    [x] consumables
    [x] url
    [x] created
    [x] edited

[x] Create Relations
    [x] with FavoriteVehicles

[x] Create serialization

[x] Create "__repr__" method
"""
class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    ### ATTRIBUTES ###
    id:              Mapped[int] = mapped_column(              primary_key=True)
    name:            Mapped[str] = mapped_column( String(100),                    nullable=False)
    model:           Mapped[str] = mapped_column( String(100),                    nullable=False)
    vehicle_class:   Mapped[str] = mapped_column( String(100),                    nullable=False)
    manufacturer:    Mapped[str] = mapped_column( String(100),                    nullable=False)
    length:          Mapped[str] = mapped_column( String(100),                    nullable=False)
    cost_in_credits: Mapped[str] = mapped_column( String(100),                    nullable=False)
    crew:            Mapped[str] = mapped_column( String(20),                     nullable=False)
    passengers:      Mapped[str] = mapped_column( String(20),                     nullable=False)
    max_atmos_speed: Mapped[str] = mapped_column( String(100),                    nullable=False)
    cargo_capacity:  Mapped[str] = mapped_column( String(100),                    nullable=False)
    consumables:     Mapped[str] = mapped_column( String(100),                    nullable=False)
    url:             Mapped[str] = mapped_column( String(200), unique=True,       nullable=False)
    created:         Mapped[datetime] = mapped_column( DateTime(timezone=True), default=func.now(), nullable=False)
    edited:          Mapped[Optional[datetime]] = mapped_column( DateTime(timezone=True), default=func.now(), onupdate=func.now())
    

    ### RELATIONS ###

    # One-to-many relationship with FavoriteVehicles - shows which users have favorited this vehicle
    favorite_by: Mapped[List["FavoriteVehicles"]] = relationship(
        back_populates='vehicle', 
        cascade='all, delete-orphan',
        lazy='select'
    )

    ### SERIALIZATION ###
    def serialize(self):
        return {
            "id":               self.id,
            "name":             self.name,
            "model":            self.model,
            "vehicle_class":    self.vehicle_class,
            "manufacturer":     self.manufacturer,
            "length":           self.length,
            "cost_in_credits":  self.cost_in_credits,
            "crew":             self.crew,
            "passengers":       self.passengers,
            "max_atmos_speed":  self.max_atmos_speed,
            "cargo_capacity":   self.cargo_capacity,
            "consumables":      self.consumables,
            "url":              self.url,
            "created":          self.created.isoformat() if self.created else None,
            "edited":           self.edited.isoformat()  if self.edited  else None
        }


    ### __repr__ METHOD ###

    def __repr__(self):
        return f"<Vehicle {self.id} - {self.name} - {self.model} - {self.vehicle_class}>"
    


############################################
#########    FavoriteVehicles    ##########
############################################
"""
Represents which vehicles each user has marked as favorites.

TO-DO's:

[x] Name the table with "__tablename__ ="

[x] Create Attributes:
    [x] id
    [x] user_id     (Foreign Key)
    [x] vehicle_id  (Foreign Key)
    [x] created_at  (added for tracking when favorite was added)

[x] Create Relations
    [x] with User
    [x] with Vehicle

[x] Create serialization

[x] Create "__repr__" method

[x] Add unique constraint to prevent duplicate favorites
"""
class FavoriteVehicles(db.Model):
    __tablename__ = 'favorite_vehicles'

    ### ATTRIBUTES ###

    id:         Mapped[int]      = mapped_column( primary_key=True)
    user_id:    Mapped[int]      = mapped_column( ForeignKey('user.id'),     nullable=False)
    vehicle_id: Mapped[int]      = mapped_column( ForeignKey('vehicle.id'),  nullable=False)
    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), default=func.now(), nullable=False)

    ### TABLE CONSTRAINTS ###
    __table_args__ = (
        UniqueConstraint('user_id', 'vehicle_id', name='unique_user_vehicle_favorite'),
    )


    ### RELATIONS ###

    # Many-to-one relationship with User - the user who favorited this vehicle
    user: Mapped["User"] = relationship(
        back_populates='favorite_vehicles'
        )
    
    # Many-to-one relationship with Vehicle - the vehicle being favorited
    vehicle: Mapped["Vehicle"] = relationship(
        back_populates='favorite_by'
        )

    ### SERIALIZATION ###
    def serialize(self):
        return {
            "id":          self.id,
            "user_id":     self.user_id,
            "vehicle_id":  self.vehicle_id,
            "vehicle":     self.vehicle.serialize(),
            "created_at":  self.created_at.isoformat() if self.created_at else None
        }


    ### __repr__ METHOD ###

    def __repr__(self):
        return f'<FavoriteVehicle ... User:{self.user_id} --> Vehicle:{self.vehicle_id}>'

#######  -------------------------------------------------------------------------  ######


#################################################################
#################################################################
##################      Favorites HANDLING     ##################
##################        MULTIPLE tables      ##################
##################       without nullables     ##################
#################################################################
#################################################################
"""
Different Versions:

    1. []  ONLY one Favorite Table  ---    Nullable entries -- NO   Enum

    2. []  ONLY one Favorite Table  --- NO Nullable entries -- WITH Enum

    3. []  ONLY one Favorite Table  --- NO Nullable entries -- NO   Enum -- Many to Many relationship

    4. [x] MULTIPLE Favorite Tables --- NO Nullable entries -- NO   Enum
          (x1 table per category)
"""
########################################################################################################