"""Controller(s) for dealing with users."""


from werkzeug.exceptions import BadRequest, Conflict

from peanuts.lib.auth import admin_need
from peanuts.controllers.base import BaseRestController
from peanuts.models.user import User, UserData, PeanutsAuth


__all__ = ['UserController']


class UserController(BaseRestController):
    """A controller for dealing with users."""
    Model = User

    def post(self, post_data):
        """Overwrites the default post method to add information to the user
            submodels including data and authentication.
        """
        password = post_data.get('password')
        password_confirm = post_data.get('confirm')

        if not password or password != password_confirm:
            raise BadRequest('Password and confirmation don\'t match')

        email = post_data.get('email')
        if not email:
            raise BadRequest('Email is required.')
        elif (
                self.db_session.query(User).join(User.data).filter(
                    UserData.email == email
                ).first()
            ):
            raise Conflict('User already exists')

        user_data = UserData(
            email=email,
            first_name=post_data.get('first_name'),
            last_name=post_data.get('last_name'),
            user_name=post_data.get('username')
            )
        peanuts_auth = PeanutsAuth(
            email=email,
            password=password
            )
        user = User(
            is_admin=post_data.get('is_admin'),
            data=user_data,
            peanuts_auth=peanuts_auth
            )

        self.db_session.add(user)
        self.commit()

        # Log the new user in, unless the current user is an admin.
        if not admin_need():
            self.session.clear()
            self.session['user_id'] = user.id_
            self.session.permanent = post_data.get('remember')

        return user
