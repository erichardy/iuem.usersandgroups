# usefull documentations :
# http://developer.plone.org/forms/z3c.form.html
# http://developer.plone.org/forms/files.html
# http://pythonhosted.org/z3c.form/

import logging
from five import grok
from plone.directives import form
from z3c.form import button
from Products.CMFCore.interfaces import ISiteRoot
from plone.namedfile.field import NamedFile
from zope.component import getUtility

from plone.i18n.normalizer.interfaces import INormalizer
from iuem.usersandgroups.users import IUsers
from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class IImportUsers(form.Schema):
    users_file = NamedFile(
            title=_(u"import a file containing iuem users"),
        )


class importUsers(form.SchemaForm):
    grok.context(IUsers)

    schema = IImportUsers
    ignoreContext = True

    label = _(u"import users file")
    description = _(u"This will create a folder containing users")

    def createUser(self,
                   title=None,
                   gid=None,
                   ssid=None,
                   shell=None,
                   arrival_date=None,
                   departure_date=None):
        self.context.invokeFactory(type_name='iuem.user',
                                   title=title,
                                   gid=gid,
                                   ssid=ssid,
                                   shell=shell,
                                   arrival_date=arrival_date,
                                   departure_date=departure_date)
        return

    def processUsers(self, data):
        # tunes = data.split('\n')
        users = data.split('\n')
        for user in users:
            luser = user.split(':')
            title = luser[0]
            gid = luser[1]
            ssid = luser[2]
            shell = luser[3]
            arrival_date = luser[4]
            departure_date = luser[5]
            self.createUser(title=title,
                            gid=gid,
                            ssid=ssid,
                            shell=shell,
                            arrival_date=arrival_date,
                            departure_date=departure_date)

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        users = data["users_file"].data
        self.processUsers(users)
        self.status = "Thank you very much!"
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
