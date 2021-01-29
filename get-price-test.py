
# Import required packages 
import glob
import os
import cv2 
import pytesseract 
import numpy as np


list_of_files = glob.glob('/home/heliocm/pc-folder/AppData/Local/Tibia/packages/Tibia/screenshots/*')
latest_file = list_of_files[-1]
#print(latest_file)
# Read image from which text needs to be extracted 
img = cv2.imread(latest_file)

sell_coins =  img[180:300, 495:1030]
cv2.imwrite('selling-prices.png', sell_coins)

buy_coins = img[365:475, 495:1030]
cv2.imwrite('buying-prices.png', buy_coins)

price_tables = [sell_coins, buy_coins]

# A text file is created and flushed 
file = open("recognized.txt", "w+") 
file.write("") 
file.close() 
iteracao = 0
for table in price_tables:
    # Preprocessing the image starts 
  
    # Convert the image to gray scale 
    gray = cv2.cvtColor(table, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('img-gray.png', gray) 
    
    # Performing OTSU threshold 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 

    cv2.imwrite('thresh.png', thresh1)
    # Specify structure shape and kernel size.  
    # Kernel size increases or decreases the area  
    # of the rectangle to be detected. 
    # A smaller value like (10, 10) will detect  
    # each word instead of a sentence. 
    
    text = pytesseract.image_to_string(thresh1)

    separated = text.split()
    #print(separated)
    offers = 0
    not_word = False
    for word in separated:
        for letter in word:
            if letter.isdigit() : not_word = True
        if not_word == False : offers += 1

    #print(offers)
    if separated[offers*2 + 1] == 'k' : final_price = separated[offers*2] + 'k'
    else : final_price = separated[offers*2]

    purpose = ''
    if iteracao == 0: purpose = 'selling' 
    else : purpose = 'buying' 
    print('Lowest price of Tibia coins for '+ purpose + ': ' + final_price)
    iteracao+=1
                    



    # Open the file in append mode 
    file = open("recognized.txt", "a") 
      
    # Appending the text into file 
    file.write(text) 
    file.write("\n") 
      
    # Close the file 
    file.close 

    #print(text)



  

  
  