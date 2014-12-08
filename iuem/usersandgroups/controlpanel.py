# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from plone.app.registry.browser import controlpanel

from iuem.usersandgroups import MessageFactory as _


class IUsersAndGroupsSettings (Interface):
    # fileds do display ????
    # make fieldsets
    pass


class UsersAndGroupsSettingsForm(controlpanel.RegistryEditForm):
    schema = IUsersAndGroupsSettings
    label = _(u"ZABrI Projects Settings")
    description = _(u"ZabriProjectSettingsDescription")

    def updateFields(self):
        super(UsersAndGroupsSettingsForm, self).updateFields()

    def updateWidgets(self):
        super(UsersAndGroupsSettingsForm, self).updateWidgets()


class UsersAndGroupsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = UsersAndGroupsSettingsForm
