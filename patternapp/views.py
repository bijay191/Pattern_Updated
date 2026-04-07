from django.shortcuts import render
from .models import TableLog, GeneratedPattern
from .utils.processor import process_filename


def generate_view(request):
    files = TableLog.objects.all()
    result = None

    if request.method == "POST":
        file_id = request.POST.get("file")
        file_obj = TableLog.objects.get(id=file_id)

        data = process_filename(file_obj.filename)

        GeneratedPattern.objects.create(
            filename=file_obj.filename,
            client=file_obj.client,
            regex=data["pattern"]
        )

        result = data
        result["filename"] = file_obj.filename

    return render(request, "generate.html", {
        "files": files,
        "result": result
    })