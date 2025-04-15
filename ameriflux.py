import csv


def sites_marker_list():
    """ Export from https://ameriflux.lbl.gov/sites/site-search/"""
    # ['network', 'lat', 'lon', 'country', 'sid', 'pi', 'desc']

    _file = 'AmeriFlux-sites.csv'
    datatable = []
    with open(_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for row in reader:
            l = ['ameriflux']
            l += [float(row[13])]
            l += [float(row[14])]
            l += [row[12]]
            l += [row[0]]
            l += [row[2]]
            l += [row[1]]

            assert len(l) == 7

            datatable.append(l)

    return datatable
