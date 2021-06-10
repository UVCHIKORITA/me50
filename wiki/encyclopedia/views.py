import random
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import Markdown
from . import util


class Search(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search"}))


class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Page Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Content"
    }))


class EditForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Content"
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": Search(),
    })


def entry(request, title):

    entry = util.get_entry(title)

    if entry != "":
        return render(request, "encyclopedia/entry.html", {
          "title": title,
          "entry": Markdown().convert(entry),
          "search_form": Search(),
          })
    return render(request, "encyclopedia/error.html", {
          "title": title
    })


def search(request):
    if request.method == "POST":
        form = Search(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = util.get_entry(title)

            if entry:
                return redirect(reverse('entry', args=[title]))
            else:
                related_titles = util.related_titles(title)

                return render(request, "encyclopedia/search.html", {
                    "title": title,
                    "related_titles": related_titles,
                    "search_form": Search()
                })

    return redirect(reverse('index'))


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
          "create_form": CreateForm(),
          "search_form": Search()
        })

    elif request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
          title = form.cleaned_data['title']
          text = form.cleaned_data['text']
        else:
          return render(request, "encyclopedia/create.html", {
            "create_form": form,
            "search_form": Search()
          })

        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
              "create_form": form,
              "search_form": Search()
            })
        else:
            util.save_entry(title, text)
            return redirect(reverse('entry', args=[title]))


def edit(request, title):

    if request.method == "GET":
        text = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
          "title": title,
          "edit_form": EditForm(initial={'text':text}),
          "search_form": Search()
        })

    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
          text = form.cleaned_data['text']
          util.save_entry(title, text)
          return redirect(reverse('entry', args=[title]))

        else:
          return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": form,
            "search_form": Search()
          })


def random_title(request):

    titles = util.list_entries()
    title = random.choice(titles)

    return redirect(reverse('entry', args=[title]))



