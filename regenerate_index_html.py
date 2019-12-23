from osgeo import gdal
import datetime
import glob
import os
import json

agency_list = json.loads(open('AGENCY.json','rb').read())
agencies = {}
for item in agency_list:
    agencies[item['id']] = item


dirnames = []
links = []
for dirname in glob.glob('*'):
    if not os.path.isdir(dirname):
        continue
    dirnames.append(dirname)

total_size = 0
set_files = set()
for dirname in sorted(dirnames):
    if '_' not in dirname:
        continue
    filenames = []
    readme_filename = None
    for f in glob.glob(dirname + '/*'):
        f = os.path.basename(f)
        if f.startswith('README'):
            assert not readme_filename
            readme_filename = f
        else:
            filenames.append(f)

    title = '<h3>%s</h3>' % (dirname)
    try:
        agency = agencies[dirname]
        title = '<h3><a href="%s">%s</h3>' % (agency['url'], agency['agency'])
    except KeyError:

        pass

    links.append('</ul><hr/><h3>%s</h3><ul>' % title )
    for f in [readme_filename] + sorted(filenames):

        assert f not in set_files
        set_files.add(f)

        full_filename = os.path.join(dirname, f)
        ds = gdal.OpenEx(full_filename)
        desc = ''
        if ds:
            imageDesc = ds.GetMetadataItem('TIFFTAG_IMAGEDESCRIPTION')
            if imageDesc:
                pos = imageDesc.find('. Converted from')
                if pos >= 0:
                    imageDesc = imageDesc[0:pos]
                desc = ': ' + imageDesc

        size_str = ''
        size = os.stat(full_filename).st_size
        total_size += size
        if size > 1024 * 1024:
            size_str = '. Size: %.1f MB' % (size / (1024. * 1024))

        if f.startswith('README'):
            last_modified = ''
        else:
            last_modified = '. Last modified: ' + datetime.datetime.utcfromtimestamp(os.stat(full_filename).st_mtime).strftime("%Y/%m/%d")

        links.append('<li><a href="%s">%s</a>%s%s%s</li>' % (f, f, desc, size_str, last_modified))

total_size_str = '%d MB' % (total_size // (1024 * 1024))

content = '<!-- This is a generated file by regenerate_index_html.py. Do not modify !!!! Modify index.html.in instead if you need to make changes-->\n\n'
content += open('index.html.in', 'rt').read().replace('${LINKS_WILL_BE_ADDED_HERE_BY_REGENERATE_INDEX_HTML}', '\n'.join(links)).replace('${TOTAL_SIZE}', total_size_str)
open('index.html', 'wt').write(content)
