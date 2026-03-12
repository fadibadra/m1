import re

textes = []

f = open('cat/note_reduite.csv')
contenu_initial = f.read()

# extract textual notes
regex = re.compile(r'\\"(.*?)\\"',re.DOTALL)
for text in regex.finditer(contenu_initial):
    textes.append(text.group(1))

# remove them temporarily
contenu_no_text = regex.sub(r'TEXT',contenu_initial)

# now assemble final content for csv file
new_lines = []
textes.reverse()
for line in contenu_no_text.split('\n'):
    if re.search('TEXT',line):
        new_lines.append(re.sub('TEXT',textes.pop().replace('\n',''),line))
    else:
        new_lines.append(line)
contenu_final = '\n'.join(new_lines)

f.close()

with open('cat/note_reduite_une_ligne.csv','a') as f:
    f.write(contenu_final)
