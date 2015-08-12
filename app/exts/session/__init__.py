#!/usr/bin/env python
# coding=utf-8

# This package is simplified from torndsession only keep redis storage. If you
# want to use other driver in your tornado application, you should install
# original torndsession package by pip.

from __future__ import absolute_import
from .session import SessionMixin
from .session_handler import SessionBaseHandler

__all__ = ['SessionMixin', 'SessionBaseHandler']
