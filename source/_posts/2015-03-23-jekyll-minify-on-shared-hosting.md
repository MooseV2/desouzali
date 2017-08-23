---
layout: post
title:  "Minifying Jekyll Content on a Shared Host"
date:   2015-03-23 15:00:00
categories: web
tags:
- script
- web
- jekyll
---
I love [Jekyll](http://jekyllrb.com/). It makes it super simple for me to create the content for this site. All I have to do is open up a text file and start typing. When I'm done, it's just a simple `git push` away from the web where it's formatted and compiled into static files.

The biggest reason why I love Jekyll is the pure minimalism factor. I can't stand bloat. Loading up a page and seeing the network requests in the hundreds and the page size in the megabytes sends shivers down my spines. When I'm coding, I write things as efficiently and legibly as possible whenever I can, and always spend time refactoring my code until I'm pleased.

So when it comes to my place on the web, I'm not going to make an exception. Now, when it comes to web content, I'm left with an interesting dillema. I can do one of two things:

1. Make the code very legible with whitespace, or
2. Make the code very small by 'minifying' it.

Well, after a lot of thinking, I decided to go with the latter. My thinking is that any half-decent web browser will already pretty-print the code when viewing the source, and barring that, someone could easily throw it into one of many [beautifiers](http://jsbeautifier.org/) available anyway. In this case, the bytes are more important.

The next step was to figure out how to minify the code automatically. Initially, I looked a plugin: a simple Ruby file that's dragged into the plugin directory and changes the way Jekyll behaves. As it turns out, **Stereobooster** has already made [jekyll-press](https://github.com/stereobooster/jekyll-press) to do just that. Unfortunately, it has some dependencies that I just couldn't install on a shared host.

So like any other logical programmer, instead of settling for less, I wrote my own.

The dependencies of my script can all be installed in the userspace without the need of gcc or other compilers. To get started (assuming you have Python Pip), simply run the following code:

    pip install --user htmlmin
    pip install --user slimit
    pip install --user csscompressor

This will install them all to the home directory.

Next, create a file named `_tidy.py` with the following content:

{% highlight python %}
{% include _tidy.py %}
{% endhighlight %}

Run it with `python _tidy.py in_dir out_dir`, or in my case, `python _tidy.py $JEKYLL_TMP/build.raw $/JEKYLL_TMP/build.min`

Good luck!!

