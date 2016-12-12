# -*- coding: utf-8 -*-

import logging
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
    form.primary('title')
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
            title=_(u"user id"),
            description=_("user id"),
            required=True,
            )
    dexteritytextindexer.searchable('gid')
    gid = schema.Int(
          title=_(u'gid number'),
          description=_(u"primary group"),
          required=True
          )
    ssid = schema.TextLine(
            title=_(u"ssid"),
            description=_("Samba SID"),
            required=True,
            )
    shell = schema.TextLine(
            title=_(u"user shell"),
            description=_("shell launched at unix loggin"),
            required=True,
            )
    arrival_date = schema.Datetime(
            title=_(u"user arrival"),
            description=_(u"when the user starts to work at IUEM"),
            required=False,
            )
    departure_date = schema.Datetime(
            title=_(u"user departure"),
            description=_(u"when the user ends to work at IUEM"),
            required=False,
            )


class User(Item):
