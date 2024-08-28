import pathlib
import tempfile

import mammoth


def main():
    docx_path = pathlib.Path("/Volumes/stuff/graphRagSandbox/assets/SmartBear_TOU-10FEB2023.docx")
    non_logging_output_dir_path = pathlib.Path("/Volumes/stuff/graphRagSandbox/non_logging_output_dir")

    if len([file for file in non_logging_output_dir_path.iterdir() if file.is_file()]) >= 3:
        for file in non_logging_output_dir_path.iterdir():
            file.unlink()

    out_temp_file = tempfile.NamedTemporaryFile(prefix="SmartBear_",
                                                suffix=".html",
                                                delete=False,
                                                dir=non_logging_output_dir_path)

    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value
        with open(out_temp_file.name, "wb") as out_file:
            print(html.encode("ascii", errors="ignore"))
            out_file.write(html.encode("ascii", "ignore"))


if "__main__" == __name__:
    main()