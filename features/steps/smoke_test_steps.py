import os
from behave import given, when, then


@given("the digitalengn repository is initialized")
def step_repo_initialized(context):
    assert os.path.exists("README.md")


@when("I check the project structure")
def step_check_structure(context):
    context.directories = ["mbse", "docs", "features"]


@then("I should see the mbse, docs, and features directories")
def step_see_directories(context):
    for directory in context.directories:
        assert os.path.isdir(directory), f"Directory {directory} not found"
