import tehr_helpers
import json
import pprint


def unpack_annotations(term, aql):

    for d in term.values():
        tId = d['terminologyId']
        tVal = d['value']

        print()
        print('path = ' + aql)
        print('terminologyId = ' + tId)
        print('code = ' + tVal)

#Generator parser
def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                #aq = item_generator(json_input, 'aqlPath')
                try:
                    aq = json_input['aqlPath']
                except:
                    aq = "None"
                yield v, aq
            else:
                for child_val in item_generator(v, lookup_key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_key):
                yield item_val

def searchTemplate (t):

    tbinds = item_generator(t, 'termBindings')

    for t, a in tbinds:
        #print(t, a)
        unpack_annotations(t, a)

#wt = tehr_helpers.getWebTemplate(templateName='KorayClinical4')
with open('..\\models\KorayClinical4-webtemplate.json') as webTemplateFile:
    wt = json.load(webTemplateFile)

searchTemplate(wt)
