from django.urls import path

from notes import views as views

urlpatterns = [
    path('v1/list-note/', views.NoteListAPI.as_view()),
    path('v1/get-note/<int:pk>', views.RetrieveNoteAPI.as_view()),
    path('v1/add-note/', views.AddNoteAPI.as_view()),
    path('v1/update-note/<int:pk>', views.UpdateNoteAPI.as_view()),
    path('v1/delete-note/<int:pk>', views.DeleteNoteAPI.as_view()),
]
