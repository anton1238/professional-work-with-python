import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_config import token
from random import randrange
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError

Base = declarative_base()

engine = sq.create_engine('postgresql://user@localhost:5432/vkinder_db',
client_encoding='utf8')
Session = sessionmaker(bind=engine)

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
session = Session()
connection = engine.connect()

class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)

class DatingUser(Base):
    __tablename__ = 'dating_user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='cascade'))

class Photos(Base):
    __tablename__ = 'photos'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_dating_user = sq.Column(sq.Integer, sq.ForeignKey('dating_user.id', ondelete='cascade'))

class blackList(Base):
    __tablename__ = 'blacklist'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='cascade'))

def delete_db_blacklist(ids):
    current_user = session.query(blackList).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()

def delete_db_favorites(ids):
    current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()

def check_db_master(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id

def check_db_user(ids):
    dating_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    blocked_user = session.query(blackList).filter_by(vk_id=ids).first()
    return dating_user, blocked_user

def check_db_black(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    all_users = session.query(blackList).filter_by(id_user=current_users_id.id).all()
    return all_users

def check_db_favorites(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    alls_users = session.query(DatingUser).filter_by(id_user=current_users_id.id).all()
    return alls_users

def write_msg(user_id, message, attachment=None):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})

def register_user(vk_id):
    try:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False

def add_user(event_id, vk_id, name, surname, city, link, id_user):
    try:
        new_user = DatingUser(
            vk_id=vk_id,
            name=name,
            surname=surname,
            city=city,
            link=link,
            id_user=id_user)
        session.add(new_user)
        session.commit()
        write_msg(event_id, 'Пользователь добавлен в избранное')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id, 'Пользователь уже в избранном.')
        return False

def add_user_photos(event_id, link_photo, likes, id_dating_user):
    try:
        new_user = Photos(
            link_photo=link_photo,
            likes=likes,
            id_dating_user=id_dating_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id, 'Фото пользователя сохранено в избранное')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id, 'Фото пользователя уже сохраннено')
        return False

def add_to_blacklist(event_id, vk_id, name, surname, city, link, link_photo, likes, id_user):
    try:
        new_user = blackList(
            vk_id=vk_id,
            name=name,
            surname=surname,
            city=city,
            link=link,
            link_photo=link_photo,
            likes=likes,
            id_user=id_user)
        session.add(new_user)
        session.commit()
        write_msg(event_id, 'Пользователь заблокирован')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id, 'Пользователь уже в черном списке')
        return False

if __name__ == '__main__':
    Base.metadata.create_all(engine)