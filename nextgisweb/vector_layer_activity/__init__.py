# -*- coding: utf-8 -*-
from pkg_resources import resource_filename

from mako.template import Template

from .. import db
from ..component import Component
from .model import Base, VectorLayerActivity
from .util import COMP_ID

__all__ = [
    "VectorLayerActivityComponent",
    "VectorLayerActivity",
]


class VectorLayerActivityComponent(Component):
    identity = COMP_ID
    tableslist_view = "%s_tableslist" % COMP_ID
    metadata = Base.metadata

    def initialize(self):
        super(
            VectorLayerActivityComponent, self
        ).initialize()

    def initialize_db(self):
        conn = self.env.core.DBSession.connection()
        with open(
            resource_filename(
                "nextgisweb",
                "vector_layer_activity/audit.mako",
            )
        ) as tmpl:
            conn.execute(
                db.text(
                    Template(tmpl.read()).render(
                        table_name=self.identity,
                        tableslist_view_name=self.tableslist_view,
                        schema_prefix="public",
                    )
                )
            )

    def setup_pyramid(self, config):
        from . import api, view

        api.setup_pyramid(self, config)
