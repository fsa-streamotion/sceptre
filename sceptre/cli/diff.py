import click

from sceptre.context import SceptreContext
from sceptre.cli.helpers import catch_exceptions, write
from sceptre.config.reader import ConfigReader

@click.command(name="diff", short_help="Show diffs with running stack.")
@click.argument("path")
@click.pass_context
@catch_exceptions
def diff_command(ctx, path):
    """
    Show diffs between the running and generated stack.

    :param path: The path to launch. Can be a Stack or StackGroup.
    :type path: str
    """
    context = SceptreContext(
        command_path=path,
        project_path=ctx.obj.get("project_path"),
        user_variables=ctx.obj.get("user_variables"),
        options=ctx.obj.get("options"),
        ignore_dependencies=ctx.obj.get("ignore_dependencies")
    )

    stacks, _ = ConfigReader(context).construct_stacks()

    for stack in list(stacks):
        diff = stack.diff()
        if diff:
            message = "\
Differences between running stack {} and \
generated template:\n\
{}".format(stack.external_name, diff)
        else:
            message = "No diffs"

        write(message, context.output_format)
