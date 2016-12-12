# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from plone.app.registry.browser import controlpanel

from iuem.usersandgroups.interfaces import IIUEMUsersAndGroupsSettings
from iuem.usersandgroups import MessageFactory as _


class IUEMUsersAndGroupsSettingsForm(controlpanel.RegistryEditForm):
    schema = IIUEMUsersAndGroupsSettings
    label = _(u"Users and groups managment")
    description = _(u"IuemUsersAndGroupsSettingsDescription")

    def updateFields(self):
        super(IUEMUsersAndGroupsSettingsForm, self).updateFields()

    def updateWidgets(self):
        super(IUEMUsersAndGroupsSettingsForm, self).updateWidgets()


class IUEMUsersAndGroupsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = IUEMUsersAndGroupsSettingsForm
