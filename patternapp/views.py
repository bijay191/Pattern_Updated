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

            generated_pattern = generate_pattern(filename)

            # 🔥 If pattern fails → everything UNKNOWN
            if not generated_pattern or generated_pattern == "UNKNOWN":
                generated_pattern = "UNKNOWN"
                layout_id = "UNKNOWN"

            else:
                layout_id = find_layout_id(generated_pattern)

                if not layout_id:
                    layout_id = "UNKNOWN"

                # ✅ Save only valid patterns
                if generated_pattern != "UNKNOWN":
                    GeneratedPattern.objects.update_or_create(
                        filename=filename,
                        defaults={
                            "client": client,
                            "regex": generated_pattern
                        }
                    )
        # if file_id:
        #     file_record = TableLog.objects.get(id=file_id)
        #     filename = file_record.filename
        #     client = file_record.client

        #     generated_pattern = generate_pattern(filename)

        #     layout_id = find_layout_id(generated_pattern)

        #     if generated_pattern:
        #         GeneratedPattern.objects.update_or_create(
        #             filename=filename,
        #             defaults={
        #                 "client": client,
        #                 "regex": generated_pattern
        #             }
        #         )

    return render(request, "generate.html", {
        "files": files,
        "generated_pattern": generated_pattern,
        "layout_id": layout_id,
        "selected_filename": filename if request.method == "POST" else None
    })