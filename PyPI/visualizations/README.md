Run with

```bash
$ [tool] -Tpng graphviz.dot -o rendered.png
```

Tools are:

* dot - "hierarchical" or layered drawings of directed graphs. This is the
  default tool to use if edges have directionality. ---- takes much too long for big graphs, over 35233,23s
* neato - "spring model'' layouts.  This is the default tool to use if the
  graph is not too large (about 100 nodes) and you don't know anything else
  about it. Neato attempts to minimize a global energy function, which is
  equivalent to statistical multi-dimensional scaling.
* fdp - "spring model'' layouts similar to those of neato, but does this by
  reducing forces rather than working with energy.
* **sfdp** - multiscale version of fdp for the layout of large graphs. ---- takes 2787,97s for big graphs
* twopi - radial layouts, after Graham Wills 97. Nodes are placed on concentric
  circles depending their distance from a given root node.
* circo - circular layout, after Six and Tollis 99, Kauffman and Wiese 02. This
  is suitable for certain diagrams of multiple cyclic structures, such as
  certain telecommunications networks.

There are some options worth investigating:

* `-x`:
* `-Goverlap=scale`:

Depending on your system, the command

```
$ convert rendered.png -resize 1600x1600 "rendered-small.png"
```

might come in handy.