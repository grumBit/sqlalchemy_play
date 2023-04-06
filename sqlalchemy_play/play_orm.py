from typing import List, Optional

from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Notes from;
# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#using-orm-declarative-forms-to-define-table-metadata


class Base(DeclarativeBase):
    # This establishes a declaritive base, with metadata and registry
    # https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#establishing-a-declarative-base
    pass


# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes


class User(Base):
    __tablename__ = "user_account_orm_style"  # Grum: Added _orm_style suffix to have both style expamples
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address_orm_style"  # Grum: Added _orm_style suffix to have both style expamples
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account_orm_style.id"))  # Grum: my _orm_style suffix needed
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
