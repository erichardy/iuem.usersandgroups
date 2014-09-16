# -*- coding: utf-8 -*-

import logging
from five import grok
from zope import schema
from plone.directives import dexterity, form
from plone import api


from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container

from zope.interface import invariant, Invalid
from zope.interface import alsoProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.component.hooks import getSite

from Products.CMFCore.utils import getToolByName

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from collective import dexteritytextindexer
from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class Ildapdirectory(form.Schema):

    port_number = schema.Text(
                    title=_(u"port number"),
                    description=_(u'port description'),
                    )


class ldapdirectory(Container):
    grok.implements(Ildapdirectory)
