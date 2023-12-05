
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, Session, relationship

# Підключення до бази даних
engine = create_engine('sqlite:///adress_book.db', echo=False)
Base = declarative_base()


# Оголошення класів моделей
class Kontackt(Base):
    __tablename__ = 'kontackt'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    email = Column(String)

class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Group_kont(Base):
    __tablename__ = 'group_kont'

    id = Column(Integer, primary_key=True)
    id_kont = Column(Integer, ForeignKey('kontackt.id'))
    id_group = Column(Integer, ForeignKey('groups.id'))

    kontackt = relationship('Kontackt')
    groups = relationship('Groups')

# Створення таблиць
Base.metadata.create_all(engine)

# Створення сесії
def create_session():
    return Session(engine)

# Функція для створення нового контакту
def create_kontackt(session, first_name, last_name, phone, email):
    new_kont = Kontackt(first_name=first_name , last_name=last_name, phone=phone, email=email)
    session.add(new_kont)
    session.commit()

# Функція для додавання нової групи
def create_groups(session, name):
    new_group = Groups(name=name)
    session.add(new_group)
    session.commit()


# Функція для отримання всіх контактів
def get_all_kont(session):
    return session.query(Kontackt).all()

# Функція для отримання всіх груп
def get_all_groups(session):
    return session.query(Groups).all()

# Функція для додавання до групи
def into_gr_kont(session, id_kont, id_group):
    into_gr_kontakt = Group_kont(id_kont=id_kont, id_group=id_group)
    session.add(into_gr_kontakt)
    session.commit()

# Функція для оновлення інформації про контакт
def update_kont(session, id_kont, new_f_name, new_l_name, new_phone, new_email):
    kont_to_update = session.query(Kontackt).filter_by(id=id_kont).first()
    if kont_to_update:
        kont_to_update.first_name = new_f_name
        kont_to_update.last_name = new_l_name
        kont_to_update.phone = new_phone
        kont_to_update.email = new_email
        session.commit()

# Функція для видалення контакту
def delete_kont(session, id_kont):
    kont_to_delete = session.query(Kontackt).filter_by(id=id_kont).first()
    if kont_to_delete:
        session.delete(kont_to_delete)
        session.commit()

# Функція для видалення груп
def delete_groups(session, id_group):
    group_to_delete = session.query(Groups).filter_by(id=id_group).first()
    if group_to_delete:
        session.delete(group_to_delete)
        session.commit()

# Функція для отримання деталей про контакт (ім'я, прізвище, телефон, email та групи)
def get_kont_details(session):
    return session.query(Kontackt.first_name, Kontackt.last_name, Kontackt.phone, Kontackt.email, Group_kont.id_group).\
        join(Group_kont, Groups.id == Group_kont.id_group).all


# Функція для вибірки кількості контактів для кожної групи
def kont_count_per_group(session):
    return session.query(Groups.name, func.count(Group_kont.id).label('kont_count')).\
        outerjoin(Group_kont, Groups.id == Group_kont.id_group).\
        group_by(Groups.id).all()

# Закриття сесії
def close_session(session):
    session.close()

# Приклад використання:
session = create_session()

# CRUD операції


# Додавання контакту
kontackt_to_add = [['Lucy', 'Linn', '+000779657', 'linn@gmail.com'],['Steav', 'Gud', '+000796588', 'Gud@gmail.com'], ['Alex', 'Beener', '+000766257', 'AlexB@gmail.com']]
for item in kontackt_to_add:
    create_kontackt(session, item[0], item[1], item[2], item[3])

# Додавання групи
clients_to_add = [['Friends'],['Work']]
for item in clients_to_add:
    create_groups(session, item[0])

# Додавання до групи
kont_gr_to_add = [[1, 1],[2, 1],[3, 2],[1, 2]]
for item in kont_gr_to_add:
    into_gr_kont(session, item[0], item [1] )


# Вивід всіх контактів
all_kont = get_all_kont(session)
print("\nВсі контакти:")
for kontackt in all_kont:
    print(kontackt.first_name, kontackt.last_name, kontackt.phone, kontackt.email)

# Вивід всіх груп
all_groups = get_all_groups(session)
print("\nВсі групи:")
for groups in all_groups:
    print(groups.name)

# оновлення контакту
kontackt_updete = [['2', 'vfdff', 'hhjhh', '+000766257', 'AlexB@gmail.com']]
for item in kontackt_updete:
    update_kont(session, item[0], item[1], item[2], item[3], item[4])
print("\nконтакти оновленно\n")

# Вивід всіх контактів
all_kont = get_all_kont(session)
print("\nВсі контакти:")
for kontackt in all_kont:
    print(kontackt.first_name, kontackt.last_name, kontackt.phone, kontackt.email)

# Виведення кількості контактів для кожної групи
kont_count = kont_count_per_group(session)
print("\nКількість контактів в групах:")
for row in kont_count:
    print(row)

# Закриття сесії
close_session(session)