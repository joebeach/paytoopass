arraystart=60
arrayend=110

t=[
0xD1, 0xA5, 0x66, 0x69, 0x81, 0xB4, 0x07, 0xCB, 0x73, 0xF8, 0x66, 0x58, 0x7F, 0xFA, 0x66, 0x5E,
0x7B, 0xFC, 0x06, 0xE0, 0xB0, 0xAF, 0x66, 0x83, 0xF4, 0xAC, 0x66, 0x57, 0x4F, 0xF5, 0x66, 0x51,
0x4B, 0x2E, 0xC0, 0x07, 0xB5, 0x9F, 0x00, 0x6E, 0x0E, 0x61, 0x0F, 0x85, 0xD1, 0xF4, 0x09, 0x6E,
0xDA, 0x65, 0x0F, 0x8C, 0x16, 0x55, 0x66, 0xAB, 0x6B, 0xA9, 0x66, 0xB0, 0xE9, 0xAB, 0x00, 0x08,
0x2B, 0x20, 0x0E, 0x2E, 0x53, 0x43, 0x46, 0x01, 0x33, 0x08, 0x32, 0x0A, 0x3F, 0x13, 0xB0, 0x08,
0x5D, 0xAB, 0x66, 0x83, 0x6F, 0x81, 0x02, 0xE0, 0x51, 0xA2, 0x66, 0xAB, 0x5F, 0xA9, 0x66, 0xA9,
0x43, 0xA9, 0x66, 0x03, 0xB1, 0xA4, 0x84, 0x2C, 0x8B, 0xCC, 0x80, 0x70, 0x71, 0xAB, 0x0F, 0x8D,
0x66, 0x55, 0x67, 0x6E, 0x0C, 0xFB, 0x10, 0x6F, 0x86, 0xE9, 0x04, 0x6F, 0xEF, 0xA4, 0xB6, 0x40,
0x81, 0xCD, 0x89, 0x06, 0xF3, 0xA9, 0x67, 0x6E, 0x1E, 0xE3, 0x08, 0x6E, 0x10, 0xA5, 0x5E, 0x0A,
0xFB, 0x0A, 0x5E, 0x0A, 0xC7, 0xA4, 0xB7, 0x06, 0xAE, 0xAB, 0x66, 0x3B, 0x7B, 0xCD, 0xF7, 0xF9,
0xCB, 0x08, 0x66, 0x0A, 0xD7, 0x0A, 0x42, 0x0A, 0xD3, 0xA8, 0x06, 0x56, 0xBB, 0xCD, 0xA3, 0x4E,
0xBF, 0xCD, 0x83, 0x36, 0xB3, 0x6A, 0x09, 0x15, 0xC4, 0x75, 0x3E, 0x5F, 0xCA, 0x2E, 0xF6, 0xF3,
0x10, 0x0F, 0x44, 0x23, 0xFC, 0x76, 0xFB, 0x59, 0x3C, 0x0B, 0x0E, 0xB2, 0x66, 0x60, 0x7C, 0x44,
0x3C, 0x54, 0x23, 0x4A, 0x30, 0x10, 0xBE, 0x3A, 0x67, 0xFF, 0xB8, 0x0F, 0x5B, 0xB8, 0x7D, 0xBC,
0x89, 0x42, 0x03, 0x60, 0x6A, 0x9E, 0x35, 0x9E, 0x09, 0x8B, 0x6B, 0x3E, 0x24, 0x49, 0x44, 0x25,
0x9B, 0x39, 0x1D, 0x67, 0xA6, 0x62, 0x3F, 0x28, 0x12, 0x55, 0x30, 0x05, 0x61, 0x74, 0xFA, 0xF1
]


def encriptar(cadena):
    start=arraystart # Esto es porque cada posicion del array debe ser expuesta a un numero distinto. Arranca en el start, pero la posicion siguiente ya no es la 60, sino la 61, etc
    encrypted=""
    for c in cadena:
            val=hex((ord(c) ^ t[start]) ^ t[t[start]])[2:]
            if len(val)<2:
                val="0%s" % val
            encrypted+=val
            start=start+1
    return encrypted.upper()

def desencriptar(cadena):
    start=arraystart # Esto es porque cada posicion del array debe ser expuesta a un numero distinto. Arranca en el start, pero la posicion siguiente ya no es la 60, sino la 61, etc
    decrypted=""
    for c in xrange(0,len(cadena),2):            #val=hex((ord(c) ^ t[start]) ^ t[t[start]])[2:]
        q = cadena[c:c+2]
        val=chr((int(q,16) ^ t[start] ^ t[t[start]]))
        decrypted+=val
        start=start+1
    return decrypted.upper()

def getDecryptedCard(cadena,pin):
    # A esta funcion se le pasa el encriptado y el codigo de seguridad
    # Devuelve el array tal como indica paytoo

    # Primer digito de tarjeta
    # 3 american
    # 4 visa
    # 5 mastercard
    # 6 Discover

    stream=desencriptar(cadena)
    print stream
    print stream[2:3]
    tipo_tarjeta=stream[2:3]
    if tipo_tarjeta == "3":
        card="AMEX"
    if tipo_tarjeta == "4":
        card="VISA"
    if tipo_tarjeta == "5":
        card="MASTERCARD"

    CreditCard = {
            'cc_type': card,
            'cc_holder_name': stream[18:43],
            'cc_number': stream[2:18],
            'cc_cvv': pin,
            'cc_month': stream[46:48],
            'cc_year': stream[44:46]
            }
    return CreditCard

def getCard(cadena,pin):
    # A esta funcion se le pasa el encriptado y el codigo de seguridad
    # Devuelve el array tal como indica paytoo

    # Primer digito de tarjeta
    # 3 american
    # 4 visa
    # 5 mastercard
    # 6 Discover

    stream=cadena
    print stream
    print stream[2:3]
    tipo_tarjeta=stream[2:3]
    if tipo_tarjeta == "3":
        card="AMEX"
    if tipo_tarjeta == "4":
        card="VISA"
    if tipo_tarjeta == "5":
        card="MASTERCARD"

    CreditCard = {
            'cc_type': card,
            'cc_holder_name': stream[18:43],
            'cc_number': stream[2:18],
            'cc_cvv': pin,
            'cc_month': stream[46:48],
            'cc_year': stream[44:46]
            }
    return CreditCard