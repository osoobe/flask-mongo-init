import flask

import os

import config
from main import util
from main import dummy
from cordovel.project.model import Project
from application import app
from cordovel.project import forms as project_forms


@app.route("/")
def index():
    project_registration_form = project_forms.ProjectRegistrationForm()
    projects = Project.objects[:5].all()
    return flask.render_template(
        "welcome.html",
        projects=projects,
        project_registration_form=project_registration_form
    )

@app.route("/bitbucket/jasigns/webhook/", methods=['POST', 'GET'])
def bitbucket_tracking():
    if flask.request.method == 'POST':
        builder = Cordovel(config.project_path)
        data = flask.request.get_json()
        commiter = data.get("author", None)
        pullrequest = data.get("pullrequest", None)
        repository = data.get("repository", None)
        if repository:
            repo_name = repository["name"]
        else:
            return "Repo information does not exists"
        project_names = [project.folder for project in dummy.projects]
        if repo_name in project_names:
            build_script = "%s/build.sh" % config.project_path
            options = [build_script, "-a", "-l", "-w"]
            builder.build(*options)
            return "Building is in progress"
    return "no data received"
