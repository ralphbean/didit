import optparse
import subprocess
import tempfile
import shelve
import datetime
import sys
import os
import os.path

from tw2.core.dottedtemplatelookup import DottedTemplateLookup
lookup = DottedTemplateLookup(input_encoding='utf-8',
                              output_encoding='utf-8',
                              imports=[],
                              default_filters=[])

relpath = "~/.didit"
abspath = os.path.expanduser("~/.didit")
message_template = """

.. What did you do?  Whatever you type above will be logged
   to file in the ``{category}`` category.
   This is a comment block by the way and will be ignored.
   `didit` messages respect ``reStructuredText``.
"""

def _global_options(parser):
    parser.add_option("-c", "--category", dest="category",
                      default="general")
    return parser

def parse_options_remember():
    parser = optparse.OptionParser()
    parser.add_option("-m", "--message", dest="message",
                      help="message to remember")
    parser = _global_options(parser)
    return parser.parse_args()

def parse_options_report():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--timespan", dest="timespan",
                      help="timespan for the report")
    parser.add_option("-C", "--categories", dest="categories",
                      default="",
                      help="comma-separated list of categories")
    parser = _global_options(parser)
    return parser.parse_args()

def process_data(d):
    _fmt = '%Y-%m-%dT%H:%M:%S'
    fmt = lambda s : datetime.datetime.strptime(s[:-7], _fmt)
    return dict([(fmt(k), v) for k, v in d.iteritems()])

def report():
    options, args = parse_options_report()

    if not options.timespan:
        options.timespan = 'week'

    tmpl = lookup.get_template('didit.templates.report')

    options.category = [options.category]
    if options.categories:
        options.category = [c.strip() for c in options.categories.split(',')]

    data = {}
    for category in options.category:
        filename = "{abspath}/{category}.db".format(
            abspath=abspath, category=category)
        d = shelve.open(filename)
        data.update(process_data(d))
        d.close()

    options = {
        'category' : ", ".join(options.category),
        'timespan' : options.timespan,
        'data' : data,
    }

    print tmpl.render(**options)


def remember():
    options, args = parse_options_remember()
    tmpl = message_template.format(category=options.category)

    if not options.message:
        filename = tempfile.mkstemp(suffix=__name__+".rst")[1]
        with open(filename, 'w') as f:
            f.write(tmpl)
        ret = subprocess.call(['$EDITOR %s' % filename], shell=True)
        if ret:
            print "Problem with $EDITOR.  Aborting."
            sys.exit(0)
        with open(filename, 'r') as f:
            options.message = f.read()

    message = options.message
    # If anything like the template is still in the message, then remove it
    if message.endswith(tmpl[2:]): message = message[:-len(tmpl[2:])]

    # Strip whitespace
    message = message.strip()

    # Abort if they didn't enter anything.
    if not message:
        print "No message.  Aborting."
        return

    filename = "{abspath}/{category}.db".format(
        abspath=abspath, category=options.category)

    if not os.path.exists(abspath) and not os.path.isdir(abspath):
        os.mkdir(abspath)

    now = datetime.datetime.now().isoformat()
    d = shelve.open(filename)
    d[now] = message
    d.close()
    print now, "-- Wrote to python shelve", filename
