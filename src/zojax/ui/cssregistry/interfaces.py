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
""" zojax.cssregistry interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zojax.cssregistry.interfaces import ICSSRegistry

_ = MessageFactory('zojax.ui.cssregistry')


class ICSSRegistryConfiglet(ICSSRegistry):
    """ css registry configlet """

    enabled = schema.Bool(
        title = _(u'Enabled'),
        default = False,
        required = True)
