# -*- coding: utf-8 -*-
import json
import aniso8601

from pyramid.response import Response
from shapely.geometry import mapping
from shapely import wkb

from ..feature_layer import IAuditableFeatureLayer
from ..resource import resource_factory, DataScope
from .model import VectorLayerActivity

PERM_READ = DataScope.read


def cget(resource, request):
    request.resource_permission(PERM_READ)

    limit = request.GET.get("limit")
    offset = request.GET.get("offset", 0)
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    action = request.GET.get("action")

    fld_map = {
        "fld_%s" % f.fld_uuid: f.keyname
        for f in resource.fields
    }

    def prepare(item):
        if item is None:
            item = {}

        prepared = {
            fld_map[key]: value
            for key, value in item.items()
            if key not in ("id", "geom")
        }

        if "id" in item:
            prepared["id"] = item["id"]

        if "geom" in item:
            prepared["geom"] = mapping(
                wkb.loads(item["geom"], hex=True)
            )
        return prepared

    query = (
        VectorLayerActivity.filter_by(
            table_name="layer_%s" % resource.tbl_uuid
        )
        .order_by(VectorLayerActivity.action_tstamp_stm)
    )

    if action is not None:
        query = query.filter_by(action=action)

    if date_from is not None:
        query = query.filter(
            VectorLayerActivity.action_tstamp_stm
            >= aniso8601.parse_datetime(date_from)
        )

    if date_to is not None:
        query = query.filter(
            VectorLayerActivity.action_tstamp_stm
            <= aniso8601.parse_datetime(date_to)
        )

    query = query.limit(limit).offset(offset)

    result = []
    for item in query.all():
        data = prepare(item.row_data)
        data.update(prepare(item.changed_fields))
        result.append(
            dict(
                data=data,
                tstamp=item.action_tstamp_stm.isoformat(),
                action=item.action,
            )
        )

    return Response(
        json.dumps(result), content_type=b"application/json"
    )


def setup_pyramid(comp, config):
    config.add_route(
        "vector_layer_activity.collection",
        "/api/resource/{id}/activity/",
        factory=resource_factory,
    ).add_view(
        cget,
        context=IAuditableFeatureLayer,
        request_method="GET",
    )
