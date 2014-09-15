from plone.app.testing import (
    PloneWithPackageLayer,
    IntegrationTesting,
    FunctionalTesting,
)
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2
import iuem.usersandgroups


FIXTURE = PloneWithPackageLayer(
    zcml_filename="configure.zcml",
    zcml_package=iuem.usersandgroups,
    additional_z2_products=[],
    gs_profile_id='iuem.usersandgroups:default',
    name="iuem.usersandgroups:FIXTURE"
)

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="iuem.usersandgroups:Integration"
)

FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,),
    name="iuem.usersandgroups:Functional"
)

ROBOT = FunctionalTesting(
    bases=(AUTOLOGIN_LIBRARY_FIXTURE, FIXTURE, z2.ZSERVER),
    name="iuem.usersandgroups:Robot"
)
