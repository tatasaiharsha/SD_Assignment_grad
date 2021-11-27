from tree_sitter import Language, Parser
import git
import os
import re
import sys
import fnmatch

Language.build_library(
    # Store the library in the `build` diectory
    'build/my-languages.so',

    # Include one or more language
    [
        'vendor/tree-sitter-go',
        'vendor/tree-sitter-javascript',
        'vendor/tree-sitter-python',
        'tree-sitter-ruby'
    ]
)
GO_LANGUAGE = Language('build/my-languages.so', 'go')
JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
PY_LANGUAGE = Language('build/my-languages.so', 'python')
RB_LANGUAGE = Language('build/my-languages.so', 'ruby')



parser = Parser()
parser.set_language(PY_LANGUAGE)

parser_js = Parser()
parser_js.set_language(JS_LANGUAGE)

parser_go = Parser()
parser_go.set_language(GO_LANGUAGE)

parser_ruby = Parser()
parser_ruby.set_language(RB_LANGUAGE)



def parsing(source, parser):
    final_list = []
    new_list = [0]
    def parseNewNode(main):
        if (len(main.children) == 0):
            return
        else:
            for root in main.children:
                if (root.type == 'identifier'):
                    final_list.append(root)
                    new_list[-1] += 1
                parseNewNode(root)

    tree = parser.parse(bytes(source, "utf8"))

    root_node = tree.root_node
    parseNewNode(root_node)
    return final_list


# source = """abc = 25
# b = 70
# print("helo",b)
# """
# tree= parsing(source,parser)
# print(tree)
main_repo = sys.argv[1]
extension = sys.argv[2]
new_name = sys.argv[3]
output1 = sys.argv[4]
output2 = sys.argv[5]
sys.stdout = open("output1", "x")
# https://github.com/Harsha2871/SdAllCodes
git.Repo.clone_from(main_repo, 'extracted_files')


# files = [f for f in os.listdir('extracted_files') if re.match(r'[0-9]+.*\.py', f)]
# files = fnmatch.filter(os.listdir('extracted_files'), "*.py")

# for f in files:
#   new_files.append(fnmatch.filter(os.listdir(''+f), "*.py"))
# print(new_files)
js_files = []
ruby_files = []
go_files = []
python_files = []

for main, sub, structure in os.walk(r'extracted_files'):
    for file in structure:
        if file.endswith('.py'):
            python_files.append(os.path.join(main, file))

for main, sub, structure in os.walk(r'extracted_files'):
    for file in structure:
        if file.endswith('.rb'):
            ruby_files.append(os.path.join(main, file))

for main, sub, structure in os.walk(r'extracted_files'):
    for file in structure:
        if file.endswith('.js'):
            js_files.append(os.path.join(main, file))

# print(python_files)

# source=source.split('\n')

for main, sub, structure in os.walk(r'extracted_files'):
    for file in structure:
        if file.endswith('.go'):
            go_files.append(os.path.join(main, file))

len_python = len(python_files)
for i in python_files:
    input_file = open(i, 'r')
    source_updated = input_file.read()
    # print(source1)
    tree_python = parsing(source_updated, parser)
    # print("The tree structure is", tree_python)


for i in js_files:
    input_file = open(i, 'r')
    source_updated_js = input_file.read()
    # print(source1)
    tree_js = parsing(source_updated_js, parser_js)
    # print("The tree structure is", tree_js)

for i in ruby_files:
    input_file = open(i, 'r')
    source_updated_ruby = input_file.read()
    # print(source1)
    tree_ruby = parsing(source_updated_ruby, parser_ruby)
    # print("The tree structure is", tree_ruby)

for i in go_files:
    input_file = open(i, 'r')
    source_updated_go = input_file.read()
    # print(source1)
    tree_go = parsing(source_updated_go, parser_ruby)
    # print("The tree structure is", tree_ruby)

# print(js_files)

source_updated = source_updated.split('\n')
# for e in source_updated:
#     print(e)
# print("The identifier is,",source_updated[node.start_point[0]][node.start_point[1]:node.end_point[1]] +" " + "present at location",node.start_point[0])

sys.stdout = open("output1", "w")
print("_____________________________________python identifiers_______________________________")
for node in tree_python:
    print("The identifier is,", source_updated[node.start_point[0]][node.start_point[1]:node.end_point[1]] + " " + "present at location",node.start_point[0])
    # sys.stdout.close()
    # output_file.write(res)


source_updated_js = source_updated_js.split('\n')
print("_____________________________________Java Script identifiers_______________________________")
for node in tree_js:
    print("The identifier is,", source_updated_js[node.start_point[0]][node.start_point[1]:node.end_point[1]] + " " + "present at location",node.start_point[0])


source_updated_ruby = source_updated_ruby.split('\n')
print("_____________________________________Ruby identifiers_______________________________")
for node in tree_ruby:
    print("The identifier is,", source_updated_ruby[node.start_point[0]][node.start_point[1]:node.end_point[1]] + " " + "present at location",node.start_point[0])


source_updated_go = source_updated_go.split('\n')
print("_____________________________________Go language identifiers_______________________________")
for node in tree_go:
    print("The identifier is,",
          source_updated_go[node.start_point[0]][node.start_point[1]:node.end_point[1]] + " " + "present at location",
          node.start_point[0])
