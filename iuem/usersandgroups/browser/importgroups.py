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


class IImportGroups(form.Schema):
    groups_file = NamedFile(
            title=_(u"import a file containing iuem groups"),
        )


class importGroups(form.SchemaForm):

    schema = IImportGroups
    ignoreContext = True

    label = _(u"import groups file")
    description = _(u"This will create a folder containing groups")

    def creatGroup(self,
                   title=None,
                   gid=None,
                   more_users=None,
                   ):
        self.context.invokeFactory('iuem.group',
                                   title,
                                   title=title,
                                   gid=gid,
                                   more_users=more_users,
                                   )
        return

    def processGroups(self, data):
        # tunes = data.split('\n')
        groups = data.split('\n')
        for group in groups:
            logger.info(group)
            lgroup = group.split(':')
            if len(lgroup) == 4:
                title = lgroup[0]
                try:
                    gid = int(lgroup[2])
                except:
                    gid = 999
                more_users = lgroup[3]
                logger.info(group)
                self.creatGroup(title=title,
                                gid=gid,
                                more_users=more_users,
                                )

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        groups = data["groups_file"].data
        self.processGroups(groups)
        self.status = "Thank you very much!"
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
