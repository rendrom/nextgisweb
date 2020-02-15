# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals
from datetime import datetime
from collections import OrderedDict

from pyramid.httpexceptions import HTTPNotFound

from .. import dynmenu as dm
from .api import audit_cget
from .util import _, es_index, audit_context


def journal_browse(request):
    request.require_administrator()

    date_from = request.params.get("date_from")
    date_to = request.params.get("date_to")
    date_last = request.params.get("date_last")
    user = request.params.get("user")

    hits = audit_cget(
        request=request,
        date_from=date_last or date_from,
        date_to=date_to,
        user=user,
        limit=None
    )

    return dict(
        title=_("Journal"),
        maxwidth=True,
        hits=list(hits),
        date_from=date_from,
        date_to=date_to,
        user=user,
        dynmenu=request.env.pyramid.control_panel)


def journal_show(request):
    request.require_administrator()
    rid = request.matchdict['id']

    timestamp = datetime.now()
    index = es_index(timestamp)

    docs = request.env.audit.es.search(
        index=index,
        body=dict(query=dict(
            ids=dict(values=[rid, ])
        )))

    hits = docs['hits']
    if hits['total']['value'] != 1:
        raise HTTPNotFound()

    doc = hits['hits'][0]

    return dict(
        title=_("Journal record: %s") % rid, doc=doc,
        dynmenu=request.env.pyramid.control_panel)


def setup_pyramid(comp, config):
    # This method can be called from other components,
    # so should be enabled even audit component disabled.
    config.add_request_method(audit_context)

    if comp.audit_enabled:
        config.add_tween(
            'nextgisweb.audit.util.elasticsearch_tween_factory',
            under=('nextgisweb.pyramid.util.header_encoding_tween_factory',))

        config.add_route(
            'audit.control_panel.journal.browse',
            '/control-panel/journal/'
        ).add_view(journal_browse, renderer='nextgisweb:audit/template/browse.mako')

        config.add_route(
            'audit.control_panel.journal.show',
            '/control-panel/journal/{id}'
        ).add_view(journal_show, renderer='nextgisweb:audit/template/show.mako')

        comp.env.pyramid.control_panel.add(
            dm.Label('audit', _("Audit")),
            dm.Link('audit/journal', _("Journal"), lambda args: (
                args.request.route_url('audit.control_panel.journal.browse'))),
        )