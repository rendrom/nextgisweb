# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from .. import db
from ..env import env
from ..resource import Serializer, SerializedProperty, ResourceScope
from ..models import declarative_base
from ..vector_layer import VectorLayer

from .util import COMP_ID

Base = declarative_base()

PR_READ = ResourceScope.read
PR_UPDATE = ResourceScope.update


class VectorLayerActivity(Base):
        __tablename__ = COMP_ID

        event_id = db.Column(db.Integer, primary_key=True)
        schema_name = db.Column(db.Unicode, nullable=False)
        table_name = db.Column(db.Unicode, nullable=False, index=True)
        relid = db.Column(db.Integer, nullable=False, index=True)
        session_user_name = db.Column(db.Unicode)
        action_tstamp_tx = db.Column(db.DateTime, nullable=False)
        action_tstamp_stm = db.Column(db.DateTime, nullable=False, index=True)
        action_tstamp_clk = db.Column(db.DateTime, nullable=False)
        transaction_id = db.Column(db.BigInteger)
        application_name = db.Column(db.Unicode)
        client_addr = db.Column(db.postgresql.INET)
        client_port = db.Column(db.Integer)
        client_query = db.Column(db.Unicode)
        action = db.Column(db.Enum('I', 'D', 'U', 'T'), nullable=False, index=True)
        row_data = db.Column(db.MutableDict.as_mutable(db.postgresql.HSTORE))
        changed_fields = db.Column(db.MutableDict.as_mutable(db.postgresql.HSTORE))
        statement_only = db.Column(db.Boolean, nullable=False)


class _enbled_attr(SerializedProperty):
    def getter(self, srlzr):
        conn = env.core.DBSession.connection()
        layer = "layer_%s" % srlzr.obj.tbl_uuid
        query = db.text(
            "SELECT 1 FROM %s WHERE auditedtable = :layer"
            % env.vector_layer_activity.tableslist_view
        )
        return (
            conn.execute(query, layer=layer).scalar()
            is not None
        )

    def setter(self, srlzr, value):
        conn = env.core.DBSession.connection()
        layer = "vector_layer.layer_%s" % srlzr.obj.tbl_uuid
        if value:
            query = db.text("SELECT audit_table(:layer)")
            conn.execute(query, layer=layer)
        else:
            query = db.text(
                "DROP TRIGGER audit_trigger_row ON %(layer)s;"
                "DROP TRIGGER audit_trigger_stm ON %(layer)s;"
                % {"layer": layer}
            )
            conn.execute(query)


class VectorLayerActivitySerializer(Serializer):
    identity = COMP_ID
    resclass = VectorLayer

    enabled = _enbled_attr(read=PR_READ, write=PR_UPDATE)
