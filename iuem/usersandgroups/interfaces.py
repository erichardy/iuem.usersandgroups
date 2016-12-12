# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
import logging

from zope import schema
from zope.interface import Interface
from zope.interface import provider
from zope.interface import Invalid, invariant
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form.interfaces import IEditForm
from z3c.relationfield.schema import RelationChoice

from plone.supermodel import model
# from plone.registry.field import SourceText
from plone.autoform import directives as form
import datetime


from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('ubl.tebl:interfaces')
#


class IIUEMUsersAndGroupsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IIUEMUsersAndGroupsSettings(Interface):
    """Settings"""
    ldap_uri = schema.TextLine(
        title=_(u"ldap uri"),
        description=_(u"in the form of : ldap://...."),
        required=True,
        default=u"ldap://annuaire-iuem.univ-brest.fr",
        )

