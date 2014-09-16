# -*- coding: utf-8 -*-

import logging
from five import grok
from plone import api
# from plone.directives import dexterity, form
from plone.directives import form

from plone.supermodel import model
from plone.dexterity.content import Item
from zope.interface import alsoProvides
from plone.autoform.interfaces import IFormFieldProvider
from collective import dexteritytextindexer

from zope import schema
from zope.interface import Invalid

from plone.namedfile.field import NamedBlobFile

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class IUser(form.Schema):
    title = schema.TextLine(
            title=_(u"user id"),
            description=_("user id"),
            required=True,
            )



class User(Item):
    grok.implements(IUser)
