from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json
import os
import urllib.request
import base64


PROJECT_PATH = "/home/prit-khatri/devops-project"

JENKINS_USER = os.environ.get("JENKINS_USER")
JENKINS_TOKEN = os.environ.get("JENKINS_TOKEN")

JENKINS_URL = "http://localhost:8080"
JENKINS_JOB = "devops-project"


def run_command(command):
    try:
        result = subprocess.check_output(
            command,
            text=True,
            stderr=subprocess.DEVNULL
        )
        return result.strip()
    except Exception:
        return ""


def get_git_branch():
    branch = run_command([
        "git",
        "-C",
        PROJECT_PATH,
        "branch",
        "--show-current"
    ])

    return branch if branch else "Unknown"


def get_docker_status():
    container = run_command([
        "docker",
        "inspect",
        "-f",
        "{{.State.Status}}",
        "my-website"
    ])

    if container == "running":
        return "Running"

    return "Stopped"


def get_docker_port():
    port = run_command([
        "docker",
        "port",
        "my-website",
        "80/tcp"
    ])

    return port if port else "Unknown"


def get_health():
    result = run_command([
        "curl",
        "-s",
        "-o",
        "/dev/null",
        "-w",
        "%{http_code}",
        "http://localhost:8081"
    ])

    if result == "200":
        return "Healthy"

    return "Unhealthy"


def get_jenkins_status():

    if not JENKINS_USER or not JENKINS_TOKEN:
        return {
            "status": "Credentials Missing",
            "build": "Unknown",
            "commit": "Unknown",
            "message": "Unknown"
        }

    try:

        url = (
            f"{JENKINS_URL}/job/"
            f"{JENKINS_JOB}/lastBuild/api/json"
        )

        credentials = (
            f"{JENKINS_USER}:{JENKINS_TOKEN}"
        )

        encoded_credentials = base64.b64encode(
            credentials.encode()
        ).decode()

        request = urllib.request.Request(url)

        request.add_header(
            "Authorization",
            f"Basic {encoded_credentials}"
        )

        with urllib.request.urlopen(
            request,
            timeout=5
        ) as response:

            data = json.loads(
                response.read().decode()
            )

        result = data.get("result")

        if result == "SUCCESS":
            status = "SUCCESS"
        elif result == "FAILURE":
            status = "FAILED"
        elif data.get("building"):
            status = "BUILDING"
        else:
            status = result or "UNKNOWN"

        commit = "Unknown"
        message = "Unknown"

        change_sets = data.get(
            "changeSets",
            []
        )

        if change_sets:

            items = change_sets[0].get(
                "items",
                []
            )

            if items:

                commit = items[0].get(
                    "commitId",
                    "Unknown"
                )

                message = items[0].get(
                    "msg",
                    "Unknown"
                )

        return {
            "status": status,
            "build": f"#{data.get('number', 'Unknown')}",
            "commit": commit,
            "message": message
        }

    except Exception:

        return {
            "status": "Offline",
            "build": "Unknown",
            "commit": "Unknown",
            "message": "Jenkins API unavailable"
        }


class DashboardAPI(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/api/status":

            jenkins = get_jenkins_status()

            data = {
                "branch": get_git_branch(),
                "docker_status": get_docker_status(),
                "docker_port": get_docker_port(),
                "health": get_health(),

                "jenkins_status":
                    jenkins["status"],

                "jenkins_build":
                    jenkins["build"],

                "jenkins_commit":
                    jenkins["commit"],

                "jenkins_message":
                    jenkins["message"]
            }

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.send_header(
                "Access-Control-Allow-Origin",
                "*"
            )

            self.end_headers()

            self.wfile.write(
                json.dumps(data).encode()
            )

        else:

            self.send_response(404)
            self.end_headers()


server = HTTPServer(
    ("0.0.0.0", 5000),
    DashboardAPI
)

print("======================================")
print("DevOps Dashboard API")
print("======================================")
print("API running on port 5000")
print("Monitoring:")
print("- Git branch")
print("- Docker status")
print("- Docker port")
print("- Application health")
print("- Jenkins build status")
print("- Jenkins build number")
print("- Jenkins commit")
print("- Jenkins commit message")
print("======================================")

server.serve_forever()
