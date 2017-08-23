# -*- coding: utf-8 -*-
"""
_tidy: Reformats and minifies HTML, JS, and CSS
_tidy [directory_in] [directory_out]

Requires:
- slimmer
- slimit
- csscompressor
To install on shared hosting, use `pip install --user <package>`

"""
#from htmlmin import minify as html_minify
from slimmer import css_slimmer as css_minify
from slimmer import html_slimmer as html_minify
from slimit import minify as js_minify
#from csscompressor import compress as css_minify
import os
import sys

reload(sys) # Python deletes setdefaultencoding, so get it back
sys.setdefaultencoding('utf8') # Otherwise, htmlmin will use ascii encoding

input_dir = u'./_site' if len(sys.argv)<=1 else sys.argv[1]
output_dir = u'./_minify' if len(sys.argv)<=2 else sys.argv[2]
valid_extensions = ['.html', '.js', '.css']
file_counts = [0]*len(valid_extensions)
compression = {
    '.html' : lambda content: html_minify(content),
    '.js'   : lambda content: js_minify(content, mangle=True),
    '.css'  : lambda content: css_minify(content)
}

for root, dirs, files in os.walk(input_dir):
    for file in files:
        file_in  = os.path.join(root, file)
        file_out = os.path.join(output_dir, os.path.relpath(file_in, start=input_dir))
        extension = os.path.splitext(file)[-1]

        if extension in valid_extensions:
            with open(file_in, 'r') as f_in:
                contents = f_in.read()

            try:
                os.makedirs(os.path.dirname(file_out))
            except Exception: # If the directory already exists
                 pass
            
            try:
                minified = compression[extension](contents)
            except Exception, e:
                print "Error parsing '%s' file '%s'" % (extension[1:], file)
                print ">>>%s" % e
            else:
                with open(file_out, 'w') as f_out:
                    file_counts[valid_extensions.index(extension)] += 1
                    f_out.write(minified)


print "Compressed %s file(s)" % sum(file_counts)
for extension, count in enumerate(file_counts):
    print "-> %s: %s" % (valid_extensions[extension], count)
