==========
goblingate
==========

Installation
------------

::

    $ cd ~/projects/goblingate
    
    # for dev
    $ sudo pip install -e .   
    
    # or optionally for deployment (not necessary)
    $ sudo pip install .

Settings
--------

Create a copy of  ``data/settings_template.yml`` at  ``~/.goblingate/settings.yml`` if does not exist and fill in details.


Help
----

::

   # available sub packages
   $ goblingate -h

   # help on specific subpackage, e.g water_level
   $ goblingate water_level -h
   
   
   
Run
---

::

    # start water level monitoring
    $ goblingate water_level
   

Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
