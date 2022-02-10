def logic_equation(P, date_first_seen_message, date_last_seen_message, user_trust, group_trust ):
    '''
    - S = vrai, si le message est classifi´e comme Spam.
    — P : vrai, si le message courant est classifi´e comme Spam selon le vocabulaire cr´e´e.
    — H : vrai, si le temps entre la date du premier message vu et la date du dernier message
        vu est est inf´erieur `a 20 jours.
    — U : vrai, si le niveau de Trust de l’utilisateur est inf´erieur `a 50.
    — G : vrai, si le niveau de Trust du groupe de l’utilisateur est sup´erieur ou ´egal `a 50.

    S = P ∗ ((H ∗ U) + (U ∗ ¬G))
    '''

    H = True if (date_last_seen_message - date_first_seen_message) < 20 else False
    U = True if user_trust < 50 else False
    G = True if group_trust >= 50 else False

    S = P and ((H and U) or (U and not G))
    return S


def logic_equation_dnf(P, date_first_seen_message, date_last_seen_message, user_trust, group_trust ):
    '''
    - S = vrai, si le message est classifi´e comme Spam.
    — P : vrai, si le message courant est classifi´e comme Spam selon le vocabulaire cr´e´e.
    — H : vrai, si le temps entre la date du premier message vu et la date du dernier message
        vu est est inf´erieur `a 20 jours.
    — U : vrai, si le niveau de Trust de l’utilisateur est inf´erieur `a 50.
    — G : vrai, si le niveau de Trust du groupe de l’utilisateur est sup´erieur ou ´egal `a 50.

    S = P ∗ ((H ∗ U) + (U ∗ ¬G))
    '''

    H = True if (date_last_seen_message - date_first_seen_message) < 20 else False
    U = True if user_trust < 50 else False
    G = True if group_trust >= 50 else False

    S = P and H and U or P and U and not G
    return S


#test
print(logic_equation(True, 25, 70, 30, 70))
print(logic_equation_dnf(True, 25, 70, 30, 70))

