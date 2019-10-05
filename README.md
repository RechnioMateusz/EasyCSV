# _**EasyCSV**_
Python module used for easy .csv editing

This module is in package form and is used to edit _.csv_ files. I decided to
create this, because i always wanted to experiment with slicing in Python and
I wanted to easily edit my _.csv_ files. For me, using readers and writers from
built-in **csv** class in Python is not as straight forward as it looks like.
I often look into its documentation to remind myself how to use it. Thats why
I have written this piece of code.

--- --- --- --- ---

To use it properly You have to import it first:

```python
from EasyCsv.easy_csv import CsvEditor
```

Next You have to initialize object of **CsvEditor**:

```python
csv_editor = CsvEditor(path="path_to_your_csv.csv")
```

And then You can use slices to determine which data You want to edit or get:

```python
# Getting data from .csv
print("third row:", csv_editor[2::])
print("rows from fourth to sixth:", csv_editor[3::2])
print("third column:", csv_editor[:2:])
print("columns from zeroth to second:", csv_editor[:0:2])
print("intersection of fourth row and third column:", csv_editor[3:2:])

# Settings data in .csv
csv_editor[2::] = ["cell1", "cell2"]
```

If You are done with editing, simply save your _.csv_ file:

```python
csv_editor.save()
```