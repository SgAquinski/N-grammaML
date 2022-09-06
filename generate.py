import train as tr
import argparse as arp
import pickle

#parser = arp.ArgumentParser(description='Process some integers.')
#parser.add_argument("-input", input, type="str")
#tr.train("Муму.txt", "model.txt")
#gen.generate("model.txt", 20, 20)

t = tr.N_gram(2)
t.fit("data/Муму.txt", "model.txt")
#t.fit("data/МертвыеДуши.txt", "model.txt")
t.generate("model.txt", 20, prefix=None)