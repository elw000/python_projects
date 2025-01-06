import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
import cv2

class QRCodeHandler:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

    def generate_qr_code(self, data, filename="qrcode.png"):
        """Generate a QR code from the given data and save it to a file"""
        # Clear any existing data
        self.qr.clear()
        # Add the data
        self.qr.add_data(data)
        self.qr.make(fit=True)

        # Create an image from the QR Code
        qr_image = self.qr.make_image(fill_color="black", back_color="white")
        qr_image.save(filename)
        print(f"QR code saved as {filename}")

    def decode_qr_code(self, filename):
        """Decode QR code from an image file"""
        try:
            # Read the image using OpenCV
            image = cv2.imread(filename)
            # Decode the QR code
            decoded_objects = decode(image)
            
            if not decoded_objects:
                return "No QR code found in the image"
            
            # Return the decoded data
            return decoded_objects[0].data.decode('utf-8')
        except Exception as e:
            return f"Error decoding QR code: {str(e)}"

def main():
    qr_handler = QRCodeHandler()
    
    while True:
        print("\nQR Code Generator/Decoder")
        print("1. Generate QR Code")
        print("2. Decode QR Code")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            data = input("Enter the data to encode: ")
            filename = input("Enter filename to save QR code (default: qrcode.png): ") or "qrcode.png"
            qr_handler.generate_qr_code(data, filename)
            
        elif choice == '2':
            filename = input("Enter the QR code image filename to decode: ")
            result = qr_handler.decode_qr_code(filename)
            print(f"Decoded data: {result}")
            
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
