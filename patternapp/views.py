from django.shortcuts import render
from .models import FileName, GeneratedPattern
from .utils.processor import process_filename


def generate_view(request):
    files = FileName.objects.all()
    result = None

    if request.method == "POST":
        file_id = request.POST.get("file")
        file_obj = FileName.objects.get(id=file_id)

        data = process_filename(file_obj.name)

        GeneratedPattern.objects.create(
            file=file_obj,
            suggested_pattern=data["pattern"],
            generic_pattern=data["generic"],
            layout_id=data["layout_id"],
            payer=data["payer"],
            data_type=data["type"],
            file_format=data["format"]
        )

        result = data
        result["filename"] = file_obj.name

    return render(request, "generate.html", {"files": files, "result": result})