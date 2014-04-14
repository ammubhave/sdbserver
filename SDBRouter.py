class SDBRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read directory models go to sdb.
        """
        if model._meta.app_label == 'directory':
            return 'sdb'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write directory models go to sdb.
        """
        if model._meta.app_label == 'directory':
            return 'sdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'directory' or \
           obj2._meta.app_label == 'directory':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == 'sdb':
            return model._meta.app_label == 'directory'
        elif model._meta.app_label == 'directory':
            return False
        return None