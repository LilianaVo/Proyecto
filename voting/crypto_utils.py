from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# --- CONFIGURACIÓN AES (Confidencialidad) ---
# Llave Simétrica de 256 bits para demostración
AES_KEY = get_random_bytes(32) 
BLOCK_SIZE = AES.block_size

def encrypt_vote_aes(vote_content):
    """Cifra el contenido del voto con AES-256 en modo CBC."""
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    ciphertext_bytes = cipher.encrypt(pad(vote_content.encode('utf-8'), BLOCK_SIZE))
    # Retorna el IV y el texto cifrado, ambos en formato hexadecimal
    return cipher.iv.hex() + ciphertext_bytes.hex()

# --- FUNCIONES RSA (Autenticación y No Repudio) ---

def generate_rsa_keys():
    """Genera un par de llaves RSA de 2048 bits."""
    key = RSA.generate(2048)
    private_key_pem = key.export_key('PEM')
    public_key_pem = key.publickey().export_key('PEM')

    return public_key_pem.decode('utf-8'), private_key_pem.decode('utf-8')

def sign_vote(vote_content, private_key_pem):
    """
    Firma el hash SHA256 del contenido del voto usando la llave privada del usuario.
    Retorna la firma en formato hexadecimal.
    """
    try:
        private_key = RSA.import_key(private_key_pem)
        h = SHA256.new(vote_content.encode('utf-8'))
        signer = pkcs1_15.new(private_key)
        signature = signer.sign(h)
        return signature.hex()
    
    except ValueError as e:
        raise ValueError("Error al cargar o usar la llave privada. Asegúrese de que el archivo es correcto.") from e

def verify_signature(vote_content, signature_hex, public_key_pem):
    """
    Verifica que la firma corresponda al contenido y a la llave pública.
    Retorna True si la verificación es exitosa. (Función faltante)
    """
    try:
        # 1. Cargar la Llave Pública del votante (desde la BD)
        public_key = RSA.import_key(public_key_pem)

        # 2. Hashing del Contenido del Voto
        h = SHA256.new(vote_content.encode('utf-8'))
        
        # 3. Decodificar la firma de hexadecimal a bytes
        signature = bytes.fromhex(signature_hex)

        # 4. Verificar la firma
        verifier = pkcs1_15.new(public_key)
        verifier.verify(h, signature)
        
        return True # Si la verificación es exitosa

    except (ValueError, TypeError):
        return False # Si la verificación falla