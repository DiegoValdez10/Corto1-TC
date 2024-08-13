from graphviz import Digraph

class Nodo:
    def __init__(self):
        self.transiciones = {}
        self.es_final = False

class Automata:
    def __init__(self):
        self.nodos = []
        self.nodo_inicial = None
        self.nodo_final = None

def construir_afn_letter():
    automata = Automata()
    inicial = Nodo()
    final = Nodo()
    final.es_final = True
    for c in 'ABab':
        inicial.transiciones[c] = [final]
    automata.nodos = [inicial, final]
    automata.nodo_inicial = inicial
    automata.nodo_final = final
    return automata

def construir_afn_digit():
    automata = Automata()
    inicial = Nodo()
    final = Nodo()
    final.es_final = True
    for c in '01':
        inicial.transiciones[c] = [final]
    automata.nodos = [inicial, final]
    automata.nodo_inicial = inicial
    automata.nodo_final = final
    return automata

def aplicar_cierre_positivo(automata):
    nuevo_inicial = Nodo()
    nuevo_final = Nodo()
    nuevo_final.es_final = True
    
    nuevo_inicial.transiciones['ε'] = [automata.nodo_inicial]
    automata.nodo_final.transiciones['ε'] = [automata.nodo_inicial, nuevo_final]
    automata.nodo_final.es_final = False
    
    automata.nodos.extend([nuevo_inicial, nuevo_final])
    automata.nodo_inicial = nuevo_inicial
    automata.nodo_final = nuevo_final
    
    return automata

def aplicar_cierre_kleene(automata):
    nuevo_inicial = Nodo()
    nuevo_final = Nodo()
    nuevo_final.es_final = True
    
    nuevo_inicial.transiciones['ε'] = [automata.nodo_inicial, nuevo_final]
    automata.nodo_final.transiciones['ε'] = [automata.nodo_inicial, nuevo_final]
    automata.nodo_final.es_final = False
    
    automata.nodos.extend([nuevo_inicial, nuevo_final])
    automata.nodo_inicial = nuevo_inicial
    automata.nodo_final = nuevo_final
    
    return automata

def aplicar_union(automata1, automata2):
    if not automata1.nodos:
        automata1.nodo_inicial = Nodo()
        automata1.nodo_final = Nodo()
        automata1.nodo_final.es_final = True
        automata1.nodos.extend([automata1.nodo_inicial, automata1.nodo_final])

    if not automata2.nodos:
        automata2.nodo_inicial = Nodo()
        automata2.nodo_final = Nodo()
        automata2.nodo_final.es_final = True
        automata2.nodos.extend([automata2.nodo_inicial, automata2.nodo_final])

    nuevo_inicial = Nodo()
    nuevo_final = Nodo()
    nuevo_final.es_final = True

    nuevo_inicial.transiciones['ε'] = [automata1.nodo_inicial, automata2.nodo_inicial]

    automata1.nodo_final.transiciones['ε'] = [nuevo_final]
    automata1.nodo_final.es_final = False
    automata2.nodo_final.transiciones['ε'] = [nuevo_final]
    automata2.nodo_final.es_final = False

    automata1.nodos.extend(automata2.nodos)
    automata1.nodos.extend([nuevo_inicial, nuevo_final])
    automata1.nodo_inicial = nuevo_inicial
    automata1.nodo_final = nuevo_final
    
    return automata1

def construir_afn_id():
    afn_letra = construir_afn_letter()
    afn_letra_o_digito = aplicar_union(construir_afn_letter(), construir_afn_digit())
    afn_cierre_letra_o_digito = aplicar_cierre_kleene(afn_letra_o_digito)

    afn_id = afn_letra
    afn_id.nodo_final.transiciones['ε'] = [afn_cierre_letra_o_digito.nodo_inicial]
    afn_id.nodos.extend(afn_cierre_letra_o_digito.nodos)
    afn_id.nodo_final = afn_cierre_letra_o_digito.nodo_final

    return afn_id

