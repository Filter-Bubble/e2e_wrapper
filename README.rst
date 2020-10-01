.. image:: https://travis-ci.com/Filter-Bubble/e2e_wrapper.svg?branch=master
    :target: https://travis-ci.com/Filter-Bubble/e2e_wrapper
################################################################################
e2e wrapper for NAF files
################################################################################

This is a wrapper around `e2e-Dutch <https://github.com/Filter-Bubble/e2e-Dutch>`_ that produces `NAF files <http://wordpress.let.vupr.nl/naf/>`_
with coreference.
It is designed to use as a component in the `NewsReader pipeline <https://vu-rm-pip3.readthedocs.io/en/latest/home.html>`__. Ït currently only works for Dutch.


Installation
------------

To install e2e_wrapper, do:

.. code-block:: console

  git clone https://github.com/Filter-Bubble/e2e_wrapper.git
  cd e2e_wrapper
  pip install .


Run tests (including coverage) with:

.. code-block:: console

  python setup.py test




Contributing
************

If you want to contribute to the development of e2e wrapper for NAF files,
have a look at the `contribution guidelines <CONTRIBUTING.rst>`_.

License
*******

Copyright (c) 2019, Netherlands eScience Center

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



Credits
*******

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ and the `NLeSC/python-template <https://github.com/NLeSC/python-template>`_.
