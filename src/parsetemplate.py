import tehr_helpers
import json
import pprint

preAql = None
def unpack_std_annotations(term, aql):

    for d in term.values():
        tId = d['terminologyId']
        tVal = d['value']

        print()
        global preAql
        if aql == 'N/A':
            print("Valuelist")
            print('path = ' + preAql)
        else:
            print('Archetype path')
            print('path = ' + aql)
            preAql = aql

        print('terminologyId = ' + tId)
        print('code = ' + tVal)


#Generator parser
def item_generator(json_input, lookup_term, key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_term:
                try:
                    aq = json_input[key]
                except:
                    aq = 'N/A'
                yield v, aq
            else:
                for child_val in item_generator(v, lookup_term, key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_term, key):
                yield item_val

def getStdTermBindings (wt):

    tbinds = item_generator(wt, 'termBindings', 'aqlPath')

    for t, a in tbinds:
        unpack_std_annotations(t, a)

def getCustomTermBindings (wt):

    custom_tbinds = item_generator(wt, 'terminology', 'list')
    for t, l in custom_tbinds:
        print()
        print('Custom terminologyId = ' + t)
        #unpack_custom_annotations(l)
        for item in l:
            print('code = ' + item['value'])

#wt = tehr_helpers.getWebTemplate(templateName='KorayClinical4')
with open('..\\models\KorayClinical4-webtemplate.json') as webTemplateFile:
    wt = json.load(webTemplateFile)

getStdTermBindings(wt)
getCustomTermBindings(wt)