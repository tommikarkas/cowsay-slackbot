from wrappers import *;


# Testing
out = cowsay(fortune(), "turkey")
print(out)

routaheOut = cowsay(routahe("Siltakuja 2", "Ratamestarinkatu 13"))
print(routaheOut)

cowfileListOut = " ".join(list_cowfiles())
print(cowfileListOut)
