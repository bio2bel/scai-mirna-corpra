# -*- coding: utf-8 -*-

"""Bio2BEL scai-mirna-corpora is a package which allows the user to work with the scai-mirna-corpora.


Installation
------------
Get the Latest
~~~~~~~~~~~~~~~
Download the most recent code from `GitHub <https://github.com/bio2bel/scai-mirna-corpora>`_ with:

.. code-block:: sh

   $ python3 -m pip install git+https://github.com/bio2bel/scai-mirna-corpora.git

For Developers
~~~~~~~~~~~~~~
Clone the repository from `GitHub <https://github.com/bio2bel/scai-mirna-corpora>`_ and install in editable mode with:

.. code-block:: sh

   $ git clone https://github.com/bio2bel/scai-mirna-corpora.git
   $ cd scai-mirna-corpora
   $ python3 -m pip install -e .


Setup
-----
1. Create a :class:`bio2bel_scai-mirna-corpora.Manager` object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> from bio2bel_scai_mirna_corpora import Manager
>>> manager = Manager()

2. Populate the database
~~~~~~~~~~~~~~~~~~~~~~~~
This step will take sometime since the scai-mirna-corpora data needs to be downloaded, parsed, and fed into the database line
by line.

>>> manager.populate()

3. Get all associations to iterate and do magic

>>> associations = manager.list_associations()
"""

from .manager import Manager

__all__ = [
    'Manager',
]

__version__ = '0.0.3-dev'

__title__ = 'bio2bel_scaimc'
__description__ = "A package for converting the SCAI miRNA Corpora to BEL."
__url__ = 'https://github.com/bio2bel/scai-mirna-corpora'

__author__ = 'Mehdi Ali, Dejan Dukic, and Charles Tapley Hoyt'
__email__ = 'charles.hoyt@scai.fraunhofer.de'

__license__ = 'MIT License'
__copyright__ = 'Copyright (c) 2018 Mehdi Ali, Dejan Dukic, and Charles Tapley Hoyt'
