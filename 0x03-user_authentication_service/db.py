#!/usr/bin/env python3
"""DB module
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email: Email address of the user
            hashed_password: Hashed password of the user

        Returns:
            User object representing the newly added user
        """

        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on the provided keyword
        arguments

        Args:
            **kwargs: Arbitrary keyword arguments representing the query
            criteria

        Returns:
            User object representing the found user

        Raises:
            NoResultFound: If no user is found based on the provided
            criteria
            InvalidRequestError: If the query arguments are invalid
        """

        if not kwargs:
            raise InvalidRequestError
        valid_attrs = ['id', 'email',
                       'hashed_password',
                       'session_id', 'reset_token']
        for key in kwargs.keys():
            if key not in valid_attrs:
                raise InvalidRequestError

        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database based on the provided user_id
            and keyword arguments

        Args:
            user_id: ID of the user to update
            **kwargs: Arbitrary keyword arguments representing the
            attributes to update

        Raises:
            ValueError: If an argument that does not correspond to a
            user attribute is passed
        """

        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(
                            f"Attribute '{key}' does not exist for User")
            self._session.commit()
        except NoResultFound:
            # Handle NoResultFound
            raise
