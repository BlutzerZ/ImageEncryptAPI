import cv2 
import math
import numpy as np
import base64
from PIL import Image
import io


class Affine:
    def __init__(self, a, b, m ):
        self.a = a
        self.b = b
        self.m = m
        while self.IsCoprime() is False:
            print(a," and ",m," Must be Coprime! ")
            a,m = map(int,input("Enter a and m (Seperated by single space): ").split(" "))
            self.a = a
            self.m = m
        self.inv_a =  self.ModInv()

    def IsCoprime(self):
        """
        Check whether a and m is prime or not. If it is prime then it return true else false
        """
        if math.gcd(self.a, self.m) == 1:
            return True
        return False

    def ModInv(self):
        """
        Form equation 1 = inv(a)*a mod m. we find inv(a)
        Inverse exist only if a and m be Coprime
        """
        for i in range(2,self.m):
            if (self.a * i) % self.m == 1 :
                return i
        return 1
 
    def E(self, x):
        """
        m is the length of range. a and b are the Keys of the cipher.
        The value a must be chosen such that a and are coprime.
        """
        
        return (self.a*x + self.b) % self.m

    def D(self,y):
        """
        Decryption at pixel level
        """
        return (self.inv_a * (y-self.b)) % self.m

    def encryption(self, original_img):
        """
        Encryption of image 
        """
        height = original_img.shape[0]
        width = original_img.shape[1]
        
        for i in range(0,height):
            for j in range(0,width):
                a = original_img[i][j]      # rgb list
                r = self.E(a[0])
                g = self.E(a[1])
                b = self.E(a[2])
                original_img[i][j] = [r,g,b]

        image_cv2 = cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR)
    
        _, buffer = cv2.imencode('.png', image_cv2)
        png_as_text = base64.b64encode(buffer)
        base64_string = png_as_text.decode('utf-8')
        
        return base64_string


    def decryption(self, encry_img):
        """
        Decryption of image 
        """

        height = encry_img.shape[0]
        width = encry_img.shape[1]

        for i in range(0,height):
            for j in range(0,width):
                a = encry_img[i][j]         # rgb list
                r = self.D(a[0])
                g = self.D(a[1])
                b = self.D(a[2])
                encry_img[i][j] = [r,g,b]

        image_cv2 = cv2.cvtColor(encry_img, cv2.COLOR_RGB2BGR)
    
        _, buffer = cv2.imencode('.png', image_cv2)
        png_as_text = base64.b64encode(buffer)
        base64_string = png_as_text.decode('utf-8')
        
        return base64_string  # Saving decrypted image


def base64_to_cv2(base64_string):
    base64_string = base64_string.split(',')[1] if ',' in base64_string else base64_string
    img_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(img_data, np.uint8)
    img_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    return img_cv2

#------------- main program -------------------
A = Affine(71,37,256)
# original_img = cv2.imread('cat.png', cv2.IMREAD_COLOR)
# A.encryption(original_img)
# encry_img = cv2.imread('encrypted_img.png')
# A.decryption(encry_img)

# file = open('base.txt', 'r')
# cv2_image = base64_to_cv2(file.read())

# with open('encrypt.txt', 'w') as file:
#     file.write(A.encryption(cv2_image))

# files = open('encrypt.txt', 'r')
# with open('decrypt.txt', 'w') as file:
#     file.write(A.decryption(base64_to_cv2(files.read())))