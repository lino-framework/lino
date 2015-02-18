=====================
Using action requests
=====================

An action request is when a given user asks to run a given action of a
given actor.

Action requests are instances of the
:class:`BaseRequest<lino.core.requests.BaseRequest>` class or one of
its subclasses (:class:`ActorRequest<lino.core.requests.ActorRequest>`
:class:`ActionRequest<lino.core.requests.ActionRequest>`
:class:`TableRequest<lino.core.tablerequest.TableRequest>`.

The traditional variable name for action requests in application code
and method signatures is ``ar``.  Except for the plain `BaseRequest`
instance returned by :func:`rt.login<lino.api.rt.login>`. This is
often called ``ses`` since you can imagine it as a session.

As a rough approximation you can say that every Django web request
gets wrapped into an action request.  The ActionRequest adds some more
information about the "context" (like the "renderer" being used) and
provides the application with methods to communicate with the user.

But there are exceptions to this approximaton.


- :meth:`show <lino.core.requests.BaseRequest.show>` 

- :meth:`set_response <lino.core.requests.BaseRequest.set_response>` 


- :meth:`ba.request_from <lino.core.boundaction.BoundAction.request_from>`
- :meth:`lino.core.request.get_permission`
- :meth:`lino.core.request.set_action_param_values`
- :meth:`lino.core.request.ar2button`

