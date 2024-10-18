import os
from markdown_blocks import markdown_to_html_node
from extracttitle import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")

    markdown_file = open(from_path)
    markdown_string = markdown_file.read()

    template_file = open(template_path)
    template_string = template_file.read()

    html_node = markdown_to_html_node(markdown_string)
    html_string = html_node.to_html()

    title = extract_title(markdown_string)

    result_template = template_string.replace("{{ Title }}", title)
    result_template = result_template.replace("{{ Content }}", html_string)

    html_page = open(dest_path, "w+")
    html_page.write(result_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        to_file_path = os.path.join(dest_dir_path, filename)
        try:
            if os.path.isfile(file_path):
                file_extension = file_path.split(".")[-1]
                to_file_path_split = to_file_path.split(".")
                to_file_name_html = f'{".".join(to_file_path_split[:-1])}.html'
                print(to_file_name_html)
                if file_extension == "md":
                    generate_page(file_path, template_path, to_file_name_html)
            elif os.path.isdir(file_path):
                generate_pages_recursive(file_path, template_path, to_file_path)
        except Exception as e:
            print('Failed to generate page %s. Reason: %s' % (file_path, e))