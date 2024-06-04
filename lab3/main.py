class VigenereCipher:
    def __init__(self, text, password):
        self.text = text
        self.password = password
        self.extended_password = self._extend_password()

    def _extend_password(self):
        extended_password = self.password
        while len(extended_password) < len(self.text):
            extended_password += self.password
        return extended_password[:len(self.text)]

    def encrypt(self):
        encrypted_text = []
        for i in range(len(self.text)):
            text_char = self.text[i]
            password_char = self.extended_password[i]
            if text_char.isalpha():  # Only encrypt alphabetic characters
                shift = ord(password_char.lower()) - ord('а')
                if text_char.islower():
                    encrypted_char = chr((ord(text_char) - ord('а') + shift) % 32 + ord('а'))
                else:
                    encrypted_char = chr((ord(text_char) - ord('А') + shift) % 32 + ord('А'))
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(text_char)
        return ''.join(encrypted_text)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Example usage
file_path = 'input.txt'
password = "Поле глазасто, а лес ушаст."
text = read_file(file_path)

cipher = VigenereCipher(text, password)
encrypted_text = cipher.encrypt()
print(encrypted_text)
