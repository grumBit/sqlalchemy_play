from inspect import isclass
from sqlalchemy import delete, Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import registry


def delete_all(app_registry: registry, engine: Engine):
    """
    Deletes all the rows in all the ORM classes registered in the apps registry.

    May break with foreign key constraints if the necessary cascade-deletes have
    not been specified in each of the ORM classes.
    https://docs.sqlalchemy.org/en/20/orm/cascades.html#using-foreign-key-on-delete-cascade-with-orm-relationships
    """
    class_registry = app_registry._class_registry
    registered_orm_classes = [i for i in class_registry.values() if isclass(i)]
    with Session(engine) as session:
        for orm_class in registered_orm_classes:
            session.execute(delete(orm_class))
        session.commit()
