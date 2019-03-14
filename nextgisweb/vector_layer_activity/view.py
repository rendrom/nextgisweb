# -*- coding: utf-8 -*-
from ..resource import Widget
from ..vector_layer import VectorLayer


class VectorLayerActivityWidget(Widget):
    resource = VectorLayer
    operation = ('create', 'update')
    amdmod = 'ngw-vector-layer-activity/Widget'
