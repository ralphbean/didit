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
    parser.add_option("-c", "--category", dest="category")
    return parser

def parse_options_remember():
    parser = optparse.OptionParser()
    parser.add_option("-m", "--message", dest="message",
                      help="message to remember")
    parser.add_option("-f", "--force", dest="force",
                      default=False, action="store_true",
                      help="forcibly create a category")
    parser = _global_options(parser)
    return parser.parse_args()

def parse_options_report():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--days", dest="days",
                      help="number of days spanning the report")
    parser.add_option("-C", "--categories", dest="categories",
                      default="",
                      help="comma-separated list of categories")
    parser.add_option("-l", "--list", dest="list",
                      default=False, action="store_true",
                      help="show a list of all categories")
    parser = _global_options(parser)
    return parser.parse_args()

def process_data(d):
    _fmt = '%Y-%m-%dT%H:%M:%S'
    fmt = lambda s : datetime.datetime.strptime(s[:-7], _fmt)
    return dict([(fmt(k), v) for k, v in d.iteritems()])

def all_categories():
    for fname in os.listdir(abspath):
        if not fname.endswith('.db'):
            continue
        yield fname[:-3]

def list_categories():
    print "Categories (stored in {abspath}):".format(abspath=abspath)
    for cname in all_categories():
        print "", fname[:-3]

def report():
    options, args = parse_options_report()

    if options.list:
        list_categories()
        return

    if not options.days:
        options.days = '7'

    try:
        options.days = int(options.days)
    except ValueError as e:
        print "Timespan must be an integer (number of days).  Aborting."
        sys.exit(3)

    begin = datetime.datetime.now()-datetime.timedelta(days=options.days)

    tmpl = lookup.get_template('didit.templates.report')

    categories = []
    if options.category:
        categories = [options.category]
    if options.categories:
        categories = [c.strip() for c in options.categories.split(',')]

    if not categories:
        categories = all_categories()

    for category in categories:
        data = {}
        filename = "{abspath}/{category}.db".format(
            abspath=abspath, category=category)
        d = shelve.open(filename)
        data.update(process_data(d))
        d.close()

        # Filter out old message
        data = dict(
            [
                (timestamp, message) for timestamp, message in data.iteritems()
                if timestamp > begin
            ]
        )

        render_opts = {
            'category' : category,
            'timespan' : options.days,
            'data' : data,
        }

        print tmpl.render(**render_opts)


def remember():
    options, args = parse_options_remember()

    if not options.category:
        print "You must specify a category.  Aborting."
        sys.exit(1)

    filename = "{abspath}/{category}.db".format(
        abspath=abspath, category=options.category)

    if not os.path.isfile(filename) and not options.force:
        print "Category '{category}' does not exist.  Use --force.".format(
            category=options.category)
        sys.exit(2)

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
