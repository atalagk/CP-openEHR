import tehr_helpers
import json
import pprint
import collections

preAql = None


def unpackStdAnnotations(term, aql):
    tbs = collections.OrderedDict()
    for d in term.values():
        tId = d['terminologyId']
        tVal = d['value']

        global preAql
        if aql == 'N/A':
            tbs['type'] = "Valuelist from Archetype"
            tbs['path'] = preAql
        else:
            tbs['type'] = 'Archetype path'
            tbs['path'] = aql

        tbs['terminologyId'] = tId
        tbs['code'] = tVal
    return tbs


# Generator parser
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
    ls = []
    tbinds = item_generator(wt, 'termBindings', 'aqlPath')

    for t, a in tbinds:
        ls.append(unpackStdAnnotations(t, a))
    return ls


def getCustomTermBindings(wt):

    custom_tbinds = item_generator(wt, 'aqlPath', 'inputs')
    tbs = collections.OrderedDict()
    ls = []
    for a, i in custom_tbinds:
        if isinstance(i, list):
            for item in i:
                try:
                    if item['suffix'] == 'code' and item['type'] == 'CODED_TEXT':
                        if item['terminology'] is not None and item['terminology'] != 'openehr':
                            for moreitem in item['list']:
                                tbs['type'] = 'Valuelist from Template'
                                tbs['path'] = a
                                tbs['terminologyId'] = item['terminology']
                                tbs['code'] = moreitem['value']
                                ls.append(tbs)
                except:
                    pass
    return ls


def getTermBindings(**kwargs):

    templateName = kwargs.get('templateName', None)
    templateFile = kwargs.get('templateFile', None)

    if templateName:
        wt = tehr_helpers.getWebTemplate(templateName=templateName).json()
    if templateFile:
        with open(templateFile) as webTemplateFile:
            wt = json.load(webTemplateFile)

    tbs = {}
    l1 = getStdTermBindings(wt)
    l2 = getCustomTermBindings(wt)
    tbs = l1 + l2

    # need to call with either TemplateName or TemplateFile BUT not both!
    if templateName and not templateFile:
        tinfo = {'Template name' : templateName}
    if templateFile and not templateName:
        tinfo = {'Template file': templateFile}
    tbdict = {'Terminology bindings':tbs}
    tbinds = {**tinfo, **tbdict}  # works Python >3.5
    return tbinds


if __name__ == "__main__":
    templateName = ''
    templateFile = ''
    templateName = 'KorayClinical4'
    #templateFile = '..\\models\KorayClinical4-webtemplate.json'
    tb = None
    if templateName and not templateFile:
        tb = getTermBindings(templateName=templateName)
    if templateFile and not templateName:
        tb = getTermBindings(templateFile=templateFile)

    print(json.dumps(tb, indent=2))
