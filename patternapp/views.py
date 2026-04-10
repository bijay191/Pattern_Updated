from django.shortcuts import render
from .models import TableLog
from .utils.processor import generate_pattern
from .utils.matcher import find_layout_id


def generate_regex(request):
    files = TableLog.objects.all()

    filename = None
    generated_pattern = None
    layout_id = None
    error_message = None

    if request.method == "POST":
        file_id = request.POST.get("file_id")
        manual_filename = request.POST.get("manual_filename", "").strip()

        file_record = None

        # Case 1: dropdown selected
        if file_id:
            file_record = TableLog.objects.filter(id=file_id).first()

            if file_record:
                filename = file_record.filename
                generated_pattern = generate_pattern(filename)

                if not generated_pattern:
                    generated_pattern = "UNKNOWN"
                    layout_id = "UNKNOWN"
                else:
                    layout_id = find_layout_id(generated_pattern, file_record.cuttingfloor)
                    if not layout_id:
                        layout_id = "UNKNOWN"

        # Case 2: manual filename entered
        elif manual_filename:
            filename = manual_filename   # important line

            file_record = TableLog.objects.filter(filename__iexact=manual_filename).first()

            if file_record:
                filename = file_record.filename   # use DB value
                generated_pattern = generate_pattern(filename)

                if not generated_pattern:
                    generated_pattern = "UNKNOWN"
                    layout_id = "UNKNOWN"
                else:
                    layout_id = find_layout_id(generated_pattern, file_record.cuttingfloor)
                    if not layout_id:
                        layout_id = "UNKNOWN"
            else:
                error_message = "File not found in database."
                generated_pattern = "UNKNOWN"
                layout_id = "UNKNOWN"

    return render(request, "generate.html", {
        "files": files,
        "filename": filename,
        "generated_pattern": generated_pattern,
        "layout_id": layout_id,
        "error_message": error_message,
    })