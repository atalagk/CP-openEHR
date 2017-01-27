import bioportal

# Get all ontologies from the REST service and parse the JSON
ontologies = bioportal.get_json("/ontologies")

# Iterate looking for ontology with acronym OPB
opb = None
for ontology in ontologies:
    if ontology["acronym"] == "OPB":
        opb = ontology

labels = []

# Using the hypermedia link called `classes`, get the first page
page = bioportal.get_json(opb["links"]["classes"])

# Iterate over the available pages adding labels from all classes
# When we hit the last page, the while loop will exit
next_page = page
while next_page:
    next_page = page["links"]["nextPage"]
    for opb_class in page["collection"]:
        labels.append(opb_class["prefLabel"])
    if next_page:
        page = bioportal.get_json(next_page)

# Output the labels
for label in labels:
    print(label)
