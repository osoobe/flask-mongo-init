from datetime import datetime

from application import db


class BaseX:

  date_created = db.DateTimeField(default=datetime.now(), required=True)

  meta = {
    'allow_inheritance': True,
    'indexes': ['-date_created'],
    'ordering': ['-date_created']
  }

  def populate_from_form(self, form):
    for element in form:
      if hasattr(self, element.name):
        setattr(self, element.name, element.data)
