
====================================
Documentation de iuem.usersandgroups
====================================
.. _IUEM: http://www-iuem.univ-brest.fr
.. _DocPlone: http://docs.plone.org/about/documentation_styleguide_addons.html
.. _Sphinx: http://sphinx-doc.org/

Documentation de ``iuem.usersandgroups`` dévéloppé à l'`IUEM`_.

Voir les recommandations pour la documentation a `DocPlone`_

Voir aussi Sphinx : `Sphinx`_


Installation
============
Ajouter *iuem.usersandgroups* à la liste definie par la variable ``eggs`` dans la
section ``[instance]`` du fichier *buildout.cfg*

et la source dans la section ``[sources]``::

   iuem.usersandgroups = git gitiuem:iuem.usersandgroups.git

Motivation
==========

Le module iuem.usersandgroups a été développé en raison des difficultés rencontrées
pour *brancher* un site *Plone 5* sur ``LDAP`` de la même manière que cela était réalisé
avec les sites *Plone 4*. C'est-à-dire que l'authentification, la gestion des comptes
utilisateurs et des groupes soit pris en charge entièrement pas l'annuaire ``LDAP``.

De ce fait, ce module réalise les opérations suivantes :

* il offre une vue qui contient la liste des groupes de l'annuaire ``LDAP``

* il permet de créer localement des groupes qui sont des miroirs des groupes ``LDAP``

* il gère la création des comptes des utilisateurs qui sont membres des groupes créés

* lors de la suppression d'un groupe, il supprime automatiquement les comptes des
  utilisateurs lorsque ceux-ci ne sont membres d'aucun autre groupe


Toute la documentation
======================

.. toctree::
    :maxdepth: 2

    Le README du package <README>
    Les types de contenu <content_types>
