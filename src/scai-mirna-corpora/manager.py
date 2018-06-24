# -*- coding: utf-8 -*-

import logging

from bio2bel.utils import get_connection
from pybel import BELGraph
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from .constants import MODULE_NAME
from .models import Entity2, Entity1, Interaction, Base
from .parser import get_scai_mirna_dfs

__all__ = ['Manager']

log = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, connection=None):
        self.connection = get_connection(MODULE_NAME, connection=connection)
        self.engine = create_engine(self.connection)
        self.session_maker = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        self.session = self.session_maker()
        self.create_all()

        self.name_e1 = {}
        self.name_e2 = {}

    def create_all(self, check_first=True):
        """Create the empty database (tables)"""
        Base.metadata.create_all(self.engine, checkfirst=check_first)

    def drop_all(self, check_first=True):
        """Create the empty database (tables)"""
        Base.metadata.drop_all(self.engine, checkfirst=check_first)

    @staticmethod
    def ensure(connection=None):
        """Checks and allows for a Manager to be passed to the function.

        :param connection: can be either an already build manager or a connection string to build a manager with.
        """
        if connection is None or isinstance(connection, str):
            return Manager(connection=connection)

        if isinstance(connection, Manager):
            return connection

        raise TypeError

    def get_e1_by_name(self, name):
        """Gets an miRNA from the database if it exists

        :param str name: A mirBase name
        :rtype: Optional[MiRNA]
        """
        return self.session.query(Entity1).filter(Entity1.entity_term == name).one_or_none()

    def get_e2_by_name(self, name):
        """Gets a Disease from the database if it exists

        :param str name: A MeSH disease name
        :rtype: Optional[Disease]
        """
        return self.session.query(Entity2).filter(Entity2.entity_term == name).one_or_none()

    def get_or_create_e1(self, name):
        """Gets an miRNA from the database or creates it if it does not exist

        :param str name: A mirBase name
        :rtype: Entity1
        """
        e1 = self.name_e1.get(name)
        if e1 is not None:
            return e1

        e1 = self.get_e1_by_name(name)
        if e1 is not None:
            self.name_e1[name] = e1
            return e1

        e1 = self.name_e1[name] = Entity1(name=name)
        self.session.add(e1)

        return e1

    def get_or_create_e2(self, name):
        """Gets a Disease from the database or creates it if it does not exist

        :param str name: A MeSH disease name
        :rtype: Entity2
        """
        e2 = self.name_e2.get(name)
        if e2 is not None:
            return e2

        e2 = self.get_e2_by_name(name)
        if e2 is not None:
            self.name_e2[name] = e2
            return e2

        e2 = self.name_e2[name] = Entity2(name=name)
        self.session.add(e2)

        return e2

    def _count_model(self, model):
        return self.session.query(model).count()

    def count_e1s(self):
        """Counts the number of miRNAs in the database

        :rtype: int
        """
        return self._count_model(Entity1)

    def count_e2s(self):
        """Counts the number of diseases in the database

        :rtype: int
        """
        return self._count_model(Entity2)

    def count_pairs(self):
        """Counts the number of miRNA-disease associations in the database

        :rtype: int
        """
        return self._count_model(Interaction)

    def populate(self, url=None):
        """Populates the database

        :param Optional[str] url: A custom data source URL
        """
        df = get_scai_mirna_dfs(url=url)

        log.info('building models')
        for _, idx, e1_name, e2_name, pubmed, description in tqdm(df.itertuples(), total=len(df.index)):
            e1 = self.get_or_create_e1(e1_name)
            e2 = self.get_or_create_e2(e2_name)

            association = Interaction(
                pubmed=pubmed,
                description=description,
                mirna=e1,
                disease=e2,
            )

            self.session.add(association)

        log.info('inserting models')
        self.session.commit()

    def get_associations(self):
        """Returns all associations

        :rtype: list[Interaction]
        """
        return self.session.query(Interaction).all()

    def to_bel_graph(self):
        """Builds a BEL graph containing all of the miRNA-disease associations in the database

        :rtype: BELGraph
        """
        graph = BELGraph()

        for association in self.get_associations():
            association.add_to_bel_graph(graph)

        return graph
