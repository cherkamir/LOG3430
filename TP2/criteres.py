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




def print_truth_table(liste):
    print( "    P     H       U      G     S" )
    for i in range(len(liste)):
        print(liste[i])



def cacc_criteria(liste):
    amount_of_couples = 1
    print("Jeu de test pour le critere CACC:")
    for k in range(len(liste[0])-1):
        found = False
        for i in range(len(liste)):
            for j in range(len(liste)):    
                if (liste[i][k] != liste[j][k] and liste[i][4] != liste[j][4] and liste[i] != liste[j] and found != True):
                    char = ''
                    if k == 0: char = 'P'
                    if k == 1: char = 'H'
                    if k == 2: char = 'U'
                    if k == 3: char = 'G'
                    print(f"{amount_of_couples}. Pour la clause {char}, on a le couple {i} {liste[i]}, {j} {liste[j]}")
                    found = True
                    amount_of_couples += 1
                    
def gicc_criteria(liste):
    print("Jeu de test pour le critere GICC:")

    for k in range(len(liste[0])-1):
        amount_of_couples_icc = 1
        char = ''
        if k == 0: char = 'P'
        if k == 1: char = 'H'
        if k == 2: char = 'U'
        if k == 3: char = 'G'
        test_cases_found_ff = False
        test_cases_found_ft = False
        test_cases_found_tt = False
        test_cases_found_tf = False
        for i in range(len(liste)):
            if (liste[i][k] == True and liste[i][4] == True and test_cases_found_tt == False ):
                print(f"{amount_of_couples_icc}. Pour la clause {char}, on a les tests {i} {liste[i]}")
                amount_of_couples_icc += 1
                test_cases_found_tt = True
            if (liste[i][k] == False and liste[i][4] == True and test_cases_found_ft == False):
                print(f"{amount_of_couples_icc}. Pour la clause {char}, on a les tests {i} {liste[i]}")
                amount_of_couples_icc += 1
                test_cases_found_ft = True
            if (liste[i][k] == True and liste[i][4] == False and test_cases_found_tf == False): 
                print(f"{amount_of_couples_icc}. Pour la clause {char}, on a les tests {i} {liste[i]}")
                amount_of_couples_icc += 1
                test_cases_found_tf = True
            if (liste[i][k] == False and liste[i][4] == False and test_cases_found_ff == False):
                print(f"{amount_of_couples_icc}. Pour la clause {char}, on a les tests {i} {liste[i]}")
                amount_of_couples_icc += 1
                test_cases_found_ff = True
            



def ic_criteria():

    print ("Jeu de tests critere ic")
    dnf_implicants = ['PHU', 'PU~G']
    negation_implicants = ['~P', '~U', '~HG']

    test_d1 = []
    test_d2 = []
    d1_used_variables = []
    d2_used_variables = []

    for i in range(len(dnf_implicants)):
        for j in range(len(dnf_implicants[i])):

            if dnf_implicants[i][j] == '~':
                if dnf_implicants[i][j + 1] not in d1_used_variables:
                    test_d1.append(dnf_implicants[i][j + 1] + ' = False')
                    d1_used_variables.append((dnf_implicants[i][j + 1]))
            elif dnf_implicants[i][j] not in d1_used_variables:
                test_d1.append(dnf_implicants[i][j] + ' = True')
                d1_used_variables.append((dnf_implicants[i][j]))

    for i in range(len(negation_implicants)):
        for j in range(len(negation_implicants[i])):
            if negation_implicants[i][j] == '~':
                if negation_implicants[i][j + 1] not in d2_used_variables:
                    test_d2.append(negation_implicants[i][j + 1] + ' = False')
                    d2_used_variables.append((negation_implicants[i][j + 1]))
            elif negation_implicants[i][j] not in d2_used_variables:
                test_d2.append(negation_implicants[i][j] + ' = True')
                d2_used_variables.append((negation_implicants[i][j]))

    print("D1 = ", test_d1)
    print("D2 = ", test_d2)


# ic_criteria()
liste = truth_table()
print_truth_table(liste)
print("---------------------------------------------")
print("---------------------------------------------")
cacc_criteria(liste)
print("---------------------------------------------")
print("---------------------------------------------")
gicc_criteria(liste)
print("---------------------------------------------")
print("---------------------------------------------")
ic_criteria()