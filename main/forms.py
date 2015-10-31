from flask.ext import wtf


class BaseForm(wtf.Form):

    # Used to map data from a datastore entity to a form
    # which has identitical field name
    def populate_from_obj(self, obj):
        for key in obj:
            if key in form:
                form[key].data = getattr(obj, key)
