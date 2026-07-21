from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.config.config_db import UsersModel

class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_telegram_id(self, telegram_id: int):
        try:
            return self.session.query(UsersModel).filter(UsersModel.telegram_id == telegram_id).first()
        except SQLAlchemyError as e:
            print(f'Error get user: {e}')
            return None

    def create_or_update_user(self, telegram_id: int, username: str, first_name: str, last_name: str, is_bot: bool) -> bool:
        try:
            user = self.get_by_telegram_id(telegram_id)
            if user:
                # Update info if changed
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                self.session.commit()
                return True
            else:
                # Create new
                new_user = UsersModel(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_bot=is_bot,
                    is_active=True # Allow by default for now
                )
                self.session.add(new_user)
                self.session.commit()
                return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Error creating user: {e}')
            return False
