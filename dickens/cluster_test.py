from clic.dickens.clusters import Clusters

clusters = Clusters()

idxName = 'quote-3gram-idx'
Materials = ['BH']

test = clusters.list_clusters(idxName, Materials)

print test


