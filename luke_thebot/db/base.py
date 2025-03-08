from peewee import Model, DatabaseProxy

# Create a database proxy that can be initialized later.
db_proxy = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = db_proxy