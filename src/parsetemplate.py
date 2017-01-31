import tehr_helpers

def unpack_annotations():
    #aql = binds[::2]
    #term = binds[1::2]

    #print(aql)
    #print(term)

    s = []
    o = []
    p = []

    for i in aql:
        #print(i)
        s.append(i)

    for t in term:
        #print(t[next(iter(t))]['terminologyId'])
        p.append(t[next(iter(t))]['terminologyId'])
        #print(t[next(iter(t))]['value'])
        o.append(t[next(iter(t))]['value'])

    for l in range(0, len(aql)):
        print(str(l))
        print('   path = ' + s[l])
        print('   terminologyId = ' + p[l])
        print('   code = ' + o[l])


#Alternative parser
def item_generator(json_input, lookup_key):     #gets all termBindings but not aqlPath :(
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                aq = item_generator(json_input, 'aqlPath')
                yield v, aq
            else:
                for child_val in item_generator(v, lookup_key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_key):
                yield item_val

def get_recursively(search_dict, field):
    fields_found = []
    aql_path = []

    for key, value in search_dict.items():

        if key == field:
            fields_found.append(value)
            if search_dict['aqlPath'] != "":
                aql_path.append(search_dict['aqlPath'])

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return aql_path + fields_found

def searchTemplate (t):
    tbinds = get_recursively(t.json(), 'termBindings')
    print(tbinds)
    quit()

    tbinds = item_generator(t.json(), 'termBindings')

    for t, a in tBinds:
        x = next(a, 'No AQL')
        if x != 'No AQL':
            print(t, x[0])
    print('End of first pass')


wt = tehr_helpers.getWebTemplate(templateName='KorayClinical4')

searchTemplate(wt)
