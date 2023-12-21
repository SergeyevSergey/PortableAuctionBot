from lot.models import CustomUser


# Restrictions
def place_restrictions(context):
    context.user_data['enable_create_lot'] = False
    context.user_data['enable_image'] = False
    context.user_data['enable_description'] = False
    context.user_data['enable_price'] = False
    context.user_data['enable_expiration_hours'] = False
    context.user_data['enable_search'] = False
    print('- restrictions placed')


# Create user
def create_user(update):
    print('- create_user function activated')
    user = CustomUser.objects.filter(user_id=update.effective_user.id).first()
    if user:
        print('     user exists')
        pass
    else:
        print('     user not exists')
        new_user = CustomUser(user_id=update.effective_user.id)
        new_user.save()
        print('     user created')


# Find minimal bid
def find_min_bid(lot):
    print('- find_min_bid function activated')
    price = lot.current_price
    print('     lot.current_price exists')
    if 0 < price < 500000:
        minimal_bid = (price/100)*15
    elif 500000 <= price < 1000000:
        minimal_bid = (price/100)*10
    elif 1000000 <= price < 10000000:
        minimal_bid = (price/100)*6
    elif 10000000 <= price < 25000000:
        minimal_bid = (price/100)*3
    elif 25000000 <= price < 100000000:
        minimal_bid = (price/100)*1.5
    else:
        minimal_bid = (price/100)
    print('     minimal_bid created')

    return round(minimal_bid, 2)

