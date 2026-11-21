"""
ceas_cuantic.py — uneltele provocării „Ceasul Cuantic al Iașului”
Qiskit Fall Fest Iași 2026 · Facultatea de Automatică și Calculatoare, TUIASI

Acest fișier NU conține răspunsuri. Verificarea, scorul și piesele secrete
(cutiile sigilate, nodul Copou, nodul Facultății, Umbra) sunt pe serverul organizatorilor.
"""

import json
import os
import urllib.error
import urllib.request

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Operator, Statevector

# Adresa serverului de verificare. Organizatorii o completează înainte de concurs.
SERVER = os.environ.get("CEAS_SERVER", "http://quantum-challenge.ac.tuiasi.ro:8000")

_SESIUNE = {"echipa": None, "cod": None}

ALFABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789().,!?-=+ĂÂÎȘȚ"
LOCATII = {
    "000": "Palatul Culturii", "001": "Teatrul Național", "010": "Teiul lui Eminescu",
    "011": "Biblioteca Centrală Universitară", "100": "Grădina Botanică", "101": "Turnul Goliei",
    "110": "Mitropolia", "111": "Campusul TUIASI",
}
NUMAR_SEMNALE_COPOU = 51
_PIESA = "qff_"


# =============================================================================
# Comunicarea cu serverul
# =============================================================================

class _Oprire(Exception):
    pass


