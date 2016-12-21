

==========================
Les cron à mettre en place
==========================

Les commandes
=============

Les ``crontab`` peuvent servir à lancer périodiquement les synchronisation des mots
de passe et des groupes entre l'annuaire ``LDAP`` et les comptes et groupes locaux.

C'est ici que l'on fait usage de la clé qui est définie dans la configuration du module. Par défaut,
cette clé a pour valeur ``abcdef``. Nous prendrons cette valeur pour les exemples ci-dessous.

D'autre part, pour les exemples donnés ci-dessous, on utilisera l'URL d'une instance de
développement ``http://localhost:8080/Plone`` comme URL de base. Cette URL devra être remplacée
par l'URL de la racine du site pour lequel on installe la synchronisation.

**La commande à lancer pour la synchronisation des mots de passe**::

   wget http://localhost:8080/Plone/@@pw-update?key=abcdef -O /dev/null

On pourra voir dans les logs les traces de cette opération::
   
   2016-12-21 13:34:45 INFO iuem.usersandgroups:utils Starting update passwords at 2016-12-21 13:34:45.557769
   2016-12-21 13:34:47 INFO iuem.usersandgroups:utils Cannot update password for coco
   2016-12-21 13:34:52 INFO iuem.usersandgroups:utils Update passwords finished at 2016-12-21 13:34:52.840790

.. note:: ici, le compte local ``coco`` n'est (évidemment) pas mis à jour.

**La commande pour la synchronisation des groupes**::

   wget http://localhost:8080/Plone/@@groups-update?key=abcdef -O /dev/null

Les logs feront apparaître aussi les groupes locaux qui ne sont pas mis à jour::

   2016-12-21 13:36:52 INFO iuem.usersandgroups:groups_update Local group not updated : Administrators
   2016-12-21 13:36:52 INFO iuem.usersandgroups:groups_update Local group not updated : Reviewers
   2016-12-21 13:36:52 INFO iuem.usersandgroups:groups_update Local group not updated : Site Administrators
   2016-12-21 13:36:52 INFO iuem.usersandgroups:groups_update Local group not updated : AuthenticatedUsers 


.. note:: dans les deux cas, si la clé passée en paramètre n'est pas la bonne, ceci est indiqué dans les logs.

::

   2016-12-21 13:35:25 INFO iuem.usersandgroups:passwords_update Access key doesn't match required key !!!!

Installation des cron
=====================

Comme pour tout système, il sera possible d'installer les ``cron`` avec la commande ``crontab -e``.

Par exemple, pour lancer les synchronisations::

   6 8,13,18 * * *  /usr/bin/wget http://myplone:8080/Plone2/@@pw-update?key=abcdef -O /dev/null
   15 8,13,18 * * *  /usr/bin/wget http://myplone:8080/Plone2/@@groups-update?key=abcdef -O /dev/null

La synchronisation des mots de passe se fera à 8h06m, 13h06m et 18h06m. Celle des groupes à 8h15m,
13h15m et 18h15m.



