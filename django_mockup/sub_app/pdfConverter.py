# source code: https://github.com/baruchel/txt2pdf
# -*- coding: utf-8 -*-

import reportlab.lib.pagesizes
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import units
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
import sys
import os

text_path="sub_app/RentalAgreementsData/RentalAgreementTextFiles/rental.txt"
pdf_path = "sub_app/RentalAgreementsData/RentalAgreementsPDFs/RentalAgreement.pdf"
class Margins(object):
    def __init__(self, right, left, top, bottom):
        self._right = right
        self._left = left
        self._top = top
        self._bottom = bottom

    @property
    def right(self):
        return self._right * units.cm

    @property
    def left(self):
        return self._left * units.cm

    @property
    def top(self):
        return self._top * units.cm

    @property
    def bottom(self):
        return self._bottom * units.cm

    def adjustLeft(self, width):
        self._left -= width / units.cm


class PDFCreator(object):
    appName = "txt2pdf (version 1.0)"

    def __init__(self, args, margins):
        pageWidth, pageHeight = reportlab.lib.pagesizes.__dict__[args['media']]
        if args['landscape']:
            pageWidth, pageHeight = reportlab.lib.pagesizes.landscape(
                (pageWidth, pageHeight))
        self.author = args['author']
        self.title = args['title']
        self.keywords = args['keywords']
        self.subject = args['subject']
        self.canvas = Canvas(args['output'], pagesize=(pageWidth, pageHeight))
        self.canvas.setCreator(self.appName)
        if len(args['author']) > 0:
            self.canvas.setAuthor(args['author'])
        if len(args['title']) > 0:
            self.canvas.setTitle(args['title'])
        if len(args['subject']) > 0:
            self.canvas.setSubject(args['subject'])
        if len(args['keywords']) > 0:
            self.canvas.setKeywords(args['keywords'])
        self.fontSize = args['font_size']
        if args['font'] not in ('Courier'):
            self.font = 'myFont'
            pdfmetrics.registerFont(TTFont('myFont', args['font']))
        else:
            self.font = args['font']
        self.kerning = args['kerning']
        self.margins = margins
        self.leading = (args['extra_vertical_space'] + 1.2) * self.fontSize
        self.linesPerPage = int(
            (self.leading + pageHeight
             - margins.top - margins.bottom - self.fontSize) / self.leading)
        self.lppLen = len(str(self.linesPerPage))
        fontWidth = self.canvas.stringWidth(
            ".", fontName=self.font, fontSize=self.fontSize)
        self.lineNumbering = args['line_numbers']
        if self.lineNumbering:
            margins.adjustLeft(fontWidth * (self.lppLen + 2))
        contentWidth = pageWidth - margins.left - margins.right
        self.charsPerLine = int(
            (contentWidth + self.kerning) / (fontWidth + self.kerning))
        self.top = pageHeight - margins.top - self.fontSize
        self.filename = args['filename']
        self.verbose = not args['quiet']
        self.breakOnBlanks = args['break_on_blanks']
        self.encoding = args['encoding']
        self.pageNumbering = args['page_numbers']
        if self.pageNumbering:
            self.pageNumberPlacement = \
               (pageWidth / 2, margins.bottom / 2)

    def _process(self, data):
        flen = os.fstat(data.fileno()).st_size
        lineno = 0
        read = 0
        for line in data:
            lineno += 1
            if sys.version_info.major == 2:
                read += len(line)
                yield flen == \
                    read, lineno, line.decode(self.encoding).rstrip('\r\n')
            else:
                read += len(line.encode(self.encoding))
                yield flen == read, lineno, line.rstrip('\r\n')

    def _readDocument(self):
        with open(self.filename, 'r') as data:
            for done, lineno, line in self._process(data):
                if len(line) > self.charsPerLine:
                    self._scribble(
                        "Warning: wrapping line %d in %s" %
                        (lineno + 1, self.filename))
                    while len(line) > self.charsPerLine:
                        yield done, line[:self.charsPerLine]
                        line = line[self.charsPerLine:]
                yield done, line

    def _newpage(self):
        textobject = self.canvas.beginText()
        textobject.setFont(self.font, self.fontSize, leading=self.leading)
        textobject.setTextOrigin(self.margins.left, self.top)
        textobject.setCharSpace(self.kerning)
        if self.pageNumbering:
            self.canvas.drawString(
                self.pageNumberPlacement[0],
                self.pageNumberPlacement[1],
                str(self.canvas.getPageNumber()))
        return textobject

    def _scribble(self, text):
        if self.verbose:
            sys.stderr.write(text + os.linesep)

    def generate(self):
        self._scribble(
            "Writing '%s' with %d characters per "
            "line and %d lines per page..." %
            (self.filename, self.charsPerLine, self.linesPerPage)
        )
        if self.breakOnBlanks:
            pageno = self._generateBob(self._readDocument())
        else:
            pageno = self._generatePlain(self._readDocument())
        self._scribble("PDF document: %d pages" % pageno)

    def _generatePlain(self, data):
        pageno = 1
        lineno = 0
        page = self._newpage()
        for _, line in data:
            lineno += 1

            # Handle form feed characters.
            (line, pageBreakCount) = re.subn(r'\f', r'', line)
            if pageBreakCount > 0 and lineno >= args['minimum_page_length']:
                for _ in range(pageBreakCount):
                    self.canvas.drawText(page)
                    self.canvas.showPage()
                    lineno = 0
                    pageno += 1
                    page = self._newpage()
                    if args['minimum_page_length'] > 0:
                        break

            page.textLine(line)

            if lineno == self.linesPerPage:
                self.canvas.drawText(page)
                self.canvas.showPage()
                lineno = 0
                pageno += 1
                page = self._newpage()
        if lineno > 0:
            self.canvas.drawText(page)
        else:
            pageno -= 1
        self.canvas.save()
        return pageno

    def _writeChunk(self, page, chunk, lineno):
        if self.lineNumbering:
            formatstr = '%%%dd: %%s' % self.lppLen
            for index, line in enumerate(chunk):
                page.textLine(
                    formatstr % (lineno - len(chunk) + index + 1, line))
        else:
            for line in chunk:
                page.textLine(line)

    def _generateBob(self, data):
        pageno = 1
        lineno = 0
        page = self._newpage()
        chunk = list()
        for last, line in data:
            if lineno == self.linesPerPage:
                self.canvas.drawText(page)
                self.canvas.showPage()
                lineno = len(chunk)
                pageno += 1
                page = self._newpage()
            lineno += 1
            chunk.append(line)
            if last or len(line.strip()) == 0:
                self._writeChunk(page, chunk, lineno)
                chunk = list()
        if lineno > 0:
            self.canvas.drawText(page)
            self.canvas.showPage()
        else:
            pageno -= 1
        if len(chunk) > 0:
            page = self._newpage()
            self.canvas.drawText(page)
            self.canvas.showPage()
            pageno += 1
        self.canvas.save()
        return pageno

args = dict()
args['filename']=text_path
args['font'] = 'Courier'
args['font_size'] = 10.0
args['extra_vertical_space'] = 0.0
args['kerning'] = 0.0
args['media'] = 'A4'
args['minimum_page_length'] = 10
args['landscape'] = False

args['margin-left'] = 2.0
args['margin-right'] = 2.0
args['margin-top'] = 2.0
args['margin-bottom'] = 2.0
args['output'] = pdf_path
args['author'] = ''
args['title'] = 'Rental Agreement'
args['quiet'] = False
args['subject'] = ''
args['keywords'] = ''
args['break_on_blanks'] = False
args['encoding'] = 'utf8'
args['page_numbers'] = True
args['line_numbers'] = False

def save_pdf_convert():
    global args
    print(args)
    PDFCreator(args, Margins(
        args['margin-right'],
        args['margin-left'],
        args['margin-top'],
        args['margin-bottom'])).generate()
