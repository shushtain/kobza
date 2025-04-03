"""Stores global variables in a thread-safe manner."""

from threading import local

ctx = local()
