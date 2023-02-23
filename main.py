# This is a sample Python script.
import collections
import itertools
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def consume(iterator, n):
    '''Advance the iterator n-steps ahead. If n is none, consume entirely.'''
    collections.deque(itertools.islice(iterator, n), maxlen=0)

def doOptions(lineIter,xmlfile):
    localIter = itertools.tee(lineIter,2)
    subline = next(localIter[0],None)
    while subline!=None :
        if subline.startswith("  *"):
            subline = subline.replace("*","")
            subline = subline.strip()
            xmlfile.write(
                "        <Option>\n")
            xmlfile.write(
                "        "+subline+"\n")
            xmlfile.write(
                "        </Option>\n")
            consume(localIter[1],1)
        else :
            return localIter[1]
        subline = next(localIter[0], None)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("moves.xml","w") as xmlfile:
        xmlfile.write("""
<?xml version="1.0" encoding="UTF-8"?>
<Moves xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="file:/D:/projects/RiderProjects/ApocalypseForge/ApocalypseForge/Moves.xsd">
""")
        for filename in os.listdir("move_md"):
            print("Processing "+filename)
            with open("move_md/"+filename,"r",encoding="utf8") as mdfile:
                fileIter = iter(mdfile)
                line = next(fileIter,None)
                while line != None:
                    line = line.strip()
                    if line.startswith("===="):
                        move_name = line[5:len(line)-5]
                    elif line.startswith("*When") or line.startswith("**When"):
                        line = line[1:len(line)-1]
                        last_space = line.rfind(' ')
                        move_stat = line[last_space+1:len(line)]
                        move_stat = move_stat.replace("*","").replace(".","")
                        xmlfile.write(
                            "  <Move Name=\""+move_name+"\" Statistic=\""+
                            move_stat+"\">\n")
                    elif line.startswith("|") :
                        sections = line.split('|')
                        sections[1] = sections[1].strip()
                        sections[2] = sections[2].strip()
                        if sections[1]!="Result":
                            xmlfile.write(
                                "    <"+sections[1].replace(" ","")+">\n")
                            xmlfile.write(
                                "      <Description>\n")
                            xmlfile.write(
                                "        "+sections[2]+"\n")
                            xmlfile.write(
                                "      </Description>\n")
                            xmlfile.write(
                                "      <Options>\n")
                            fileIter=doOptions(fileIter,xmlfile)
                            xmlfile.write(
                                "      </Options>\n")
                            xmlfile.write(
                                "    </"+sections[1].replace(" ","")+">\n")
                    line = next(fileIter, None)
                xmlfile.write("  </Move>\n")
        xmlfile.write("</Moves>\n")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
