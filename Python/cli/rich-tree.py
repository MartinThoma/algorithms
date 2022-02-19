from rich.tree import Tree
from rich import print

tree = Tree("Life")

prokaryota = tree.add("Prokaryota")
prokaryota.add("Eubacteria")
prokaryota.add("Archaebacteria")

eukaryota = tree.add("Eukaryota")
eukaryota.add("Protozoa")
eukaryota.add("Chordata")
plantae = eukaryota.add("Plantae")
plantae.add("glaucophytes")
plantae.add("[red]red algae")
plantae.add("[green][bold]green algae")
plantae.add("land plants 🌳")
eukaryota.add("Fungi")
eukaryota.add("Animalia")
print(tree)
