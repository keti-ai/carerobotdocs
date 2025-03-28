# doc_carerobot


Install:
```bash
pip install sphinx
pip install sphinx-rtd-theme
```

Edit source/conf.py:
```
CODE_PATH_HERE
```

Generate Docs from Code
```
sphinx-apidoc -f -o source/apidoc $CORE_DIR  
```
Note: __init__.py should be in subdirs

Build
```
mkdir build
make clean
make html
```

Deloy
```
rm -rf docs
cp -r build/html docs
```


Edit skils:

Heading level
```
Level 1: = (e.g., document title)
Level 2: - (e.g., sections)
Level 3: * (e.g., subsections)
Level 4: + (e.g., subsubsections)
Level 5: ^ (e.g., paragraphs)
```

Adding image
```
.. figure:: path/to/image.png
   :alt: Alternative text
   :width: 300px
   :align: center

   Caption for the image.
```

Adding tables
```
.. list-table:: Robot Skills
   :header-rows: 1
   :widths: 20 40

   * - Skill
     - Description
   * - pick
     - Grasp an object
   * - place
     - Release object
```

Adding math
```
.. math::

   equation1\\
   equation2
```

Adding code
```
.. code-block:: language

   Code goes here
```







