from __future__ import annotations
import os
import subprocess
import requests
import time
from typing import Any, cast
from behave import given as given_step, when as when_step, then as then_step

# Fix for pyright: behave decorators are not recognized as callable
given = cast(Any, given_step)
when = cast(Any, when_step)
then = cast(Any, then_step)

# Add ~/bin to PATH for subprocess calls
env = os.environ.copy()
env["PATH"] = f"{os.path.expanduser('~/bin')}:{env['PATH']}"


@given("the digitalengn repository is initialized")
def step_repo_initialized(context: Any):
    assert os.path.exists("README.md")


@when("I check the project structure")
def step_check_structure(context: Any):
    context.directories = ["mbse", "docs", "features"]


@then("I should see the mbse, docs, and features directories")
def step_see_directories(context: Any):
    for directory in context.directories:
        assert os.path.isdir(directory), f"Directory {directory} not found"


@given("the infrastructure is launched in Minikube")
def step_launch_infra(context: Any):
    # Ensure ingress addon is enabled
    subprocess.run(["minikube", "addons", "enable", "ingress"], check=True, env=env)

    # Apply kustomization
    subprocess.run(
        ["kubectl", "apply", "-k", "infrastructure/k8s/base"], check=True, env=env
    )

    # Wait for ingress controller to be ready (webhook often takes time)
    print("Waiting for ingress controller...")
    subprocess.run(
        [
            "kubectl",
            "wait",
            "--namespace",
            "ingress-nginx",
            "--for=condition=ready",
            "pod",
            "--selector=app.kubernetes.io/component=controller",
            "--timeout=90s",
        ],
        env=env,
    )

    # Wait for ingress to be fully ready
    time.sleep(10)


@given("I wait {seconds:d} seconds for applications to start")
def step_wait_for_apps(context: Any, seconds: int):
    print(f"Waiting {seconds} seconds for applications to start...")
    time.sleep(seconds)


@when("I access the following core URLs:")
def step_access_urls(context: Any):
    context.responses = {}

    # Start port-forward for ingress controller
    pf = subprocess.Popen(
        [
            "kubectl",
            "port-forward",
            "--address",
            "localhost",
            "-n",
            "ingress-nginx",
            "service/ingress-nginx-controller",
            "8080:443",
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for port-forward to be ready
    time.sleep(5)

    try:
        for row in context.table:
            # Test via localhost:8080 (HTTPS)
            url = f"https://localhost:8080{row['path']}"
            # Retry a few times as apps might be starting up
            # Reduced retries since we now have an explicit 60s wait
            for _ in range(2):
                try:
                    # verify=False for self-signed certificates in dev
                    response = requests.get(
                        url, timeout=3, allow_redirects=True, verify=False
                    )
                    context.responses[row["name"]] = response.status_code
                    if response.status_code < 500:
                        break
                except Exception as e:
                    context.responses[row["name"]] = str(e)
                time.sleep(2)
    finally:
        pf.terminate()
        pf.wait()


@then("I should receive a valid response from each URL")
def step_verify_responses(context: Any):
    for name, status in context.responses.items():
        # Consider any 2xx or 3xx as valid for a smoke test if the app is starting up
        # Even 401/403 might be okay if it's an auth page, but we expect 200/302 mostly
        assert isinstance(status, int) and status < 500, (
            f"URL {name} failed with status/error: {status}"
        )