def _cere(cale, date, cu_echipa=True):
    if cu_echipa:
        if not _SESIUNE["cod"]:
            raise _Oprire("Rulați întâi celula de pregătire: start(ECHIPA, COD_ECHIPA).")
        date = {"cod": _SESIUNE["cod"], **date}
    corp = json.dumps(date).encode("utf-8")
    cerere = urllib.request.Request(SERVER.rstrip("/") + cale, data=corp,
                                    headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(cerere, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as ex:
        raise _Oprire(f"Nu pot contacta serverul provocării ({SERVER}). Verificați rețeaua și anunțați mentorul. [{ex}]")


def _sigur(functie):
    """Afișează mesajele de eroare prietenos, fără traceback lung."""
    def invelis(*a, **k):
        try:
            return functie(*a, **k)
        except _Oprire as ex:
            print("⚠ " + str(ex))
        except _Gresit as ex:
            print("✘ Încă nu. " + str(ex))
    invelis.__name__, invelis.__doc__ = functie.__name__, functie.__doc__
    return invelis


class _Gresit(Exception):
    pass


# =============================================================================
# Trimiterea circuitelor
# =============================================================================

def _serializeaza(qc):
    if not isinstance(qc, QuantumCircuit):
        raise _Gresit("Era așteptat un QuantumCircuit.")
    ops = []
    for instr in qc.data:
        op = instr.operation
        qargs = [qc.find_bit(q).index for q in instr.qubits]
        if op.name == "measure":
            ops.append(["m", qargs[0], qc.find_bit(instr.clbits[0]).index])
        elif op.name in ("barrier", "delay"):
            continue
        elif op.name.startswith(_PIESA):
            ops.append(["ph", op.name, qargs, [float(p) for p in op.params]])
        else:
            if getattr(op, "condition", None) is not None or op.name in ("reset", "if_else", "while_loop", "for_loop"):
                raise _Gresit(f"Poarta „{op.name}” nu este acceptată de server în această provocare.")
            try:
                m = Operator(op).data
            except Exception:
                raise _Gresit(f"Poarta „{op.name}” nu poate fi trimisă. Nu împachetați cutiile sau semnalele în alte porți.")
            ops.append(["u", qargs, [[float(z.real), float(z.imag)] for z in np.asarray(m).ravel()]])
    return {"n": qc.num_qubits, "nc": qc.num_clbits, "ops": ops}


def _are_piese(qc):
    return any(instr.operation.name.startswith(_PIESA) for instr in qc.data)


def _are_masuratori(qc):
    return any(instr.operation.name == "measure" for instr in qc.data)


def _cu_masuratori(qc):
    c = qc.copy()
    if not _are_masuratori(c):
        c.measure_all()
    return c


def _piesa(nume, n, eticheta, params=()):
    g = Gate(nume, n, list(params))
    g.label = eticheta
    return g


# =============================================================================
# Pornire, turn, scor
# =============================================================================

def _svg_clopot(aprins, nr):
    c = "#E3A81B" if aprins else "none"
    k = "#9A6B00" if aprins else "#9AA0A6"
    t = "#3A2A00" if aprins else "#9AA0A6"
    return (f'<svg width="46" height="56" viewBox="0 0 46 56"><path d="M23 6 C12 6 10 18 10 28 L6 40 L40 40 L36 28 '
            f'C36 18 34 6 23 6 Z" fill="{c}" stroke="{k}" stroke-width="2"/><circle cx="23" cy="45" r="4" fill="{k}"/>'
            f'<text x="23" y="31" font-size="13" text-anchor="middle" font-family="sans-serif" font-weight="bold" '
            f'fill="{t}">{nr}</text></svg>')


def _afiseaza_turn(st):
    aprinse = st["clopote"]
    try:
        from IPython.display import HTML, display
        clopote = "".join(f'<div title="{st["clopote_nume"].get(str(i), "")}">{_svg_clopot(i in aprinse, i)}</div>'
                          for i in range(1, 9))
        display(HTML(f'<div style="border:1px solid #c9ced6;border-radius:10px;padding:12px 16px;max-width:520px;'
                     f'font-family:sans-serif"><div style="font-weight:600;margin-bottom:6px">Turnul echipei '
                     f'„{st["echipa"]}” — {len(aprinse)}/8 clopote · {st["scor"]} puncte</div>'
                     f'<div style="display:flex;gap:6px">{clopote}</div></div>'))
    except Exception:
        print(f"Turnul echipei {st['echipa']}: " + " ".join("[*]" if i in aprinse else "[ ]" for i in range(1, 9))
              + f"  {st['scor']} puncte")


@_sigur
def start(echipa, cod, server=None):
    """Înregistrează echipa în acest notebook. Folosiți același nume și cod în toate notebook-urile."""
    global SERVER
    if server:
        SERVER = server
    if not str(echipa).strip() or str(echipa).lower().startswith("numele"):
        raise _Oprire("Scrieți numele real al echipei voastre în ghilimele.")
    r = _cere("/api/start", {"cod": str(cod).strip().upper(), "echipa": str(echipa).strip()}, cu_echipa=False)
    if not r.get("ok"):
        raise _Oprire(r.get("mesaj"))
    _SESIUNE.update(echipa=r["echipa"], cod=str(cod).strip().upper())
    print(f"Bine ați venit, echipa „{r['echipa']}”! Sunteți conectați la serverul provocării.")
    _afiseaza_turn(r)


@_sigur
def turn():
    """Afișează turnul cu cele 8 clopote și scorul echipei."""
    r = _cere("/api/stare", {})
    if not r.get("ok"):
        raise _Oprire(r.get("mesaj"))
    _afiseaza_turn(r)


def scor():
    """Scorul curent al echipei."""
    try:
        r = _cere("/api/stare", {})
        return r.get("scor")
    except _Oprire as ex:
        print("⚠ " + str(ex))


def _verifica(sarcina, date):
    r = _cere("/api/verifica", {"sarcina": sarcina, "date": date})
    if not r.get("ok"):
        raise _Gresit(r.get("mesaj", ""))
    if r.get("info"):
        print(r["info"])
    if sarcina not in ("6C_hartie",):
        if r.get("deja"):
            print(f"✔ Corect! (Sarcina {sarcina} era deja rezolvată — punctele se acordă o singură dată.)")
        else:
            print(f"✔ Corect! Sarcina {sarcina} — {r.get('descriere')}: +{r.get('puncte')} puncte.")
            if r.get("clopot"):
                print(f"🔔 Clopotul {r['clopot']} s-a aprins: {r['clopot_nume']}.")
        _afiseaza_turn(r["stare"])
    else:
        print("✔ Corect!")


@_sigur
def indiciu(nivel, nr):
    """Arată un indiciu. Indiciul 1 costă 10%, indiciul 2 costă 20% din punctele nivelului."""
    r = _cere("/api/indiciu", {"nivel": nivel, "nr": nr})
    if not r.get("ok"):
        raise _Oprire(r.get("mesaj"))
    print(f"Indiciul {nr} pentru nivelul {nivel} ({'−' + str(r['cost']) + ' puncte' if r['nou'] else 'deja plătit'}):\n")
    print(r["text"])


@_sigur
def kit_de_salvare(nivel):
    """Nivelurile 3 și 4: primiți rezultatul necesar ca să continuați.
    Sarcina înlocuită (3B sau 4C) nu mai poate fi punctată, iar clopotul ei rămâne stins."""
    r = _cere("/api/kit", {"nivel": nivel})
    if not r.get("ok"):
        raise _Oprire(r.get("mesaj"))
    ce = "Mesajul de la Copou" if nivel == 3 else "Ghicitoarea"
    print(f"{ce}: „{r['text']}”  (sarcina {'3B' if nivel == 3 else '4C'} nu mai poate fi punctată)")
    return r["text"]


# =============================================================================
# Măsurare
# =============================================================================

def _ruleaza_pe_server(circuite, shots, experiment=False):
    r = _cere("/api/ruleaza", {"circuite": [_serializeaza(c) for c in circuite], "shots": shots,
                               "experiment": experiment})
    if not r.get("ok"):
        raise _Gresit(r.get("mesaj"))
    return r


def _local(circuite, shots):
    rez = StatevectorSampler().run(circuite, shots=shots).result()
    out = []
    for r in rez:
        date = r.data
        out.append(date.meas.get_counts() if hasattr(date, "meas") else list(date.values())[0].get_counts())
    return out


def masoara_toate(circuite, shots=1000):
    """Rulează o listă de circuite și returnează lista numărătorilor.
    Circuitele cu piese sigilate (cutii, semnale, qubiți de la Facultate) rulează pe serverul provocării."""
    circuite = [_cu_masuratori(c) for c in circuite]
    if any(_are_piese(c) for c in circuite):
        try:
            return _ruleaza_pe_server(circuite, shots)["counts"]
        except (_Gresit, _Oprire) as ex:
            raise RuntimeError(str(ex)) from None
    return _local(circuite, shots)


def masoara(qc, shots=1000):
    """Rulează circuitul de shots ori și returnează numărătorile, de ex. {'0': 507, '1': 493}.
    Dacă circuitul nu are măsurători, le adaugă automat la final."""
    try:
        return masoara_toate([qc], shots)[0]
    except RuntimeError as ex:
        print("⚠ " + str(ex))


def masoara_biti(circuite):
    """Măsoară o singură dată fiecare circuit cu 1 qubit și returnează lista biților (0 sau 1)."""
    return [int(next(iter(c))) for c in masoara_toate(circuite, shots=1)]


def probabilitatea_de_1(counts, qubit):
    """Din numărătorile unui circuit cu mai mulți qubiți: cât de des a ieșit 1 pe qubitul dat.
    Atenție: Qiskit scrie qubitul 0 în DREAPTA șirului de biți."""
    total = sum(counts.values())
    return sum(v for k, v in counts.items() if k[::-1][qubit] == "1") / total


# =============================================================================
# NIVELUL 1
# =============================================================================

@_sigur
def verifica_1A(qc_zero, qc_unu, qc_plus):
    _verifica("1A", {"qc_zero": _serializeaza(qc_zero), "qc_unu": _serializeaza(qc_unu),
                     "qc_plus": _serializeaza(qc_plus)})


@_sigur
def verifica_1B(calibreaza):
    p = [0.25, 0.5, 0.9, 0.7, 0.1]
    _verifica("1B", {"p": p, "circuite": [_serializeaza(calibreaza(x)) for x in p]})


def ry_defect(qc, theta, qubit=0):
    """Rotația defectă a ceasului: rotește cu un unghi greșit, de k ori mai mare (k secret)."""
    qc.append(_piesa("qff_rydefect", 1, "Ry defect", [float(theta)]), [qubit])
    return qc


@_sigur
def verifica_extra1(k_estimat):
    _verifica("X1", {"k": float(k_estimat)})


# =============================================================================
# NIVELUL 2
# =============================================================================

@_sigur
def verifica_2A(hzh, hxh):
    _verifica("2A", {"hzh": str(hzh), "hxh": str(hxh)})


def cutie(qc, nr, qubit=0):
    """Aplică cutia sigilată cu numărul nr (1..5) pe qubitul dat."""
    if nr not in range(1, 6):
        raise ValueError("Cutiile sunt numerotate de la 1 la 5.")
    qc.append(_piesa(f"qff_cutie_{nr}", 1, f"Cutia {nr}"), [qubit])
    return qc


def cutie_dubla(qc, q0=0, q1=1):
    """Cutia dublă (extra): ascunde CNOT (control q0, țintă q1), CZ sau SWAP."""
    qc.append(_piesa("qff_cutiedubla", 2, "Cutia dublă"), [q0, q1])
    return qc


def experiment(qc, shots=1000):
    """Rulează un experiment (se numără!) și returnează rezultatele măsurătorilor."""
    try:
        r = _ruleaza_pe_server([_cu_masuratori(qc)], shots, experiment=True)
    except (_Gresit, _Oprire) as ex:
        print("✘ " + str(ex))
        return None
    counts = r["counts"][0]
    print(f"Experimentul nr. {r['experimente']}: {dict(sorted(counts.items()))}")
    return counts


@_sigur
def verifica_2B(raspuns):
    try:
        r = {int(k): str(v) for k, v in dict(raspuns).items()}
    except Exception:
        raise _Gresit("Răspunsul trebuie să fie un dicționar, de ex. {1: \"X\", 2: \"H\", ...}.")
    _verifica("2B", {"raspuns": r})


@_sigur
def verifica_extra2(raspuns):
    _verifica("X2", {"raspuns": str(raspuns)})


# =============================================================================
# NIVELUL 3
# =============================================================================

def semnal_copou(i):
    """Al i-lea semnal trimis de nodul Copou: un circuit cu 2 qubiți, gata de decodat."""
    if not 0 <= i < NUMAR_SEMNALE_COPOU:
        raise ValueError(f"Semnalele sunt numerotate de la 0 la {NUMAR_SEMNALE_COPOU - 1}.")
    qc = QuantumCircuit(2)
    qc.append(_piesa(f"qff_copou_{i}", 2, "Copou"), [0, 1])
    return qc


@_sigur
def verifica_3A(phi_plus, phi_minus, psi_plus, psi_minus):
    _verifica("3A", {"phi_plus": _serializeaza(phi_plus), "phi_minus": _serializeaza(phi_minus),
                     "psi_plus": _serializeaza(psi_plus), "psi_minus": _serializeaza(psi_minus)})


def _test_copou(j):
    qc = QuantumCircuit(2)
    qc.append(_piesa(f"qff_copoutest_{j}", 2, "Copou (test)"), [0, 1])
    return qc


@_sigur
def verifica_3B(decodeaza):
    circuite = [decodeaza(_test_copou(j)) for j in range(4)]
    _verifica("3B", {"circuite": [_serializeaza(c) for c in circuite]})
    print("Citiți acum mesajul cu citeste_mesajul(decodeaza).")


def biti_in_text(biti):
    """Transformă o listă de biți (multiplu de 6) în text, cu alfabetul de 6 biți."""
    biti = [int(b) for b in biti]
    litere = []
    for i in range(0, len(biti) - len(biti) % 6, 6):
        idx = int("".join(map(str, biti[i:i + 6])), 2)
        litere.append(ALFABET[idx] if idx < len(ALFABET) else "#")
    return "".join(litere)


def text_in_biti(text):
    return [int(b) for ch in text for b in format(ALFABET.index(ch), "06b")]


@_sigur
def citeste_mesajul(decodeaza):
    """Decodează toate semnalele de la Copou cu decodorul vostru și afișează mesajul."""
    circuite = [decodeaza(semnal_copou(i)) for i in range(NUMAR_SEMNALE_COPOU)]
    biti = []
    for c in masoara_toate(circuite, shots=50):
        biti += [int(b) for b in max(c, key=c.get)[-2:]]
    text = biti_in_text(biti)
    print(f"Mesaj primit de la Copou: „{text}”")
    return text


@_sigur
def verifica_extra3(teleportare):
    _verifica("X3", {"tele": _serializeaza(teleportare)})


# =============================================================================
# NIVELUL 4
# =============================================================================

def genereaza_biti(n):
    """n biți aleatori (0 sau 1)."""
    return [int(b) for b in np.random.default_rng().integers(0, 2, n)]


def genereaza_baze(n):
    """n baze aleatoare: 'Z' (standard) sau 'X' (diagonală)."""
    return [str(b) for b in np.random.default_rng().choice(["Z", "X"], n)]


def cerne(biti, baze_alice, baze_bob):
    """Cernerea BB84: păstrează biții de pe pozițiile unde Alice și Bob au folosit aceeași bază."""
    return [b for b, a, c in zip(biti, baze_alice, baze_bob) if a == c]


def rata_erorilor(cheie_a, cheie_b):
    """Fracția pozițiilor unde cele două chei diferă (între 0 și 1)."""
    if len(cheie_a) == 0:
        return 0.0
    return sum(1 for a, b in zip(cheie_a, cheie_b) if a != b) / len(cheie_a)


def canal_test(qc):
    """Linia de test din laborator: fără Umbra."""
    return qc


@_sigur
def verifica_4A(alice_pregateste, bob_alege_baza, cheie_alice, cheie_bob):
    comb = [(0, "Z"), (1, "Z"), (0, "X"), (1, "X")]
    alice = [_serializeaza(alice_pregateste(b, z)) for b, z in comb]
    bob = [_serializeaza(_cu_masuratori(bob_alege_baza(alice_pregateste(b, z), z))) for b, z in comb]
    _verifica("4A", {"alice": alice, "bob": bob, "cheie_alice": [int(x) for x in cheie_alice],
                     "cheie_bob": [int(x) for x in cheie_bob]})


class Legatura:
    """Rezultatul conexiunii BB84 cu nodul Facultății pe o linie."""

    def __init__(self, linie, sesiune, rata, cheie):
        self.linie, self.sesiune, self.rata, self.cheie = linie, sesiune, rata, cheie

    def __repr__(self):
        return f"Legatura(linia {self.linie}: rata erorilor {self.rata:.1%}, cheie de {len(self.cheie)} biți)"


ESANTION_BB84 = 40


@_sigur
def conecteaza_la_facultate(linie, n, bob_alege_baza):
    """BB84 cu nodul Facultății (Alice), pe linia "A" sau "B".
    1. Facultatea trimite n qubiți; Bob îi măsoară în baze alese aleator (cu funcția voastră).
    2. Alice anunță public bazele ei; păstrați pozițiile cu aceeași bază.
    3. Primii 40 de biți se compară public (rata erorilor) și se aruncă; restul formează cheia."""
    r = _cere("/api/bb84/start", {"linie": linie, "n": int(n)})
    if not r.get("ok"):
        raise _Gresit(r.get("mesaj"))
    sid = r["sesiune"]
    baze_bob = genereaza_baze(n)
    circuite = []
    for i in range(n):
        qc = QuantumCircuit(1)
        qc.append(_piesa(f"qff_fac_{sid}_{i}", 1, "Facultate"), [0])
        circuite.append(_cu_masuratori(bob_alege_baza(qc, baze_bob[i])))
    biti_bob = [int(next(iter(c))) for c in _ruleaza_pe_server(circuite, 1)["counts"]]
    r = _cere("/api/bb84/baze", {"sesiune": sid, "baze_bob": baze_bob})
    if not r.get("ok"):
        raise _Gresit(r.get("mesaj"))
    cheie_bob = cerne(biti_bob, r["baze_alice"], baze_bob)
    r = _cere("/api/bb84/esantion", {"sesiune": sid, "esantion": cheie_bob[:ESANTION_BB84]})
    if not r.get("ok"):
        raise _Gresit(r.get("mesaj"))
    leg = Legatura(str(linie).upper(), sid, r["rata"], cheie_bob[ESANTION_BB84:])
    print(leg)
    return leg


@_sigur
def verifica_4B(linia_sigura):
    _verifica("4B", {"linia_sigura": str(linia_sigura)})


@_sigur
def cere_ghicitoarea(legatura):
    """Nodul Facultății trimite ghicitoarea criptată (XOR) cu cheia construită pe această legătură."""
    if not isinstance(legatura, Legatura):
        raise _Gresit("Dați ca argument rezultatul lui conecteaza_la_facultate(...).")
    r = _cere("/api/bb84/ghicitoare", {"sesiune": legatura.sesiune})
    if not r.get("ok"):
        raise _Gresit(r.get("mesaj"))
    return r["cifru"]


@_sigur
def verifica_4C(text_descifrat):
    _verifica("4C", {"text": str(text_descifrat)})


@_sigur
def verifica_extra4(k):
    _verifica("X4", {"k": k})


# =============================================================================
# NIVELUL 5
# =============================================================================

def marcheaza_111(qc):
    """Pune semnul minus doar pe starea |111⟩ (poarta CCZ = H · Toffoli · H pe qubitul 2)."""
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    return qc


def difuzor(n):
    """Difuzorul lui Grover pe n qubiți (2 sau 3): „inversarea față de medie”."""
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    if n == 2:
        qc.cx(0, 1)
    else:
        qc.ccx(0, 1, 2)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc


def arata_amplitudini(qc, titlu=""):
    """Desenează amplitudinile stării (fără măsurători) ca bare."""
    import matplotlib.pyplot as plt
    v = np.asarray(Statevector(qc.remove_final_measurements(inplace=False)).data)
    n = qc.num_qubits
    etichete = [format(i, f"0{n}b") for i in range(2 ** n)]
    if n == 3:
        etichete = [f"{e}\n{LOCATII[e].split()[0]}" for e in etichete]
    fig, ax = plt.subplots(figsize=(1.1 * 2 ** n + 1, 3))
    ax.bar(range(2 ** n), np.real(v), color=["#c0392b" if a < 0 else "#2c7fb8" for a in np.real(v)])
    ax.axhline(0, color="gray", lw=0.8)
    ax.axhline(np.mean(np.real(v)), color="gray", lw=0.8, ls="--")
    ax.set_xticks(range(2 ** n))
    ax.set_xticklabels(etichete, fontsize=8)
    ax.set_ylabel("amplitudine")
    ax.set_ylim(-1.05, 1.05)
    ax.set_title(titlu or "Amplitudini (linia punctată = media)")
    plt.tight_layout()
    plt.show()


@_sigur
def verifica_5A(grover_4):
    _verifica("5A", {"grover_4": _serializeaza(grover_4)})


@_sigur
def verifica_5B(oracol_8, grover_8, k_optim, locatie):
    qc = QuantumCircuit(3)
    oracol_8(qc)
    _verifica("5B", {"oracol": _serializeaza(qc), "grover_2": _serializeaza(grover_8(2)),
                     "k_optim": int(k_optim), "locatie": str(locatie)})


@_sigur
def verifica_extra5(k):
    _verifica("X5", {"k": k})


# =============================================================================
# NIVELUL 6
# =============================================================================

def _eroare_citire(backend, q):
    try:
        e = backend.target["measure"][(q,)].error
        return float(e) if e is not None else 1.0
    except Exception:
        return 1.0


@_sigur
def verifica_6A(pereche, backend):
    muchii = [list(map(int, m)) for m in backend.coupling_map.get_edges()]
    qubiti = sorted({q for m in muchii for q in m})
    _verifica("6A", {"pereche": [int(pereche[0]), int(pereche[1])], "muchii": muchii,
                     "erori": {str(q): _eroare_citire(backend, q) for q in qubiti}})


@_sigur
def verifica_6B(counts_bell, backend, cod_mentor=None):
    _verifica("6B", {"counts_bell": {str(k): int(v) for k, v in counts_bell.items()},
                     "backend": str(getattr(backend, "name", "")), "cod_mentor": cod_mentor})


@_sigur
def verifica_6C_hartie(p0, p1):
    _verifica("6C_hartie", {"p0": float(p0), "p1": float(p1)})


def corecteaza_citirea(counts_cal, counts):
    """Corectează erorile de citire.
    counts_cal: dicționar {starea pregătită: numărători}, de ex. {"00": {...}, "01": {...}, ...}
    counts:     numărătorile circuitului de corectat.
    Returnează (M, p_masurat, p_corectat), în ordinea stărilor din counts_cal.
    M[i, j] = probabilitatea de a citi starea i când ați pregătit starea j."""
    stari = list(counts_cal)
    M = np.zeros((len(stari), len(stari)))
    for j, s in enumerate(stari):
        total = sum(counts_cal[s].values())
        for i, r in enumerate(stari):
            M[i, j] = counts_cal[s].get(r, 0) / total
    total = sum(counts.values())
    p_masurat = np.array([counts.get(r, 0) / total for r in stari])
    p_corectat = np.clip(np.linalg.solve(M, p_masurat), 0, None)   # rezolvăm M · p = p_masurat
    p_corectat = p_corectat / p_corectat.sum()
    return M, p_masurat, p_corectat


@_sigur
def verifica_6C(M, p_corectat, counts_bell, f_inainte=None, f_dupa=None):
    _verifica("6C", {"M": np.asarray(M, dtype=float).tolist(), "p_corectat": np.asarray(p_corectat, dtype=float).tolist(),
                     "counts_bell": {str(k): int(v) for k, v in counts_bell.items()},
                     "f_inainte": None if f_inainte is None else float(f_inainte),
                     "f_dupa": None if f_dupa is None else float(f_dupa)})


@_sigur
def verifica_extra6(p_brut, p_corectat):
    _verifica("X6", {"p_brut": float(p_brut), "p_corectat": float(p_corectat)})
