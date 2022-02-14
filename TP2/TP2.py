def logic_equation(P, date_first_seen_message, date_last_seen_message, user_trust, group_trust ):

    H = True if (date_last_seen_message - date_first_seen_message) < 20 else False
    U = True if user_trust < 50 else False
    G = True if group_trust >= 50 else False

    S = P and ((H and U) or (U and not G))
    return S


def logic_equation_dnf(P, date_first_seen_message, date_last_seen_message, user_trust, group_trust ):

    H = True if (date_last_seen_message - date_first_seen_message) < 20 else False
    U = True if user_trust < 50 else False
    G = True if group_trust >= 50 else False

    S = P and H and U or P and U and not G
    return S


def truth_table():
    table = []
    for P in range(0,2):
        for H in range(0,2):
            for U in range(0,2):
                for G in range(0,2):
                    row = []
                    row.append(bool(P))
                    row.append(bool(H))
                    row.append(bool(U))
                    row.append(bool(G))
                    S = bool(P) and ((bool(H) and bool(U)) or (bool(U) and bool(G)))
                    row.append(S)
                    table.append(row)
    return table 

def truth_table_dnf():

    table = []
    for P in range(0,2):
        for H in range(0,2):
            for U in range(0,2):
                for G in range(0,2):
                    row = []
                    row.append(bool(P))
                    row.append(bool(H))
                    row.append(bool(U))
                    row.append(bool(G))
                    S = bool(P) and bool(H) and bool(U) or bool(P) and bool(U) and bool(G)
                    row.append(S)
                    table.append(row)
    return table 

#test
# print(logic_equation(True, 25, 70, 30, 70))
# print(logic_equation_dnf(True, 25, 70, 30, 70))

# liste2 = truth_table()
# print(liste[len(liste)-1][3])
liste = truth_table_dnf()
counter = 0
print("Jeu de test pour le critere CACC:")
for k in range(len(liste[0])-1):
    for i in range(len(liste)):
        for j in range(len(liste)):    
            if (liste[i][k] != liste[j][k] and liste[i][4] != liste[j][4] and liste[i] != liste[j]):
                char = ''
                if k == 0: char = 'P'
                if k == 1: char = 'H'
                if k == 2: char = 'U'
                if k == 3: char = 'G'
                print(f"{counter}. Pour la clause {char}, on a le couple [{i}, {j}]")
                counter += 1
