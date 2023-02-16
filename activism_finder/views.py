from django.db.models import Count, ObjectDoesNotExist
from django.http import Http404, HttpResponse, JsonResponse
from django.template import Template, loader

from .models import Keyword, Source


# Create your views here.

def index(request):
    return HttpResponse(loader.render_to_string("activism_finder/index.html", request=request))


def _get_dict_from_Source(item: Source):
    return {"id": item.id, "name": item.name, "description": item.description, "website": item.website, "code": item.code}


def search(request):
    term = request.GET.get("term")
    if not term:
        return JsonResponse({"data": []})
    else:
        query = list((Source.objects.filter(name__icontains=term) or Source.objects.filter(code__icontains=term)).order_by("name").all())
        query.extend([item.source for item in Keyword.objects.filter(word__icontains=term)])
        return JsonResponse({"data": [_get_dict_from_Source(item) for item in sorted(set(query), key=lambda item: item.name)]})


def list_activisms(request):
    return HttpResponse(
        loader.render_to_string("activism_finder/list.html", request=request, context=dict(sources=Source.objects.order_by("name").all())))


def list_tags(request):
    return HttpResponse(
        loader.render_to_string("activism_finder/tags.html", request=request, context=dict(
            keywords=[(item["word"], item["num_sources"], item["word"].replace(" ", "_")) for item in
                      Keyword.objects.values("word").annotate(num_sources=Count("word")).order_by("-num_sources")])))


def individual(request, code: str):
    try:
        obj = Source.objects.get(code=code)
    except ObjectDoesNotExist:
        raise Http404()
    else:
        template: Template = loader.get_template("activism_finder/detail.html")
        return HttpResponse(template.render({
            "name": obj.name, "description": obj.description, "website": obj.website,
            "tags": Keyword.objects.filter(source__code=obj.code).all()
        }))


def tag(request, tag_name: str):
    obj = Keyword.objects.filter(word=tag_name.replace("_", " ")).first()
    if obj is None:
        raise Http404()
    else:
        template: Template = loader.get_template("activism_finder/tag.html")
        return HttpResponse(
            template.render({"name": obj.word, "sources": [item.source for item in Keyword.objects.filter(word=obj.word).order_by("source__name")]}))
