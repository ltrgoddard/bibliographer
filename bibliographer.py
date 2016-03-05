#!/usr/bin/env python

import re
import sys

# open file from first command-line argument
with open(str(sys.argv[1]),"r") as input:

	text = input.read()

# compile main citation-scraper regex
scraper = re.compile(
	r"(\^\[| \(|; |see )([A-Z]|\').{1,100}, " # author names or equivalent
	"(\'.{1,100}\', )?(in )?\*.{1,100}\*.{0,200}" # titles
	"(( |\(|\[)\d{4})?" # a date in brackets (optional)
	"(, (p\. |pp\. )([\d-]{1,10})" # page numbers (opt.)
	"(, (n\. )([0-9]{1,10}))?)?" # note numbers (opt.)
	"(, (\&|\<|\\<).*?" # URL (opt.)
	"(accessed.*?\d{4}))?" # access date (opt.)
	"((\)|\]|[0-9ivxlcdm])(\.\]|\. |; |, quoted))") # end of citation

# initialise list for storing output
biblio = []

# loop through input by citations
for citation in re.finditer(scraper, text):

	# chop off "^[" and ".]" or equivalent
	note = str(citation.group())[2:-2]

	# convert square braces to parentheses around dates (incl. access dates)
	note = re.sub(r"(\[|\\\[)(?=[A-Z]|\d)", "(", note)
	note = re.sub(r"(?<=(, | \()\d{4})\\?\]", ")", note)

	# delete internal page numbers and add "p." or "pp." to main page numbers/ranges
	note = re.sub(r"(\(|\[)(p\. |pp\. )([\divxlcdm]{1,10}|[\divxlcdm]{{1,10}\-(\-)?[\divxlcdm]{1,10})(\)|\])", "", note)
	note = re.sub(r", (?=[\divxlcdm]{1,10}\-(\-)?[\divxlcdm]{1,10})", ", pp. ", note)
	
	# delete stray trailing parentheses
	note = re.sub(r"((?<=\])\)| \))", "", note)

	# if note begins with a title, we're done---write to list
	if note[0] == "\'":

		biblio.append(note + "  ")
	else:

		# find primary author surnames
		name = re.compile(r"(^| )[A-Za-z\'\-]*(, | and )")
		surnames = re.search(name, note)

		if surnames != None:

			# get rid of trailing commas
			surname = surnames.group(0).strip(",")

			# is first character of surname a space?
			if  surname[0] == " ":
		
				# is it preceded by "and"?
				if surname[-5:] == " and ":

					# rewrite note with surname first 
					note = surname[1:-5] + ", " + re.sub(name, " and ", note, 1)

				else:

					# do same for single-author notes
					note = surname[1:] + re.sub(name, ", ", note, 1)
			
				# write note to bibliography list
				biblio.append(note + "  ")

# sort bibliography alphabetically
biblio.sort(key=lambda x: x.strip("\'").lower())

# write out to file specified in second command-line argument 
with open(str(sys.argv[2]),"w") as output:

	output.write("\n".join(biblio))
