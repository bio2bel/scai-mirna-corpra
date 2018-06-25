# -*- coding: utf-8 -*-

from pybel.constants import ASSOCIATION
from pybel.dsl import mirna as mirna_dsl, pathology as pathology_dsl
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .constants import MODULE_NAME

Entity1_TABLE_NAME = '{}_mirna'.format(MODULE_NAME)
Entity2_TABLE_NAME = '{}_disease_or_gene'.format(MODULE_NAME)
INTERACTION_TABLE_NAME = '{}_association'.format(MODULE_NAME)

Base = declarative_base()


class Entity1(Base):
    """This class represents the miRNA table"""

    __tablename__ = Entity1_TABLE_NAME
    id = Column(Integer, primary_key=True)
    entity_term = Column(String(255), nullable=False, unique=True, index=True, doc='text mentioning of the entity')
    entity_type = Column(String(255), nullable=False, unique=True, index=True, doc='type of the entity')
    entity_offsets = Column(String(255), nullable=False, unique=True, index=True, doc='text spans of the entity')

    def __repr__(self):
        return self.entity_term, self.entity_type, self.entity_offsets


class Entity2(Base):
    """This class represents the table cotaining diesases and genes associated with a miRNA"""

    __tablename__ = Entity2_TABLE_NAME
    id = Column(Integer, primary_key=True)
    entity_term = Column(String(255), nullable=False, unique=True, index=True, doc='text mentioning of the entity')
    entity_type = Column(String(255), nullable=False, unique=True, index=True, doc='type of the entity')
    entity_offsets = Column(String(255), nullable=False, unique=True, index=True, doc='text spans of the entity')

    def __repr__(self):
        return self.entity_term, self.entity_type, self.entity_offsets


class Interaction(Base):
    """This class represents the interaction table"""

    __tablename__ = INTERACTION_TABLE_NAME
    id = Column(Integer, primary_key=True)
    pubmed = Column(String(32), nullable=False)
    sentence = Column(String, doc='The sentence from which the pair is extracted')
    interaction = Column(String(20), doc='Describes the existence or absence of an interaction')
    interaction_type = Column(String(255), doc='Describes the type of the interaction')
    e1_id = Column(Integer, ForeignKey('{}.id'.format(Entity1_TABLE_NAME)))
    e1 = relationship('Entity1')
    e2_id = Column(Integer, ForeignKey('{}.id'.format(Entity2_TABLE_NAME)))
    e2 = relationship('Entity2')


    def __repr__(self):
        return '{} and {} from {}'.format(self.e1, self.e2, self.pubmed, self.interaction, self.interaction_type)
