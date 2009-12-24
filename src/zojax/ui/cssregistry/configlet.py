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
"""

$Id$
"""
from BTrees.OOBTree import OOBTree
from zope import interface, component
from zope.component import getUtility

from zojax.cssregistry.registry import CSSRegistry, registries
from zojax.cssregistry.interfaces import ICSSRegistry, ICSSRegistryLayer

from interfaces import ICSSRegistryConfiglet


class CSSRegistryConfiglet(CSSRegistry):
    """ css registry configlet """
    interface.implements(ICSSRegistryConfiglet)

    @property
    def properties(self):
        properties = self.data.get('properties')
        if properties is None:
            properties = OOBTree()
            self.data['properties'] = properties

        return properties


@interface.implementer(ICSSRegistry)
@component.adapter(ICSSRegistryLayer, interface.Interface)
def portalCssRegistry(layer, request):
    css = getUtility(ICSSRegistryConfiglet)
    if css.enabled:
        return css
