import train as tr
import generate as gen

tr.train("text.txt", "model.txt")
gen.generate("model.txt", 20, 20)