
print("HEllo")

def myReplace(myString):
	dictionary = {"-":  r"\-", "]":  r"\]", "\\": r"\\", "^":  r"\^", "$":  r"\$", "*":  r"\*", ".":  r"\.", "'":  r"\'", '"':  r'\"'}
	for character in myString:
		if character in dictionary:
			print("found " + character +" to be replaced with " + dictionary[character])
			myString = myString.replace(character, dictionary[character])
	return myString

delete_chars=''.join(chr(i) for i in xrange(32))                        
print("Kiran" , '\x00abc\x01def\x1fg'.translate(None,delete_chars))

string = "kira'n"
print(myReplace(string))


