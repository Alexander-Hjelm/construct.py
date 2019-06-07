import json
#import jsonpickle
import os
#import textile
import markdown
import sys

class json_serializable:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

class page_block(json_serializable):
    def __init__(self, id):
        self.id = id

    def set_html_snippet_file(self, html_snippet_file):
        self.html_snippet_file = html_snippet_file

    def set_markdown_file(self, markdown_file):
        self.markdown_file = markdown_file

    def set_stylesheet_file(self, stylesheet_file):
        self.stylesheet_file = stylesheet_file

    def set_template_block_file(self, template_block_file):
        self.template_block_file = template_block_file

    def set_sub_blocks(self, sub_blocks):
        self.sub_blocks = sub_blocks

    def fromJSON(j):
        pb = page_block("")
        pb.__dict__ = json.loads(j)
        return pb

    def fromDict(dictionary):
        pb = page_block("")
        pb.__dict__ = dictionary
        return pb

print(str(sys.argv))

def write_str_to_file(filename, content):
    file = open(filename,"w") 
    file.write(content) 
    file.close()

def read_str_from_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

def write_json_object_to_file(filename, data):
    write_str_to_file(filename, data.toJSON())

for i in range(0, len(sys.argv)):

    arg = sys.argv[i]

    # Iniitalize a new webpage
    if arg == "--init" or arg == "-i":
        root_path = sys.argv[i+1]

        if not os.path.exists(root_path + "/markdown"):
            os.makedirs(root_path + "/markdown")

        if not os.path.exists(root_path + "/stylesheets"):
            os.makedirs(root_path + "/stylesheets")

        if not os.path.exists(root_path + "/html-snippets"):
            os.makedirs(root_path + "/html-snippets")

        if not os.path.exists(root_path + "/template-blocks"):
            os.makedirs(root_path + "/template-blocks")

        sub_block = page_block("todo")
        sub_block.set_markdown_file("things-to-do")

        top_block = page_block("index")
        top_block.set_markdown_file("welcome")
        top_block.set_stylesheet_file("example_stylesheet")
        top_block.set_sub_blocks([[sub_block]])

        write_json_object_to_file(root_path + "/index.json", top_block)

        md_top = """
# Hello from construct.py!

If you see this text, then it means you have successfully generated a test webpage.
Now you may customize it to your heart's content.
"""

        md_sub = """## A few places to start:
- Add more pages by creating json block files in the project root directory. Use **index.json** as an example.
- Change the page contents by editing the markdown files in the **markdown/** folder
- Change the stylesheet of this page by changing the file: **stylesheets/index.css**
- Add html snippets in **htmp-snippets/** to insert custom html code in a page
"""

        write_str_to_file(root_path + "/markdown/welcome.md", md_top)
        write_str_to_file(root_path + "/markdown/things-to-do.md", md_sub)

        example_stylesheet = """.red {
   color: red;
}
.thick {
   font-size:20px;
}
.green {
   color:green;
}
"""

        write_str_to_file(root_path + "/stylesheets/example_sheet.css", example_stylesheet)

        #print(page_block.fromJSON(read_str_from_file("index.json")).markdown_file)


    if arg == "--build" or arg == "-b":
        root_path = sys.argv[i+1]
        html_doc = ""
        html_doc += """<!DOCTYPE html>
<html>
<body>
"""

        markdowns = {}
        stylesheets = {}
        template_blocks = {}
        html_snippets = {}

        # Iterate over all markdown files
        for markdown_file in [f for f in os.listdir(root_path + "/markdown")]:
            print("found markdown file: " + markdown_file)
            markdowns[markdown_file] = read_str_from_file(root_path + "/markdown/" + markdown_file)

        # Iterate over all stylesheet files
        for stylesheet_file in [f for f in os.listdir(root_path + "/stylesheets")]:
            print("found stylesheet file: " + stylesheet_file)
            stylesheets[stylesheet_file] = read_str_from_file(root_path + "/stylesheets/" + stylesheet_file)
 
        # Iterate over all template block files
        for template_block_file in [f for f in os.listdir(root_path + "/template-blocks")]:
            print("found template block file: " + template_block_file)
            template_blocks[template_block_file] = read_str_from_file(root_path + "/template-blocks/" + template_block_file)

        # Iterate over all html snippet files
        for html_snippet_file in [f for f in os.listdir(root_path + "/html-snippets")]:
            print("found html snippet file: " + html_snippet_file)
            html_snippet_file[html_snippet_file] = read_str_from_file(root_path + "/html-snippets/" + html_snippet_file)

        # Iterate over all block files in project root dir
        for block_file in [f for f in os.listdir(root_path) if os.path.isfile(os.path.join(root_path, f))]:
            print("found block file: " + block_file)

            block = page_block.fromJSON(read_str_from_file(root_path + "/" + block_file))

            html = markdown.markdown(markdowns[block.markdown_file + ".md"])
            html_doc += html
            print(html)

        for sub_block_array in block.sub_blocks:
            for sub_block_dict in sub_block_array:
                sub_block = page_block.fromDict(sub_block_dict)

                html = markdown.markdown(markdowns[sub_block.markdown_file + ".md"])
                html_doc += html
                print(html)



        html_doc += """</body>
</html>
"""

        print(html_doc)
        write_str_to_file("index.html", html_doc)
