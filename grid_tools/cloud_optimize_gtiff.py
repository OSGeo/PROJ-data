#!/usr/bin/env python
###############################################################################
# $Id$
#
#  Project:  PROJ
#  Purpose:  Cloud optimize a GeoTIFF file
#  Author:   Even Rouault <even.rouault at spatialys.com>
#
###############################################################################
#  Copyright (c) 2019, Even Rouault <even.rouault at spatialys.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
###############################################################################

from osgeo import gdal

import argparse
import os
import struct


def get_args():
    parser = argparse.ArgumentParser(
        description='Convert a GeoTIFF file into a cloud optimized one.')
    parser.add_argument('source',
                        help='Source GeoTIFF file')
    parser.add_argument('dest',
                        help='Destination GeoTIFF file')

    return parser.parse_args()


def generate_optimized_file(srcfilename, destfilename):

    TIFF_BYTE = 1        # 8-bit unsigned integer
    TIFF_ASCII = 2       # 8-bit bytes w/ last byte null
    TIFF_SHORT = 3       # 16-bit unsigned integer
    TIFF_LONG = 4        # 32-bit unsigned integer
    TIFF_RATIONAL = 5    # 64-bit unsigned fraction
    TIFF_SBYTE = 6       # !8-bit signed integer
    TIFF_UNDEFINED = 7   # !8-bit untyped data
    TIFF_SSHORT = 8      # !16-bit signed integer
    TIFF_SLONG = 9       # !32-bit signed integer
    TIFF_SRATIONAL = 10  # !64-bit signed fraction
    TIFF_FLOAT = 11      # !32-bit IEEE floating point
    TIFF_DOUBLE = 12     # !64-bit IEEE floating point
    TIFF_IFD = 13        # %32-bit unsigned integer (offset)
    TIFF_LONG8 = 16      # BigTIFF 64-bit unsigned integer
    TIFF_SLONG8 = 17     # BigTIFF 64-bit signed integer
    TIFF_IFD8 = 18        # BigTIFF 64-bit unsigned integer (offset)

    TIFFTAG_STRIPOFFSETS = 273
    TIFFTAG_SAMPLESPERPIXEL = 277
    TIFFTAG_STRIPBYTECOUNTS = 279
    TIFFTAG_PLANARCONFIG = 284
    TIFFTAG_TILEOFFSETS = 324
    TIFFTAG_TILEBYTECOUNTS = 325

    PLANARCONFIG_CONTIG = 1
    PLANARCONFIG_SEPARATE = 2

    TIFFTAG_GDAL_METADATA = 42112

    typesize = {}
    typesize[TIFF_BYTE] = 1
    typesize[TIFF_ASCII] = 1
    typesize[TIFF_SHORT] = 2
    typesize[TIFF_LONG] = 4
    typesize[TIFF_RATIONAL] = 8
    typesize[TIFF_SBYTE] = 1
    typesize[TIFF_UNDEFINED] = 1
    typesize[TIFF_SSHORT] = 2
    typesize[TIFF_SLONG] = 4
    typesize[TIFF_SRATIONAL] = 8
    typesize[TIFF_FLOAT] = 4
    typesize[TIFF_DOUBLE] = 8
    typesize[TIFF_IFD] = 4
    typesize[TIFF_LONG8] = 8
    typesize[TIFF_SLONG8] = 8
    typesize[TIFF_IFD8] = 8

    class OfflineTag:
        def __init__(self, tagtype, nvalues, data, fileoffset_in_out_ifd):
            self.tagtype = tagtype
            self.nvalues = nvalues
            self.data = data
            self.fileoffset_in_out_ifd = fileoffset_in_out_ifd

        def unpack_array(self):
            if type(self.data) == type((0,)):
                return self.data
            elif self.tagtype == TIFF_SHORT:
                return struct.unpack('<' + ('H' * self.nvalues), self.data)
            elif self.tagtype == TIFF_LONG:
                return struct.unpack('<' + ('I' * self.nvalues), self.data)
            else:
                assert False

    class IFD:
        def __init__(self, tagdict):
            self.tagdict = tagdict

    ds = gdal.Open(srcfilename)
    assert ds
    first_band_to_put_at_end = None
    if ds.GetMetadataItem('TYPE') == 'HORIZONTAL_OFFSET' and \
       ds.RasterCount >= 4 and \
       ds.GetRasterBand(1).GetDescription() == 'latitude_offset' and \
       ds.GetRasterBand(2).GetDescription() == 'longitude_offset' and \
       ds.GetRasterBand(3).GetDescription() == 'latitude_offset_accuracy' and \
       ds.GetRasterBand(4).GetDescription() == 'longitude_offset_accuracy':
        first_band_to_put_at_end = 3
    elif ds.GetMetadataItem('TYPE') == 'VELOCITY' and \
       ds.RasterCount >= 6 and \
       ds.GetRasterBand(1).GetDescription() == 'east_velocity' and \
       ds.GetRasterBand(2).GetDescription() == 'north_velocity' and \
       ds.GetRasterBand(3).GetDescription() == 'up_velocity' and \
       ds.GetRasterBand(4).GetDescription() == 'east_velocity_accuracy' and \
       ds.GetRasterBand(5).GetDescription() == 'north_velocity_accuracy' and \
       ds.GetRasterBand(6).GetDescription() == 'up_velocity_accuracy':
        first_band_to_put_at_end = 4
    del ds

    in_f = open(srcfilename, 'rb')
    signature = in_f.read(4)
    assert signature == b'\x49\x49\x2A\x00'
    next_ifd_offset = struct.unpack('<I', in_f.read(4))[0]

    out_f = open(destfilename, 'wb')
    out_f.write(signature)
    next_ifd_offset_out_offset = 4
    # placeholder for pointer to next IFD
    out_f.write(struct.pack('<I', 0xDEADBEEF))

    out_f.write(b'\n-- Generated by cloud_optimize_gtiff.py v1.0 --\n')
    essential_metadata_size_hint_offset_to_patch = out_f.tell()
    dummy_metadata_hint = b'-- Metadata size: XXXXXX --\n'
    out_f.write(dummy_metadata_hint)

    ifds = []

    offlinedata_to_offset = {}

    reuse_offlinedata = True

    while next_ifd_offset != 0:

        in_f.seek(next_ifd_offset)

        cur_pos = out_f.tell()
        if (cur_pos % 2) == 1:
            out_f.write(b'\x00')
            cur_pos += 1
        out_f.seek(next_ifd_offset_out_offset)
        out_f.write(struct.pack('<I', cur_pos))
        out_f.seek(cur_pos)

        numtags = struct.unpack('<H', in_f.read(2))[0]
        out_f.write(struct.pack('<H', numtags))

        tagdict = {}
        ifd = IFD(tagdict)

        # Write IFD
        for i in range(numtags):
            tagid = struct.unpack('<H', in_f.read(2))[0]
            tagtype = struct.unpack('<H', in_f.read(2))[0]
            tagnvalues = struct.unpack('<I', in_f.read(4))[0]
            tagvalueoroffset_raw = in_f.read(4)
            tagvalueoroffset = struct.unpack('<I', tagvalueoroffset_raw)[0]
            #print(tagid, tagtype, tagnvalues, tagvalueoroffset)
            tagvalsize = typesize[tagtype] * tagnvalues

            if tagid == TIFFTAG_PLANARCONFIG:
                assert tagvalueoroffset in (
                    PLANARCONFIG_CONTIG, PLANARCONFIG_SEPARATE)
                ifd.planarconfig_contig = True if tagvalueoroffset == PLANARCONFIG_CONTIG else False
            elif tagid == TIFFTAG_SAMPLESPERPIXEL:
                ifd.nbands = tagvalueoroffset

            out_f.write(struct.pack('<H', tagid))
            out_f.write(struct.pack('<H', tagtype))
            out_f.write(struct.pack('<I', tagnvalues))
            if tagvalsize <= 4:
                if tagid in (TIFFTAG_STRIPOFFSETS, TIFFTAG_TILEOFFSETS):
                    ifd.offset_out_offsets = out_f.tell()
                    if tagtype == TIFF_SHORT:
                        tagdict[tagid] = OfflineTag(
                            tagtype, tagnvalues, struct.unpack('<HH', tagvalueoroffset_raw), -ifd.offset_out_offsets)
                    elif tagtype == TIFF_LONG:
                        tagdict[tagid] = OfflineTag(
                            tagtype, tagnvalues, struct.unpack('<I', tagvalueoroffset_raw), -ifd.offset_out_offsets)
                    out_f.write(struct.pack('<I', 0xDEADBEEF))  # placeholder
                else:
                    if tagtype == TIFF_SHORT:
                        tagdict[tagid] = OfflineTag(
                            tagtype, tagnvalues, struct.unpack('<HH', tagvalueoroffset_raw), -1)
                    elif tagtype == TIFF_LONG:
                        tagdict[tagid] = OfflineTag(
                            tagtype, tagnvalues, struct.unpack('<I', tagvalueoroffset_raw), -1)
                    out_f.write(struct.pack('<I', tagvalueoroffset))
            else:
                curinoff = in_f.tell()
                in_f.seek(tagvalueoroffset)
                tagdata = in_f.read(tagvalsize)
                in_f.seek(curinoff)

                if reuse_offlinedata and tagdata in offlinedata_to_offset:
                    tagdict[tagid] = OfflineTag(
                        tagtype, tagnvalues, tagdata, -1)
                    out_f.write(struct.pack(
                        '<I', offlinedata_to_offset[tagdata]))
                else:
                    tagdict[tagid] = OfflineTag(
                        tagtype, tagnvalues, tagdata, out_f.tell())
                    out_f.write(struct.pack('<I', 0xDEADBEEF))  # placeholder

        next_ifd_offset = struct.unpack('<I', in_f.read(4))[0]
        next_ifd_offset_out_offset = out_f.tell()
        # placeholder for pointer to next IFD
        out_f.write(struct.pack('<I', 0xDEADBEEF))

        # Write data for all out-of-line tags,
        # except the offset and byte count ones, and the GDAL metadata for the
        # IFDs after the first one, and patch IFD entries
        for id in tagdict:
            if tagdict[id].fileoffset_in_out_ifd < 0:
                continue
            if id in (TIFFTAG_STRIPOFFSETS, TIFFTAG_STRIPBYTECOUNTS,
                      TIFFTAG_TILEOFFSETS, TIFFTAG_TILEBYTECOUNTS):
                continue
            if id == TIFFTAG_GDAL_METADATA:
                if len(ifds) != 0:
                    continue
            cur_pos = out_f.tell()
            out_f.seek(tagdict[id].fileoffset_in_out_ifd)
            out_f.write(struct.pack('<I', cur_pos))
            out_f.seek(cur_pos)
            out_f.write(tagdict[id].data)
            if reuse_offlinedata:
                offlinedata_to_offset[tagdict[id].data] = cur_pos

        ifds.append(ifd)

    # Write GDAL_METADATA of ifds other than the first one
    for ifd in ifds[1:]:
        tagdict = ifd.tagdict

        if TIFFTAG_GDAL_METADATA in tagdict:
            id = TIFFTAG_GDAL_METADATA
            cur_pos = out_f.tell()
            out_f.seek(tagdict[id].fileoffset_in_out_ifd)
            out_f.write(struct.pack('<I', cur_pos))
            out_f.seek(cur_pos)
            out_f.write(tagdict[id].data)

    metadata_hint = ('-- Metadata size: %06d --\n' %
                     out_f.tell()).encode('ASCII')
    assert len(metadata_hint) == len(dummy_metadata_hint)
    out_f.seek(essential_metadata_size_hint_offset_to_patch)
    out_f.write(metadata_hint)
    out_f.seek(0, os.SEEK_END)

    # Write strile bytecounts and dummy offsets
    for idx_ifd, ifd in enumerate(ifds):
        tagdict = ifd.tagdict

        for id in tagdict:
            if tagdict[id].fileoffset_in_out_ifd < 0:
                continue
            if id not in (TIFFTAG_STRIPOFFSETS, TIFFTAG_STRIPBYTECOUNTS,
                          TIFFTAG_TILEOFFSETS, TIFFTAG_TILEBYTECOUNTS):
                continue

            cur_pos = out_f.tell()
            out_f.seek(tagdict[id].fileoffset_in_out_ifd)
            out_f.write(struct.pack('<I', cur_pos))
            out_f.seek(cur_pos)
            if id in (TIFFTAG_STRIPOFFSETS, TIFFTAG_TILEOFFSETS):
                ifd.offset_out_offsets = out_f.tell()
                # dummy. to be rewritten
                out_f.write(b'\00' * len(tagdict[id].data))
            else:
                out_f.write(tagdict[id].data)  # bytecounts don't change

    # Write blocks in a band-interleaved way
    for ifd in ifds:
        tagdict = ifd.tagdict

        if TIFFTAG_STRIPOFFSETS in tagdict:
            ifd.num_striles = tagdict[TIFFTAG_STRIPOFFSETS].nvalues
            assert ifd.num_striles == tagdict[TIFFTAG_STRIPBYTECOUNTS].nvalues
            ifd.strile_offset_in = tagdict[TIFFTAG_STRIPOFFSETS].unpack_array()
            ifd.strile_length_in = tagdict[TIFFTAG_STRIPBYTECOUNTS].unpack_array(
            )
        else:
            ifd.num_striles = tagdict[TIFFTAG_TILEOFFSETS].nvalues
            assert ifd.num_striles == tagdict[TIFFTAG_TILEBYTECOUNTS].nvalues
            ifd.strile_offset_in = tagdict[TIFFTAG_TILEOFFSETS].unpack_array()
            ifd.strile_length_in = \
                tagdict[TIFFTAG_TILEBYTECOUNTS].unpack_array()

        ifd.strile_offset_out = [0] * ifd.num_striles
        if ifd.planarconfig_contig:
            ifd.num_striles_per_band = ifd.num_striles
        else:
            assert (ifd.num_striles % ifd.nbands) == 0
            ifd.num_striles_per_band = ifd.num_striles // ifd.nbands

        if ifd.planarconfig_contig:
            list_bands = (0,)
        elif first_band_to_put_at_end:
            list_bands = range(first_band_to_put_at_end - 1)
        else:
            list_bands = range(ifd.nbands)

        for i in range(ifd.num_striles_per_band):
            for iband in list_bands:
                idx_strile = ifd.num_striles_per_band * iband + i
                in_f.seek(ifd.strile_offset_in[idx_strile])
                data = in_f.read(ifd.strile_length_in[idx_strile])
                ifd.strile_offset_out[idx_strile] = out_f.tell()
                out_f.write(data)

    # And then the errors at end for NTv2 like products
    if not ifd.planarconfig_contig and first_band_to_put_at_end and \
       ifd.nbands >= first_band_to_put_at_end:
        for ifd in ifds:
            if ifd.nbands < first_band_to_put_at_end:
                continue

            for i in range(ifd.num_striles_per_band):
                for iband in range(first_band_to_put_at_end-1, ifd.nbands):
                    idx_strile = ifd.num_striles_per_band * iband + i
                    in_f.seek(ifd.strile_offset_in[idx_strile])
                    data = in_f.read(ifd.strile_length_in[idx_strile])
                    ifd.strile_offset_out[idx_strile] = out_f.tell()
                    out_f.write(data)

    # Write strile offset arrays
    for ifd in ifds:
        tagdict = ifd.tagdict

        if TIFFTAG_STRIPOFFSETS in tagdict:
            tagtype = tagdict[TIFFTAG_STRIPOFFSETS].tagtype
        else:
            tagtype = tagdict[TIFFTAG_TILEOFFSETS].tagtype

        if ifd.offset_out_offsets < 0:
            assert ifd.offset_out_offsets != -1
            out_f.seek(-ifd.offset_out_offsets)
        else:
            out_f.seek(ifd.offset_out_offsets)
        if tagtype == TIFF_SHORT:
            for v in ifd.strile_offset_out:
                assert v < 65536
                out_f.write(struct.pack('<H', v))
        else:
            for v in ifd.strile_offset_out:
                out_f.write(struct.pack('<I', v))

    # Patch pointer to last IFD
    out_f.seek(next_ifd_offset_out_offset)
    out_f.write(struct.pack('<I', 0))

    in_f.close()
    out_f.close()


if __name__ == '__main__':

    args = get_args()

    generate_optimized_file(args.source, args.dest)
