##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" `browser:cssregistry` directive

$Id$
"""
from zope import interface, event
from zope.security.proxy import getObject
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.lifecycleevent import ObjectModifiedEvent

from zojax.cssregistry.registry import registries
from zojax.cssregistry.property import Property, CSSProperty
from zojax.cssregistry.interfaces import _, ICSSRegistry
from zojax.statusmessage.interfaces import IStatusMessage


class ViewRegistry(object):

    template = ViewPageTemplateFile('view.pt')

    def listRegistries(self):
        regs = []
        for key, registry in registries.items():
            name, layer = key

            regs.append({'name': name or _('Without name'),
                         'layer': '%s.%s'%(layer.__module__, layer.__name__),
                         'registry': registry})

        return regs

    def update(self):
        request = self.request

        if 'form.copy' in request:
            reg = request.get('registry', None)

            registry = self.listRegistries()[int(reg)]['registry']

            for prop, value in registry.items():
                self.context[prop] = CSSProperty(
                    value.name, value.value,
                    value.title, value.description, value.type)

            event.notify(ObjectModifiedEvent(self.context))

            IStatusMessage(request).add(
                _(u"CSS Registry has been copied."))

        if 'form.add' in request:
            name = request.get('form.add.name', '').strip()
            if not name:
                IStatusMessage(request).add(
                    _(u"Can't add property with emtpy name."), 'error')
            else:
                self.context[name] = CSSProperty(
                    name, request.get('form.add.value', ''))

                event.notify(ObjectModifiedEvent(self.context))

        if 'form.remove' in request:
            for prop in request.get('property', ()):
                del self.context[prop]
            event.notify(ObjectModifiedEvent(self.context))
            IStatusMessage(request).add(_(u"Properties have been removed."))

        if 'form.save' in request:
            for key, value in request.form.items():
                if key.startswith('prop-'):
                    key = key[5:]
                    old = self.context[key]
                    property = CSSProperty(
                        old.name, value,
                        old.title, old.description, old.type)

                    self.context[key] = property

            if request.get('form.enabled') == 'yes':
                self.context.enabled = True
            else:
                self.context.enabled = False

            event.notify(ObjectModifiedEvent(self.context))
            IStatusMessage(request).add(_(u"Properties have been changed."))
