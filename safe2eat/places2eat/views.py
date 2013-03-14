from django.shortcuts import render

from .forms import SearchEntry
from .methods import (patch_http_response_read, get_start_loc, get_list,
                      process_list, get_report, process_report
                      )


def get_entry(request):
    results = ''
    if request.method == 'POST':
        form = SearchEntry(request.POST)
        if request.POST.get('clear') == '':
            form = SearchEntry()
        else:
            if form.is_valid():
                street = form.cleaned_data['street_address']
                city_zip = form.cleaned_data['city_zip']
                dist = int(form.cleaned_data['search_distance'])
                address = street + ' ' + city_zip
                # get latitude/longitude for given addres vie Google Place API
                coords = get_start_loc(address)

                # Get restaurant listings based on search
                # using Google's Places API
                rest_results = get_list(coords, dist)

                # Process results of rest_list
                rest_list = process_list(rest_results)

                for item in rest_list:  # TODO:  Create method.

                    name = item['Name']
                    address = item['Address']
                    raw_report = get_report(name, address)
                    clean_report = process_report(raw_report, name, address)


                    # If an inspection was found.

                    if clean_report != "No inspection information found.":
                        try:
                            item['Inspection Date'] = clean_report[0]
                            item['Inspection Result'] = clean_report[1]
                        #  If there were dangerous violations.
                            if len(clean_report) > 2:
                                score, v_list = clean_report[2:]
                                item['Inspection Score'] = score
                                item['Violations'] = v_list
                        except TypeError:
                                pass
                    # results = item

                results = rest_list

    else:
        form = SearchEntry()
    return render(request, 'search.html', {'form': form,
                                           'results': results})