def construir_afn_number():
    afn_digits = aplicar_cierre_positivo(construir_afn_digit())

    afn_punto = Automata()
    inicial_punto = Nodo()
    final_punto = Nodo()
    final_punto.es_final = True
    inicial_punto.transiciones['.'] = [final_punto]
    afn_punto.nodos = [inicial_punto, final_punto]
    afn_punto.nodo_inicial = inicial_punto
    afn_punto.nodo_final = final_punto

    afn_fraccion = aplicar_cierre_positivo(construir_afn_digit())
    afn_punto.nodo_final.transiciones['ε'] = [afn_fraccion.nodo_inicial]
    afn_fraccion.nodo_final.es_final = True

    afn_fraccion_completa = Automata()
    afn_fraccion_completa.nodos = afn_punto.nodos + afn_fraccion.nodos
    afn_fraccion_completa.nodo_inicial = afn_punto.nodo_inicial
    afn_fraccion_completa.nodo_final = afn_fraccion.nodo_final

    afn_fraccion_opcional = aplicar_union(afn_fraccion_completa, Automata())

    afn_igual = Automata()
    inicial_igual = Nodo()
    final_igual = Nodo()
    final_igual.es_final = True
    inicial_igual.transiciones['='] = [final_igual]
    afn_igual.nodos = [inicial_igual, final_igual]
    afn_igual.nodo_inicial = inicial_igual
    afn_igual.nodo_final = final_igual

    afn_exponente = Automata()
    inicial_exp = Nodo()
    final_exp = Nodo()
    final_exp.es_final = True
    inicial_exp.transiciones['E'] = [final_exp]
    afn_exponente.nodos = [inicial_exp, final_exp]
    afn_exponente.nodo_inicial = inicial_exp
    afn_exponente.nodo_final = final_exp

    afn_signo = Automata()
    inicial_signo = Nodo()
    final_signo = Nodo()
    final_signo.es_final = True
    inicial_signo.transiciones['+'] = [final_signo]
    inicial_signo.transiciones['-'] = [final_signo]
    afn_signo.nodos = [inicial_signo, final_signo]
    afn_signo.nodo_inicial = inicial_signo
    afn_signo.nodo_final = final_signo

    afn_signo_opcional = aplicar_union(afn_signo, Automata())

    afn_digits_opcional = aplicar_union(aplicar_cierre_positivo(construir_afn_digit()), Automata())

    afn_number_completo = Automata()
    afn_number_completo.nodos = (
        afn_digits.nodos +
        afn_fraccion_opcional.nodos +
        afn_igual.nodos +
        afn_exponente.nodos +
        afn_signo_opcional.nodos +
        afn_digits_opcional.nodos
    )
    afn_number_completo.nodo_inicial = afn_digits.nodo_inicial

    afn_digits.nodo_final.transiciones['ε'] = [afn_fraccion_opcional.nodo_inicial]
    afn_fraccion_opcional.nodo_final.transiciones['ε'] = [afn_igual.nodo_inicial]
    afn_igual.nodo_final.transiciones['ε'] = [afn_exponente.nodo_inicial]
    afn_exponente.nodo_final.transiciones['ε'] = [afn_signo_opcional.nodo_inicial]
    afn_signo_opcional.nodo_final.transiciones['ε'] = [afn_digits_opcional.nodo_inicial]

    afn_number_completo.nodo_final = afn_digits_opcional.nodo_final

    return afn_number_completo

def guardar_afn(afn, nombre):
    dot = Digraph(comment=f'AFN para {nombre}')
    dot.attr(rankdir='LR', size='10,7', dpi='300')  # Ajusta la resolución a 300 dpi

    with dot.subgraph(name=f'cluster_{nombre}') as c:
        c.attr(label=f'AFN para {nombre}')
        for i, nodo in enumerate(afn.nodos):
            forma = 'doublecircle' if nodo.es_final else 'circle'
            c.node(f'{nombre}{i}', shape=forma, fontsize='14')  # Ajusta el tamaño de la fuente
            for simbolo, nodos_siguientes in nodo.transiciones.items():
                for nodo_siguiente in nodos_siguientes:
                    c.edge(f'{nombre}{i}', f'{nombre}{afn.nodos.index(nodo_siguiente)}', label=simbolo, fontsize='12')  # Ajusta el tamaño de la fuente

    dot.render(f'{nombre}_afn', format='png', cleanup=True)
    print(f"El gráfico para {nombre} se ha guardado como '{nombre}_afn.png'")

# Crear y guardar cada AFN
afn_letter = construir_afn_letter()
guardar_afn(afn_letter, 'letter')

afn_digit = construir_afn_digit()
guardar_afn(afn_digit, 'digit')

afn_digits = aplicar_cierre_positivo(construir_afn_digit())
guardar_afn(afn_digits, 'digits')

afn_id = construir_afn_id()
guardar_afn(afn_id, 'id')

afn_number = construir_afn_number()
guardar_afn(afn_number, 'number')

