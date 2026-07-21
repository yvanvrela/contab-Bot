from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.config.config_db import GroupsModel

class GroupsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_telegram_id(self, telegram_id: int):
        try:
            return self.session.query(GroupsModel).filter(GroupsModel.telegram_id == telegram_id).first()
        except SQLAlchemyError as e:
            print(f'Error get group: {e}')
            return None

    def create_or_update_group(self, telegram_id: int, title: str, group_type: str) -> bool:
        try:
            group = self.get_by_telegram_id(telegram_id)
            if group:
                # Update info if changed
                group.title = title
                group.type = group_type
                self.session.commit()
                return True
            else:
                # Create new
                new_group = GroupsModel(
                    telegram_id=telegram_id,
                    title=title,
                    type=group_type,
                    is_active=True # Allow by default
                )
                self.session.add(new_group)
                self.session.commit()
                return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Error creating group: {e}')
            return False
