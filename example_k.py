import http
import ktorgb
np = ktorgb.setup()


def kset(k, i):
    ktorgb.set_all(np, ktorgb.ktorgb(int(k)), float(i))
    return ""


http.serve({'ktorgb': kset})
