# -*- coding: UTF-8 -*-
# Copyright 2020 by Rumma & Ko Ltd.
# License: BSD, see file LICENSE for more details.

"""
This defines the :manage:`passwd` management command.

See :doc:`/dev/users`.

"""

import djclick as click
import getpass

from lino.api import rt

def default_username():
    return getpass.getuser()

# copied from getlino.utils:
BATCH_HELP = "Whether to run in batch mode, i.e. without asking any questions.  "\
             "Don't use this on a machine that is already being used."

# copied from getlino.utils:
def yes_or_no(msg, yes="yY", no="nN", default=True):
    """Ask for confirmation without accepting a mere RETURN."""
    click.echo(msg + " [y or n]", nl=False)
    while True:
        c = click.getchar()
        if c in yes:
            click.echo(" Yes")
            return True
        elif c in no:
            click.echo(" No")
            return False


@click.command()
@click.pass_context
@click.argument('username', default=default_username)
@click.option('-c', '--create/--no-create', default=False, help="""
Create the given user. Fail if that username eixsts already.
""")
@click.option('--batch/--no-batch', default=False, help=BATCH_HELP)
def command(ctx, username, create, batch):
    """
    Update or optionally create password, name and type of a user.

    USERNAME : The username of the user to process.

    """
    User = rt.models.users.User
    UserTypes = rt.models.users.UserTypes
    try:
        user = User.objects.get(username=username)
        if create:
            raise click.UsageError("Cannot create existing user named '{}'".format(username))
    except User.DoesNotExist:
        if create:
            user = User(username=username)
            click.echo("Creating new user")
        else:
            raise click.UsageError("We have no user named '{}'".format(username))

    dut = user.user_type or UserTypes.user
    if not batch:
        user.first_name  = click.prompt("First name", default=user.first_name or username)
        user.last_name  = click.prompt("Last name", default=user.last_name or username)
        user_type  = click.prompt("User type", type=click.Choice(
            [ut.name for ut in UserTypes.get_list_items() if ut.name]),
            default=dut.name)
        if user_type:
            user.user_type = UserTypes.get_by_name(user_type)
        else:
            user.user_type = None
        passwd = click.prompt(
            "Password (leave blank to deactivate user account)",
            hide_input=True, confirmation_prompt=True, default='')
        if passwd:
            user.set_password(passwd)
        else:
            user.set_unusable_password()
    user.full_clean()
    if batch or yes_or_no('Going to save {}. Are you sure?'.format(user)):
        user.save()
        click.echo("User {} has been saved.".format(user))
