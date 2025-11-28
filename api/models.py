from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from .database import Base


# Association Table (for many-to-many)
workout_routine_association = Table(
    'workout_routine', Base.metadata,
    Column('workout_id', Integer, ForeignKey('workouts.id')),
    Column('routine_id', Integer, ForeignKey('routines.id'))
)


class User(Base):
    ''' user model '''
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Workout(Base):
    ''' workout model '''
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)
    description = Column(String)
    # back_populates links to Routine.workouts
    routines = relationship(
        'Routine',
        secondary=workout_routine_association,
        back_populates='workouts'
    )


class Routine(Base):
    ''' routine model '''
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)
    description = Column(String, index=True)
    # symmetrical many-to-many mapping
    workouts = relationship(
        'Workout',
        secondary=workout_routine_association,
        back_populates='routines'
    )
