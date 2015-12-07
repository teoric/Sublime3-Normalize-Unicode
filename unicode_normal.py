import sublime
import sublime_plugin
import unicodedata


ST3 = sublime.version() == '' or int(sublime.version()) > 3000


def get_current_encoding(view, default='utf8'):
    """Get the encoding of view, else return default
    """
    view_encoding = view.encoding()
    if view_encoding == 'Undefined':
        view_encoding = view.settings().get('default_encoding', default)

    br1 = view_encoding.find('(')
    br2 = view_encoding.find(')')
    if br2 > br1:
        view_encoding = view_encoding[br1+1:br2].replace(' ', '-')

    return view_encoding


def selections(view, default_to_all=True):
    """Return all non-empty selections in view
    If None, return entire view if default_to_all is True
    """
    regions = [r for r in view.sel() if not r.empty()]

    if not regions and default_to_all:
        regions = [sublime.Region(0, view.size())]

    return regions





class NormalizeUnicode(sublime_plugin.TextCommand):

    def run(self, edit, **args):
        view = self.view
        for region in selections(view):
            s = view.substr(region)
            view.replace(edit, region, unicodedata.normalize(args["nf"], s))
            # äöü
