#!/bin/bash


# change the directory to where this script is
cd "$(realpath $(dirname $0))"
# change upwards from the to whereevery the project root is
. lib/ensure_project_root.sh

# Background Info:
#   https://stackoverflow.com/questions/62774695/pandoc-where-are-css-files-for-syntax-highlighting-code
# Special Answers:
#   https://stackoverflow.com/a/62778531
#   https://stackoverflow.com/a/70805078

PANDOC_STYLE=zenburn
HIGHLIGHT_CSS=src/highlight.css
declare -A LANGUAGES=(                      \
    ["c"]="int main() { return 0; }"        \
    ["bash"]="@echo hi"                     \
    ["python"]="print('hi')"                \
    ["cs"]="Console.WriteLine(\"hi\");"     \
    ["cisco"]="show interface brief"        \
    ["javascript"]="console.write(\"hi\");" \
    ["ini"]="text=hi"                       \
    ["latex"]="\\documentclass{standalone}" \
    ["markdown"]="hi"                       \
    ["makefile"]="CC=gcc"                   \
    ["html"]="<p>hi</p>"                    \
    ["gnuassembler"]="pop %edx"             \
    ["dockerfile"]="RUN echo 'hi'"          \
    ["css"]="html { display: none; }"       \
    ["powershell"]="Write-Host \"Hi\""      \
    ["sql"]="SELECT \* FROM dual"           \
    ["yacc"]="Hi : \"hi\""                  \
    ["yaml"]="text: hi"                     \
    ["default"]="hi"                        \
)

EXAMPLES="~~~\nhi\n~~~"
for k in "${!LANGUAGES[@]}"
do
    #echo "Language: $k"
    #echo "Example: ${LANGUAGES[$k]}"
    EXAMPLES+=$(echo "~~~$k\n${LANGUAGES[$k]}\n~~~\n")
done

TEMP_FILE=$(mktemp)
echo "\$highlighting-css\$" > "$TEMP_FILE"
echo -e $EXAMPLES | pandoc --metadata title="dummy" --highlight-style=$PANDOC_STYLE --template="$TEMP_FILE" > "$HIGHLIGHT_CSS"
rm -f "$TEMP_FILE"

