"""
На стороне сервера БД содержит следующие таблицы: 

клиент:
    ■ логин;
    ■ информация. 

история_клиента:
    ■ время входа;
    ■ ip-адрес.

список_контактов (составляется на основании выборки всех записей с id_владельца):
    ■ id_владельца; 
    ■ id_клиента.
"""
from datetime import datetime
from pprint import pprint
from sqlalchemy.orm import validates

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import String, ForeignKey

from typing import Optional
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    information: Mapped[Optional[str]]

    active_status: Mapped[List['UserActiveStatus']] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class UserActiveStatus(Base):
    __tablename__ = "UserActiveStatus"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    ip_address: Mapped[str] = mapped_column(String(30))  # todo ip
    port: Mapped[int] = mapped_column(String(30))  # todo port
    login_time: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)  # todo time
    logout_time: Mapped[Optional[datetime]] = mapped_column(DateTime())  # todo time

    user: Mapped["User"] = relationship(back_populates="active_status")

    # пример валидации через SQLAlchemy
    @validates("port")
    def validate_port(self, attr, value):
        if not 1023 < int(value) < 65536:
            raise ValueError("Invalid port value")
        return value

    def __repr__(self) -> str:
        return f"ActiveHistory(id={self.id!r}, user={self.user_id!r}: {self.user!r}, last login_time={self.login_time})"


class Contact(Base):
    __tablename__ = "contacts"

    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)
    status: Mapped[str] = mapped_column(String(30))

    user: Mapped[User] = relationship("User", foreign_keys=[user_id])
    contact: Mapped[User] = relationship("User", foreign_keys=[contact_id])

    def __repr__(self) -> str:
        return f"Contact(user_id={self.user_id!r}, contact_id={self.contact_id!r}, status={self.status!r})"


# connection to DB
# SQLite
engine = create_engine(
    'sqlite:///messenger.db',
    echo=True,
    pool_recycle=7200,
)

# создаем таблицы
Base.metadata.create_all(engine)

# создаем новую сессию для работы с БД
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":

    # тестовые запросы
    new_user = User(name='John Doe3', information='Some information about John Doe')
    session.add(new_user)
    session.commit()

    active = UserActiveStatus(
        user=new_user,
        ip_address='127.0.0.1',
        port=63423,
    )
    session.add(active)
    session.commit()

    contact = Contact(
        user=new_user,
        contact=new_user,
        status='active',
    )

    session.add(contact)
    session.commit()

    query = session.query(
        User.name,
        UserActiveStatus.ip_address,
        UserActiveStatus.port,
        UserActiveStatus.login_time,
    ).join(User)
    # Возвращаем список кортежей
    print()

    pprint(query.all())