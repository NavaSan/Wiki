from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django import forms
from random import choice

from . import util

from markdown2 import Markdown

def convert_md_to_html(title):
    content = util.get_entry(title)

    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entryPage(request, title):
    page = convert_md_to_html(title)

    if page is None:
        return render(request, "encyclopedia/error.html",{
            "title": "error",
            "form": SearchForm()
        })
    return render(request, "encyclopedia/entry.html",{
        "title": title.capitalize,
        "content": page,
        "form": SearchForm()
    })

def searchResults(request):
    if request.method == "GET":
        form = SearchForm(request.GET)

        if form.is_valid():
            searchquery = form.cleaned_data["search"].lower()
            all_entries = util.list_entries()

            files = [filename for filename in all_entries if searchquery in filename.lower()]

            if len(files) == 0:
                return render(request, "encyclopedia/search.html",{
                    "error": "No result found",
                    "form": form
                })

            elif len(files) == 1 and files[0].lower() == searchquery:
                title = files[0]
                return entryPage(request, title)

        else:
            title = [filename for filename in files if searchquery == filename.lower()]

            if len(title) > 0:
                return entryPage(request, title[0])
            else:
                return render(request, "encyclopedia/search.html",{
                    "results": files,
                    "form": form
                })
    else:
        return index(request)

    return index(request)

def newPage(request):
    add = AddForm()
    if request.method == "POST":
        add = AddForm(request.POST)

        if add.is_valid():
            title = add.cleaned_data["title"]
            content = add.cleaned_data["content"]

            titleEntry = util.get_entry(title)

            if titleEntry is not None:
                return render(request, "encyclopedia/error.html", {
                    "message": "This page already exixst, try again"
                })

            util.save_entry(title, content)

            return entryPage(request, title)
        else:
            return render(request, 'encyclopedia/add.html', {
                "add": add
            })

    return render(request, "encyclopedia/add.html", {
        "form": SearchForm(),
        "addForm": add
    })

def editPage(request, title):
    if request.method == "GET":
        page = util.get_entry(title)

        editForm = EditForm(initial={'title': title, 'content': page})

    return render(request, "encyclopedia/edit.html",{
        "form": SearchForm(),
        "editForm": editForm
    })

def save(request):
    editForm = EditForm(request.POST)

    if editForm.is_valid():
       title = editForm.cleaned_data["title"]
       content = editForm.cleaned_data["content"] 

       util.save_entry(title, content)

       return entryPage(request, title)
    return render(request, "encyclopedia/edit.html", {
        "form": SearchForm(),
        "editForm": editForm
    }) 

def random(request):
    return entryPage(request, choice(util.list_entries()))



class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget= forms.TextInput(
        attrs={'placeholder':'Search Encyclopedia'}
    ))

class AddForm(forms.Form):
    title = forms.CharField(label="Title", required=True, widget= forms.TextInput(
        attrs={'placeholder': 'Write the title here...', 'class': 'form-control '}
    ))
    content = forms.CharField(label="Content", required=True, widget= forms.Textarea(
        attrs={'class':'form-control'}
    ))

class EditForm(forms.Form):
    title = forms.CharField(label="Title", required=True, widget= forms.TextInput(
        attrs={'placeholder': 'Write the title here...', 'class': 'form-control '}
    ))
    content = forms.CharField(label="Content", required=True, widget= forms.Textarea(
        attrs={'class':'form-control'}
    ))