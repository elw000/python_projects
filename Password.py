import random
import string

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.numbers = string.digits
        self.special_chars = string.punctuation

    def generate_password(self, length=12, use_uppercase=True, use_numbers=True, use_special=True):
        """Generate a random password with specified parameters"""
        # Initialize character pool with lowercase letters
        char_pool = self.lowercase

        # Add other character types based on parameters
        if use_uppercase:
            char_pool += self.uppercase
        if use_numbers:
            char_pool += self.numbers
        if use_special:
            char_pool += self.special_chars

        # Ensure minimum length of 8 characters
        if length < 8:
            length = 8

        # Generate password
        password = ''.join(random.choice(char_pool) for _ in range(length))

        # Ensure at least one character of each required type is included
        if use_uppercase and not any(c.isupper() for c in password):
            password = self._replace_random_char(password, self.uppercase)
        if use_numbers and not any(c.isdigit() for c in password):
            password = self._replace_random_char(password, self.numbers)
        if use_special and not any(c in self.special_chars for c in password):
            password = self._replace_random_char(password, self.special_chars)

        return password

    def _replace_random_char(self, password, char_set):
        """Replace a random character in the password with one from the given character set"""
        position = random.randint(0, len(password) - 1)
        password_list = list(password)
        password_list[position] = random.choice(char_set)
        return ''.join(password_list)

    def generate_multiple_passwords(self, count=5, **kwargs):
        """Generate multiple passwords with the same parameters"""
        return [self.generate_password(**kwargs) for _ in range(count)]


if __name__ == '__main__':
    # Example usage
    generator = PasswordGenerator()
    
    # Generate a single password with default parameters
    password = generator.generate_password()
    print(f"Single password: {password}")
    
    # Generate multiple passwords with custom parameters
    passwords = generator.generate_multiple_passwords(
        count=3,
        length=16,
        use_uppercase=True,
        use_numbers=True,
        use_special=True
    )
    print("\nMultiple passwords:")
    for i, pwd in enumerate(passwords, 1):
        print(f"Password {i}: {pwd}")
