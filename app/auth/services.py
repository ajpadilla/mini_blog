from .forms import LoginForm


class LoginFormService():
    def __init__(self):
        self._form = LoginForm()

    def is_validate_on_submit(self) -> bool:
        return self._form.validate_on_submit()

    def get_email(self):
        return self._form.email.data

    def get_password(self):
        return self._form.password.data

    def get_remember_me(self):
        return self._form.remember_me.data

    def get_form(self):
        return self._form
