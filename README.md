# bibliographer

A Python script to scrape MHRA-style citations from Markdown documents and turn them into alphabetically ordered bibliographies. The main regex function is extremely buggy and needs some serious refining, but I don't have time to work on it at present. Still, the script as a whole is useful for a first pass, which can then be checked and tidied up by hand.

*Usage*: python bibliographer.py [input.markdown] [output.markdown]

## To do

* Remove stray parentheses and braces
* Unicode support
