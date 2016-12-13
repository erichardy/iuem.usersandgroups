# usefull documentations :
# http://developer.plone.org/forms/z3c.form.html
# http://developer.plone.org/forms/files.html
# http://pythonhosted.org/z3c.form/

import logging
from plone.directives import form
from z3c.form import button
from plone.namedfile.field import NamedFile

from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class IImportUsers(form.Schema):
    users_file = NamedFile(
            title=_(u"import a file containing iuem users"),
        )


class importUsers(form.SchemaForm):

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
        context = self.context
        try:
            context.invokeFactory('iuem.user',
                                  title,
                                  title=title,
                                  gid=gid,
                                  ssid=ssid,
                                  shell=shell,
                                  arrival_date=arrival_date,
                                  departure_date=departure_date)
        except:
            logger.info('User already in directory:' + title)

        return

    def processUsers(self, data):
        # tunes = data.split('\n')
        users = data.split('\n')
        for user in users:
            luser = user.split(':')
            logger.info(luser)
            if len(luser) == 6:
                title = luser[0]
                try:
                    gid = int(luser[1])
                except:
                    gid = 999
                ssid = luser[2]
                shell = luser[3]
                arrival_date = luser[4]
                """
                if arrival_date == 'DATE_ARRIVEE':
                    arrival_date = None
                departure_date = luser[5]
                if departure_date == 'DATE_DEPART':
                    departure_date = None
                """
                # actuellement, on ne gere pas les dates arrivee et depart !
                arrival_date = None
                departure_date = None
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
