# -*- coding: utf-8 -*-
from pyramid.events import BeforeRender, subscriber
from sqlalchemy.orm.exc import NoResultFound

from pyramid.httpexceptions import HTTPUnauthorized, HTTPFound, HTTPForbidden
from pyramid.security import remember, forget

from ..object_widget import ObjectWidget
from ..views import ModelController, permalinker
from .. import dynmenu as dm

from .models import SRS

from .util import _


def setup_pyramid(comp, config):

    def check_permission(request):
        """ To avoid interdependency of two components:
        auth and security, permissions to edit users
        are limited by administrators group membership criterion"""

        request.require_administrator()

    class SRSWidget(ObjectWidget):

        def is_applicable(self):
            return self.operation in ('create', 'edit')

        def populate_obj(self):
            super(SRSWidget, self).populate_obj()

            self.obj.display_name = self.data.get('display_name')
            self.obj.auth_name = self.data.get('auth_name')
            self.obj.auth_srid = self.data.get('auth_srid', False)
            self.obj.wkt = self.data.get('wkt', False)

            self.obj.disabled = self.data.get('disabled', False)


        def validate(self):
            result = super(SRSWidget, self).validate()
            self.error = []

            if self.operation == 'create':
                conflict = SRS.filter_by(
                    auth_srid=self.data.get("auth_srid")).first()
                if conflict:
                    result = False
                    self.error.append(dict(
                        message=self.request.localizer.translate(
                            _("SRS is not unique."))))

            return result

        def widget_params(self):
            result = super(SRSWidget, self).widget_params()

            if self.obj:
                result['value'] = dict(
                    display_name=self.obj.display_name,
                    auth_name=self.obj.auth_name,
                    auth_srid=self.obj.auth_srid,
                    wkt=self.obj.wkt,
                    disabled=self.obj.disabled
                )

            return result

        def widget_module(self):
            return 'ngw-spatial-ref-sys/SRSWidget'

    class SRSModelController(ModelController):

        def create_context(self, request):
            check_permission(request)
            return dict(template=dict(
                subtitle=("Create new Spatial Reference System"),
                dynmenu=SRS.__dynmenu__))

        def edit_context(self, request):
            check_permission(request)
            obj = SRS.filter_by(**request.matchdict).one()

            return dict(
                obj=obj,
                template=dict(obj=obj)
            )

        def create_object(self, context):
            return SRS()

        def query_object(self, context):
            return context['obj']

        def widget_class(self, context, operation):
            return SRSWidget

        def template_context(self, context):
            return context['template']

    SRSModelController('srs.list', '/srs/list').includeme(config)

    permalinker(SRS, 'srs.list.edit')

    def srs_browse(request):
        check_permission(request)
        return dict(
            title=('SRS'),
            obj_list=SRS.filter_by(),
            dynmenu=request.env.pyramid.control_panel)

    config.add_route('srs.list.browse', '/srs/list/') \
        .add_view(srs_browse, renderer='nextgisweb:spatial_ref_sys/template/srs_browse.mako')

    class SRSMenu(dm.DynItem):

        def build(self, kwargs):
            yield dm.Link(
                self.sub('browse'), _("List"),
                lambda kwargs: kwargs.request.route_url('srs.list.browse')
            )

            yield dm.Link(
                self.sub('create'), _("Create"),
                lambda kwargs: kwargs.request.route_url('srs.list.create')
            )

            if 'obj' in kwargs and isinstance(kwargs.obj, SRS):
                yield dm.Link(
                    self.sub('edit'), _("Edit"),
                    lambda kwargs: kwargs.request.route_url(
                        'srs.list.edit',
                        id=kwargs.obj.id
                    )
                )

  
    SRS.__dynmenu__ = comp.env.pyramid.control_panel

    comp.env.pyramid.control_panel.add(
        dm.Label('srs-list', _("SRS")),
        SRSMenu('srs-list'),
    )

