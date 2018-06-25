# -*- coding: utf-8 -*-

import logging
from typing import List

from bio2bel import AbstractManager
from pybel import BELGraph
from tqdm import tqdm

from .constants import MODULE_NAME
from .models import Base, Entity1, Entity2, Interaction
from .parser import get_scai_mirna_dfs

__all__ = ['Manager']

log = logging.getLogger(__name__)


class Manager(AbstractManager):
    """Manager for Bio2bel SCAI-miRNA-Corpora"""
    module_name = MODULE_NAME
    flask_admin_models = [Entity1, Entity2, Interaction]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name_e1 = {}
        self.name_e2 = {}

    @property
    def _base(self):
        return Base

    def is_populated(self):
        return 0 < self.count_e1s()

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

    def list_associations(self) -> List[Interaction]:
        """Returns all associations

        :rtype: list[Interaction]
        """
        return self._list_model(Interaction)

    def to_bel_graph(self):
        """Builds a BEL graph containing all of the miRNA-disease associations in the database

        :rtype: BELGraph
        """
        graph = BELGraph()

        for interaction in self.list_associations():
            interaction.add_to_bel_graph(graph)

        return graph
