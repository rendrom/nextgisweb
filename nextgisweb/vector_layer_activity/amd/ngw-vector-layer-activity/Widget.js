/* globals define */
define([
    "dojo/_base/declare",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "ngw-resource/serialize",
    "ngw-pyramid/i18n!vector_layer_activity",
    "ngw-pyramid/hbs-i18n",
    "dojo/text!./template/Widget.hbs"
], function (
    declare,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    serialize,
    i18n,
    hbsI18n,
    template
) {
    return declare([_WidgetBase, serialize.Mixin, _TemplatedMixin, _WidgetsInTemplateMixin], {
        serializePrefix: "vector_layer_activity",
        title: i18n.gettext("Activity"),
        templateString: hbsI18n(template, i18n)
    });
});
