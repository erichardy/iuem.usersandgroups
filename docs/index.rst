
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

Principe général
================

A l'IUEM, nous disposons d'un annuaire LDAP qui est un méta annuaire composé de l'annuaire
``LDAP`` de l'UBO et d'un annuaire local à l'IUEM. Ce dernier contient les groupes
qui satisfont aux usages de nos services et une branche ``people`` qui contient des
comptes utilisateurs extérieurs, qui ne sont donc pas dans l'annuaire de l'UBO.
De ce fait, les comptes des utilisateurs extérieurs commencent tous par ``ext_``.

**Par ce module, on gère les utilisateurs par l'intermédiaire des groupes**. De ce fait, on ne
crée pas ou ne supprime pas de compte d'utilisateur directement, ces opérations se font au
travers de la création ou de la suppression des groupes.

.. note:: l'idée de base part du principe qu'un compte utilisateur n'existe que parce que
   celui-ci est membre d'un groupe. S'il n'est membre d'aucun groupe, le compte est
   automatiquement supprimé. 


Motivation
==========

Le module iuem.usersandgroups a été développé en raison des difficultés rencontrées
pour *brancher* un site *Plone 5* sur ``LDAP`` de la même manière que cela était réalisé
avec les sites *Plone 4*. C'est-à-dire que l'authentification, la gestion des comptes
utilisateurs et des groupes soit pris en charge entièrement par l'annuaire ``LDAP``.

Ce module réalise les opérations suivantes :

* il offre une vue qui contient la liste des groupes de l'annuaire ``LDAP``

* par cette vue, il permet de créer localement des groupes qui sont des miroirs des groupes ``LDAP``

* il gère la création des comptes des utilisateurs qui sont membres des groupes créés

* lors de la suppression d'un groupe, il supprime automatiquement les comptes des
  utilisateurs lorsque ceux-ci ne sont membres d'aucun autre groupe

* il permet la synchronisation des mots de passe entre l'annuaire ``LDAP`` et les comptes locaux

* il permet la synchronisation de la composition des groupes entre l'annuaire ``LDAP`` et les groupes locaux

Toute la documentation
======================

.. toctree::
    :maxdepth: 2

    L'installation <install>
    La configuration <config>
    Droits pour accéder à la gestion des utilisateurs et groupes <permissions>
    La vue de gestion des groupes <view>
    Les cron à mettre en place <cron>
