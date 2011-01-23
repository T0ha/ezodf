#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: observer pattern
# Created: 22.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from weakref import WeakSet

class Observer:
    """ Simple implementation of the observer pattern for broadcasting messages
    to objects.

    For every event the subscriber object need an event handler called 'on_event_handler'
    accepting the parameter 'msg'.

    Because of the simple implementation of the algorithm it is neccessary to
    register the objects an not only the listener methods, because the methods of
    different objects of the same calss have the same 'id' and managing the
    listeners in a WeakSet is not possible for different objects (you could
    only manage one table in one document instance).

    Example for event: 'save'
        # module 'one'
        class Listener:
            def on_save_handler(self, msg):
                pass

        listener = Listener()
        observer.subscribe('save', listener)

        # module 'two'
        # calls listener.on_save_handler(msg=None)
        observer.broadcast('save', msg=None)
    """
    # TODO: By one global observer-object, if more than one document is opened,
    # the event is send to all documents, the receiver can not distingush if
    # the sender is its own document-object or not.
    # SOLVED: No global observer-object, every document has its own observer-object
    # and objects have to know their own document-object to subscribe an events.
    #
    #    document.observer.subscribe('save', listener)
    #    document.observer.broadcast('save', msg=None)

    def __init__(self):
        self._listeners = dict()

    def subscribe(self, event, listener_object):
        event_handler_name = "on_%s_handler" % event
        if not hasattr(listener_object, event_handler_name):
            raise AttributeError("Listener object has no '%s' event handler." % event)
        try:
            event_listeners = self._listeners[event]
        except KeyError:
            event_listeners = WeakSet()
            self._listeners[event] = event_listeners
        event_listeners.add(listener_object)

    def unsubscribe(self, event, listener_object):
        """ Unsubscribing for objects which will be destroyed is not neccessary,
        just unsubscribe objects that should not receive further messages.
        """
        event_listeners = self._listeners[event]
        event_listeners.remove(listener_object)

    def broadcast(self, event, msg=None):
        try:
            event_listeners = self._listeners[event]
        except KeyError:
            # ok, because there is just no listener for this event
            # but mispelling of 'event' is an error trap
            return
        event_handler_name = "on_%s_handler" % event
        for listener in event_listeners:
            method = getattr(listener, event_handler_name)
            method(msg=msg)

    def _has_listener(self, event):
        # just for testing
        return self._count_listeners(event) > 0

    def _count_listeners(self, event):
        # just for testing
        try:
            return len(self._listeners[event])
        except KeyError:
            return 0
