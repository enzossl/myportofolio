from django.urls import path

from main.views import show_main, show_experience, show_achievements, create_project, show_projects, get_projects_json, delete_project, create_experience, get_experience_json, delete_experience, update_experience 

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("achievements/", show_achievements, name="show_achievements"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/", show_projects, name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/update/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/",delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
]