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

If you want to print the files, you can use `tree -a .`. This is the
example tree, that is generated:

```
 .
 |-- another folder
 |   |-- analysis.tex
 |   |-- test.tmp
 |   `-- .tmp
 |-- index.html
 |-- README.md
 |-- sample.tmp
 |   |-- inner.tmp
 |   |-- subfolder
 |   |   |-- inner2
 |   |   |   `-- abc.tmp
 |   |   |-- inner folder
 |   |   |   |-- asdf.tmp
 |   |   |   `-- gimp.txt
 |   |   |-- inner.tmp
 |   |   `-- .tmp
 |   `-- .tmp
 |-- test.tmp
 `-- .tmp 
```

A correct command should result in:

```
.
|-- another folder
|   `-- analysis.tex
|-- index.html
|-- README.md
`-- sample.tmp
    `-- subfolder
        |-- inner2
        `-- inner folder
            `-- gimp.txt
```

rm
--
You should read [man rm](http://unixhelp.ed.ac.uk/CGI/man-cgi?rm).
Some options you should know are:

* *-r*: remove directories and their contents recursively


Why does(n't) this work?
------------------------
`rm -r *.tmp`

`find . -type f -name '*.tmp' -exec rm -rf {} \;`

