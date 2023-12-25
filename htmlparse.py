import sys

def usage():
  print("usage: htmlparse.py file_in file_out")

args = sys.argv

try:
  fileIn_Path = args[1]
except:
  usage()
  sys.exit()

try:
  fileOut_Path = args[2]
except:
  fileOut_Path = ""

file = open(fileIn_Path, "r")
gridFile = file.read()
file.close()

gridList = []
pos = 0
while pos < len(gridFile):
  if gridFile[pos] == "~":
    if not(pos == 0):
      gridList.append(gridFile[:pos])
    gridList.append(0)
    gridFile = gridFile[pos+1:]
    pos = -1
  elif gridFile[pos] == "}":
    if not(pos == 0):
      gridList.append(gridFile[:pos])
    gridList.append(1)
    gridFile = gridFile[pos+1:]
    pos = -1
  pos += 1
gridList.append(gridFile)

tagList = {
  'metadata': 'head',
  'document': 'body',
  'link'    : 'a',
  'code'    : 'script',
}
attribList = {
  "link" : {
    "surf" : "href"
  },
  "img"  : {
    "surf" : "src"
  },
}

tags = []
output = []

def doTag(inStr):
  if "(" in inStr:
    tag, attribs = inStr.split("(", 1)
    attribs = attribs[:-1]
    # # do something to attribs here to HTML them # #
    attrFullList = attribs.split(",")
    for i, attr in enumerate(attrFullList):
      if attr[0] == " ":
        attrFullList[i] = attr[1:]
    attrList = []
    for attrPair in attrFullList:
      attrList.append(attrPair.split(":"))
    for i in range(len(attrList)):
      if (tag.lower() in attribList and
          type(attribList[tag.lower()]) is dict and
          attrList[i][0].lower() in attribList[tag.lower()]):
        attrList[i][0] = attribList[tag.lower()][attrList[i][0].lower()]
      elif (attrList[i][0] in attribList):
        attrList[i][0] = attribList[attrList[i][0]]
    attribs = ''
    for pairs in attrList:
      attribs += " " + pairs[0] + "=" + pairs[1]
  else:
    tag = inStr
    attribs = ''
  if tag.lower() in tagList:
    tag = tagList[tag.lower()]
  return tag, attribs

splitType = -1
for item in gridList:
  if isinstance(item, int):
    splitType = item
  else:
    if splitType == 0:
      tag, attribs = doTag(item.split("{", 1)[0])
      tags.append(tag)
      output.append("<" + tags[-1] + attribs + ">")
      if (len(item.split("{", 1)) > 1):
        output.append(item.split("{", 1)[1])
    elif splitType == 1:
      output.append("</" + tags.pop() + ">")
      output.append(item)
    else:
      output.append(item)
    splitType = -1

writeToFile = ""
for items in output:
  writeToFile += items

if fileOut_Path != "":
  fileOut = open(fileOut_Path, "w")
  fileOut.write(writeToFile)
  fileOut.close()
else:
  print(writeToFile)
