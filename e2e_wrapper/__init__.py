# -*- coding: utf-8 -*-

import logging

from .__version__ import __version__
from .e2e_wrapper import parse, get_naf

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Dafne van Kuppevelt"
__email__ = 'd.vankuppevelt@esciencecenter.nl'
