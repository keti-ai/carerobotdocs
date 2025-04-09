# Installations

This repository contains documentation for the CareRobot project. Below are the steps to set up, generate, and deploy the documentation using Sphinx.

## Installation
To install the necessary dependencies, run:
```bash
pip install sphinx sphinx-rtd-theme
```

## Configuration
Edit the `source/conf.py` file and update the necessary paths:
```python
CODE_PATH_HERE
```

## Generating Documentation from Code
Run the following command to generate API documentation from your source code:
```bash
sphinx-apidoc -f -o source/apidoc $CORE_DIR  
```
**Note:** Ensure that `__init__.py` is present in subdirectories for correct module recognition.

## Building the Documentation
```bash
mkdir build
make clean && make html
```

## Deployment
To deploy the generated documentation:
```bash
rm -rf docs
cp -r build/html docs
touch docs/.nojekyll

git push $REPOSITORY
```
Then, update GitHub Pages settings:
- Go to **Settings** → **Pages** → **Build and deployment**
- Set **Source** to **Deploy from branch**
- Choose the `docs` branch

Your documentation will be available at:
```
https://keti-ai.github.io/$REPOSITORY_NAME
```

---

# Writing code with description
Example
```
def sum(a, b):
   """
   Summation of 2 numbers

    Args:
        a: First number.
        b: Sencod number

    Returns:
        summation of 2 numbers.
    Notes:
         input number can be float, int, or numpy.ndarray
    """
    
    return a + b
```

# Editing .rst Guide

## Heading Levels
Use the following syntax for different heading levels:
```
Level 1: = (e.g., Document Title)
Level 2: - (e.g., Sections)
Level 3: * (e.g., Subsections)
Level 4: + (e.g., Subsubsections)
Level 5: ^ (e.g., Paragraphs)
```

## Adding Images
To insert an image:
```rst
.. figure:: path/to/image.png
   :alt: Alternative text
   :width: 300px
   :align: center

   Caption for the image.
```

## Adding Tables
To create a table:
```rst
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

## Adding Math Equations
To include mathematical expressions:
```rst
.. math::

   equation1\\
   equation2
```

## Adding Code Blocks
To display code:
```rst
.. code-block:: language

   Code goes here
```

---

This `README.md` provides an overview of setting up and managing the documentation for the CareRobot project. If you have any questions, refer to the Sphinx documentation or reach out to the maintainers.
