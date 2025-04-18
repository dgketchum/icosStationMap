import csv


def sites_marker_list():
    """ Export from https://ameriflux.lbl.gov/sites/site-search/"""
    # ['network', 'lat', 'lon', 'country', 'sid', 'pi', 'desc']

    _file = 'OzFlux_sites.csv'
    datatable = []
    with open(_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for row in reader:
            l = ['ozflux']
            l += [float(row[4])]
            l += [float(row[5])]
            l += ['']
            l += [row[1]]
            l += [row[7]]
            l += [row[2]]

            assert len(l) == 7

            datatable.append(l)

    return datatable
