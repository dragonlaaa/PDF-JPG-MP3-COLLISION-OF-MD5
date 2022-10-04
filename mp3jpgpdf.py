
import os
import sys
import struct
import hashlib

fnMP3, fnJPG, fnPDF= sys.argv[1:4]
#with open("pmp3HDR21.mp3" , "rb") as f:
 # pmp3HDR = f.read()
def EnclosedString(d, starts, ends):
  off = d.find(starts) + len(starts)
  return d[off:d.find(ends, off)]
def getCount(d):
  s = EnclosedString(d, "/Count ", "/")
  count = int(s)
  return count
template = """%%PDF-1.3
%%\xC2\xB5\xC2\xB6

1 0 obj
<</Length 2 0 R>>
stream
%(suffix)s
endstream
endobj

2 0 obj
%(lensuffix)i
endobj 

3 0 obj
<<
  /Type /Catalog
  /Pages 4 0 R
>>
endobj

4 0 obj  
<</Type/Pages/Count %(count)i/Kids[%(kids)s]>>
endobj
"""

with open("jpgpdf.bin", "rb") as f:
  prefjpg = f.read()

with open("mp3jpg.bin", "rb") as f:
  prefmp3 = f.read()

with open("pdfmp3.bin", "rb") as f:
  prefpdf = f.read()


with open(fnMP3, "rb") as f:
  mp3 = f.read()

with open(fnJPG, "rb") as f:
  JPG = f.read()

with open(fnPDF, "rb") as f:
  PDF = f.read()

JPG = JPG[2:]
jpgsuffix = JPG
mp3suffix = mp3
LEN=len(mp3suffix)
cout=LEN/0xf000
pad=mp3suffix+"\0"*(0xf000-LEN%0xf000)

print(cout)
for i in range (cout+1):
  pad=pad[:i*0xf000] +b'\xff\xfe\xEF\xFE'+pad[(i)*0xf000+4:]

suffix="\0"*(0x1000-0x230+1+0x200)+pad+JPG

os.system('mutool merge -o merged.pdf dummy.pdf %s' % (fnPDF))
with open("merged.pdf", "rb") as f:
  dm = f.read()

count = getCount(dm) - 1

kids = EnclosedString(dm, "/Kids[", "]")

# we skip the first dummy that should be 4 0 R because of the `mutool merge`
assert kids.startswith("4 0 R ")
kids = kids[6:]

dm = dm[dm.find("5 0 obj"):]
dm = dm.replace("/Parent 2 0 R", "/Parent 4 0 R")
dm = dm.replace("/Root 1 0 R", "/Root 3 0 R")

lensuffix = len(suffix) 
with open("hacked.pdf", "wb") as f:
  f.write(template % locals())
  f.write(dm)


print
print "KEEP CALM and IGNORE THE NEXT ERRORS"
os.system('mutool clean hacked.pdf cleaned.pdf')
lenPrefix = len(prefpdf)
with open("cleaned.pdf", "rb") as f:
  cleaned = f.read()
file1 = prefjpg + cleaned[lenPrefix:]
file2 = prefmp3 + cleaned[lenPrefix:]
file3 = prefpdf + cleaned[lenPrefix:]
with open("collision.jpg", "wb") as f:
  f.write(file1)
with open("collision.mp3", "wb") as f:
  f.write(file2)
with open("collision.pdf", "wb") as f:
  f.write(file3)
os.remove('merged.pdf')
os.remove('hacked.pdf')
os.remove('cleaned.pdf')

md5 = hashlib.md5(file1).hexdigest()

assert md5 == hashlib.md5(file2).hexdigest()

# to prove the files should be 100% valid
print
os.system('mutool info -X collision.pdf')
print

print
print "MD5: %s" % md5
print "Success!"





