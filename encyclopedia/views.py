from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

import markdown2 as md2
import random

class ContentForm(forms.Form):
    entry_content = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":"5"}))
    

class EntryForm(ContentForm):
    entry_title = forms.CharField(label="Title")
    field_order = ['entry_title', 'entry_content']


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry_title):

    entry_content = util.get_entry(entry_title)
    entry_page = "encyclopedia/entry.html"
    notfound = False

    if entry_content is None:
        entry_title = f"{entry_title} not found"
        entry_content = f"The requested page was not found."
        notfound = not notfound
        

    return render(request, entry_page, {
        "entry_title": entry_title,
        "entry_content": md2.Markdown().convert(entry_content),
        "notfound": notfound
    })


def add(request):
    add_page = "encyclopedia/add.html"
    error_message = "An entry with this title name already exists."
    
    if request.method == "POST":
        form = EntryForm(request.POST)
        
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_content = form.cleaned_data['entry_content']
            
            if util.get_entry(entry_title) is None:
                util.save_entry(entry_title, entry_content)
                
                return HttpResponseRedirect(reverse("entry", args=[entry_title]))
            else:
                return render(request, add_page, {
                    "form": form,
                    "error_message": error_message
                })
    else:
        return render(request, add_page, {
            "form": EntryForm()
        })


def edit(request, entry_title):
    
    if request.method == "POST":
        form = ContentForm(request.POST)

        if form.is_valid():
            edited_content = form.cleaned_data['entry_content']
            
            util.save_entry(entry_title, edited_content)
            
            return HttpResponseRedirect(reverse("entry", args=[entry_title]))
    else:
        entry_content = util.get_entry(entry_title)
        edit_page = "encyclopedia/edit.html"
            
        form = ContentForm({'entry_content': entry_content})
        
        return render(request, edit_page, {
            "form": form,
            "entry_title": entry_title,
            "entry_content": entry_content
        })


def random_entry(request):
    list = util.list_entries()
    
    entry_index = random.randint(0, len(list) - 1)
        
    return HttpResponseRedirect(reverse("entry", args=[list[entry_index]]))


def search(request):
    q = request.GET.get('q')

    found = util.get_entry(q)

    if found is not None:
        return HttpResponseRedirect(reverse("entry", args=[q]))
    else:
        found_list = util.list_entries_substring(q)
        print(found_list)
        
        return render(request, "encyclopedia/results.html", {
            "entries": found_list,
            "query": q 
        })