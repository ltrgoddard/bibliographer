#!/usr/bin/env python

import re
import sys

with open(str(sys.argv[1]),"r") as input:

	text = input.read()

scraper = re.compile(r"(\^\[| \(|; |see )([A-Z]|\').{1,100}, (\'.{1,100}\', )?(in )?\*.{1,100}\*.{0,200}(( |\(|\[)\d{4})?(, (p\. |pp\. )([\d-]{1,10})(, (n\. )([0-9]{1,10}))?)?(, (\&|\<|\\<).*?(accessed.*?\d{4}))?((\)|\]|[0-9ivxlcdm])(\.\]|\. |; |, quoted))")

biblio = []

for citation in re.finditer(scraper, text):

	note = str(citation.group())[2:-2]
	note = re.sub(r"(\[|\\\[)(?=[A-Z]|\d)", "(", note)
	note = re.sub(r"(?<=(, | \()\d{4})\\?\]", ")", note)
	note = re.sub(r"(\(|\[)(p\. |pp\. )([\divxlcdm]{1,10}|[\divxlcdm]{{1,10}\-(\-)?[\divxlcdm]{1,10})(\)|\])", "", note)
	note = re.sub(r", (?=[\divxlcdm]{1,10}\-(\-)?[\divxlcdm]{1,10})", ", pp. ", note)
	note = re.sub(r"((?<=\])\)| \))", "", note)

	if note[0] == "\'":

		biblio.append(note + "  ")
	else:

		name = re.compile(r"(^| )[A-Za-z\'\-]*(, | and )")
		surnames = re.search(name, note)
		surname = surnames.group(0).strip(",")
		if surname[0] == " ":

			if surname[-5:] == " and ":

				note = surname[1:-5] + ", " + re.sub(name, " and ", note, 1)

			else:

				note = surname[1:] + re.sub(name, ", ", note, 1)
		biblio.append(note + "  ")

biblio.sort(key=lambda x: x.strip("\'").lower())

with open(str(sys.argv[2]),"w") as output:

	output.write("\n".join(biblio))
