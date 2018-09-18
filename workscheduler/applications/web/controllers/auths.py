# -*- coding: utf-8 -*-

from workscheduler.applications.services.authentication_service import AuthenticationService
from workscheduler.infrastructures.user_repository import UserRepository
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required
from ..db import get_db_session


bp = Blueprint('auths', __name__)


def load_user(user_id):
    return UserRepository(get_db_session()).get_user(user_id)


@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, role = AuthenticationService(get_db_session()).login(request.form['username'], request.form['password'])
        if not user:
            flash('Invalid username or password', 'error')
            return render_template('login.html')
        login_user(user)
        flash('You were logged in')
        return redirect(url_for('menus.show_menu'))
    return render_template('login.html')


@login_required
@bp.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('users.login'))