Task
====

A blogger posted [an article](http://stu.mp/2012/10/my-patent-pending-3-question-technical-interview.html)
about interview questions. One of them was:

> There is a multi-level directory tree, say a local git checkout, 
> that has a number of files all with the extension .tmp. How would 
> you delete all files with the .tmp extension in a single command 
> regardless of where they sit in the directory tree?

I've added some sample files and directories for you to test if 
your solution works.

If you want to reset the directory, you can use `git checkout -f HEAD`.

rm
--
You should read [man rm](http://unixhelp.ed.ac.uk/CGI/man-cgi?rm).
Some options you should know are:

* *-r*: remove directories and their contents recursively


Why does(n't) this work?
------------------------
* `rm -r *.tmp`
