import tehr_helpers
import json
import collections

archPathAnnots = []

def unpackStdAnnotations(term, aqlPath, nodeId, type):
    for d in term.values():
        tbs = {}
        tid = d['terminologyId']
        tval = d['value']
        if aqlPath:
            global archPathAnnots
            tbs['type'] = type
            tbs['aqlPath'] = aqlPath
            tbs['nodeId'] = nodeId
            tbs['terminologyId'] = tid
            tbs['code'] = tval
            archPathAnnots.append(tbs)


# Generator parser
def item_generator(json_input, lookup_term, key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_term:
                try:
                    aq = json_input[key]
                except:
                    aq = None
                try:
                    nodeid = json_input['nodeId']
                except:
                    nodeid = None
                yield v, aq, nodeid
            else:
                for child_val in item_generator(v, lookup_term, key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_term, key):
                yield item_val


def getStdTermBindings (wt):
    tbinds = item_generator(wt, 'termBindings', 'aqlPath')
    for t, a, n in tbinds:
        unpackStdAnnotations(t, a, n, 'Archetype path')


def getValueTermBindings(wt):
    custom_tbinds = item_generator(wt, 'aqlPath', 'inputs')
    ls = []
    for aqlPath, inputs, nodeId in custom_tbinds:
        if isinstance(inputs, list):
            for item in inputs:
                try:
                    if item['suffix'] == 'code' and item['type'] == 'CODED_TEXT':
                        try:
                            if item['terminology'] is not None and item['terminology'] != 'openehr':
                                for moreitem in item['list']:
                                    tbs = collections.OrderedDict()
                                    tbs['type'] = 'Template valuelist'
                                    tbs['path'] = aqlPath
                                    tbs['nodeId'] = nodeId
                                    tbs['terminologyId'] = item['terminology']
                                    tbs['code'] = moreitem['value']
                                    ls.append(tbs)

                        except KeyError:
                            for moreitem in item['list']:
                                tbs = moreitem['termBindings']
                                nodeId = moreitem['value']
                                unpackStdAnnotations(tbs, aqlPath, nodeId, 'Archetype valuelist')

                except KeyError:
                    pass
    return ls


def getTermBindings(**kwargs):

    template_name = kwargs.get('templateName', None)
    template_file = kwargs.get('templateFile', None)

    if template_name and not template_file:
        wt = tehr_helpers.getWebTemplate(templateName=template_name).json()
    if template_file and not template_name:
        with open(template_file) as webTemplateFile:
            wt = json.load(webTemplateFile)

    term_bindings = {}
    l1 = getValueTermBindings(wt)
    getStdTermBindings(wt)
    term_bindings= l1 + archPathAnnots

    return term_bindings


if __name__ == "__main__":
    templateName = ''
    templateFile = ''

    #templateName = 'KorayClinical4'
    templateFile = '..\\models\KorayClinical4-webtemplate.json'
    #templateFile = '..\\models\ANZACS-ACS.webtemplate.json'

    tb = None
    if templateName and not templateFile:
        tb = getTermBindings(templateName=templateName)
    if templateFile and not templateName:
        tb = getTermBindings(templateFile=templateFile)

    print(json.dumps(tb, indent=2))
