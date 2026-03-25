def read_file(upload_file):
    try:
        content = upload_file.file.read()
        upload_file.file.seek(0)

        return content.decode("utf-8", errors="ignore")

    except Exception as e:
        print("File read error:", str(e))
        return ""
