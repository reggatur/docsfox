As explained in the [[Docsfox Quick Start Guide]] and [[How to Install Docsfox]], *** you use either LibreOffice Writer or Notepad++ as the editor for your document templates.

Creating document templates with either editor is exactly the same. You insert variables and optional clauses using the same tags.  A variable looks like this: `<<ClientFirst>>`. An optional clause or text looks like this: `<<Clause1>>The contract may be terminated via email.<<Clause1/>>`

The content of a client data file is also the same whether using LibreOffice Writer or Notepad++ as your editor. You can use LibreOffice Calc, MS Excel, another spreadsheet application, or even a text editing application to create client data files as explained here.

## Editing a template

You can start editing a new template by:

- Opening a copy of an existing form or word processing document.
- Copying and pasting the content of an existing document into a new, blank document.

## Variables

In the document, replace client-specific and variable text with variables bounded by `<<` and `>>`.

### Example of Variables

`Pat Secada, President, PFS Wright, Inc., agrees to the following terms...`

is replaced with:

`<<ClientFirst>> <<ClientLast>>, <<ClientTitle>>, <<ClientOrg>>, agrees to the following terms...`

## Optional Text

Optional Text can be a word, phrase or clause, really any type of text, that can be included or excluded from a document.

Place pairs of tags, such as `<<Option1>>` and `<<Option1/>>`, before and after any  Optional Text.

You may use whatever letters and numbers you choose for tags. They are enclosed in double pointy brackets. The second tag needs a slash "`/`" before the closing pointy brackets.

### Example of Optional Text

In this sentence, you want the option to include the word, "NOT":

My Agent shall NOT have authority to make health care decisions.

The edited text reads:

My Agent shall `<<Option1>>`NOT `<<Option1/>>`have authority to make health care decisions.

**NOTE:** Pay attention to space characters. A good practice is to:

1. Insert the first tag immediately BEFORE the optional text.
2. Insert the second tag immediately AFTER a space at the  end of the optional text.

## Alternative Text

In some places you may want to include either of two alternative words, phrases or clauses, but not both. Use pairs of tags for each of the alternative texts  just as you would for Optional Text.

In the Template Data File for the template, there is a Description column. In this column you write instructions stating: Enter a T for Option1 or 2. Not for both.

### Example of Alternative Text

`<<Option1>>upon execution. <<Option1/>><<Option2>>upon my incapacity as determined by a licensed physician. <<Option2/>>`

|**Find**|**Replace**|**Type**|**Value**|**Description**|
|---|---|---|---|---|
|Option1||TF|T|Enter T for Option1 or 2. Not for both.|
|Option2||TF||Enter T for Option1 or 2. Not for both.|









