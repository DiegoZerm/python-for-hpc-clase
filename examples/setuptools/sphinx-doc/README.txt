The command

sphinx-quickstart doc

was run to generate the skeleton for the documentation.


To generate the documentation,

install the package first to make it importable

   pip install .[doc]

and run

   sphinx-build -b html doc/ doc/_build

to generate the HTML documentation.
