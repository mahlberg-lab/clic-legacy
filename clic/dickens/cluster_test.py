from dickens.clusters import Clusters

clusters = Clusters()

idxName = 'quote-3gram-idx'
Materials = ['dickens']

test = clusters.list_clusters(idxName, Materials)

print test


