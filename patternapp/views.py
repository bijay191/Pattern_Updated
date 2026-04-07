from django.shortcuts import render
from .models import TableLog, GeneratedPattern
from .utils.processor import generate_pattern
from .utils.matcher import find_layout_id


def generate_regex(request):
    files = TableLog.objects.all()

    generated_pattern = None
    layout_id = None

    if request.method == "POST":
        file_id = request.POST.get("file_id")

        if file_id:
            file_record = TableLog.objects.get(id=file_id)
            filename = file_record.filename
            client = file_record.client

            # STEP 1: Generate pattern
            generated_pattern = generate_pattern(filename)

            # STEP 2: Find layout
            layout_id = find_layout_id(generated_pattern)

            # ✅ STEP 3: SAVE TO DB
            GeneratedPattern.objects.update_or_create(
                filename=filename,
                defaults={
                    "client": client,
                    "regex": generated_pattern
                }
            )

    return render(request, "generate.html", {
        "files": files,
        "generated_pattern": generated_pattern,
        "layout_id": layout_id
    })