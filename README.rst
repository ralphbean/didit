didit
-----

Lightweight, commandline tool for keeping track of wtf I did last week.

.. split here

The Problem
-----------

    `Timeclocks are too cumbersome -- just keep track of the things I did.`

In my job, I tend to do a lot of development which involves losing track of
time and getting lost in other peoples' code.  I **also** happen to do user
support which involves reacting to received emails, phone calls, and
disturbances I notice on our systems.

Every two weeks, I have to report on "what I've been doing for the past two
weeks" and tend to forget everything of importance (who I helped which
actually translates to `who owes us something`) and only remember all the
things that are really important to me -- my code.

All the time tracking tools I investigated (including the `online ones
<http://www.toggl.com/>`_ and even the command line ones (`this one
<http://pypi.python.org/pypi/Hammertime/0.1.3>`_ was the coolest)) were too
cumbersome.  I didn't want to keep track of *exactly* how much time I spent
doing X, Y, and Z, I didn't want to remember to punch in and out of my own
workspace.  Thus, I wrote ``didit`` one afternoon.

Features:
 - Simple, CLI, and doesn't impose timeclock behavior on your otherwise
   flexible self.
 - Respects ``.rst`` markup just like `pypi` and `python`.
 - Will look for an ``$EDITOR`` environment variable when it needs one.
 - Keeps its database(s) in python ``shelve`` files in a ``~/.didit/``
   folder making it easy to reference your done-deals from other python
   code should you want to.

There are too many tools like this out there.  This one isn't a game-changer,
but its about as simple as can be.

I hope you like it.

Installation
------------
::

    % sudo pip install diddit

Usage
-----
::

    % didit-remember -c work -m 'Wrote `diddit`.  Thank god.'
    % didit-remember --message 'Helped L. User parallelize his ``Mathematica`` code.'
    % didit-remember -c personal       # <-- This launches `vim` for me!

    % didit-report --categories=work,general,personal
    Category 'work, general, personal' over timespan 'week'
    -------------------------------------------------------

    ----

    2011-05-05:

      - Wrote `diddit`.  Thank god.
      - Helped L. User parallelize his ``Mathematica`` code.
      - Drank a beer.

One of the benefits of ``.rst``::

    % didit-report --category=work > thisweek.rst && rst2pdf thisweek.rst

Get the source
--------------

...from my `github account <http://github.com/ralphbean/didit>`_ and make it better!
