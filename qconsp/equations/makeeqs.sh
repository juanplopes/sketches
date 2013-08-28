#!/bin/sh
rm *.svg
pdf2svg eq.pdf eq%d.svg all
