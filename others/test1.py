from PIL import Image, ImageOps
import subprocess, sys, os, glob

# minimum run of adjacent pixels to call something a line
H_THRESH = 300
V_THRESH = 300

def get_hlines(pix, w, h):
    """Get start/end pixels of lines containing horizontal runs of at least THRESH black pix"""
    hlines = []
    for y in range(h):
        x1, x2 = (None, None)
        black = 0
        run = 0
        for x in range(w):
            if pix[x,y] == (0,0,0):
                black = black + 1
                if not x1: x1 = x
                x2 = x
            else:
                if black > run:
                    run = black
                black = 0
        if run > H_THRESH:
            hlines.append((x1,y,x2,y))
    return hlines

def get_vlines(pix, w, h):
    """Get start/end pixels of lines containing vertical runs of at least THRESH black pix"""
    vlines = []
    for x in range(w):
        y1, y2 = (None,None)
        black = 0
        run = 0
        for y in range(h):
            if pix[x,y] == (0,0,0):
                black = black + 1
                if not y1: y1 = y
                y2 = y
            else:
                if black > run:
                    run = black
                black = 0
        if run > V_THRESH:
            vlines.append((x,y1,x,y2))
    return vlines
 
def get_cols(vlines):
    """Get top-left and bottom-right coordinates for each column from a list of vertical lines"""
    cols = []
    for i in range(1, len(vlines)):
        if vlines[i][0] - vlines[i-1][0] > 1:
            cols.append((vlines[i-1][0],vlines[i-1][1],vlines[i][2],vlines[i][3]))
    return cols
 
def get_rows(hlines):
    """Get top-left and bottom-right coordinates for each row from a list of vertical lines"""
    rows = []
    for i in range(1, len(hlines)):
        if hlines[i][1] - hlines[i-1][3] > 1:
            rows.append((hlines[i-1][0],hlines[i-1][1],hlines[i][2],hlines[i][3]))
    return rows          
 
def get_cells(rows, cols):
    """Get top-left and bottom-right coordinates for each cell usings row and column coordinates"""
    cells = {}
    for i, row in enumerate(rows):
        cells.setdefault(i, {})
        for j, col in enumerate(cols):
            x1 = col[0]
            y1 = row[1]
            x2 = col[2]
            y2 = row[3]
            cells[i][j] = (x1,y1,x2,y2)
    return cells
 
def ocr_cell(im, cells, x, y):
    """Return OCRed text from this cell"""
    fbase = "working/%d-%d" % (x, y)
    ftif = "%s.tif" % fbase
    ftxt = "%s.txt" % fbase
    cmd = "tesseract %s %s" % (ftif, fbase)
    # extract cell from whole image, grayscale (1-color channel), monochrome
    region = im.crop(cells[x][y])
    region = ImageOps.grayscale(region)
    region = region.point(lambda p: p > 200 and 255)
    # determine background color (most used color)
    histo = region.histogram()
    if histo[0] > histo[255]: bgcolor = 0
    else: bgcolor = 255
    # trim borders by finding top-left and bottom-right bg pixels
    pix = region.load()
    x1,y1 = 0,0
    x2,y2 = region.size
    x2,y2 = x2-1,y2-1
    while pix[x1,y1] != bgcolor:
        x1 += 1
        y1 += 1
    while pix[x2,y2] != bgcolor:
        x2 -= 1
        y2 -= 1
    # save as TIFF and extract text with Tesseract OCR
    trimmed = region.crop((x1,y1,x2,y2))
    trimmed.save(ftif, "TIFF")
    subprocess.call([cmd], shell=True, stderr=subprocess.PIPE)
    lines = [l.strip() for l in open(ftxt).readlines()]
    return lines[0]
 
def get_image_data(filename):
    """Extract textual data[rows][cols] from spreadsheet-like image file"""
    im = Image.open(filename)
    pix = im.load()
    width, height = im.size
    hlines = get_hlines(pix, width, height)
    sys.stderr.write("%s: hlines: %d\n" % (filename, len(hlines)))
    vlines = get_vlines(pix, width, height)
    sys.stderr.write("%s: vlines: %d\n" % (filename, len(vlines)))
    rows = get_rows(hlines)
    sys.stderr.write("%s: rows: %d\n" % (filename, len(rows)))
    cols = get_cols(vlines)
    sys.stderr.write("%s: cols: %d\n" % (filename, len(cols)))
    cells = get_cells(rows, cols)
 
    data = []
    for row in range(len(rows)):
        data.append([ocr_cell(im,cells, row, col) for col in range(len(cols))])
    return data
 
def split_pdf(filename):
    """Split PDF into PNG pages, return filenames"""
    prefix = filename[:-4]
    cmd = "magick convert -density 600 %s working/%s-%%d.png" % (filename, prefix)
    print('cmd = ',cmd)
    subprocess.call([cmd], shell=True)
    return [f for f in glob.glob(os.path.join('working', '%s*' % prefix))]

def extract_pdf(filename):
    """Extract table data from pdf"""
    #pngfiles = split_pdf(filename)
    pngfiles = [ "dic.png" ]
    sys.stderr.write("Pages: %d\n" % len(pngfiles))
    # extract table data from each page
    data = []
    for pngfile in pngfiles:
        pngdata = get_image_data(pngfile)
        for d in pngdata:
            data.append(d)
        # remove temp files for this page
        #os.system("rm working/*.tif")
        #os.system("rm working/*.txt")
    # remove split pages
    #os.system("rm working/*")
    return data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("Usage: ctocr.py FILENAME")
        exit()
    # split target pdf into pages
    filename = sys.argv[1]
    data = extract_pdf(filename)
    for row in data:
        print ("\t".join(row))