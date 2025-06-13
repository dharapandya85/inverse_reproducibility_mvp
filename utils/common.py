def get_file_extension(filename):
    return filename.split('.')[-1].lower()
def clean_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in ('.','_','-')).rstrip()