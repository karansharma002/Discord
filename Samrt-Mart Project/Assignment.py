import json



def register_product():

    # LOADING DATABASE
    with open('Database.json') as f:
        data = json.load(f)

    '''
    In this function we register the products with Product NUmber as a key into database.
    '''

    prd_num = str(input('Enter the Product Number: '))
    prd_name = str(input('Enter the Product Name: '))
    prd_desc = str(input('Enter the Product Description: '))
    prd_price = str(input('Enter the Product Unit Selling Price: '))
    data[prd_num] = {}
    data[prd_num]['Name'] = prd_name
    data[prd_num]['Description'] = prd_desc
    data[prd_num]['Price'] = prd_price
    data[prd_num]['Units'] = 0
    data[prd_num]['Bought'] = 0

    # STORING THE DATA INTO DATABASE
    with open('Database.json', 'w') as f:
        json.dump(data,f,indent = 3)

    return

def shop():
    # LOADING DATABASE
    with open('Database.json') as f:
        data = json.load(f)

    # TEMP LIST TO STORE ITEMS BOUGHT

    cart = []

    # In this function we take the product number as an  input and do the following actions
    
    '''
    1: If product exists?
    2: Take input of  Units to Buy
    3: Storing the Product Id and Units bought into cart list
    4: Once the user finalise, We Print the total products and Amount with 15% TAX
    '''

    while True:
        prd_num = str(input('Enter the Product Number: '))
        
        if not prd_num in data:
            print('------- INVALID PRODUCT NUMBER ------- ')
            continue

        prd_units = str(input('Enter the Units Sold: ')) 
        if data[prd_num]['Units'] >= 0 or data[prd_num]['Units'] - prd_units > 0:
            print('-------- SORRY, The product is out of stock.')
            continue

        data[prd_num]['Units'] -= prd_units
        cart.append([prd_num, prd_units])

        confirm = input('Product Added, Would you like to Add More? [Y/N]').lower()
        if confirm in ('yes', 'y'):
            continue    
        else:
            break
    
    total_units = 0
    total_amount = 0
    for x in cart:
        total_units += data[x[0]]
        total_amount += data[x[1]]

    # 15% TAX
    tax = round(total_amount / 15 * 100)
    total_amount = total_amount + tax

    # SHOW DATA
    print('1: Total Products Bought: {}'.format(total_amount))
    print('2: Total Amount To Pay Including Tax: {}'.format(total_amount))        
   
    # STORING THE DATA INTO DATABASE
    with open('Database.json', 'w') as f:
        json.dump(data,f,indent = 3)

    return

def sale_report():
    # LOADING DATABASE
    with open('Database.json') as f:
        data = json.load(f)

    # In this function we query the database and take the product number 
    # If the Units of the Product are not Equal to Units Bought we proceed
    # When above actions are true, we query database and add the data into msg.

    msg = ''
    total_products = 0

    for x in data:
        if data[x]['Units'] != data[x]['Bought']:
            total_products += data[x]['Bought']
            msg += f"1:{x} - {data[x]['Name']}\
                \n2:Units Bought: {data[x]['Bought']}\
                \n3: Total price of the product: {data[x]['Price']}\n\n"

    
    for x in data:
        msg += f"- Totals of the All Products bought: {total_products}"
    
    print(msg)

    return

def mstock_report():
    # LOADING DATABASE
    with open('Database.json') as f:
        data = json.load(f)

    # In this function we query the database and  take the product number 
    # If the Units of the Product are less than zero we add them into msg

    msg = ''
    for x in data:
        if data[x]['Units'] <= 0:
            msg += f"{x} - {data[x]['Name']} | Units Left: {data[x]['Units']}\n"
    
    if msg == '':
        msg = 'No Items needs to be ordered'

    print(msg)

    return

def ship():
    # LOADING DATABASE
    with open('Database.json') as f:
        data = json.load(f)

    # In this function we take the product number as an  input and do the following actions
    '''
    1: If product exists?
    2: Take input of Product, Units, Price and Expiry 
    3: Storing it into the Database
    4: Ask user whether to add more or exit
    '''

    while True:
        prd_num = str(input('Enter the Product Number: '))
        if not prd_num in data:
            print('----- Invalid Product Number ------')
            continue
        prd_units = str(input('Enter the Product Units Received into the store: '))
        prd_price = str(input('Enter the Product wholesale Price: '))
        prd_expiry = str(input('Enter the Product Expiry Date'))
        data[prd_num]['Price'] = prd_price
        data[prd_num]['Units'] += prd_units
        data[prd_num]['Expiry'] = prd_expiry

        confirm = input('Product Added, Would you like to Add More? [Y/N]').lower()
        if confirm in ('yes', 'y'):
            continue    
        else:
            break

    # STORING THE DATA INTO DATABASE
    with open('Database.json', 'w') as f:
        json.dump(data,f,indent = 3)

    return

def menu():
    while True:
        # Main Menu

        msg = '1: Register Product\
            \n2: Shop Products\
            \n3: Sale Report\
            \n4: Stocks Report\
            \n5: Ship products'

        print(msg)
        
        choice = int(input('Enter the Choice: '))
        if choice < 0 or choice > 5:
            print('Invalid Choice')
            continue
        
        # CLEARING SCREEN
        print('\n' * 1000)

        # Returning to the Individual Function as per user choice
        if choice == 1:
            register_product()
        
        elif choice == 2:
            shop()
        
        elif choice == 3:
            sale_report()
        
        elif choice == 4:
            mstock_report()
        
        elif choice == 5:
            ship()
        
        


menu()