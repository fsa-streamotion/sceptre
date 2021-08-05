import click
import webbrowser

from sceptre.context import SceptreContext
from sceptre.cli.helpers import (
    catch_exceptions,
    write
)
from sceptre.plan.plan import SceptrePlan


@click.command(name="validate", short_help="Validates the template.")
@click.argument("path")
@click.pass_context
@catch_exceptions
def validate_command(ctx, path):
    """
    Validates the template used for stack in PATH.
    \f

    :param path: Path to execute the command on.
    :type path: str
    """
    context = SceptreContext(
        command_path=path,
        project_path=ctx.obj.get("project_path"),
        user_variables=ctx.obj.get("user_variables"),
        options=ctx.obj.get("options"),
        output_format=ctx.obj.get("output_format"),
        ignore_dependencies=ctx.obj.get("ignore_dependencies")
    )

    plan = SceptrePlan(context)
    responses = plan.validate()

    for stack, response in responses.items():
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            del response['ResponseMetadata']
            click.echo("Template {} is valid. Template details:\n".format(stack.name))
        write(response, context.output_format)


@click.command(name="generate", short_help="Prints the template.")
@click.argument("path")
@click.pass_context
@catch_exceptions
def generate_command(ctx, path):
    """
    Prints the template used for stack in PATH.
    \f

    :param path: Path to execute the command on.
    :type path: str
    """
    context = SceptreContext(
        command_path=path,
        project_path=ctx.obj.get("project_path"),
        user_variables=ctx.obj.get("user_variables"),
        options=ctx.obj.get("options"),
        output_format=ctx.obj.get("output_format"),
        ignore_dependencies=ctx.obj.get("ignore_dependencies")
    )

    plan = SceptrePlan(context)
    responses = plan.generate()
    output = [template for template in responses.values()]
    write(output, context.output_format)


@click.command(name="fetch-remote-template", short_help="Prints the remote template.")
@click.argument("path")
@click.pass_context
@catch_exceptions
def fetch_remote_template_command(ctx, path):
    """
    Prints the remote template used for stack in PATH.
    \f

    :param path: Path to execute the command on.
    :type path: str
    """
    context = SceptreContext(
        command_path=path,
        project_path=ctx.obj.get("project_path"),
        user_variables=ctx.obj.get("user_variables"),
        options=ctx.obj.get("options"),
        output_format=ctx.obj.get("output_format"),
        ignore_dependencies=ctx.obj.get("ignore_dependencies")
    )

    plan = SceptrePlan(context)
    responses = plan.fetch_remote_template()
    output = [template for template in responses.values()]
    write(output, context.output_format)


@click.command(name="stack-name", short_help="Reveal the stack name or names.")
@click.argument("path")
@click.pass_context
@catch_exceptions
def stack_name_command(ctx, path):
    """
    Show the stack names of all stacks.
    \f

    :param path: The path to execute the command on.
    :type path: str
    """
    context = SceptreContext(
        command_path=path,
        project_path=ctx.obj.get("project_path"),
        user_variables=ctx.obj.get("user_variables"),
        options=ctx.obj.get("options"),
        ignore_dependencies=ctx.obj.get("ignore_dependencies")
    )

    plan = SceptrePlan(context)
    responses = plan.stack_name()

    for stack_name in responses.values():
        write(stack_name, context.output_format)


@click.command(name="diff", short_help="Show diffs with running stack.")
@click.argument("path")
@click.option(
    "-D", "--differ", type=click.Choice(["difflib", "dictdiffer"]),
    default="difflib", help="Specify diff library, default difflib."
)
@click.pass_context
@catch_exceptions
def diff_command(ctx, path, differ):
    """
    Show diffs between the running and generated stack.

    :param difflib: The diff library to use, default difflib.
    :type path: str
    """
    context = SceptreContext(
        command_path=path,
        project_path=ctx.obj.get("project_path"),
        user_variables=ctx.obj.get("user_variables"),
        options=ctx.obj.get("options"),
        ignore_dependencies=ctx.obj.get("ignore_dependencies")
    )

    plan = SceptrePlan(context)
    responses = plan.diff(differ)
    output = "\n".join([
        stack_name + ": " + template
        for stack_name, template in responses.values()
    ])
    write(output, context.output_format)


@click.command(name="estimate-cost", short_help="Estimates the cost of the template.")
@click.argument("path")
@click.pass_context
@catch_exceptions
def estimate_cost_command(ctx, path):
    """
    Prints a URI to STOUT that provides an estimated cost based on the
    resources in the stack. This command will also attempt to open a web
    browser with the returned URI.
    \f

    :param path: Path to execute the command on.
    :type path: str
    """
    context = SceptreContext(
        command_path=path,
        project_path=ctx.obj.get("project_path"),
        user_variables=ctx.obj.get("user_variables"),
        options=ctx.obj.get("options"),
        output_format=ctx.obj.get("output_format"),
        ignore_dependencies=ctx.obj.get("ignore_dependencies")
    )

    plan = SceptrePlan(context)
    responses = plan.estimate_cost()

    for stack, response in responses.items():
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            del response['ResponseMetadata']
            click.echo("View the estimated cost for {} at:".format(stack.name))
            response = response["Url"]
            webbrowser.open(response, new=2)
        write(response + "\n", 'text')
